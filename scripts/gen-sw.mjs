// Post-build: writes dist/precache.json (pages + hashed assets) used by public/sw.js to precache the app shell.
// Data files (public/data), pagefind and Pyodide are cached at runtime instead (they are large).
import { readdirSync, statSync, writeFileSync } from 'node:fs';
import { join, relative } from 'node:path';
const dist = 'dist';
const out = [];
(function walk(d) {
  for (const n of readdirSync(d)) {
    const p = join(d, n);
    if (statSync(p).isDirectory()) { if (n === 'pagefind' || n === 'data') continue; walk(p); continue; }
    const rel = relative(dist, p).split('\\').join('/');
    if (rel === 'sw.js' || rel === 'precache.json' || rel.endsWith('.map')) continue;
    if (/\.(html|css|js|svg|png|webmanifest|wasm|json)$/.test(rel)) out.push(rel.endsWith('/index.html') ? rel.slice(0, -'index.html'.length) : rel);
  }
})(dist);
writeFileSync(join(dist, 'precache.json'), JSON.stringify(out.sort()));
console.log(`precache.json: ${out.length} entries`);
