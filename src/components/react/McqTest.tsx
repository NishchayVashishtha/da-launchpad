import { useEffect, useMemo, useRef, useState } from 'react';
import Md from './Md';
import { useCountdown, fmtClock } from './useCountdown';
import { useProgress } from '../../lib/progress-react';
import { addMock } from '../../lib/progress';

export type MQ = { id: string; module: string; topic: string; section?: string; difficulty: string; question: string; options: string[]; answerIndex: number; explanation: string; shortcut?: string };
const shuffle = <T,>(a: T[]) => { const x = [...a]; for (let i = x.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [x[i], x[j]] = [x[j], x[i]]; } return x; };
type Phase = 'setup' | 'run' | 'review';

/** Timed MCQ practice. `kind` is the history type stored in progress (aptitude | mcq-statistics). Handles zero items. */
export default function McqTest({ items, kind, title, groupBy = 'section' }: { items: MQ[]; kind: string; title: string; groupBy?: 'section' | 'topic' }) {
  const store = useProgress();
  const groupOf = (m: MQ) => (groupBy === 'section' ? m.section : m.topic) || 'general';
  const groups = useMemo(() => [...new Set(items.map(groupOf))].sort(), [items]);
  const [group, setGroup] = useState('all');
  const [topic, setTopic] = useState('all');
  const [count, setCount] = useState(10);
  const [minutes, setMinutes] = useState(10);
  const [phase, setPhase] = useState<Phase>('setup');
  const [qs, setQs] = useState<MQ[]>([]);
  const [ans, setAns] = useState<(number | null)[]>([]);
  const [idx, setIdx] = useState(0);
  const [startedAt, setStartedAt] = useState(0);
  const [endedAt, setEndedAt] = useState(0);
  const phaseRef = useRef<Phase>('setup'); const qsRef = useRef<MQ[]>([]); const ansRef = useRef<(number | null)[]>([]);
  const timer = useCountdown(() => finish());
  qsRef.current = qs; ansRef.current = ans;
  const pool = items.filter((m) => (group === 'all' || groupOf(m) === group) && (topic === 'all' || m.topic === topic));
  const topics = [...new Set(items.filter((m) => group === 'all' || groupOf(m) === group).map((m) => m.topic))].sort();
  const n = Math.min(count, pool.length);
  useEffect(() => { setMinutes(Math.max(1, Math.round(n * 0.75))); }, [n]);
  useEffect(() => { if (phase !== 'run') return; const h = (e: BeforeUnloadEvent) => { e.preventDefault(); }; window.addEventListener('beforeunload', h); return () => window.removeEventListener('beforeunload', h); }, [phase]);

  if (!items.length) return <div className="card"><strong>No questions yet.</strong><p className="muted" style={{ marginBottom: 0 }}>Questions for {title} have not been added. Check back after the next content update.</p></div>;

  function begin() {
    const pick = shuffle(pool).slice(0, n);
    setQs(pick); setAns(pick.map(() => null)); setIdx(0); setPhase('run'); phaseRef.current = 'run'; qsRef.current = pick; ansRef.current = pick.map(() => null); setStartedAt(Date.now());
    timer.start(minutes * 60);
  }
  function finish() {
    if (phaseRef.current !== 'run') return;
    phaseRef.current = 'review';
    timer.stop();
    const cur = qsRef.current; const a = ansRef.current;
    const sc = cur.reduce((x, m, i) => x + (a[i] === m.answerIndex ? 1 : 0), 0);
    if (cur.length) addMock({ type: kind, label: `${title}${group !== 'all' ? ' / ' + group : ''}`, score: sc, total: cur.length, durationSec: Math.round((Date.now() - startedAt) / 1000) });
    setEndedAt(Date.now()); setPhase('review');
  }
  const score = qs.reduce((s, m, i) => s + (ans[i] === m.answerIndex ? 1 : 0), 0);
  const history = [...store.mocks].filter((m) => m.type === kind).reverse().slice(0, 10);
  const field = { padding: '.4rem .5rem', borderRadius: 6, border: '1px solid var(--border)', background: 'var(--bg)', color: 'var(--text)' } as const;

  if (phase === 'setup') {
    return (
      <div>
        <form className="card" onSubmit={(e) => { e.preventDefault(); if (n > 0) begin(); }} style={{ display: 'grid', gap: '.75rem', maxWidth: '32rem' }}>
          <label>{groupBy === 'section' ? 'Section' : 'Topic group'}<br /><select value={group} onChange={(e) => { setGroup(e.target.value); setTopic('all'); }} style={{ ...field, width: '100%' }}><option value="all">All</option>{groups.map((g) => <option key={g} value={g}>{g}</option>)}</select></label>
          {groupBy === 'section' && <label>Topic<br /><select value={topic} onChange={(e) => setTopic(e.target.value)} style={{ ...field, width: '100%' }}><option value="all">All topics</option>{topics.map((g) => <option key={g} value={g}>{g}</option>)}</select></label>}
          <label>Number of questions<br /><select value={count} onChange={(e) => setCount(+e.target.value)} style={{ ...field, width: '100%' }}>{[5, 10, 15, 20, 30].map((c) => <option key={c}>{c}</option>)}</select></label>
          <label>Time limit (minutes)<br /><input type="number" min={1} max={120} value={minutes} onChange={(e) => setMinutes(Math.max(1, +e.target.value || 1))} style={{ ...field, width: '100%' }} /></label>
          <p className="muted" style={{ margin: 0, fontSize: '.85rem' }}>{pool.length} questions match. This test will use {n}.</p>
          <button className="btn btn-primary" type="submit" disabled={n === 0}>Start test</button>
        </form>
        <h2>Past attempts</h2>
        {history.length === 0 ? <p className="muted">No attempts yet.</p> : (
          <div className="table-wrap"><table className="data"><thead><tr><th>Date</th><th>Set</th><th>Score</th><th>Time</th></tr></thead><tbody>
            {history.map((h) => <tr key={h.id}><td>{new Date(h.at).toLocaleString()}</td><td>{h.label}</td><td>{h.score}/{h.total} ({Math.round((100 * h.score) / h.total)}%)</td><td>{h.durationSec != null ? fmtClock(h.durationSec) : ''}</td></tr>)}
          </tbody></table></div>
        )}
      </div>
    );
  }

  if (phase === 'run') {
    const m = qs[idx];
    const answered = ans.filter((a) => a !== null).length;
    return (
      <section aria-label="Test in progress">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '.5rem', flexWrap: 'wrap' }}>
          <strong>Question {idx + 1} of {qs.length}</strong>
          <span className="chip" role="timer" aria-label="Time left" style={timer.left < 30 ? { color: 'var(--bad, #b91c1c)' } : undefined}>⏱ {fmtClock(timer.left)}</span>
        </div>
        <div className="card" style={{ margin: '.75rem 0' }}>
          <fieldset style={{ border: 0, padding: 0, margin: 0 }}>
            <legend style={{ fontWeight: 600, marginBottom: '.5rem' }}><Md inline>{m.question}</Md></legend>
            {m.options.map((o, j) => (
              <label key={j} style={{ display: 'flex', gap: '.5rem', padding: '.4rem', borderRadius: 6, cursor: 'pointer', background: ans[idx] === j ? 'var(--accent-soft, rgba(99,102,241,.12))' : undefined }}>
                <input type="radio" name={`mcq-${m.id}`} checked={ans[idx] === j} onChange={() => setAns(ans.map((a, k) => (k === idx ? j : a)))} />
                <span><Md inline>{o}</Md></span>
              </label>
            ))}
          </fieldset>
        </div>
        <div style={{ display: 'flex', gap: '.5rem', flexWrap: 'wrap' }}>
          <button className="btn" onClick={() => setIdx(idx - 1)} disabled={idx === 0}>Previous</button>
          <button className="btn" onClick={() => setIdx(idx + 1)} disabled={idx === qs.length - 1}>Next</button>
          <button className="btn btn-primary" style={{ marginLeft: 'auto' }} onClick={() => { if (answered === qs.length || confirm(`${qs.length - answered} question(s) unanswered. Submit anyway?`)) finish(); }}>Submit ({answered}/{qs.length} answered)</button>
        </div>
        <div style={{ display: 'flex', gap: '.3rem', flexWrap: 'wrap', marginTop: '.75rem' }} aria-label="Jump to question">
          {qs.map((_, i) => <button key={i} className="btn btn-sm" aria-current={i === idx} onClick={() => setIdx(i)} style={{ minWidth: '2.2rem', fontWeight: ans[i] !== null ? 700 : 400, outline: i === idx ? '2px solid currentColor' : undefined }}>{i + 1}</button>)}
        </div>
      </section>
    );
  }

  return (
    <section aria-label="Test review">
      <div className="verdict info" role="status"><strong>Score: {score}/{qs.length} ({Math.round((100 * score) / Math.max(1, qs.length))}%)</strong> in {fmtClock(Math.round((endedAt - startedAt) / 1000))}</div>
      <button className="btn btn-primary" style={{ margin: '.75rem 0' }} onClick={() => setPhase('setup')}>New test</button>
      <ol style={{ paddingLeft: '1.2rem' }}>
        {qs.map((m, i) => {
          const ok = ans[i] === m.answerIndex;
          return (
            <li key={m.id} style={{ marginBottom: '1.1rem' }}>
              <div><strong><Md inline>{m.question}</Md></strong></div>
              <p style={{ margin: '.3rem 0' }}>{ok ? '✓ Correct' : ans[i] === null ? '✗ Not answered' : '✗ Wrong'}. Your answer: {ans[i] === null ? 'none' : m.options[ans[i]!]}. {!ok && <>Correct: <strong>{m.options[m.answerIndex]}</strong></>}</p>
              <div className="callout callout-real" style={{ margin: 0 }}><div className="callout-title">Explanation</div><Md>{m.explanation}</Md>{m.shortcut && <p><strong>Shortcut:</strong> {m.shortcut}</p>}</div>
            </li>
          );
        })}
      </ol>
    </section>
  );
}
