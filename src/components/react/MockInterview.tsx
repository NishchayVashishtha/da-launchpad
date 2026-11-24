import { useMemo, useRef, useState } from 'react';
import Md from './Md';
import { useCountdown, fmtClock } from './useCountdown';
import { useProgress } from '../../lib/progress-react';
import { addMock, getNote, setNote } from '../../lib/progress';
import { url } from '../../lib/url';
import type { IQ } from './InterviewBank';

const shuffle = <T,>(a: T[]) => { const x = [...a]; for (let i = x.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [x[i], x[j]] = [x[j], x[i]]; } return x; };
const SCRIPT = [
  ['Problem', 'What business question did you answer? Who asked for it?'],
  ['Data', 'Where did the data come from? How big was it? What did you clean?'],
  ['Approach', 'Which tools and steps did you use, and why those?'],
  ['Insight', 'What was the main finding? Give one number.'],
  ['Impact', 'What decision or action did it change?'],
  ['Learning', 'What would you do differently next time?'],
];
const NOTE_KEY = 'mock:project-script';

function Chart({ points }: { points: { pct: number; label: string }[] }) {
  if (points.length < 2) return <p className="muted">Complete two or more sessions to see your trend.</p>;
  const W = 480, H = 160, P = 24;
  const xy = points.map((p, i) => [P + (i * (W - 2 * P)) / (points.length - 1), H - P - (p.pct / 100) * (H - 2 * P)]);
  return (
    <figure style={{ margin: 0 }}>
      <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`Score history: ${points.map((p) => p.pct + '%').join(', ')}`} style={{ width: '100%', maxWidth: 520, height: 'auto' }}>
        {[0, 50, 100].map((g) => { const y = H - P - (g / 100) * (H - 2 * P); return <g key={g}><line x1={P} x2={W - P} y1={y} y2={y} stroke="currentColor" opacity=".15" /><text x={2} y={y + 4} fontSize="10" fill="currentColor" opacity=".6">{g}%</text></g>; })}
        <polyline fill="none" stroke="currentColor" strokeWidth="2" points={xy.map((p) => p.join(',')).join(' ')} />
        {xy.map((p, i) => <circle key={i} cx={p[0]} cy={p[1]} r="3.5" fill="currentColor"><title>{points[i].label}: {points[i].pct}%</title></circle>)}
      </svg>
      <figcaption className="muted" style={{ fontSize: '.8rem' }}>Average self-rating per session, as a percent of 5. Oldest on the left.</figcaption>
    </figure>
  );
}

