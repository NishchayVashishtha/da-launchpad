import { useState } from 'react';
import { runSql, type SqlResult } from '../../lib/sqlrunner';
import ResultTable from './ResultTable';

export function useTabIndent() {
  return (e: React.KeyboardEvent<HTMLTextAreaElement>, run?: () => void) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') { e.preventDefault(); run?.(); }
  };
}

/** Standalone SQL editor + result. Props: dataset (db id), query (initial SQL), rows (initial height). */
export default function SqlPlayground({ dataset = 'ecommerce', query = 'SELECT 1 AS n', title }: { dataset?: string; query?: string; title?: string }) {
  const [sql, setSql] = useState(query);
  const [res, setRes] = useState<SqlResult | null>(null);
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);
  const onKey = useTabIndent();
  async function run() {
    setBusy(true); setErr(''); setRes(null);
    try { setRes(await runSql(dataset, sql)); } catch (e: any) { setErr(String(e.message || e)); }
    setBusy(false);
  }
  return (
    <div className="card no-print" style={{ margin: '1.25rem 0' }}>
      <div style={{ display: 'flex', gap: '.5rem', alignItems: 'center', marginBottom: '.5rem', flexWrap: 'wrap' }}>
        <strong>{title ?? 'Try it'}</strong><span className="chip">SQLite · {dataset}</span>
      </div>
      <label className="sr-only" htmlFor={`pg-${dataset}-${query.length}`}>SQL query</label>
      <textarea id={`pg-${dataset}-${query.length}`} className="editor" value={sql} spellCheck={false} onChange={(e) => setSql(e.target.value)} onKeyDown={(e) => onKey(e, run)} rows={Math.min(14, Math.max(4, sql.split('\n').length + 1))} />
      <div style={{ display: 'flex', gap: '.5rem', margin: '.5rem 0', alignItems: 'center' }}>
        <button className="btn btn-primary" onClick={run} disabled={busy}>{busy ? 'Running...' : '▶ Run'}</button>
        <span className="muted" style={{ fontSize: '.75rem' }}>Ctrl/Cmd+Enter to run</span>
        {res && <span className="muted" style={{ fontSize: '.75rem' }}>{res.ms.toFixed(0)} ms</span>}
      </div>
      {err && <div className="verdict fail" role="alert">{err}</div>}
      {res && (res.columns.length ? <ResultTable columns={res.columns} rows={res.rows} /> : <div className="verdict info">Query ran. No rows returned.</div>)}
    </div>
  );
}
