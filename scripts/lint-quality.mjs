#!/usr/bin/env node
// Content quality lint. Reports WARNINGS only: never fails the build (always exits 0).
// Writes the full result to reports/quality.json and prints a compact summary.

import { readFileSync, readdirSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, relative, dirname, basename, extname, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const CONTENT = join(ROOT, 'src', 'content');
const REPORT_DIR = join(ROOT, 'reports');
const REPORT_FILE = join(REPORT_DIR, 'quality.json');
const CODE_MODULES = new Set(['sql', 'python']); // excel/power-bi lessons are often click-based
const SUMMARY_MAX_LINES = 40;
const TOP_N = 25;

const CHECK_KEYS = [
  'lesson-words', 'lesson-section', 'lesson-interviewq', 'lesson-quiz',
  'lesson-mistakes', 'lesson-takeaways', 'lesson-worked',
  'practice-explanation', 'practice-commonMistake', 'practice-hint', 'practice-question',
  'practice-expected-missing', 'practice-rows-0', 'practice-rows-50+', 'practice-duplicate',
  'interview-modelAnswer', 'interview-followUps',
  'flashcard-back', 'glossary-definition', 'mcq-explanation', 'mcq-answerIndex',
  'parse-error',
];

const issues = [];
const parseErrors = [];
const lessonsPerModule = {};
const practicePerModule = {};
let draftLessons = 0;

function rel(p) {
  return relative(ROOT, p).split(sep).join('/');
}

function addIssue(check, file, ref, message, score = 1) {
  issues.push({ check, file, ref, message, score: Math.max(score, 0.01) });
}

// Recursively list files under dir, skipping any file or folder whose name starts with "_".
function walk(dir, ext) {
  const out = [];
  let entries;
  try {
    entries = readdirSync(dir, { withFileTypes: true });
  } catch {
    return out;
  }
  for (const e of entries) {
    if (e.name.startsWith('_')) continue;
    const full = join(dir, e.name);
    if (e.isDirectory()) out.push(...walk(full, ext));
    else if (e.isFile() && extname(e.name) === ext) out.push(full);
  }
  return out.sort();
}

function wordCount(text) {
  if (typeof text !== 'string') return 0;
  return text.trim().split(/\s+/).filter(Boolean).length;
}

// Prose-only text: drop fenced code and JSX tags (approximate).
function proseText(text) {
  return text
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/<\/?[A-Za-z][\w.]*[^<>]*\/?>/g, ' ');
}

// Split an MDX body into H2 sections, ignoring "## " lines inside code fences.
function splitSections(body) {
  const sections = [{ heading: null, lines: [] }];
  let inFence = false;
  for (const line of body.split('\n')) {
    if (/^\s*```/.test(line)) inFence = !inFence;
    const m = !inFence && line.match(/^## (.+?)\s*$/);
    if (m) sections.push({ heading: m[1].trim(), lines: [] });
    else sections[sections.length - 1].lines.push(line);
  }
  return sections;
}

// Count list items in lines, ignoring those inside code fences.
function countBullets(lines, { numbered = true } = {}) {
  let inFence = false;
  let n = 0;
  const re = numbered ? /^\s*(?:[-*+]|\d+\.)\s+\S/ : /^\s*[-*+]\s+\S/;
  for (const line of lines) {
    if (/^\s*```/.test(line)) { inFence = !inFence; continue; }
    if (!inFence && re.test(line)) n++;
  }
  return n;
}

function parseFrontmatter(src) {
  if (!src.startsWith('---')) return { fm: '', body: src };
  const end = src.indexOf('\n---', 3);
  if (end === -1) return { fm: '', body: src };
  const fm = src.slice(3, end);
  const body = src.slice(end + 4);
  return { fm, body };
}

