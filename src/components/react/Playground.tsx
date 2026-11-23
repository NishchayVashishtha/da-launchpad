import { useEffect, useState } from 'react';
import { getSchema, runSql, type SqlResult, type TableInfo } from '../../lib/sqlrunner';
import { useTabIndent } from './SqlPlayground';
import ResultTable from './ResultTable';

export default function Playground({ datasets }: { datasets: { id: string; title: string }[] }) {
  const [ds, setDs] = useState(datasets[0]?.id ?? '');
  const [schema, setSchema] = useState<TableInfo[]>([]);
  const [sql, setSql] = useState('');
  const [res, setRes] = useState<SqlResult | null>(null);
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);
  const onKey = useTabIndent();
  useEffect(() => {
    const p = new URLSearchParams(location.search).get('dataset');
    if (p && datasets.some((d) => d.id === p)) setDs(p);
  }, []);
  useEffect(() => {
    if (!ds) return;
    setSchema([]); setErr(''); setRes(null);
    getSchema(ds).then((s) => { setSchema(s); setSql((cur) => cur || `SELECT * FROM ${s[0]?.name ?? 'table_name'} LIMIT 10;`); }).catch((e) => setErr(String(e.message || e)));
  }, [ds]);
  async function run() {
    setBusy(true); setErr(''); setRes(null);
    try { setRes(await runSql(ds, sql)); } catch (e: any) { setErr(String(e.message || e)); }
    setBusy(false);
  }
  if (!datasets.length) return <p className="card">No datasets available yet.</p>;
  return (
    <div style={{ display: 'grid', gap: '1rem', gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 18rem), 1fr))', alignItems: 'start' }}>
      <aside className="card">
        <label className="lbl" htmlFor="ds">Dataset</label>
        <select id="ds" className="field" value={ds} onChange={(e) => { setDs(e.target.value); setSql(''); }}>{datasets.map((d) => <option key={d.id} value={d.id}>{d.title}</option>)}</select>
        <h2 style={{ fontSize: '1rem', margin: '1rem 0 .4rem' }}>Tables</h2>
        {schema.length === 0 && !err && <p className="muted">Loading schema...</p>}
        {schema.map((t) => (
          <details key={t.name} style={{ marginBottom: '.4rem' }}>
            <summary style={{ cursor: 'pointer' }}><strong>{t.name}</strong> <span className="muted" style={{ fontSize: '.78rem' }}>{t.rowCount.toLocaleString('en-IN')} rows</span></summary>
            <ul style={{ margin: '.3rem 0', paddingLeft: '1rem', fontSize: '.82rem', listStyle: 'none' }}>
              {t.columns.map((c) => <li key={c.name}><code>{c.name}</code> <span className="muted">{c.type}{c.pk ? ' · PK' : ''}</span></li>)}
            </ul>
            <button className="btn btn-sm" onClick={() => setSql(`SELECT * FROM ${t.name} LIMIT 10;`)}>Preview</button>
          </details>
        ))}
        <p className="muted" style={{ fontSize: '.78rem' }}>Engine: SQLite (via sql.js). Syntax differs slightly from MySQL, PostgreSQL and SQL Server.</p>
      </aside>
      <section>
        <label className="sr-only" htmlFor="pg-sql">SQL query</label>
        <textarea id="pg-sql" className="editor" rows={9} value={sql} spellCheck={false} onChange={(e) => setSql(e.target.value)} onKeyDown={(e) => onKey(e, run)} />
        <div style={{ display: 'flex', gap: '.5rem', margin: '.5rem 0', alignItems: 'center' }}>
          <button className="btn btn-primary" onClick={run} disabled={busy || !sql.trim()}>{busy ? 'Running...' : '▶ Run'}</button>
          <span className="muted" style={{ fontSize: '.75rem' }}>Ctrl/Cmd+Enter</span>{res && <span className="muted" style={{ fontSize: '.75rem' }}>{res.ms.toFixed(0)} ms</span>}
        </div>
        {err && <div className="verdict fail" role="alert">{err}</div>}
        {res && (res.columns.length ? <ResultTable columns={res.columns} rows={res.rows} /> : <div className="verdict info">Done. No rows returned.</div>)}
      </section>
    </div>
  );
}
