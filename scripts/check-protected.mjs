// Gate: for every changed practice JSON vs git HEAD, verify only text fields changed
// (question, hint, explanation, commonMistake) and no entries were added/removed.
// Usage: node scripts/check-protected.mjs [--allow field,field]
import { execSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
const allowArg = process.argv.indexOf('--allow');
const allowed = new Set(['question', 'hint', 'explanation', 'commonMistake',
  ...(allowArg > 0 ? process.argv[allowArg + 1].split(',') : [])]);
const files = execSync('git diff --name-only HEAD -- src/content/practice', { encoding: 'utf8' })
  .split('\n').filter(f => f.endsWith('.json'));
let bad = 0;
for (const f of files) {
  let a, b;
  try { a = JSON.parse(readFileSync(f, 'utf8')); } catch (e) { console.log(`${f}: INVALID JSON ${e.message}`); bad++; continue; }
  b = JSON.parse(execSync(`git show HEAD:${f}`, { encoding: 'utf8' }));
  const byId = new Map(a.map(x => [x.id, x]));
  if (a.length !== b.length) { console.log(`${f}: count ${b.length} -> ${a.length}`); bad++; }
  for (const old of b) {
    const cur = byId.get(old.id);
    if (!cur) { console.log(`${f}: missing ${old.id}`); bad++; continue; }
    for (const k of new Set([...Object.keys(old), ...Object.keys(cur)]))
      if (!allowed.has(k) && JSON.stringify(old[k]) !== JSON.stringify(cur[k])) { console.log(`${f}: ${old.id}.${k} changed`); bad++; }
  }
}
console.log(`check-protected: ${files.length} changed files, ${bad} problems`);
process.exit(bad ? 1 : 0);
