import { useRef, useState } from 'react';
import { downloadExport, importJson, resetAll } from '../../lib/progress';
export default function ProgressIO() {
  const file = useRef<HTMLInputElement>(null);
  const [msg, setMsg] = useState('');
  async function onFile(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0]; if (!f) return;
    const r = importJson(await f.text()); setMsg(r.message); e.target.value = '';
  }
  return (
    <div className="no-print" style={{ display: 'flex', gap: '.5rem', flexWrap: 'wrap', alignItems: 'center' }}>
      <button className="btn" onClick={downloadExport}>⬇ Export progress (JSON)</button>
      <button className="btn" onClick={() => file.current?.click()}>⬆ Import progress</button>
      <input ref={file} type="file" accept="application/json,.json" hidden onChange={onFile} aria-label="Import progress file" />
      <button className="btn btn-ghost" onClick={() => { if (confirm('Delete ALL your progress, notes and profile from this browser?')) { resetAll(); setMsg('Progress cleared.'); } }}>Reset all</button>
      <span role="status" className="muted" style={{ fontSize: '.85rem' }}>{msg}</span>
    </div>
  );
}
