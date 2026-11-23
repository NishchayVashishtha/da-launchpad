#!/usr/bin/env node
// Runs every SQL/Python practice solution and compares with expectedOutput.
// Flags: --file <path>  only that practice JSON file | --only sql|python | --fill  write missing expectedOutput
import { readFileSync, writeFileSync, existsSync, mkdtempSync, rmSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { tmpdir } from 'node:os';
import { spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { ROOT, readJsonCollection, rel } from './lib.mjs';
import { compareResults } from '../src/lib/compare.js';

const args = process.argv.slice(2);
const flag = (n) => args.includes(n);
const val = (n) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : undefined; };
const onlyFile = val('--file') && resolve(val('--file'));
const only = val('--only');
const fill = flag('--fill');
const MAX_ROWS = 50;

const files = readJsonCollection('practice').filter((f) => !onlyFile || f.file === onlyFile);
if (onlyFile && files.length === 0) { console.error(`No practice file matches ${val('--file')}`); process.exit(1); }

const failures = [];
const filled = [];
let checked = 0, skipped = 0;
const fail = (q, file, msg) => failures.push({ id: q.id, file: rel(file), msg });

// ---------- SQL ----------
const sqlQs = [];
const pyQs = [];
const seen = new Set();
for (const f of files) {
  for (const q of f.items) {
    if (seen.has(q.id)) fail(q, f.file, 'duplicate id'); seen.add(q.id);
    if (q.language === 'sql' && (!only || only === 'sql')) sqlQs.push({ q, f });
    else if (q.language === 'python' && (!only || only === 'python')) pyQs.push({ q, f });
    else skipped++;
  }
}

function handle(q, f, actual) {
  checked++;
  if (!q.expectedOutput) {
    if (fill) { q.expectedOutput = actual; f.dirty = true; filled.push(q.id); }
    else fail(q, f.file, 'missing expectedOutput (run: npm run validate -- --fill --file <file>)');
    return;
  }
  const c = compareResults(actual, q.expectedOutput, { orderMatters: q.orderMatters });
  if (!c.pass) fail(q, f.file, `${c.message}${c.missing.length ? ' First missing row: ' + JSON.stringify(c.missing[0]) : ''}${c.extra.length ? ' First unexpected row: ' + JSON.stringify(c.extra[0]) : ''}`);
  if ('rows' in actual && actual.rows.length > MAX_ROWS) fail(q, f.file, `result has ${actual.rows.length} rows (> ${MAX_ROWS}); add LIMIT`);
}

if (sqlQs.length) {
  const require = createRequire(import.meta.url);
  const initSqlJs = require('sql.js');
  const SQL = await initSqlJs();
  const dbs = new Map();
  for (const { q, f } of sqlQs) {
    const name = q.dataset;
    let db = dbs.get(name);
    if (db === undefined) {
      if (!name || name === 'none') db = new SQL.Database();
      else {
        const p = join(ROOT, 'public/data/sqlite', `${name}.sqlite`);
        db = existsSync(p) ? new SQL.Database(readFileSync(p)) : null;
        if (!db) console.warn(`! database missing: public/data/sqlite/${name}.sqlite (run the dataset generators)`);
      }
      dbs.set(name, db);
    }
    if (!db) { fail(q, f.file, `database "${name}" not found at public/data/sqlite/${name}.sqlite`); continue; }
    try {
      const res = db.exec(q.solutionSql);
      const last = res[res.length - 1];
      handle(q, f, last ? { columns: last.columns, rows: last.values } : { columns: [], rows: [] });
    } catch (e) { fail(q, f.file, 'SQL error: ' + e.message); }
  }
}

// ---------- Python ----------
if (pyQs.length) {
  const venv = join(ROOT, '.venv/bin/python');
  const py = existsSync(venv) ? venv : 'python3';
  const tmp = mkdtempSync(join(tmpdir(), 'dal-py-'));
  const BATCH = 60;
  for (let i = 0; i < pyQs.length; i += BATCH) {
    const batch = pyQs.slice(i, i + BATCH);
    const inp = join(tmp, `in-${i}.json`);
    writeFileSync(inp, JSON.stringify({ root: ROOT, items: batch.map(({ q }) => ({ id: q.id, code: q.solutionCode })) }));
    const r = spawnSync(py, [join(ROOT, 'scripts/py_harness.py'), inp], { encoding: 'utf8', maxBuffer: 1 << 28, timeout: 10 * 60 * 1000 });
    const marker = (r.stdout || '').split('@@RESULT@@')[1];
    if (!marker) { for (const { q, f } of batch) fail(q, f.file, `python harness crashed: ${(r.stderr || r.error || '').toString().slice(-400)}`); continue; }
    const out = JSON.parse(marker);
    for (const { q, f } of batch) {
      const o = out[q.id];
      if (!o?.ok) { fail(q, f.file, 'Python error: ' + (o?.error ?? 'no output').trim().split('\n').slice(-2).join(' | ')); continue; }
      handle(q, f, o.result);
    }
  }
  rmSync(tmp, { recursive: true, force: true });
}

// ---------- write fills ----------
if (fill) {
  for (const f of files) {
    if (!f.dirty) continue;
    const reorder = (q) => {
      if (!q.expectedOutput) return q;
      const o = {}; const eo = q.expectedOutput;
      for (const k of Object.keys(q)) { if (k === 'expectedOutput') continue; o[k] = q[k]; if (k === 'solutionSql' || k === 'solutionCode') o.expectedOutput = eo; }
      if (!o.expectedOutput) o.expectedOutput = eo;
      return o;
    };
    const items = f.items.map(reorder);
    writeFileSync(f.file, JSON.stringify(f.isArray ? items : items[0], null, 2) + '\n');
  }
  if (filled.length) console.log(`Filled expectedOutput for ${filled.length} question(s): ${filled.join(', ')}`);
}

console.log(`Validated ${checked} question(s) (${sqlQs.length} sql, ${pyQs.length} python); ${skipped} non-runnable skipped.`);
if (failures.length) {
  console.error(`\n${failures.length} FAILURE(S):`);
  for (const x of failures) console.error(` - [${x.id}] ${x.file}\n     ${x.msg}`);
  process.exit(1);
}
console.log('All solutions pass.');
