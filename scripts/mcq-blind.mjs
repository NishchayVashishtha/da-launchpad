// Blind MCQ cross-check gate.
//   node scripts/mcq-blind.mjs prep <glob-prefix> [chunks]   -> .work/verify/blind-<n>.json + key.json
//   (a cheap agent answers each blind file into .work/verify/answers-<n>.json as {id: index, _unsure: {...}})
//   node scripts/mcq-blind.mjs compare                       -> prints disagreements (exit 1 if any)
import fs from 'node:fs';
const dir = '.work/verify'; fs.mkdirSync(dir, { recursive: true });
const [cmd, prefix = '', chunks = '2'] = process.argv.slice(2);
if (cmd === 'prep') {
  const all = [], key = {};
  for (const f of fs.readdirSync('src/content/mcq').filter(f => f.startsWith(prefix) && f.endsWith('.json')))
    for (const q of JSON.parse(fs.readFileSync(`src/content/mcq/${f}`, 'utf8'))) { all.push({ id: q.id, question: q.question, options: q.options }); key[q.id] = q.answerIndex; }
  const n = +chunks, size = Math.ceil(all.length / n);
  for (let i = 0; i < n; i++) fs.writeFileSync(`${dir}/blind-${i + 1}.json`, JSON.stringify(all.slice(i * size, (i + 1) * size), null, 1));
  fs.writeFileSync(`${dir}/key.json`, JSON.stringify(key));
  console.log(`${all.length} MCQs -> ${n} blind files in ${dir}`);
} else if (cmd === 'compare') {
  const key = JSON.parse(fs.readFileSync(`${dir}/key.json`, 'utf8')); let bad = 0, n = 0;
  for (const f of fs.readdirSync(dir).filter(f => /^answers-\d+\.json$/.test(f))) {
    const a = JSON.parse(fs.readFileSync(`${dir}/${f}`, 'utf8'));
    for (const [id, v] of Object.entries(a)) { if (id === '_unsure') continue; n++; if (key[id] !== v) { bad++; console.log(`${id}: key=${key[id]} blind=${v}`); } }
    for (const [id, why] of Object.entries(a._unsure || {})) console.log(`${id}: unsure (${why})`);
  }
  console.log(`mcq-blind: ${n} answered, ${bad} disagree`); process.exit(bad ? 1 : 0);
} else console.log('usage: prep <prefix> [chunks] | compare');