export default function MockInterview({ items }: { items: IQ[] }) {
  const store = useProgress();
  const cats = useMemo(() => [...new Set(items.map((i) => i.category))].sort(), [items]);
  const [sel, setSel] = useState<string[]>([]);
  const [mins, setMins] = useState(3);
  const [num, setNum] = useState(5);
  const [phase, setPhase] = useState<'setup' | 'ask' | 'reveal' | 'done'>('setup');
  const [queue, setQueue] = useState<IQ[]>([]);
  const [i, setI] = useState(0);
  const [ratings, setRatings] = useState<number[]>([]);
  const startedAt = useRef(0);
  const timer = useCountdown(() => {});
  const [script, setScript] = useState(() => getNote(NOTE_KEY));
  const [saved, setSaved] = useState('');
  const chosen = sel.length ? sel : cats;
  const pool = items.filter((x) => chosen.includes(x.category));
  const n = Math.min(num, pool.length);
  const field = { padding: '.4rem .5rem', borderRadius: 6, border: '1px solid var(--border)', background: 'var(--bg)', color: 'var(--text)' } as const;

  function begin() { const q = shuffle(pool).slice(0, n); setQueue(q); setI(0); setRatings([]); startedAt.current = Date.now(); setPhase('ask'); timer.start(mins * 60); }
  function rate(r: number) {
    const rs = [...ratings, r]; setRatings(rs);
    if (i + 1 >= queue.length) {
      addMock({ type: 'mock-interview', label: chosen.join(', '), score: rs.reduce((a, b) => a + b, 0), total: 5 * rs.length, durationSec: Math.round((Date.now() - startedAt.current) / 1000), detail: { ids: queue.map((q) => q.id), ratings: rs } });
      timer.stop(); setPhase('done');
    } else { setI(i + 1); setPhase('ask'); timer.start(mins * 60); }
  }
  const hist = store.mocks.filter((m) => m.type === 'mock-interview');
  const points = hist.slice(-12).map((m) => ({ pct: Math.round((100 * m.score) / Math.max(1, m.total)), label: new Date(m.at).toLocaleDateString() }));

  const main = (() => {
    if (!items.length) return <div className="card"><strong>No interview questions yet.</strong><p className="muted" style={{ marginBottom: 0 }}>Question banks have not been added.</p></div>;
    if (phase === 'setup') return (
      <form className="card" onSubmit={(e) => { e.preventDefault(); if (n > 0) begin(); }} style={{ display: 'grid', gap: '.75rem', maxWidth: '36rem' }}>
        <fieldset style={{ border: 0, padding: 0, margin: 0 }}>
          <legend style={{ fontWeight: 600 }}>Categories (none selected means all)</legend>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '.4rem .9rem' }}>
            {cats.map((c) => <label key={c} style={{ display: 'inline-flex', gap: '.3rem' }}><input type="checkbox" checked={sel.includes(c)} onChange={(e) => setSel(e.target.checked ? [...sel, c] : sel.filter((x) => x !== c))} />{c} ({items.filter((x) => x.category === c).length})</label>)}
          </div>
        </fieldset>
        <label>Time per question<br /><select value={mins} onChange={(e) => setMins(+e.target.value)} style={{ ...field, width: '100%' }}>{[1, 2, 3, 5].map((m) => <option key={m} value={m}>{m} min</option>)}</select></label>
        <label>Questions in session<br /><select value={num} onChange={(e) => setNum(+e.target.value)} style={{ ...field, width: '100%' }}>{[3, 5, 8, 10].map((m) => <option key={m}>{m}</option>)}</select></label>
        <p className="muted" style={{ margin: 0, fontSize: '.85rem' }}>{pool.length} questions available. Speak your answer out loud, then check the model answer.</p>
        <button className="btn btn-primary" disabled={n === 0}>Start session</button>
      </form>
    );
    if (phase === 'done') {
      const tot = ratings.reduce((a, b) => a + b, 0);
      return (
        <div>
          <div className="verdict info" role="status"><strong>Session done. Average self-rating: {(tot / ratings.length).toFixed(1)} / 5</strong></div>
          <ol>{queue.map((q, k) => <li key={q.id}>{q.question} <span className="chip">{ratings[k]}/5</span></li>)}</ol>
          <p className="muted">Review any question rated 3 or lower in the <a href={url('/interview/banks/')}>question banks</a>.</p>
          <button className="btn btn-primary" onClick={() => setPhase('setup')}>New session</button>
        </div>
      );
    }
    const q = queue[i];
    return (
      <section aria-label="Mock interview">
        <div style={{ display: 'flex', justifyContent: 'space-between', gap: '.5rem', flexWrap: 'wrap' }}>
          <strong>Question {i + 1} of {queue.length}</strong>
          <span className="chip" role="timer" aria-label="Time left" style={timer.left === 0 && phase === 'ask' ? { color: 'var(--bad, #b91c1c)' } : undefined}>⏱ {phase === 'ask' ? fmtClock(timer.left) : 'time up / revealed'}</span>
        </div>
        <div className="card" style={{ margin: '.75rem 0' }}>
          <div className="pq-head"><span className="chip">{q.category}</span><span className={`chip chip-${q.difficulty}`}>{q.difficulty}</span></div>
          <h2 style={{ fontSize: '1.15rem', margin: '.25rem 0 .75rem' }}>{q.question}</h2>
          {phase === 'ask' && <button className="btn btn-primary" onClick={() => { timer.stop(); setPhase('reveal'); }}>{timer.left === 0 ? 'Time is up: show model answer' : 'Done answering: show model answer'}</button>}
          {phase === 'reveal' && (
            <div>
              <p className="muted" style={{ fontSize: '.85rem' }}><strong>Interviewer is testing:</strong> {q.whatInterviewerIsTesting}</p>
              <Md>{q.modelAnswer}</Md>
              {q.followUps.length > 0 && <><h4>Possible follow-ups</h4><ul>{q.followUps.map((f, k) => <li key={k}>{f}</li>)}</ul></>}
              <fieldset style={{ border: 0, padding: 0, marginTop: '.75rem' }}>
                <legend style={{ fontWeight: 600 }}>How did your answer compare? (1 = missed it, 5 = nailed it)</legend>
                <div style={{ display: 'flex', gap: '.5rem' }}>{[1, 2, 3, 4, 5].map((r) => <button key={r} className="btn" onClick={() => rate(r)} aria-label={`Rate ${r} out of 5`}>{r}</button>)}</div>
              </fieldset>
            </div>
          )}
        </div>
      </section>
    );
  })();

  return (
    <div>
      {main}
      <h2>Score history</h2>
      <Chart points={points} />
      {hist.length > 0 && <p className="muted" style={{ fontSize: '.85rem' }}>{hist.length} session(s) so far.</p>}
      <h2 id="project-script">Talk through your project</h2>
      <p>Interviewers often say "Walk me through a project." Prepare a 2-minute answer. Fill each part in your own words, then read it aloud with a timer. Your notes stay on this device.</p>
      <ol>{SCRIPT.map(([h, d]) => <li key={h}><strong>{h}.</strong> {d}</li>)}</ol>
      <label htmlFor="proj-script" className="sr-only">Project script</label>
      <textarea id="proj-script" className="editor" rows={10} value={script} onChange={(e) => { setScript(e.target.value); setSaved(''); }} placeholder={'Problem: ...\nData: ...\nApproach: ...\nInsight: ...\nImpact: ...\nLearning: ...'} />
      <div style={{ display: 'flex', gap: '.5rem', alignItems: 'center', margin: '.5rem 0', flexWrap: 'wrap' }}>
        <button className="btn" onClick={() => { setNote(NOTE_KEY, script); setSaved('Saved.'); }}>Save script</button>
        <PracticeTimer />
        <span role="status" className="muted">{saved}</span>
      </div>
      <p className="muted" style={{ fontSize: '.85rem' }}>Words: {script.trim() ? script.trim().split(/\s+/).length : 0}. Aim for about 250 words, which takes two minutes to say.</p>
    </div>
  );
}

function PracticeTimer() {
  const t = useCountdown(() => {});
  return t.running ? <><span className="chip" role="timer">⏱ {fmtClock(t.left)}</span><button className="btn" onClick={t.stop}>Stop</button></> : <button className="btn" onClick={() => t.start(120)}>Start 2-minute timer</button>;
}
