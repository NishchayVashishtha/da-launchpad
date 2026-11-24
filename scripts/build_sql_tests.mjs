// Builds src/content/tests/sql-tests.json: 10 SQL screening tests from the SQL practice pool.
// Deterministic: same input files always give the same output.
// Usage: node scripts/build_sql_tests.mjs
import { readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const practiceDir = join(root, 'src/content/practice/sql');
const outFile = join(root, 'src/content/tests/sql-tests.json');

const TEST_COUNT = 10;
const DURATION = 45;
const DIFFICULTY_SLOTS = ['easy', 'medium', 'medium', 'hard', 'hard'];
const FINTECH_MIN = 3; // tests 1-3 lean fintech
const PATTERN_MIN = 3; // tests 9-10 lean on interview patterns (ids sql-pattern-)

// 1. Load the pool: SQL-language questions only, one entry per question.
const pool = [];
for (const file of readdirSync(practiceDir).sort()) {
  if (!file.endsWith('.json') || file.startsWith('_')) continue;
  const items = JSON.parse(readFileSync(join(practiceDir, file), 'utf8'));
  if (!Array.isArray(items)) continue;
  for (const q of items) {
    if (q.language !== 'sql' || !q.solutionSql) continue;
    pool.push({
      id: q.id,
      topic: file.replace(/\.json$/, ''),
      dataset: q.dataset,
      difficulty: q.difficulty,
    });
  }
}
pool.sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));

const used = new Set();
const isFintech = (q) => q.dataset === 'fintech';
const isPattern = (q) => q.id.startsWith('sql-pattern-');

// 2. Build one test. Quota items (fintech / pattern) are picked first, then the rest.
function buildTest(index) {
  const picked = [];
  const remaining = [...DIFFICULTY_SLOTS];
  const topics = new Set();
  const datasets = new Set();
  // Rotate the start point so consecutive tests draw from different parts of the pool.
  const start = (index * 17) % pool.length;
  const order = [...pool.slice(start), ...pool.slice(0, start)];

  const take = (q) => {
    const slot = remaining.indexOf(q.difficulty);
    if (slot === -1 || used.has(q.id) || topics.has(q.topic)) return false;
    remaining.splice(slot, 1);
    picked.push(q);
    used.add(q.id);
    topics.add(q.topic);
    datasets.add(q.dataset);
    return true;
  };

  const quotas = [];
  if (index < 3) quotas.push({ name: 'fintech', min: FINTECH_MIN, test: isFintech });
  if (index >= 8) quotas.push({ name: 'pattern', min: PATTERN_MIN, test: isPattern });

  for (const quota of quotas) {
    let count = 0;
    for (const q of order) {
      if (count >= quota.min) break;
      if (quota.test(q) && take(q)) count++;
    }
    if (count < quota.min) throw new Error(`test ${index + 1}: not enough ${quota.name} questions`);
  }

  // Fill the rest: prefer a dataset not yet in this test, then anything that fits.
  for (const requireNewDataset of [true, false]) {
    for (const q of order) {
      if (remaining.length === 0) break;
      if (requireNewDataset && datasets.has(q.dataset)) continue;
      take(q);
    }
  }

  if (remaining.length) throw new Error(`test ${index + 1}: could not fill slots ${remaining.join(', ')}`);
  return picked;
}

// 3. Build all tests and check the rules.
const tests = [];
for (let i = 0; i < TEST_COUNT; i++) {
  const qs = buildTest(i);
  const n = i + 1;
  const topicCount = new Set(qs.map((q) => q.topic)).size;
  const datasetCount = new Set(qs.map((q) => q.dataset)).size;
  if (qs.length !== 5) throw new Error(`test ${n}: ${qs.length} questions`);
  if (topicCount !== 5) throw new Error(`test ${n}: topics repeat`);
  if (datasetCount < 3) throw new Error(`test ${n}: only ${datasetCount} datasets`);
  tests.push({
    id: `sql-test-${String(n).padStart(2, '0')}`,
    title: `SQL Screening Test ${n} — ${title(n)}`,
    durationMinutes: DURATION,
    questionIds: qs.map((q) => q.id),
  });
}

function title(n) {
  if (n <= 3) return 'Fintech focus';
  if (n >= 9) return 'Interview patterns';
  return 'Mixed';
}

const ids = tests.flatMap((t) => t.questionIds);
if (new Set(ids).size !== ids.length) throw new Error('a question is reused across tests');

writeFileSync(outFile, JSON.stringify(tests, null, 2) + '\n');
console.log(`wrote ${tests.length} tests (${ids.length} questions) to ${outFile}`);
