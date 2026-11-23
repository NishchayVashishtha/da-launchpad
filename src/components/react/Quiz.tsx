import { useEffect, useState } from 'react';
import Md from './Md';
import { recordQuiz } from '../../lib/progress';
import { useProgress } from '../../lib/progress-react';
import { base } from '../../lib/url';

export type QuizQ = { q: string; options: string[]; answer: number; explanation: string };
/** Props: questions (usually 5), id? (defaults to the lesson path), topic? (label for weak-topic detector). */
export default function Quiz({ questions, id, topic }: { questions: QuizQ[]; id?: string; topic?: string }) {
  const [qid, setQid] = useState(id ?? '');
  const [label, setLabel] = useState(topic ?? '');
  const [picked, setPicked] = useState<(number | null)[]>(() => questions.map(() => null));
  const [submitted, setSubmitted] = useState(false);
  const store = useProgress();
  useEffect(() => {
    const path = '/' + location.pathname.replace(base, '');
    if (!id) setQid(path);
    if (!topic) setLabel(document.querySelector('h1')?.textContent?.trim() || path);
  }, []);
  const score = picked.reduce<number>((n, p, i) => n + (p === questions[i].answer ? 1 : 0), 0);
  const prev = qid ? store.quizzes[qid] : undefined;
  function submit() { setSubmitted(true); if (qid) recordQuiz(qid, label, score, questions.length); }
  function retry() { setPicked(questions.map(() => null)); setSubmitted(false); }
  return (
    <section className="card no-print" style={{ margin: '1.25rem 0' }} aria-label="Quiz">
      {prev && !submitted && <p className="muted" style={{ marginTop: 0, fontSize: '.85rem' }}>Last score: {prev.score}/{prev.total} on {new Date(prev.at).toLocaleDateString()}</p>}
      <ol style={{ paddingLeft: '1.2rem', margin: 0 }}>
        {questions.map((qq, i) => (
          <li key={i} style={{ marginBottom: '1.1rem' }}>
            <fieldset style={{ border: 0, padding: 0, margin: 0 }}>
              <legend style={{ fontWeight: 600 }}><Md inline>{qq.q}</Md></legend>
              {qq.options.map((o, j) => {
                const right = submitted && j === qq.answer; const wrong = submitted && picked[i] === j && j !== qq.answer;
                return (
                  <label key={j} style={{ display: 'flex', gap: '.5rem', padding: '.25rem .4rem', borderRadius: 6, cursor: 'pointer', background: right ? 'var(--ok-soft)' : wrong ? 'var(--bad-soft)' : undefined }}>
                    <input type="radio" name={`quiz-${qid}-${i}`} checked={picked[i] === j} disabled={submitted} onChange={() => setPicked(picked.map((p, k) => (k === i ? j : p)))} />
                    <span><Md inline>{o}</Md></span>{right && <span aria-label="correct">✓</span>}{wrong && <span aria-label="wrong">✗</span>}
                  </label>
                );
              })}
            </fieldset>
            {submitted && <div className="callout callout-real" style={{ margin: '.4rem 0 0' }}><div className="callout-title">{picked[i] === qq.answer ? 'Correct' : 'Not quite'}</div><Md>{qq.explanation}</Md></div>}
          </li>
        ))}
      </ol>
      {!submitted
        ? <button className="btn btn-primary" onClick={submit} disabled={picked.some((p) => p === null)}>Check answers</button>
        : <div style={{ display: 'flex', gap: '.75rem', alignItems: 'center' }}><strong role="status">Score: {score}/{questions.length}</strong><button className="btn" onClick={retry}>Try again</button></div>}
    </section>
  );
}
