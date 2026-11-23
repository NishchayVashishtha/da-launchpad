import { useState } from 'react';
import Md from './Md';
import ResultTable from './ResultTable';
import { useTabIndent } from './SqlPlayground';
import { useProgress } from '../../lib/progress-react';
import { recordAttempt, setQuestionDone, toggleBookmark } from '../../lib/progress';
import { runSql } from '../../lib/sqlrunner';
import { runPython } from '../../lib/pyrunner';
import { compareResults, type Result } from '../../lib/compare.js';
import { url } from '../../lib/url';

export type PQ = {
  id: string; module: string; topic: string; difficulty: 'easy' | 'medium' | 'hard';
  language: 'sql' | 'python' | 'excel' | 'dax' | 'text'; question: string; dataset: string; hint: string;
  solutionSql?: string; solutionCode?: string; solution?: string; expectedOutput?: Result;
  orderMatters?: boolean; explanation: string; commonMistake: string; interviewFrequency: string;
  estimatedMinutes: number; tags?: string[];
};

const fmtDate = (iso?: string) => (iso ? new Date(iso).toLocaleString() : '');
const asTable = (r: Result | null | undefined) => (r && 'rows' in r ? r : null);

export function Question({ q, compact = false }: { q: PQ; compact?: boolean }) {
  const store = useProgress();
  const rec = store.questions[q.id];
  const starred = !!store.bookmarks[q.id];
  const runnable = q.language === 'sql' || q.language === 'python';
  const [code, setCode] = useState('');
  const [hint, setHint] = useState(false);
  const [sol, setSol] = useState(false);
  const [busy, setBusy] = useState(false);
  const [status, setStatus] = useState('');
  const [out, setOut] = useState<Result | null>(null);
  const [stdout, setStdout] = useState('');
  const [err, setErr] = useState('');
  const [cmp, setCmp] = useState<ReturnType<typeof compareResults> | null>(null);
  const onKey = useTabIndent();
  const meta = { module: q.module, topic: q.topic };

  async function execute(): Promise<Result | null> {
    setBusy(true); setErr(''); setCmp(null); setStdout('');
    try {
      if (q.language === 'sql') {
        const r = await runSql(q.dataset, code);
        const res: Result = { columns: r.columns, rows: r.rows };
        setOut(res); return res;
      }
      const r = await runPython(code, setStatus);
      setStdout(r.stdout);
      if (r.error) { setErr(r.error); setOut(null); return null; }
      setOut(r.result); return r.result;
    } catch (e: any) { setErr(String(e.message || e)); setOut(null); return null; }
    finally { setBusy(false); setStatus(''); }
  }
  async function compare() {
    if (!code.trim()) { setErr('Write your answer first.'); return; }
    const res = await execute();
    if (!res || !q.expectedOutput) return;
    const c = compareResults(res, q.expectedOutput, { orderMatters: q.orderMatters });
    setCmp(c);
    recordAttempt(q.id, c.pass, meta);
  }

  const expected = asTable(q.expectedOutput);
  const outTable = asTable(out);
  const solutionCode = q.solutionSql ?? q.solutionCode;

  return (
    <article className={`pq ${rec?.doneAt ? 'done' : ''}`} id={`q-${q.id}`} aria-label={`Question ${q.id}`}>
      <div className="pq-head">
        <span className={`chip chip-${q.difficulty}`}>{q.difficulty}</span>
        <span className="chip">{q.language.toUpperCase()}</span>
        {q.dataset !== 'none' && <a className="chip" href={url(`/datasets/${q.dataset}/`)}>{q.dataset}</a>}
        <span className="chip">{q.estimatedMinutes} min</span>
        {compact && <span className="chip">{q.module}/{q.topic}</span>}
        <span className="chip" title="How often asked in interviews">asked: {q.interviewFrequency}</span>
        <code className="muted" style={{ fontSize: '.7rem', marginLeft: 'auto' }}>{q.id}</code>
        <button className="star" aria-pressed={starred} aria-label={starred ? 'Remove bookmark' : 'Bookmark question'} title="Bookmark" onClick={() => toggleBookmark(q.id)}>{starred ? '★' : '☆'}</button>
      </div>
      <div className="pq-body">
        <Md>{q.question}</Md>
        {runnable && (
          <>
            <label className="sr-only" htmlFor={`ed-${q.id}`}>Your {q.language} answer</label>
            <textarea id={`ed-${q.id}`} className="editor" value={code} onChange={(e) => setCode(e.target.value)} onKeyDown={(e) => onKey(e, execute)} spellCheck={false}
              placeholder={q.language === 'sql' ? '-- Write your SQL here (SQLite). Ctrl/Cmd+Enter runs it.' : '# Write Python here. Use load("dataset", "table") and assign your answer to `result`.'} rows={6} />
          </>
        )}
        {q.language === 'python' && q.dataset !== 'none' && <p className="muted" style={{ fontSize: '.75rem', margin: '.25rem 0' }}>Example: <code>df = load("{q.dataset}", "table_name")</code>. Assign your answer to <code>result</code>.</p>}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '.5rem', margin: '.6rem 0' }}>
          {runnable && <button className="btn btn-primary" onClick={execute} disabled={busy || !code.trim()}>▶ Run</button>}
          {runnable && q.expectedOutput && <button className="btn" onClick={compare} disabled={busy || !code.trim()}>Compare with expected</button>}
          <button className="btn" aria-expanded={hint} onClick={() => setHint(!hint)}>{hint ? 'Hide hint' : 'Show hint'}</button>
          <button className="btn" aria-expanded={sol} onClick={() => setSol(!sol)}>{sol ? 'Hide solution' : 'Show solution'}</button>
          <label style={{ display: 'inline-flex', gap: '.4rem', alignItems: 'center', marginLeft: 'auto', fontSize: '.875rem' }}>
            <input type="checkbox" checked={!!rec?.doneAt} onChange={(e) => setQuestionDone(q.id, e.target.checked, meta)} /> Mark as done
            {rec?.doneAt && <span className="muted" style={{ fontSize: '.72rem' }}>({fmtDate(rec.doneAt)})</span>}
          </label>
        </div>
        {busy && <div className="verdict info" role="status">{status || 'Running...'}</div>}
        {hint && <div className="callout callout-tip"><div className="callout-title">Hint</div><Md>{q.hint}</Md></div>}
        {err && <div className="verdict fail" role="alert" style={{ whiteSpace: 'pre-wrap' }}>{err}</div>}
        {stdout && <pre className="editor" style={{ minHeight: 0 }}>{stdout}</pre>}
        {out && (outTable ? <ResultTable columns={outTable.columns} rows={outTable.rows} /> : <div className="verdict info">Value: <code>{JSON.stringify((out as any).value)}</code></div>)}
        {cmp && (
          <div role="status">
            <div className={`verdict ${cmp.pass ? 'pass' : 'fail'}`}>{cmp.pass ? '✓ ' : '✗ '}{cmp.message}</div>
            {!cmp.pass && (cmp.missing.length > 0 || cmp.extra.length > 0) && outTable && (
              <div style={{ display: 'grid', gap: '.75rem', gridTemplateColumns: 'repeat(auto-fit, minmax(16rem, 1fr))' }}>
                {cmp.missing.length > 0 && <div><strong style={{ fontSize: '.8rem' }}>Expected but missing</strong><ResultTable columns={outTable.columns.length ? (expected?.columns ?? outTable.columns) : []} rows={cmp.missing} mark="bad" max={20} /></div>}
                {cmp.extra.length > 0 && <div><strong style={{ fontSize: '.8rem' }}>Unexpected rows in your output</strong><ResultTable columns={outTable.columns} rows={cmp.extra} mark="bad" max={20} /></div>}
              </div>
            )}
          </div>
        )}
        {rec && rec.attempts > 0 && <p className="muted" style={{ fontSize: '.75rem', margin: '.4rem 0 0' }}>Checked {rec.attempts} time(s): {rec.passes} correct, {rec.fails} not matching.</p>}
        {sol && (
          <div style={{ marginTop: '.75rem' }}>
            <h4 style={{ margin: '.25rem 0' }}>Solution</h4>
            {solutionCode ? <pre className="editor" style={{ whiteSpace: 'pre-wrap', minHeight: 0 }}><code>{solutionCode}</code></pre> : <Md>{q.solution ?? ''}</Md>}
            {expected && <><strong style={{ fontSize: '.8rem' }}>Expected output</strong><ResultTable columns={expected.columns} rows={expected.rows} max={20} /></>}
            {q.expectedOutput && 'value' in q.expectedOutput && <p>Expected value: <code>{JSON.stringify(q.expectedOutput.value)}</code></p>}
            <Md>{q.explanation}</Md>
            <div className="callout callout-mistake"><div className="callout-title">Common mistake</div><Md>{q.commonMistake}</Md></div>
          </div>
        )}
      </div>
    </article>
  );
}

const ORDER: PQ['difficulty'][] = ['easy', 'medium', 'hard'];
export default function PracticeSet({ questions }: { questions: PQ[] }) {
  if (!questions.length) return <p className="verdict fail">No practice questions found for this PracticeSet.</p>;
  return (
    <section aria-label="Practice questions" className="no-print-solutions">
      {ORDER.map((d) => {
        const qs = questions.filter((q) => q.difficulty === d);
        if (!qs.length) return null;
        return (
          <div key={d}>
            <h3 style={{ textTransform: 'capitalize' }}>{d} <span className="muted" style={{ fontSize: '.8rem', fontWeight: 400 }}>({qs.length})</span></h3>
            {qs.map((q) => <Question key={q.id} q={q} />)}
          </div>
        );
      })}
    </section>
  );
}
