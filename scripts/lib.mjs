// Shared helpers for validate.mjs and audit.mjs
import { readdirSync, readFileSync, statSync, existsSync } from 'node:fs';
import { join, resolve, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = resolve(fileURLToPath(new URL('..', import.meta.url)));
export const MODULES = ['start-here', 'excel', 'sql', 'power-bi', 'python', 'statistics', 'business', 'interview', 'projects', 'job-search', 'cheat-sheets'];

export function walk(dir, ext, out = []) {
  if (!existsSync(dir)) return out;
  for (const n of readdirSync(dir).sort()) {
    const p = join(dir, n);
    if (statSync(p).isDirectory()) walk(p, ext, out);
    else if (n.endsWith(ext)) out.push(p);
  }
  return out;
}
export const rel = (p) => relative(ROOT, p);

/** Reads every JSON file in a content folder. Returns [{file, items:[...], isArray}] */
export function readJsonCollection(name) {
  return walk(join(ROOT, 'src/content', name), '.json').map((file) => {
    const json = JSON.parse(readFileSync(file, 'utf8'));
    return { file, isArray: Array.isArray(json), items: Array.isArray(json) ? json : [json] };
  });
}

/** Minimal frontmatter reader (flat keys + simple yaml lists are enough for audit needs). */
export function readMdx(file) {
  const raw = readFileSync(file, 'utf8');
  const m = raw.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  const fm = {};
  if (m) {
    for (const line of m[1].split('\n')) {
      const kv = line.match(/^([A-Za-z]+):\s*(.*)$/);
      if (kv) fm[kv[1]] = kv[2].replace(/^["']|["']$/g, '');
    }
  }
  return { raw, fm, body: m ? m[2] : raw };
}
