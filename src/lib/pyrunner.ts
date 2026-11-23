import { url } from './url';
import serializeSrc from './py/serialize.py?raw';

const PYODIDE_VERSION = '0.27.7';
const CDN = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;
let pyPromise: Promise<any> | null = null;
export type PyStatus = (msg: string) => void;

function loadScript(src: string) {
  return new Promise<void>((res, rej) => {
    if ((window as any).loadPyodide) return res();
    const s = document.createElement('script');
    s.src = src; s.onload = () => res(); s.onerror = () => rej(new Error('Could not load Pyodide from the CDN. Python needs an internet connection the first time.'));
    document.head.appendChild(s);
  });
}

export function getPyodide(status?: PyStatus): Promise<any> {
  pyPromise ||= (async () => {
    status?.('Downloading Python runtime (first time only, about 10 MB)...');
    await loadScript(CDN + 'pyodide.js');
    const py = await (window as any).loadPyodide({ indexURL: CDN });
    status?.('Loading pandas...');
    await py.loadPackage(['pandas', 'numpy']);
    py.runPython(serializeSrc);
    py.FS.mkdirTree('/data');
    return py;
  })().catch((e) => { pyPromise = null; throw e; });
  return pyPromise;
}

const fetched = new Set<string>();
async function ensureCsv(py: any, dataset: string, table: string) {
  const path = `/data/${dataset}/${table}.csv`;
  if (fetched.has(path)) return;
  const res = await fetch(url(`data/csv/${dataset}/${table}.csv`));
  if (!res.ok) throw new Error(`Could not load data/csv/${dataset}/${table}.csv (HTTP ${res.status})`);
  py.FS.mkdirTree(`/data/${dataset}`);
  py.FS.writeFile(path, new Uint8Array(await res.arrayBuffer()));
  fetched.add(path);
}

export type PyRun = { result: { columns: string[]; rows: any[][] } | { value: any } | null; stdout: string; error?: string };

/** Runs learner code. Convention: assign the answer to `result`. `load(dataset, table)` returns a DataFrame. */
export async function runPython(code: string, status?: PyStatus): Promise<PyRun> {
  const py = await getPyodide(status);
  // Pre-fetch every CSV referenced via load("dataset", "table")
  const re = /load\(\s*['"]([\w-]+)['"]\s*,\s*['"]([\w-]+)['"]\s*\)/g;
  let m: RegExpExecArray | null;
  const jobs: Promise<void>[] = [];
  while ((m = re.exec(code))) jobs.push(ensureCsv(py, m[1], m[2]));
  status?.('Loading data...');
  await Promise.all(jobs);
  status?.('Running...');
  let out = '';
  py.setStdout({ batched: (s: string) => { out += s + '\n'; } });
  py.setStderr({ batched: (s: string) => { out += s + '\n'; } });
  const ns = py.globals.get('dict')();
  try {
    py.runPython(
      `import pandas as pd, numpy as np\ndef load(dataset, table):\n    return pd.read_csv(f"/data/{dataset}/{table}.csv")\n`,
      { globals: ns },
    );
    await py.runPythonAsync(code, { globals: ns });
    if (!ns.has('result')) return { result: null, stdout: out, error: 'Your code did not assign a variable named `result`.' };
    py.globals.set('__r', ns.get('result'));
    const json = py.runPython('to_json(__r)');
    py.globals.delete('__r');
    return { result: JSON.parse(json), stdout: out };
  } catch (e: any) {
    return { result: null, stdout: out, error: String(e.message || e).split('\n').slice(-6).join('\n') };
  } finally { ns.destroy?.(); }
}
