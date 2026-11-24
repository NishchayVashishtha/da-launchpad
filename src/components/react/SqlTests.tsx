import { useRef, useState } from 'react';
import Md from './Md';
import ResultTable from './ResultTable';
import { useTabIndent } from './SqlPlayground';
import { useCountdown, fmtClock } from './useCountdown';
import { useProgress } from '../../lib/progress-react';
import { addMock, recordAttempt } from '../../lib/progress';
import { runSql } from '../../lib/sqlrunner';
import { url } from '../../lib/url';
import { compareResults, type Result } from '../../lib/compare.js';

export type TQ = { id: string; module: string; topic: string; difficulty: string; question: string; dataset: string; hint: string; solutionSql: string; expectedOutput?: Result; orderMatters?: boolean; explanation: string };
export type SqlTest = { id: string; title: string; durationMinutes: number; questions: TQ[] };
type Graded = { pass: boolean; message: string; error?: string };
const tbl = (r: Result | null | undefined) => (r && 'rows' in r ? r : null);

export default function SqlTests({ tests }: { tests: SqlTest[] }) {
  const store = useProgress();
  const [test, setTest] = useState<SqlTest | null>(null);
  const [code, setCode] = useState<string[]>([]);
  const [idx, setIdx] = useState(0);
  const [out, setOut] = useState<Result | null>(null);
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);
  const [phase, setPhase] = useState<'list' | 'run' | 'review'>('list');
  const [graded, setGraded] = useState<Graded[]>([]);
  const [startedAt, setStartedAt] = useState(0);
  const [elapsed, setElapsed] = useState(0);
  const codeRef = useRef<string[]>([]); const testRef = useRef<SqlTest | null>(null); const phaseRef = useRef('list');
  const timer = useCountdown(() => submit());
  const onKey = useTabIndent();

  if (!tests.length) return <div className="card"><strong>No SQL tests yet.</strong><p className="muted" style={{ marginBottom: 0 }}>Tests have not been added. Meanwhile, use <a href={url('/practice/?module=sql')}>SQL practice</a>.</p></div>;

  function start(t: SqlTest) {
    const c = t.questions.map(() => '');
    setTest(t); testRef.current = t; setCode(c); codeRef.current = c; setIdx(0); setOut(null); setErr(''); setPhase('run'); phaseRef.current = 'run'; setStartedAt(Date.now());
    timer.start(t.durationMinutes * 60);
  }
  function setCur(v: string) { const c = codeRef.current.map((x, i) => (i === idx ? v : x)); codeRef.current = c; setCode(c); }
  async function run() {
    setBusy(true); setErr(''); setOut(null);
    try { const r = await runSql(test!.questions[idx].dataset, code[idx]); setOut({ columns: r.columns, rows: r.rows }); }
    catch (e: any) { setErr(String(e.message || e)); } finally { setBusy(false); }
  }
  function go(i: number) { setIdx(i); setOut(null); setErr(''); }
  async function submit() {
    if (phaseRef.current !== 'run') return;
    phaseRef.current = 'review'; timer.stop();
    const t = testRef.current!; const codes = codeRef.current; const res: Graded[] = [];
    for (let i = 0; i < t.questions.length; i++) {
      const q = t.questions[i]; const sql = codes[i];
      if (!sql.trim()) { res.push({ pass: false, message: 'Not attempted.' }); continue; }
      try {
        const r = await runSql(q.dataset, sql);
        const c = q.expectedOutput ? compareResults({ columns: r.columns, rows: r.rows }, q.expectedOutput, { orderMatters: q.orderMatters }) : { pass: false, message: 'No expected output to compare.' };
        res.push({ pass: c.pass, message: c.message });
        recordAttempt(q.id, c.pass, { module: q.module, topic: q.topic });
      } catch (e: any) { res.push({ pass: false, message: 'Query failed.', error: String(e.message || e) }); recordAttempt(q.id, false, { module: q.module, topic: q.topic }); }
    }
    const secs = Math.round((Date.now() - startedAt) / 1000);
    addMock({ type: 'sql-test', label: t.title, score: res.filter((x) => x.pass).length, total: t.questions.length, durationSec: secs, detail: { testId: t.id } });
    setElapsed(secs); setGraded(res); setPhase('review');
  }

  if (phase === 'list') {
    const hist = [...store.mocks].filter((m) => m.type === 'sql-test').reverse().slice(0, 15);
    return (
      <div>
        <ul style={{ listStyle: 'none', padding: 0, display: 'grid', gap: '.6rem' }}>
          {tests.map((t) => {
            const last = [...store.mocks].reverse().find((m) => m.type === 'sql-test' && (m.detail as any)?.testId === t.id);
            return (
              <li key={t.id} className="card" style={{ display: 'flex', gap: '.75rem', alignItems: 'center', flexWrap: 'wrap' }}>
                <span style={{ flex: '1 1 14rem' }}><strong>{t.title}</strong><br /><span className="muted" style={{ fontSize: '.85rem' }}>{t.questions.length} questions, {t.durationMinutes} min{last ? `. Last score ${last.score}/${last.total}` : ''}</span></span>
                <button className="btn btn-primary" onClick={() => start(t)}>Start test</button>
              </li>
            );
          })}
        </ul>
        <h2>Attempt history</h2>
        {hist.length === 0 ? <p className="muted">No attempts yet.</p> : <div className="table-wrap"><table className="data"><thead><tr><th>Date</th><th>Test</th><th>Score</th><th>Time</th></tr></thead><tbody>{hist.map((h) => <tr key={h.id}><td>{new Date(h.at).toLocaleString()}</td><td>{h.label}</td><td>{h.score}/{h.total}</td><td>{h.durationSec != null ? fmtClock(h.durationSec) : ''}</td></tr>)}</tbody></table></div>}
      </div>
    );
  }

  const t = test!;
  if (phase === 'run') {
    const q = t.questions[idx]; const o = tbl(out);
    return (
      <section aria-label="SQL test in progress">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '.5rem', flexWrap: 'wrap' }}>
          <strong>{t.title}: question {idx + 1} of {t.questions.length}</strong>
          <span className="chip" role="timer" aria-label="Time left">⏱ {fmtClock(timer.left)}</span>
        </div>
        <div className="card" style={{ margin: '.75rem 0' }}>
          <div className="pq-head"><span className={`chip chip-${q.difficulty}`}>{q.difficulty}</span><span className="chip">{q.dataset}</span></div>
          <Md>{q.question}</Md>
          <label className="sr-only" htmlFor="sqt-ed">Your SQL</label>
          <textarea id="sqt-ed" className="editor" rows={8} spellCheck={false} value={code[idx]} onChange={(e) => setCur(e.target.value)} onKeyDown={(e) => onKey(e, run)} placeholder="-- Write SQL (SQLite). Ctrl/Cmd+Enter runs it." />
          <div style={{ display: 'flex', gap: '.5rem', margin: '.6rem 0', flexWrap: 'wrap' }}>
            <button className="btn btn-primary" onClick={run} disabled={busy || !code[idx].trim()}>▶ Run</button>
            <button className="btn" onClick={() => go(idx - 1)} disabled={idx === 0}>Previous</button>
            <button className="btn" onClick={() => go(idx + 1)} disabled={idx === t.questions.length - 1}>Next</button>
            <button className="btn btn-primary" style={{ marginLeft: 'auto' }} onClick={() => { if (confirm('Submit the test now?')) submit(); }}>Submit test</button>
          </div>
          {err && <div className="verdict fail" role="alert" style={{ whiteSpace: 'pre-wrap' }}>{err}</div>}
          {o && <ResultTable columns={o.columns} rows={o.rows} max={20} />}
        </div>
        <div style={{ display: 'flex', gap: '.3rem', flexWrap: 'wrap' }} aria-label="Jump to question">
          {t.questions.map((_, i) => <button key={i} className="btn btn-sm" onClick={() => go(i)} style={{ minWidth: '2.2rem', fontWeight: code[i]?.trim() ? 700 : 400, outline: i === idx ? '2px solid currentColor' : undefined }}>{i + 1}</button>)}
        </div>
      </section>
    );
  }

  if (graded.length === 0) return <div className="verdict info" role="status">Checking your answers...</div>;
  const score = graded.filter((g) => g.pass).length;
  return (
    <section aria-label="SQL test review">
      <div className="verdict info" role="status"><strong>Score: {score}/{t.questions.length}</strong> in {fmtClock(elapsed)}</div>
      <button className="btn btn-primary" style={{ margin: '.75rem 0' }} onClick={() => { setPhase('list'); setGraded([]); }}>Back to tests</button>
      {t.questions.map((q, i) => {
        const g = graded[i]; const e = tbl(q.expectedOutput);
        return (
          <article key={q.id} className="pq">
            <div className="pq-head"><span className={`chip chip-${q.difficulty}`}>{q.difficulty}</span><strong>Question {i + 1}</strong><span className={`verdict ${g.pass ? 'pass' : 'fail'}`} style={{ margin: 0 }}>{g.pass ? '✓ Correct' : '✗ ' + g.message}</span></div>
            <div className="pq-body">
              <Md>{q.question}</Md>
              <h4 style={{ margin: '.25rem 0' }}>Your answer</h4>
              <pre className="editor" style={{ whiteSpace: 'pre-wrap', minHeight: 0 }}><code>{codeRef.current[i] || '(blank)'}</code></pre>
              {g.error && <div className="verdict fail" style={{ whiteSpace: 'pre-wrap' }}>{g.error}</div>}
              <h4 style={{ margin: '.25rem 0' }}>Solution</h4>
              <pre className="editor" style={{ whiteSpace: 'pre-wrap', minHeight: 0 }}><code>{q.solutionSql}</code></pre>
              {e && <ResultTable columns={e.columns} rows={e.rows} max={10} />}
              <Md>{q.explanation}</Md>
            </div>
          </article>
        );
      })}
    </section>
  );
}
