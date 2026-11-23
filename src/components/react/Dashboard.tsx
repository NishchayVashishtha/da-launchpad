import { useState } from 'react';
import { useProgress } from '../../lib/progress-react';
import { logHours, saveSettings, setGoal, streak, today, weekStart, weeklyHours, weakTopics, dueFlashcards, addDays, dayKey } from '../../lib/progress';
import { url } from '../../lib/url';
import ProgressIO from './ProgressIO';

type PlanDay = { week: number; day: number; title: string; tasks: string[]; links?: { label: string; href: string }[] };
type Props = {
  modules: { slug: string; title: string; lessonIds: string[]; questionIds: string[] }[];
  flashcardIds: string[]; plan: PlanDay[]; name: string; quickLinks: { label: string; href: string }[];
};

function Ring({ pct }: { pct: number }) {
  const r = 52, c = 2 * Math.PI * r;
  return (
    <svg width="132" height="132" viewBox="0 0 132 132" role="img" aria-label={`Overall progress ${pct} percent`}>
      <circle cx="66" cy="66" r={r} fill="none" stroke="var(--surface-2)" strokeWidth="12" />
      <circle cx="66" cy="66" r={r} fill="none" stroke="var(--brand)" strokeWidth="12" strokeLinecap="round" strokeDasharray={c} strokeDashoffset={c * (1 - pct / 100)} transform="rotate(-90 66 66)" />
      <text x="66" y="72" textAnchor="middle" fontSize="26" fontWeight="700" fill="var(--text)">{pct}%</text>
    </svg>
  );
}

function HoursChart({ data, goal }: { data: { date: string; hours: number }[]; goal?: number }) {
  const max = Math.max(1, ...data.map((d) => d.hours), (goal ?? 0) / 7);
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  return (
    <svg viewBox="0 0 280 120" width="100%" role="img" aria-label={`Study hours this week: ${data.map((d, i) => `${days[i]} ${d.hours.toFixed(1)}`).join(', ')}`}>
      {data.map((d, i) => {
        const h = (d.hours / max) * 80;
        return (
          <g key={d.date}>
            <rect x={i * 40 + 8} y={90 - h} width="24" height={h} rx="4" fill={d.date === today() ? 'var(--brand)' : 'var(--brand-soft)'} stroke="var(--brand)" strokeWidth="1" />
            {d.hours > 0 && <text x={i * 40 + 20} y={86 - h} textAnchor="middle" fontSize="9" fill="var(--text)">{d.hours.toFixed(1)}</text>}
            <text x={i * 40 + 20} y="108" textAnchor="middle" fontSize="10" fill="var(--muted)">{days[i]}</text>
          </g>
        );
      })}
      <line x1="0" y1="90" x2="280" y2="90" stroke="var(--border)" />
    </svg>
  );
}