function fmValue(fm, key) {
  const m = fm.match(new RegExp(`^${key}:\\s*(.*?)\\s*$`, 'm'));
  return m ? m[1].replace(/^["']|["']$/g, '') : '';
}

// ---------- Lessons ----------
function lintLessons() {
  for (const file of walk(join(CONTENT, 'lessons'), '.mdx')) {
    const module = relative(join(CONTENT, 'lessons'), file).split(sep)[0];
    const id = basename(file, '.mdx');
    const path = rel(file);
    let src;
    try {
      src = readFileSync(file, 'utf8');
    } catch (err) {
      addIssue('parse-error', path, id, `cannot read: ${err.message}`);
      continue;
    }
    const { fm, body } = parseFrontmatter(src);
    if (/^draft:\s*true\s*$/m.test(fm)) {
      draftLessons++;
      continue;
    }
    lessonsPerModule[module] = (lessonsPerModule[module] || 0) + 1;

    // Body word count
    const words = wordCount(proseText(body));
    if (words < 1200) {
      addIssue('lesson-words', path, id, `body has ${words} words (< 1200)`, (1200 - words) / 1200);
    }

    // Per-H2 section word count
    const sections = splitSections(body);
    for (const s of sections) {
      if (s.heading === null) continue;
      // Sections whose content is a component (PracticeSet, Quiz, FurtherReading) are fine short.
      if (/<(PracticeSet|Quiz|FurtherReading)\b/.test(s.lines.join('\n'))) continue;
      const n = wordCount(proseText(s.lines.join('\n')));
      if (n < 40) {
        addIssue('lesson-section', path, `## ${s.heading}`, `${n} words (< 40)`, (40 - n) / 40);
      }
    }

    // InterviewQ count
    const interviewQ = (body.match(/<InterviewQ\b/g) || []).length;
    if (interviewQ < 3) {
      addIssue('lesson-interviewq', path, id, `${interviewQ} <InterviewQ> (< 3)`, (3 - interviewQ) / 3);
    }

    // Quiz questions (approximate: count "q:" / "\"q\":" inside each <Quiz ... /> block)
    const quizBlocks = body.match(/<Quiz\b[\s\S]*?\/>/g) || [];
    let quizQs = 0;
    for (const block of quizBlocks) {
      quizQs += (block.match(/(?:^|[\s{,[])"?q"?\s*:/gm) || []).length;
    }
    if (quizBlocks.length === 0) {
      addIssue('lesson-quiz', path, id, 'no <Quiz> block (expected 5 questions)');
    } else if (quizQs !== 5) {
      addIssue('lesson-quiz', path, id, `Quiz has ${quizQs} questions (expected 5)`, 0.5);
    }

    // Common mistakes
    const mistakesSec = sections.find((s) => s.heading && /^common mistakes$/i.test(s.heading));
    const cmComponents = (body.match(/<CommonMistake\b/g) || []).length;
    const cmListItems = mistakesSec ? countBullets(mistakesSec.lines) : 0;
    if (cmComponents === 0 && cmListItems === 0) {
      addIssue('lesson-mistakes', path, '## Common mistakes', 'no <CommonMistake> and no list items');
    }

    // Key takeaways bullets
    const takeSec = sections.find((s) => s.heading && /key takeaways/i.test(s.heading));
    const bullets = takeSec ? countBullets(takeSec.lines, { numbered: false }) : 0;
    if (bullets < 5) {
      addIssue('lesson-takeaways', path, '## Key takeaways', `${bullets} bullets (< 5)`, (5 - bullets) / 5);
    }

    // Worked examples: code block or SqlPlayground required for code modules
    if (CODE_MODULES.has(module)) {
      const weSec = sections.find((s) => s.heading && /worked examples/i.test(s.heading));
      const weText = weSec ? weSec.lines.join('\n') : '';
      const hasExample = /^\s*```/m.test(weText) || /<SqlPlayground\b/.test(weText);
      if (!hasExample) {
        addIssue('lesson-worked', path, '## Worked examples', 'no code block or SqlPlayground');
      }
    }
  }
}

// ---------- JSON collections ----------
function loadArray(file) {
  const path = rel(file);
  let data;
  try {
    data = JSON.parse(readFileSync(file, 'utf8'));
  } catch (err) {
    parseErrors.push(path);
    addIssue('parse-error', path, basename(file), `invalid JSON: ${err.message.split('\n')[0]}`);
    return [];
  }
  if (!Array.isArray(data)) {
    addIssue('parse-error', path, basename(file), 'top-level value is not an array');
    return [];
  }
  return data;
}

function lintPractice() {
  const base = join(CONTENT, 'practice');
  const seen = new Map();
  for (const file of walk(base, '.json')) {
    const module = relative(base, file).split(sep)[0];
    const path = rel(file);
    for (const [i, item] of loadArray(file).entries()) {
      if (!item || typeof item !== 'object') {
        addIssue('parse-error', path, `[${i}]`, 'item is not an object');
        continue;
      }
      if (item.draft === true) continue;
      const id = String(item.id ?? `[${i}]`);
      const diff = item.difficulty || 'unknown';
      practicePerModule[module] ??= {};
      practicePerModule[module][diff] = (practicePerModule[module][diff] || 0) + 1;

      const expl = wordCount(item.explanation);
      if (expl < 25) addIssue('practice-explanation', path, id, `explanation ${expl} words (< 25)`, (25 - expl) / 25);
      const cm = wordCount(item.commonMistake);
      if (cm < 12) addIssue('practice-commonMistake', path, id, `commonMistake ${cm} words (< 12)`, (12 - cm) / 12);
      const hint = wordCount(item.hint);
      if (hint < 6) addIssue('practice-hint', path, id, `hint ${hint} words (< 6)`, (6 - hint) / 6);
      const q = wordCount(item.question);
      if (q < 15) addIssue('practice-question', path, id, `question ${q} words (< 15)`, (15 - q) / 15);

      if (item.language === 'sql' || item.language === 'python') {
        const eo = item.expectedOutput;
        if (eo === undefined || eo === null) {
          addIssue('practice-expected-missing', path, id, `${item.language} item has no expectedOutput`);
        } else if (Array.isArray(eo.rows)) {
          if (eo.rows.length === 0) addIssue('practice-rows-0', path, id, 'expectedOutput has 0 rows');
          else if (eo.rows.length > 50) {
            addIssue('practice-rows-50+', path, id, `expectedOutput has ${eo.rows.length} rows (> 50)`, (eo.rows.length - 50) / 50);
          }
        }
      }

      // Duplicate-ish question text within a module
      const norm = String(item.question ?? '').toLowerCase().replace(/[^a-z]/g, '');
      if (norm) {
        const key = `${module}|${norm}`;
        if (seen.has(key)) {
          addIssue('practice-duplicate', path, id, `same question text as ${seen.get(key)}`);
        } else {
          seen.set(key, id);
        }
      }
    }
  }
}

function lintSimpleCollections() {
  for (const file of walk(join(CONTENT, 'interview'), '.json')) {
    const path = rel(file);
    for (const [i, item] of loadArray(file).entries()) {
      if (!item || typeof item !== 'object') continue;
      const id = String(item.id ?? `[${i}]`);
      const ma = wordCount(item.modelAnswer);
      if (ma < 60) addIssue('interview-modelAnswer', path, id, `modelAnswer ${ma} words (< 60)`, (60 - ma) / 60);
      if (!Array.isArray(item.followUps) || item.followUps.length === 0) {
        addIssue('interview-followUps', path, id, 'followUps is empty');
      }
    }
  }

  for (const file of walk(join(CONTENT, 'flashcards'), '.json')) {
    const path = rel(file);
    for (const [i, item] of loadArray(file).entries()) {
      if (!item || typeof item !== 'object') continue;
      const id = String(item.id ?? `[${i}]`);
      const back = wordCount(item.back);
      if (back < 8) addIssue('flashcard-back', path, id, `back ${back} words (< 8)`, (8 - back) / 8);
    }
  }

  for (const file of walk(join(CONTENT, 'glossary'), '.json')) {
    const path = rel(file);
    for (const [i, item] of loadArray(file).entries()) {
      if (!item || typeof item !== 'object') continue;
      const id = String(item.id ?? `[${i}]`);
      const def = wordCount(item.definition);
      if (def < 10) addIssue('glossary-definition', path, id, `definition ${def} words (< 10)`, (10 - def) / 10);
    }
  }

  for (const file of walk(join(CONTENT, 'mcq'), '.json')) {
    const path = rel(file);
    for (const [i, item] of loadArray(file).entries()) {
      if (!item || typeof item !== 'object') continue;
      const id = String(item.id ?? `[${i}]`);
      const expl = wordCount(item.explanation);
      if (expl < 10) addIssue('mcq-explanation', path, id, `explanation ${expl} words (< 10)`, (10 - expl) / 10);
      const opts = Array.isArray(item.options) ? item.options : [];
      const ai = item.answerIndex;
      if (!Number.isInteger(ai) || ai < 0 || ai >= opts.length) {
        addIssue('mcq-answerIndex', path, id, `answerIndex ${JSON.stringify(ai)} out of range (${opts.length} options)`);
      }
    }
  }
}

// ---------- Output ----------
function run() {
  lintLessons();
  lintPractice();
  lintSimpleCollections();

  const counts = Object.fromEntries(CHECK_KEYS.map((k) => [k, 0]));
  for (const i of issues) counts[i.check] = (counts[i.check] || 0) + 1;

  const ranked = [...issues].sort(
    (a, b) => b.score - a.score || a.file.localeCompare(b.file) || a.ref.localeCompare(b.ref),
  );

  const lessonTotal = Object.values(lessonsPerModule).reduce((a, b) => a + b, 0);
  const practiceTotal = Object.values(practicePerModule)
    .flatMap((d) => Object.values(d))
    .reduce((a, b) => a + b, 0);

  // Full report
  mkdirSync(REPORT_DIR, { recursive: true });
  const report = {
    generatedAt: new Date().toISOString(),
    note: 'Quality warnings only. This script never fails the build.',
    totals: {
      lessons: lessonTotal,
      lessonDrafts: draftLessons,
      lessonsPerModule: lessonsPerModule,
      practice: practiceTotal,
      practicePerModule: practicePerModule,
    },
    counts,
    issues: ranked.map(({ check, file, ref, message }) => ({ check, file, ref, message })),
  };
  writeFileSync(REPORT_FILE, JSON.stringify(report, null, 2) + '\n');

  // Compact summary
  const lines = [];
  lines.push(`quality: ${issues.length} warnings, ${lessonTotal} lessons, ${practiceTotal} practice items (exit 0)`);
  const perLine = 4;
  for (let i = 0; i < CHECK_KEYS.length; i += perLine) {
    lines.push(
      '  ' + CHECK_KEYS.slice(i, i + perLine).map((k) => `${k}=${counts[k]}`).join('  '),
    );
  }
  lines.push(
    'lessons per module: ' +
      (Object.entries(lessonsPerModule).map(([m, n]) => `${m}=${n}`).join(' ') || 'none') +
      ` (drafts skipped: ${draftLessons})`,
  );
  const practiceLine = Object.entries(practicePerModule)
    .map(([m, d]) => `${m} ` + Object.entries(d).map(([k, n]) => `${k}=${n}`).join(' '))
    .join(' | ');
  lines.push('practice per module: ' + (practiceLine || 'none'));
  lines.push(`worst ${Math.min(TOP_N, ranked.length)} offenders (file :: id-or-heading :: issue):`);
  const room = SUMMARY_MAX_LINES - lines.length - 1;
  for (const i of ranked.slice(0, Math.min(TOP_N, Math.max(room, 0)))) {
    let line = `${i.file} :: ${i.ref} :: ${i.message}`;
    if (line.length > 180) line = line.slice(0, 177) + '...';
    lines.push(line);
  }
  lines.push(`full report: ${rel(REPORT_FILE)}`);
  console.log(lines.join('\n'));
}

try {
  run();
} catch (err) {
  // Never fail the build: report and exit 0.
  console.log(`quality: lint crashed (warnings only, exit 0): ${err && err.message}`);
}
process.exit(0);
