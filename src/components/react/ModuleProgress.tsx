import { useProgress } from '../../lib/progress-react';
export default function ModuleProgress({ lessonIds }: { module: string; lessonIds: string[] }) {
  const s = useProgress();
  if (!lessonIds.length) return null;
  const done = lessonIds.filter((id) => s.lessons[id]).length;
  const pct = Math.round((done / lessonIds.length) * 100);
  return (
    <div style={{ margin: '1rem 0' }} aria-label="Module progress">
      <div className="bar" role="progressbar" aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100}><i style={{ width: `${pct}%` }} /></div>
      <p className="muted" style={{ fontSize: '.8rem', margin: '.25rem 0' }}>{done} of {lessonIds.length} lessons complete ({pct}%)</p>
    </div>
  );
}
