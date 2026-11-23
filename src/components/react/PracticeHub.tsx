import { useEffect, useMemo, useState } from 'react';
import { useProgress } from '../../lib/progress-react';
import { Question, type PQ } from './PracticeSet';
import { url } from '../../lib/url';

export type Slim = { id: string; module: string; topic: string; difficulty: string; language: string; question: string; tags: string[] };
let fullCache: Record<string, PQ> | null = null;

function Row({ q }: { q: Slim }) {
  const [open, setOpen] = useState(false);
  const [full, setFull] = useState<PQ | null>(null);
  const [err, setErr] = useState('');
  const s = useProgress();
  const rec = s.questions[q.id];
  useEffect(() => {
    if (!open || full) return;
    (async () => {
      try {
        fullCache ||= await (await fetch(url('practice-data.json'))).json();
        setFull(fullCache![q.id]);
      } catch (e: any) { setErr('Could not load the question: ' + e.message); }
    })();
  }, [open]);
  const plain = q.question.replace(/[`*_#>]/g, '').slice(0, 140);
  return (
    <li style={{ listStyle: 'none', margin: '.4rem 0' }}>
      <button className="btn" style={{ width: '100%', justifyContent: 'flex-start', textAlign: 'left', gap: '.6rem' }} aria-expanded={open} onClick={() => setOpen(!open)}>
        <span aria-label={rec?.doneAt ? 'done' : 'not done'} style={{ color: 'var(--ok)', width: '1rem' }}>{rec?.doneAt ? '✓' : ''}</span>
        <span className={`chip chip-${q.difficulty}`}>{q.difficulty}</span>
        <span style={{ flex: 1 }}>{plain}{q.question.length > 140 ? '...' : ''}</span>
        <span className="chip">{q.language}</span>
        {s.bookmarks[q.id] && <span style={{ color: '#e0a100' }} aria-label="bookmarked">★</span>}
      </button>
      {open && (full ? <Question q={full} compact /> : <p className="muted">{err || 'Loading...'}</p>)}
    </li>
  );
}

export default function PracticeHub({ questions, only }: { questions: Slim[]; only?: 'bookmarks' }) {
  const s = useProgress();
  const [f, setF] = useState({ module: '', topic: '', difficulty: '', language: '', status: '', text: '', bookmarked: only === 'bookmarks' });
  const [limit, setLimit] = useState(30);
  useEffect(() => {
    const p = new URLSearchParams(location.search);
    setF((x) => ({ ...x, module: p.get('module') ?? '', topic: p.get('topic') ?? '', difficulty: p.get('difficulty') ?? '' }));
  }, []);
  const modules = useMemo(() => [...new Set(questions.map((q) => q.module))], [questions]);
  const topics = useMemo(() => [...new Set(questions.filter((q) => !f.module || q.module === f.module).map((q) => q.topic))].sort(), [questions, f.module]);
  const list = questions.filter((q) =>
    (!f.module || q.module === f.module) && (!f.topic || q.topic === f.topic) && (!f.difficulty || q.difficulty === f.difficulty) &&
    (!f.language || q.language === f.language) &&
    (f.status === '' || (f.status === 'done') === !!s.questions[q.id]?.doneAt) &&
    (!f.bookmarked || s.bookmarks[q.id]) &&
    (!f.text || (q.question + q.tags.join(' ') + q.topic + q.id).toLowerCase().includes(f.text.toLowerCase())));
  const sel = (label: string, key: keyof typeof f, opts: string[]) => (
    <div><label className="lbl" htmlFor={`f-${key}`}>{label}</label>
      <select id={`f-${key}`} className="field" value={String(f[key])} onChange={(e) => { setF({ ...f, [key]: e.target.value, ...(key === 'module' ? { topic: '' } : {}) }); setLimit(30); }}>
        <option value="">All</option>{opts.map((o) => <option key={o} value={o}>{o}</option>)}
      </select></div>
  );
  if (!questions.length) return <p className="card">No practice questions yet. Questions are added as modules are written.</p>;
  return (
    <div>
      <div style={{ display: 'grid', gap: '.6rem', gridTemplateColumns: 'repeat(auto-fit, minmax(9rem, 1fr))', marginBottom: '1rem' }}>
        {sel('Module', 'module', modules)}{sel('Topic', 'topic', topics)}{sel('Difficulty', 'difficulty', ['easy', 'medium', 'hard'])}{sel('Language', 'language', ['sql', 'python', 'excel', 'dax', 'text'])}
        <div><label className="lbl" htmlFor="f-status">Status</label>
          <select id="f-status" className="field" value={f.status} onChange={(e) => setF({ ...f, status: e.target.value })}><option value="">All</option><option value="done">Done</option><option value="todo">Not done</option></select></div>
        <div><label className="lbl" htmlFor="f-text">Search</label><input id="f-text" className="field" value={f.text} onChange={(e) => setF({ ...f, text: e.target.value })} /></div>
      </div>
      <label style={{ display: 'inline-flex', gap: '.4rem', marginBottom: '.5rem' }}><input type="checkbox" checked={f.bookmarked} disabled={only === 'bookmarks'} onChange={(e) => setF({ ...f, bookmarked: e.target.checked })} /> Bookmarked only</label>
      <p className="muted" role="status">{list.length} question{list.length === 1 ? '' : 's'}</p>
      <ul style={{ padding: 0 }}>{list.slice(0, limit).map((q) => <Row key={q.id} q={q} />)}</ul>
      {list.length > limit && <button className="btn" onClick={() => setLimit(limit + 30)}>Show more</button>}
    </div>
  );
}
