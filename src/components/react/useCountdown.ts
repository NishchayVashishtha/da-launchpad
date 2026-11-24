import { useEffect, useRef, useState } from 'react';
/** Countdown in seconds. start(sec) begins; onEnd fires once at zero. Uses wall-clock so background tabs stay correct. */
export function useCountdown(onEnd: () => void) {
  const [left, setLeft] = useState(0);
  const [running, setRunning] = useState(false);
  const endAt = useRef(0);
  const cb = useRef(onEnd); cb.current = onEnd;
  useEffect(() => {
    if (!running) return;
    const t = setInterval(() => {
      const l = Math.max(0, Math.round((endAt.current - Date.now()) / 1000));
      setLeft(l);
      if (l <= 0) { setRunning(false); cb.current(); }
    }, 250);
    return () => clearInterval(t);
  }, [running]);
  return {
    left, running,
    start(sec: number) { endAt.current = Date.now() + sec * 1000; setLeft(sec); setRunning(true); },
    stop() { setRunning(false); },
  };
}
export const fmtClock = (s: number) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
