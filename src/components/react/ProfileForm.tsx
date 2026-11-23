import { useState } from 'react';
import { useProgress } from '../../lib/progress-react';
import { saveProfile, saveSettings } from '../../lib/progress';
import ProgressIO from './ProgressIO';

const LABELS: Record<string, [string, boolean?]> = {
  name: ['Name'], degree: ['Degree'], branch: ['Branch'], gradYear: ['Graduation year'], codingLevel: ['Coding level (none / basic / intermediate)'],
  hoursPerDay: ['Study hours per day'], targetCities: ['Target cities / remote'], targetIndustries: ['Target industries (in priority order)'],
  background: ['Strengths, hobbies, internships, projects', true], timeline: ['Timeline to first job'], longTermGoal: ['Long-term goal', true],
};
export default function ProfileForm({ defaults }: { defaults: Record<string, string | number> }) {
  const s = useProgress();
  const merged = { ...defaults, ...s.profile };
  const [draft, setDraft] = useState<Record<string, string | number> | null>(null);
  const [saved, setSaved] = useState(false);
  const values = draft ?? merged;
  const set = (k: string, v: string) => { setDraft({ ...values, [k]: v }); setSaved(false); };
  return (
    <div style={{ maxWidth: '44rem' }}>
      <form onSubmit={(e) => { e.preventDefault(); saveProfile(values); setDraft(null); setSaved(true); }} className="card" style={{ display: 'grid', gap: '.8rem' }}>
        {Object.keys(defaults).map((k) => {
          const [label, multi] = LABELS[k] ?? [k];
          return (
            <div key={k}>
              <label className="lbl" htmlFor={`p-${k}`}>{label}</label>
              {multi ? <textarea id={`p-${k}`} className="field" rows={2} value={String(values[k] ?? '')} onChange={(e) => set(k, e.target.value)} />
                : <input id={`p-${k}`} className="field" value={String(values[k] ?? '')} onChange={(e) => set(k, e.target.value)} />}
            </div>
          );
        })}
        <div style={{ display: 'flex', gap: '.75rem', alignItems: 'center', flexWrap: 'wrap' }}>
          <button className="btn btn-primary">Save profile</button>
          <button type="button" className="btn" onClick={() => { setDraft({ ...defaults }); setSaved(false); }}>Reset to defaults</button>
          <span role="status" className="muted">{saved ? 'Saved in this browser.' : ''}</span>
        </div>
      </form>
      <h2>Study plan start date</h2>
      <div style={{ display: 'flex', gap: '.75rem', alignItems: 'end' }}>
        <div><label className="lbl" htmlFor="sd">Day 1 of the 12-week plan</label>
          <input id="sd" type="date" className="field" value={s.settings.startDate ?? ''} onChange={(e) => saveSettings({ startDate: e.target.value || undefined })} /></div>
      </div>
      <h2>Backup and restore</h2>
      <ProgressIO />
    </div>
  );
}
