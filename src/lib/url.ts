/** Base-aware URL helper. url('/sql/select/') -> '<base>sql/select/'. Safe for external URLs. */
const BASE = (import.meta.env.BASE_URL || '/').replace(/\/?$/, '/');

export function url(path = ''): string {
  if (/^([a-z]+:)?\/\//i.test(path) || path.startsWith('mailto:') || path.startsWith('#') || path.startsWith('data:')) return path;
  const p = path.replace(/^\/+/, '');
  if (BASE !== '/' && (BASE.slice(0, -1) === '/' + p || ('/' + p).startsWith(BASE))) return '/' + p; // already prefixed
  return BASE + p;
}
export const base = BASE;
