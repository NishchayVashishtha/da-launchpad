import { useEffect, useRef, useState } from 'react';
let seq = 0;
/** Client-side Mermaid diagram (lazy import). Prop: chart (mermaid source). Re-renders on theme change. */
export default function Mermaid({ chart, caption }: { chart: string; caption?: string }) {
  const ref = useRef<HTMLDivElement>(null);
  const [err, setErr] = useState('');
  useEffect(() => {
    let dead = false;
    const draw = async () => {
      try {
        const mermaid = (await import('mermaid')).default;
        const dark = document.documentElement.dataset.theme === 'dark';
        mermaid.initialize({ startOnLoad: false, theme: dark ? 'dark' : 'default', securityLevel: 'strict' });
        const { svg } = await mermaid.render(`mmd-${++seq}`, chart);
        if (!dead && ref.current) ref.current.innerHTML = svg;
      } catch (e: any) { if (!dead) setErr(String(e.message || e)); }
    };
    draw();
    const mo = new MutationObserver(draw);
    mo.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
    return () => { dead = true; mo.disconnect(); };
  }, [chart]);
  return (
    <figure style={{ margin: '1.25rem 0', overflowX: 'auto' }}>
      <div ref={ref} role="img" aria-label={caption ?? 'Diagram'}><pre className="muted" style={{ fontSize: '.75rem' }}>{chart}</pre></div>
      {err && <p className="verdict fail">Diagram error: {err}</p>}
      {caption && <figcaption className="muted" style={{ fontSize: '.8rem' }}>{caption}</figcaption>}
    </figure>
  );
}