export default function Dashboard({ modules, flashcardIds, plan, name, quickLinks }: Props) {
  const s = useProgress();
  const [mins, setMins] = useState('60');
  const sorted = [...plan].sort((a, b) => a.week - b.week || a.day - b.day);
  const abs = (p: PlanDay) => (p.week - 1) * 7 + p.day;
  const start = s.settings.startDate;
  let dayNo = 0;
  if (start) { const [y, m, d] = start.split('-').map(Number); dayNo = Math.floor((new Date().setHours(0, 0, 0, 0) - new Date(y, m - 1, d).getTime()) / 86400000) + 1; }
  const todayTask = !start || !sorted.length ? null : [...sorted].reverse().find((p) => abs(p) <= dayNo) ?? sorted[0];

  const totalL = modules.reduce((n, m) => n + m.lessonIds.length, 0);
  const totalQ = modules.reduce((n, m) => n + m.questionIds.length, 0);
  const doneL = modules.reduce((n, m) => n + m.lessonIds.filter((id) => s.lessons[id]).length, 0);
  const doneQ = modules.reduce((n, m) => n + m.questionIds.filter((id) => s.questions[id]?.doneAt).length, 0);
  const pct = totalL + totalQ ? Math.round(((doneL + doneQ) / (totalL + totalQ)) * 100) : 0;
  const st = streak(s);
  const wk = weeklyHours(s);
  const weekTotal = wk.reduce((n, d) => n + d.hours, 0);
  const wkKey = weekStart();
  const goal = s.goals[wkKey];
  const due = dueFlashcards(flashcardIds, s).length;
  const weak = weakTopics(s).slice(0, 5);
  const weekQs = Object.values(s.questions).filter((r) => r.doneAt && r.doneAt.slice(0, 10) >= wkKey && r.doneAt.slice(0, 10) <= addDays(wkKey, 6)).length;

  return (
    <div style={{ maxWidth: '72rem', margin: '0 auto' }}>
      <h1 style={{ marginTop: 0 }}>{((s.profile.name as string) || name) ? `Welcome back, ${((s.profile.name as string) || name).split(' ')[0]}` : 'Dashboard'}</h1>
      <div style={{ display: 'grid', gap: '1rem', gridTemplateColumns: 'repeat(auto-fit, minmax(17rem, 1fr))' }}>
        <section className="card" aria-labelledby="today-h" style={{ gridColumn: '1 / -1' }}>
          <h2 id="today-h" style={{ fontSize: '1.1rem' }}>Today&apos;s task {todayTask && <span className="chip">Week {todayTask.week} · Day {todayTask.day}</span>}</h2>
          {!start ? (
            <div><p>Start your 12-week plan to see a task for each day.</p><button className="btn btn-primary" onClick={() => saveSettings({ startDate: today() })}>Start plan today</button></div>
          ) : !todayTask ? <p className="muted">The plan has no entries yet.</p> : (
            <>
              <p style={{ fontWeight: 600, margin: '0 0 .4rem' }}>{todayTask.title}</p>
              <ul style={{ margin: 0, paddingLeft: '1.2rem' }}>{todayTask.tasks.map((t, i) => <li key={i}>{t}</li>)}</ul>
              <p style={{ display: 'flex', gap: '.5rem', flexWrap: 'wrap', marginBottom: 0 }}>
                {todayTask.links?.map((l) => <a key={l.href} className="btn btn-sm" href={url(l.href)}>{l.label}</a>)}
                <span className="muted" style={{ fontSize: '.78rem', alignSelf: 'center' }}>Plan day {dayNo} (started {start}) · <button className="btn btn-ghost btn-sm" onClick={() => saveSettings({ startDate: today() })}>restart from today</button></span>
              </p>
            </>
          )}
        </section>

        <section className="card" style={{ display: 'flex', gap: '1rem', alignItems: 'center' }} aria-label="Overall progress">
          <Ring pct={pct} />
          <div><strong>Overall</strong><p className="muted" style={{ margin: '.2rem 0', fontSize: '.88rem' }}>{doneL}/{totalL} lessons<br />{doneQ}/{totalQ} questions</p></div>
        </section>

        <section className="card" aria-label="Streak">
          <h2 style={{ fontSize: '1.1rem' }}>Streak</h2>
          <p style={{ fontSize: '2rem', fontWeight: 800, margin: 0 }}>🔥 {st.current} <span style={{ fontSize: '.9rem', fontWeight: 400 }} className="muted">day{st.current === 1 ? '' : 's'}</span></p>
          <p className="muted" style={{ margin: 0, fontSize: '.85rem' }}>Longest: {st.longest} days. Any lesson, question or logged hour counts.</p>
        </section>

        <section className="card" aria-label="Weekly study hours">
          <h2 style={{ fontSize: '1.1rem' }}>This week: {weekTotal.toFixed(1)} h {goal && <span className="muted" style={{ fontSize: '.8rem' }}>/ goal {goal.hours} h</span>}</h2>
          <HoursChart data={wk} goal={goal?.hours} />
          <form style={{ display: 'flex', gap: '.5rem', alignItems: 'end', flexWrap: 'wrap' }} onSubmit={(e) => { e.preventDefault(); const n = parseInt(mins); if (n > 0) logHours(n); }}>
            <div><label className="lbl" htmlFor="mins">Log study time (minutes)</label><input id="mins" className="field" type="number" min="5" step="5" value={mins} onChange={(e) => setMins(e.target.value)} style={{ width: '7rem' }} /></div>
            <button className="btn btn-primary">Add</button>
          </form>
          <form style={{ display: 'flex', gap: '.5rem', alignItems: 'end', marginTop: '.6rem', flexWrap: 'wrap' }} onSubmit={(e) => { e.preventDefault(); const f = new FormData(e.currentTarget); setGoal(wkKey, Number(f.get('h')) || 0, Number(f.get('q')) || 0); }}>
            <div><label className="lbl" htmlFor="gh">Weekly goal: hours</label><input id="gh" name="h" className="field" type="number" min="0" defaultValue={goal?.hours ?? 30} style={{ width: '5.5rem' }} /></div>
            <div><label className="lbl" htmlFor="gq">questions</label><input id="gq" name="q" className="field" type="number" min="0" defaultValue={goal?.questions ?? 30} style={{ width: '5.5rem' }} /></div>
            <button className="btn btn-sm">Set goal</button>
          </form>
          {goal && <p className="muted" style={{ fontSize: '.82rem', marginBottom: 0 }}>Questions done this week: {weekQs}/{goal.questions}</p>}
        </section>

        <section className="card" aria-label="Module progress" style={{ gridColumn: 'span 1' }}>
          <h2 style={{ fontSize: '1.1rem' }}>Modules</h2>
          {modules.map((m) => {
            const dl = m.lessonIds.filter((id) => s.lessons[id]).length, dq = m.questionIds.filter((id) => s.questions[id]?.doneAt).length;
            const t = m.lessonIds.length + m.questionIds.length; const p = t ? Math.round(((dl + dq) / t) * 100) : 0;
            return (
              <div key={m.slug} style={{ marginBottom: '.6rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '.88rem' }}><a href={url(`/${m.slug}/`)}>{m.title}</a><span className="muted">{t ? `${p}%` : 'soon'}</span></div>
                <div className="bar" role="progressbar" aria-label={`${m.title} progress`} aria-valuenow={p} aria-valuemin={0} aria-valuemax={100}><i style={{ width: `${p}%` }} /></div>
              </div>
            );
          })}
        </section>

        <section className="card" aria-label="Revision">
          <h2 style={{ fontSize: '1.1rem' }}>Upcoming revision</h2>
          {flashcardIds.length > 0 && <p style={{ margin: '0 0 .5rem' }}><strong>{due}</strong> flashcard{due === 1 ? '' : 's'} due today.</p>}
          <h3 style={{ fontSize: '.95rem', margin: '.5rem 0 .25rem' }}>Weak topics</h3>
          {weak.length === 0 ? <p className="muted" style={{ fontSize: '.88rem', margin: 0 }}>Nothing flagged yet. Practise questions and take quizzes; topics with a low pass rate show up here.</p> : (
            <ul style={{ margin: 0, paddingLeft: '1.1rem', fontSize: '.9rem' }}>
              {weak.map((w) => <li key={w.key}>{w.href ? <a href={url(w.href)}>{w.label}</a> : w.label} <span className="muted">({Math.round(w.pct * 100)}%)</span></li>)}
            </ul>
          )}
        </section>

        <section className="card" aria-label="Quick links">
          <h2 style={{ fontSize: '1.1rem' }}>Quick links</h2>
          <div style={{ display: 'flex', gap: '.5rem', flexWrap: 'wrap' }}>
            {quickLinks.map((l) => <a key={l.href} className="btn" href={url(l.href)}>{l.label}</a>)}
          </div>
        </section>
      </div>
      <h2 style={{ fontSize: '1.1rem', marginTop: '2rem' }}>Backup</h2>
      <p className="muted" style={{ fontSize: '.88rem', marginTop: 0 }}>Your progress lives only in this browser. Export a backup now and then.</p>
      <ProgressIO />
    </div>
  );
}
