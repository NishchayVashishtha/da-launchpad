import { useSyncExternalStore } from 'react';
import { load, subscribe, empty, type Store } from './progress';

const serverSnap = empty();
/** React hook: re-renders whenever the progress store changes. SSR renders an empty store. */
export function useProgress(): Store {
  return useSyncExternalStore(subscribe, load, () => serverSnap);
}
/** True after hydration; use to avoid server/client markup mismatch for localStorage-driven UI. */
import { useEffect, useState } from 'react';
export function useMounted() { const [m, setM] = useState(false); useEffect(() => setM(true), []); return m; }
