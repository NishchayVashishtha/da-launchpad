// Shared answer comparator. Used by the browser (SQL/Python practice) AND scripts/validate.mjs.
// Inputs: {columns:string[], rows:any[][]} or {value:any}.
export const TOL = 1e-6;

function norm(v) {
  if (v === undefined || v === null) return null;
  if (typeof v === 'boolean') return v ? 1 : 0;
  if (typeof v === 'bigint') return Number(v);
  return v;
}
function eqVal(a, b) {
  a = norm(a); b = norm(b);
  if (a === null || b === null) return a === b;
  if (typeof a === 'number' && typeof b === 'number') {
    if (Number.isNaN(a) && Number.isNaN(b)) return true;
    return Math.abs(a - b) <= TOL * Math.max(1, Math.abs(a), Math.abs(b)) || Math.abs(a - b) <= TOL;
  }
  if (typeof a === 'number' && typeof b === 'string' && b.trim() !== '' && !isNaN(Number(b))) return eqVal(a, Number(b));
  if (typeof b === 'number' && typeof a === 'string' && a.trim() !== '' && !isNaN(Number(a))) return eqVal(Number(a), b);
  if (Array.isArray(a) && Array.isArray(b)) return a.length === b.length && a.every((x, i) => eqVal(x, b[i]));
  if (typeof a === 'object' && typeof b === 'object') {
    const ka = Object.keys(a).sort(), kb = Object.keys(b).sort();
    return ka.length === kb.length && ka.every((k, i) => k === kb[i] && eqVal(a[k], b[k]));
  }
  return a === b;
}
const eqRow = (r1, r2) => r1.length === r2.length && r1.every((x, i) => eqVal(x, r2[i]));
const fmt = (v) => (v === null || v === undefined ? 'NULL' : typeof v === 'number' ? String(Math.round(v * 1e6) / 1e6) : String(v));
const key = (r) => r.map((v) => { v = norm(v); return v === null ? 'N' : typeof v === 'number' ? 'n' + Math.round(v * 1e3) : 's' + v; }).join('|');

/** @returns {{pass:boolean, message:string, missing:any[][], extra:any[][]}} */
export function compareResults(actual, expected, opts = {}) {
  const orderMatters = !!opts.orderMatters;
  if (!expected) return { pass: true, message: 'No expected output to compare.', missing: [], extra: [] };
  if (!actual) return { pass: false, message: 'No result produced.', missing: [], extra: [] };
  // scalar expectations
  if ('value' in expected && !('rows' in expected)) {
    let a = actual;
    if ('rows' in a && a.rows.length === 1 && a.rows[0].length === 1) a = { value: a.rows[0][0] };
    if (!('value' in a)) return { pass: false, message: 'Expected a single value but got a table.', missing: [], extra: [] };
    const pass = eqVal(a.value, expected.value);
    return { pass, message: pass ? 'Matches expected output.' : `Expected ${JSON.stringify(expected.value)} but got ${JSON.stringify(a.value)}.`, missing: [], extra: [] };
  }
  if (!('rows' in actual)) {
    if ('value' in actual && expected.rows.length === 1 && expected.rows[0].length === 1)
      return compareResults({ columns: expected.columns, rows: [[actual.value]] }, expected, opts);
    return { pass: false, message: 'Expected a table but got a single value.', missing: [], extra: [] };
  }
  const ac = actual.columns || [], ec = expected.columns || [];
  if (ac.length !== ec.length)
    return { pass: false, message: `Expected ${ec.length} column(s) [${ec.join(', ')}] but got ${ac.length} [${ac.join(', ')}].`, missing: [], extra: [] };
  const nameMismatch = ac.some((c, i) => String(c).toLowerCase() !== String(ec[i]).toLowerCase());
  const missing = [], extra = [];
  if (orderMatters) {
    const n = Math.max(actual.rows.length, expected.rows.length);
    for (let i = 0; i < n; i++) {
      const a = actual.rows[i], e = expected.rows[i];
      if (a && e && eqRow(a, e)) continue;
      if (e) missing.push(e);
      if (a) extra.push(a);
    }
  } else {
    const pool = actual.rows.map((r) => ({ r, k: key(r), used: false }));
    for (const e of expected.rows) {
      const ek = key(e);
      let hit = pool.find((p) => !p.used && p.k === ek && eqRow(p.r, e)) || pool.find((p) => !p.used && eqRow(p.r, e));
      if (hit) hit.used = true; else missing.push(e);
    }
    for (const p of pool) if (!p.used) extra.push(p.r);
  }
  const rowsOk = missing.length === 0 && extra.length === 0;
  if (rowsOk && nameMismatch)
    return { pass: false, message: `Rows match, but column names differ. Expected [${ec.join(', ')}], got [${ac.join(', ')}].`, missing, extra };
  if (rowsOk) return { pass: true, message: 'Matches expected output.', missing, extra };
  const cnt = actual.rows.length !== expected.rows.length ? ` Row count: expected ${expected.rows.length}, got ${actual.rows.length}.` : '';
  const ord = orderMatters ? ' (row order matters for this question)' : '';
  return { pass: false, message: `Output does not match${ord}.${cnt} ${missing.length} expected row(s) missing, ${extra.length} unexpected row(s).`, missing, extra };
}
export { fmt as formatCell };
