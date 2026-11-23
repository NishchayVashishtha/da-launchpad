/**
 * Progress store. ALL user data lives under ONE localStorage key (KEY) as a single JSON blob.
 * Safe on the server (no-ops). Subscribe with `subscribe(fn)` or the React hook `useProgress()` in progress-react.ts.
 */
export const KEY = 'dal:v1';
export const THEME_KEY = 'dal:theme';

export type QuestionRecord = {
  module?: string; topic?: string;
  doneAt?: string; attempts: number; passes: number; fails: number;
  lastResult?: 'pass' | 'fail'; lastAt?: string;
};
export type QuizRecord = { topic: string; score: number; total: number; at: string; history: { score: number; total: number; at: string }[] };
export type MockRecord = { id: string; type: string; label?: string; score: number; total: number; at: string; durationSec?: number; detail?: unknown };
export type FlashRecord = { box: number; due: string; seen: number };
export type Application = {
  id: string; company: string; role: string; status: 'Applied' | 'Screening' | 'Interview' | 'Offer' | 'Rejected';
  appliedOn: string; followUpOn?: string; link?: string; notes?: string; city?: string; salary?: string;
};
export type Profile = Record<string, string | number>;
export type Store = {
  version: 1;
  profile: Profile;
  settings: { startDate?: string; weeklyHoursGoal?: number; weeklyQuestionsGoal?: number };
  lessons: Record<string, { doneAt: string }>;
  questions: Record<string, QuestionRecord>;
  quizzes: Record<string, QuizRecord>;
  bookmarks: Record<string, string>;
  notes: Record<string, { text: string; at: string }>;
  hours: Record<string, number>; // YYYY-MM-DD -> minutes
  activity: Record<string, number>; // YYYY-MM-DD -> event count
  goals: Record<string, { hours: number; questions: number }>; // week start date
  mocks: MockRecord[];
  flashcards: Record<string, FlashRecord>;
  applications: Application[];
};

export const empty = (): Store => ({
  version: 1, profile: {}, settings: {}, lessons: {}, questions: {}, quizzes: {}, bookmarks: {}, notes: {},
  hours: {}, activity: {}, goals: {}, mocks: [], flashcards: {}, applications: [],
});

const isBrowser = typeof window !== 'undefined';
let cache: Store | null = null;
const listeners = new Set<() => void>();

export function load(): Store {
  if (cache) return cache;
  let s = empty();
  if (isBrowser) {
    try {
      const raw = localStorage.getItem(KEY);
      if (raw) s = { ...empty(), ...JSON.parse(raw) };
    } catch { /* corrupted or blocked storage: start empty */ }
  }
  cache = s;
  return s;
}
function save(s: Store) {
  cache = { ...s }; // new reference so React re-renders
  if (isBrowser) { try { localStorage.setItem(KEY, JSON.stringify(cache)); } catch { /* quota or blocked */ } }
  listeners.forEach((l) => l());
}
function update(fn: (s: Store) => void, markActive = true) {
  const s = structuredClone(load());
  fn(s);
  if (markActive) { const d = today(); s.activity[d] = (s.activity[d] || 0) + 1; }
  save(s);
}
export function subscribe(fn: () => void) {
  listeners.add(fn);
  const onStorage = (e: StorageEvent) => { if (e.key === KEY) { cache = null; fn(); } };
  if (isBrowser) window.addEventListener('storage', onStorage);
  return () => { listeners.delete(fn); if (isBrowser) window.removeEventListener('storage', onStorage); };
}

// ---------- dates ----------
export const dayKey = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
export const today = () => dayKey(new Date());
export const nowIso = () => new Date().toISOString();
export function weekStart(d = new Date()) { const x = new Date(d); const diff = (x.getDay() + 6) % 7; x.setDate(x.getDate() - diff); return dayKey(x); }
export function addDays(key: string, n: number) { const [y, m, d] = key.split('-').map(Number); const x = new Date(y, m - 1, d + n); return dayKey(x); }

// ---------- lessons ----------
export const isLessonDone = (id: string) => !!load().lessons[id];
export function setLessonDone(id: string, done: boolean) {
  update((s) => { if (done) s.lessons[id] = { doneAt: nowIso() }; else delete s.lessons[id]; });
}

// ---------- questions ----------
export const getQuestion = (id: string): QuestionRecord | undefined => load().questions[id];
const q = (s: Store, id: string, meta?: { module?: string; topic?: string }): QuestionRecord =>
  (s.questions[id] ||= { attempts: 0, passes: 0, fails: 0, ...meta });
export function setQuestionDone(id: string, done: boolean, meta?: { module?: string; topic?: string }) {
  update((s) => { const r = q(s, id, meta); if (done) r.doneAt = nowIso(); else delete r.doneAt; });
}
export function recordAttempt(id: string, pass: boolean, meta?: { module?: string; topic?: string }) {
  update((s) => {
    const r = q(s, id, meta);
    r.attempts++; pass ? r.passes++ : r.fails++;
    r.lastResult = pass ? 'pass' : 'fail'; r.lastAt = nowIso();
    if (pass && !r.doneAt) r.doneAt = nowIso();
  });
}

// ---------- quizzes ----------
export function recordQuiz(id: string, topic: string, score: number, total: number) {
  update((s) => {
    const prev = s.quizzes[id];
    const entry = { score, total, at: nowIso() };
    s.quizzes[id] = { topic, score, total, at: entry.at, history: [...(prev?.history || []), entry].slice(-20) };
  });
}

