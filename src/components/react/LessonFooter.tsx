import { useEffect, useState } from 'react';
import { useProgress } from '../../lib/progress-react';
import { setLessonDone, setNote, getNote } from '../../lib/progress';

export function CompleteBar({ lessonId }: { lessonId: string }) {
  const s = useProgress();
  const done = s.lessons[lessonId];
  return (
    <div className="card complete-bar" style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap', margin: '2rem 0 1rem' }}>
      <button className={`btn ${done ? '' : 'btn-primary'}`} aria-pressed={!!done} onClick={() => setLessonDone(lessonId, !done)}>
        {done ? '✓ Completed (click to undo)' : 'Mark lesson complete'}
      </button>
      {done && <span className="muted" style={{ fontSize: '.85rem' }}>Completed on {new Date(done.doneAt).toLocaleString()}</span>}
    </div>
  );
}

export function Notes({ lessonId, title }: { lessonId: string; title: string }) {
  const [text, setText] = useState('');
  const [saved, setSaved] = useState('');
  useEffect(() => setText(getNote(lessonId)), [lessonId]);
  useEffect(() => {
    const t = setTimeout(() => { if (text !== getNote(lessonId)) { setNote(lessonId, text); setSaved('Saved'); } }, 500);
    return () => clearTimeout(t);
  }, [text]);
  function exportNote() {
    const blob = new Blob([`# Notes: ${title}\n\n${text}\n`], { type: 'text/markdown' });
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = `notes-${lessonId.replace('/', '-')}.md`; a.click();
  }
  return (
    <section className="card notes-box" aria-label="My notes">
      <h2 style={{ fontSize: '1.1rem', margin: '0 0 .5rem' }}>My notes</h2>
      <label className="sr-only" htmlFor="note-area">Notes for this lesson</label>
      <textarea id="note-area" className="field" rows={5} value={text} onChange={(e) => { setText(e.target.value); setSaved(''); }} placeholder="Write what you learned, doubts, or things to revise. Saved in this browser only." />
      <div style={{ display: 'flex', gap: '.75rem', alignItems: 'center', marginTop: '.5rem' }}>
        <button className="btn btn-sm" onClick={exportNote} disabled={!text.trim()}>Export note (.md)</button>
        <span className="muted" role="status" style={{ fontSize: '.8rem' }}>{saved}</span>
      </div>
    </section>
  );
}
