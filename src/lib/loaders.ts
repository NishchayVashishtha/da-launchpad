import type { Loader } from 'astro/loaders';
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';

function walk(dir: string, out: string[] = []): string[] {
  let names: string[] = [];
  try { names = readdirSync(dir); } catch { return out; }
  for (const n of names.sort()) {
    const p = join(dir, n);
    if (statSync(p).isDirectory()) walk(p, out);
    else if (n.endsWith('.json')) out.push(p);
  }
  return out;
}

/**
 * Loads every *.json file under `base`. Each file may hold ONE object or an ARRAY of objects;
 * every element becomes its own collection entry, keyed by its `id`. Duplicate ids fail the build.
 * Folders/files starting with "_" are loaded too (e.g. _sample/).
 */
export function jsonArrayLoader(opts: { base: string }): Loader {
  return {
    name: 'json-array-loader',
    load: async ({ store, parseData, generateDigest, config, logger, watcher }) => {
      const root = new URL(opts.base.replace(/\/?$/, '/'), config.root).pathname;
      const run = async () => {
        store.clear();
        const seen = new Map<string, string>();
        for (const file of walk(root)) {
          const rel = relative(process.cwd(), file);
          let json: unknown;
          try { json = JSON.parse(readFileSync(file, 'utf8')); }
          catch (e) { throw new Error(`Invalid JSON in ${rel}: ${(e as Error).message}`); }
          const items = Array.isArray(json) ? json : [json];
          for (const raw of items) {
            const id = String((raw as any)?.id ?? '');
            if (!id) throw new Error(`Entry without id in ${rel}`);
            if (seen.has(id)) throw new Error(`Duplicate id "${id}" in ${rel} (also in ${seen.get(id)})`);
            seen.set(id, rel);
            let data;
            try { data = await parseData({ id, data: raw as any, filePath: rel }); }
            catch (e) { throw new Error(`Schema error in ${rel} (id "${id}"): ${(e as Error).message}`); }
            store.set({ id, data, filePath: rel, digest: generateDigest(raw as any) });
          }
        }
        logger.info(`loaded ${store.keys().length} entries from ${opts.base}`);
      };
      await run();
      watcher?.add(root);
      watcher?.on('change', (p) => { if (p.startsWith(root)) run(); });
    },
  };
}