// ---------- bookmarks, notes ----------
export const isBookmarked = (id: string) => !!load().bookmarks[id];
export function toggleBookmark(id: string) {
  update((s) => { if (s.bookmarks[id]) delete s.bookmarks[id]; else s.bookmarks[id] = nowIso(); }, false);
}
export const getNote = (key: string) => load().notes[key]?.text ?? '';
export function setNote(key: string, text: string) {
  update((s) => { if (text.trim()) s.notes[key] = { text, at: nowIso() }; else delete s.notes[key]; }, false);
}

// ---------- hours, goals, streak ----------
export function logHours(minutes: number, date = today()) {
  update((s) => { s.hours[date] = Math.max(0, (s.hours[date] || 0) + minutes); s.activity[date] = (s.activity[date] || 0) + 1; }, false);
}
export function setGoal(week: string, hours: number, questions: number) {
  update((s) => { s.goals[week] = { hours, questions }; }, false);
}
export function streak(s = load()): { current: number; longest: number } {
  const days = new Set(Object.keys(s.activity).filter((k) => s.activity[k] > 0).concat(Object.keys(s.hours).filter((k) => s.hours[k] > 0)));
  let current = 0; let d = today();
  if (!days.has(d)) d = addDays(d, -1); // today not yet active: streak still alive until midnight
  while (days.has(d)) { current++; d = addDays(d, -1); }
  const sorted = [...days].sort(); let longest = 0, run = 0, prev = '';
  for (const k of sorted) { run = prev && addDays(prev, 1) === k ? run + 1 : 1; longest = Math.max(longest, run); prev = k; }
  return { current, longest };
}
export function weeklyHours(s = load(), weeks = 1): { date: string; hours: number }[] {
  const start = addDays(weekStart(), -7 * (weeks - 1));
  return Array.from({ length: 7 * weeks }, (_, i) => { const date = addDays(start, i); return { date, hours: (s.hours[date] || 0) / 60 }; });
}

// ---------- mocks ----------
export function addMock(m: Omit<MockRecord, 'id' | 'at'>) {
  update((s) => { s.mocks.push({ ...m, id: crypto.randomUUID?.() ?? String(Date.now()), at: nowIso() }); });
}

// ---------- flashcards (Leitner) ----------
export const LEITNER_DAYS = [0, 1, 2, 4, 8, 16];
export function reviewFlashcard(id: string, correct: boolean) {
  update((s) => {
    const r = s.flashcards[id] || { box: 1, due: today(), seen: 0 };
    r.box = correct ? Math.min(5, r.box + 1) : 1;
    r.due = addDays(today(), LEITNER_DAYS[r.box]); r.seen++;
    s.flashcards[id] = r;
  });
}
export function dueFlashcards(allIds: string[], s = load()) {
  const t = today();
  return allIds.filter((id) => !s.flashcards[id] || s.flashcards[id].due <= t);
}

// ---------- applications ----------
export function saveApplication(a: Application) {
  update((s) => { const i = s.applications.findIndex((x) => x.id === a.id); if (i >= 0) s.applications[i] = a; else s.applications.push(a); });
}
export function deleteApplication(id: string) { update((s) => { s.applications = s.applications.filter((a) => a.id !== id); }, false); }

// ---------- profile / settings ----------
export function saveProfile(p: Profile) { update((s) => { s.profile = p; }, false); }
export function saveSettings(p: Partial<Store['settings']>) { update((s) => { s.settings = { ...s.settings, ...p }; }, false); }

// ---------- weak topics ----------
export type WeakTopic = { key: string; label: string; pct: number; source: 'practice' | 'quiz'; href?: string };
export function weakTopics(s = load(), minAttempts = 3, threshold = 0.6): WeakTopic[] {
  const by: Record<string, { module: string; topic: string; p: number; t: number }> = {};
  for (const r of Object.values(s.questions)) {
    if (!r.attempts || !r.module) continue;
    const k = `${r.module}/${r.topic}`;
    const e = (by[k] ||= { module: r.module, topic: r.topic || '', p: 0, t: 0 });
    e.p += r.passes > 0 ? 1 : 0; e.t += 1;
    // weight failures: a question with more fails than passes counts as a miss
    if (r.fails > r.passes && r.passes > 0) e.p -= 0.5;
  }
  const out: WeakTopic[] = [];
  for (const [k, e] of Object.entries(by)) {
    if (e.t < Math.min(minAttempts, 2)) continue;
    const pct = Math.max(0, e.p / e.t);
    if (pct < threshold) out.push({ key: k, label: `${e.module}: ${e.topic}`, pct, source: 'practice', href: `/practice/?module=${e.module}&topic=${encodeURIComponent(e.topic)}` });
  }
  for (const [id, r] of Object.entries(s.quizzes)) {
    const pct = r.score / r.total;
    if (pct < threshold) out.push({ key: 'quiz:' + id, label: `Quiz: ${r.topic}`, pct, source: 'quiz', href: id.startsWith('/') ? id : undefined });
  }
  return out.sort((a, b) => a.pct - b.pct);
}

// ---------- export / import ----------
export function exportJson(): string { return JSON.stringify({ app: 'da-launchpad', exportedAt: nowIso(), data: load() }, null, 2); }
export function downloadExport() {
  const blob = new Blob([exportJson()], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = `da-launchpad-progress-${today()}.json`; a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}
export function importJson(text: string): { ok: boolean; message: string } {
  try {
    const parsed = JSON.parse(text);
    const data = parsed.app === 'da-launchpad' ? parsed.data : parsed;
    if (!data || typeof data !== 'object' || data.version !== 1) return { ok: false, message: 'This file is not a DA Launchpad progress export.' };
    save({ ...empty(), ...data });
    return { ok: true, message: 'Progress imported.' };
  } catch (e) { return { ok: false, message: 'Could not read the file: ' + (e as Error).message }; }
}
export function resetAll() { save(empty()); }
