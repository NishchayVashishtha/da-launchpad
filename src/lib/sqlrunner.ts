import { url } from './url';

type SqlJs = any;
let sqlPromise: Promise<SqlJs> | null = null;
const bytesCache = new Map<string, Uint8Array>();
const dbCache = new Map<string, any>();

export async function getSqlJs(): Promise<SqlJs> {
  sqlPromise ||= import('sql.js').then((m: any) => (m.default ?? m)({ locateFile: () => url('sql-wasm.wasm') }));
  return sqlPromise;
}

export async function getDb(dataset: string) {
  const SQL = await getSqlJs();
  if (dbCache.has(dataset)) return dbCache.get(dataset);
  let db;
  if (!dataset || dataset === 'none') db = new SQL.Database();
  else {
    let bytes = bytesCache.get(dataset);
    if (!bytes) {
      const res = await fetch(url(`data/sqlite/${dataset}.sqlite`));
      if (!res.ok) throw new Error(`Could not load database "${dataset}" (HTTP ${res.status}). Run the dataset generator first.`);
      bytes = new Uint8Array(await res.arrayBuffer());
      bytesCache.set(dataset, bytes);
    }
    db = new SQL.Database(bytes);
  }
  dbCache.set(dataset, db);
  return db;
}
export function resetDb(dataset: string) { try { dbCache.get(dataset)?.close(); } catch { /* ignore */ } dbCache.delete(dataset); }

export type SqlResult = { columns: string[]; rows: any[][]; ms: number };
export async function runSql(dataset: string, sql: string): Promise<SqlResult> {
  const db = await getDb(dataset);
  const t0 = performance.now();
  let res;
  try { res = db.exec(sql); }
  finally { if (/\b(insert|update|delete|drop|alter|create|replace|attach|pragma)\b/i.test(sql)) resetDb(dataset); }
  const ms = performance.now() - t0;
  const last = res[res.length - 1];
  if (!last) return { columns: [], rows: [], ms };
  return { columns: last.columns, rows: last.values, ms };
}

export type TableInfo = { name: string; columns: { name: string; type: string; pk: boolean }[]; rowCount: number };
export async function getSchema(dataset: string): Promise<TableInfo[]> {
  const db = await getDb(dataset);
  const tables = db.exec("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")[0]?.values.map((r: any[]) => String(r[0])) ?? [];
  return tables.map((name: string) => {
    const info = db.exec(`PRAGMA table_info("${name}")`)[0]?.values ?? [];
    const rowCount = Number(db.exec(`SELECT COUNT(*) FROM "${name}"`)[0].values[0][0]);
    return { name, rowCount, columns: info.map((r: any[]) => ({ name: String(r[1]), type: String(r[2]), pk: !!r[5] })) };
  });
}
