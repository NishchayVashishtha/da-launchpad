import { useMemo, useState } from 'react';
import Md from './Md';
import { useProgress } from '../../lib/progress-react';
import { setQuestionDone, toggleBookmark } from '../../lib/progress';

export type IQ = { id: string; category: string; question: string; whatInterviewerIsTesting: string; modelAnswer: string; followUps: string[]; commonMistakes: string[]; difficulty: 'easy' | 'medium' | 'hard' };
type Status = 'all' | 'todo' | 'practised' | 'bookmarked';

/** Browse interview questions. `category` locks the list to one category; otherwise a category filter is shown. */
export default function InterviewBank({ items, category }: { items: IQ[]; category?: string }) {
  const store = useProgress();
  const [q, setQ] = useState('');
  const [diff, setDiff] = useState('all');
  const [cat, setCat] = useState('all');
  const [status, setStatus] = useState<Status>('all');
  const [open, setOpen] = useState<Record<string, boolean>>({});
  const cats = useMemo(() => [...new Set(items.map((i) => i.category))].sort(), [items]);
  const shown = items.filter((i) => {
    if (category && i.category !== category) return false;
    if (!category && cat !== 'all' && i.category !== cat) return false;
    if (diff !== 'all' && i.difficulty !== diff) return false;
    const done = !!store.questions[i.id]?.doneAt; const star = !!store.bookmarks[i.id];
    if (status === 'todo' && done) return false;
    if (status === 'practised' && !done) return false;
    if (status === 'bookmarked' && !star) return false;
    if (q.trim()) { const t = q.toLowerCase(); if (!(i.question + ' ' + i.modelAnswer + ' ' + i.whatInterviewerIsTesting).toLowerCase().includes(t)) return false; }
    return true;
  });
  if (!items.length) return <p className="card">No interview questions are available yet.</p>;
  const field = { padding: '.4rem .5rem', borderRadius: 6, border: '1px solid var(--border)', background: 'var(--bg)', color: 'var(--text)' } as const;
  return (
    <div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '.5rem', margin: '1rem 0' }} role="search">
        <label className="sr-only" htmlFor="ib-q">Search questions</label>
        <input id="ib-q" type="search" placeholder="Search questions" value={q} onChange={(e) => setQ(e.target.value)} style={{ ...field, flex: '1 1 14rem' }} />
        {!category && <><label className="sr-only" htmlFor="ib-cat">Category</label><select id="ib-cat" value={cat} onChange={(e) => setCat(e.target.value)} style={field}><option value="all">All categories</option>{cats.map((c) => <option key={c} value={c}>{c}</option>)}</select></>}
        <label className="sr-only" htmlFor="ib-d">Difficulty</label>
        <select id="ib-d" value={diff} onChange={(e) => setDiff(e.target.value)} style={field}><option value="all">Any difficulty</option><option>easy</option><option>medium</option><option>hard</option></select>
        <label className="sr-only" htmlFor="ib-s">Status</label>
        <select id="ib-s" value={status} onChange={(e) => setStatus(e.target.value as Status)} style={field}><option value="all">All</option><option value="todo">Not practised</option><option value="practised">Practised</option><option value="bookmarked">Bookmarked</option></select>
      </div>
      <p className="muted" role="status" style={{ fontSize: '.85rem' }}>{shown.length} of {category ? items.filter((i) => i.category === category).length : items.length} questions. {shown.filter((i) => store.questions[i.id]?.doneAt).length} practised.</p>
      {shown.map((i) => {
        const isOpen = !!open[i.id]; const done = !!store.questions[i.id]?.doneAt; const star = !!store.bookmarks[i.id];
        return (
          <article key={i.id} className={`pq ${done ? 'done' : ''}`} id={i.id} aria-label={i.question}>
            <div className="pq-head">
              <span className={`chip chip-${i.difficulty}`}>{i.difficulty}</span>
              {!category && <span className="chip">{i.category}</span>}
              {done && <span className="chip">practised</span>}
              <button className="star" style={{ marginLeft: 'auto' }} aria-pressed={star} aria-label={star ? 'Remove bookmark' : 'Bookmark question'} onClick={() => toggleBookmark(i.id)}>{star ? '★' : '☆'}</button>
            </div>
            <div className="pq-body">
              <h3 style={{ margin: '0 0 .5rem', fontSize: '1.05rem' }}>{i.question}</h3>
              <button className="btn" aria-expanded={isOpen} aria-controls={`${i.id}-ans`} onClick={() => setOpen({ ...open, [i.id]: !isOpen })}>{isOpen ? 'Hide model answer' : 'Show model answer'}</button>
              <label style={{ display: 'inline-flex', gap: '.4rem', alignItems: 'center', marginLeft: '.75rem', fontSize: '.875rem' }}>
                <input type="checkbox" checked={done} onChange={(e) => setQuestionDone(i.id, e.target.checked, { module: 'interview', topic: i.category })} /> Practised
              </label>
              {isOpen && (
                <div id={`${i.id}-ans`} style={{ marginTop: '.75rem' }}>
                  <p className="muted" style={{ margin: '0 0 .4rem', fontSize: '.85rem' }}><strong>Interviewer is testing:</strong> {i.whatInterviewerIsTesting}</p>
                  <Md>{i.modelAnswer}</Md>
                  {i.followUps.length > 0 && <><h4 style={{ margin: '.6rem 0 .2rem' }}>Follow-ups</h4><ul>{i.followUps.map((f, k) => <li key={k}>{f}</li>)}</ul></>}
                  {i.commonMistakes.length > 0 && <div className="callout callout-mistake"><div className="callout-title">Common mistakes</div><ul style={{ margin: 0 }}>{i.commonMistakes.map((f, k) => <li key={k}>{f}</li>)}</ul></div>}
                </div>
              )}
            </div>
          </article>
        );
      })}
      {shown.length === 0 && <p className="card">No questions match these filters.</p>}
    </div>
  );
}
