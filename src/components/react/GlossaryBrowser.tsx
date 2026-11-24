import React, { useState, useMemo } from 'react';

export type GlossaryTerm = {
  id: string;
  term: string;
  definition: string;
  example?: string;
  related?: string[];
};

type Props = {
  terms: GlossaryTerm[];
};

const MODULE_FILTERS = [
  { id: 'all', label: 'All Modules' },
  { id: 'sql', label: 'SQL' },
  { id: 'py', label: 'Python & Pandas' },
  { id: 'xl', label: 'Excel' },
  { id: 'pbi', label: 'Power BI & DAX' },
  { id: 'stat', label: 'Statistics' },
  { id: 'biz', label: 'Business & Metrics' },
  { id: 'de', label: 'Data Engineering' },
];

const ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');

export default function GlossaryBrowser({ terms }: Props) {
  const [search, setSearch] = useState('');
  const [selectedModule, setSelectedModule] = useState('all');
  const [selectedLetter, setSelectedLetter] = useState<string | null>(null);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const filteredTerms = useMemo(() => {
    return terms.filter((t) => {
      // Module prefix check
      if (selectedModule !== 'all') {
        const prefix = `gl-${selectedModule}-`;
        if (!t.id.startsWith(prefix)) return false;
      }
      // Letter filter
      if (selectedLetter) {
        if (!t.term.toUpperCase().startsWith(selectedLetter)) return false;
      }
      // Text search
      if (search.trim()) {
        const q = search.toLowerCase();
        const matchesTerm = t.term.toLowerCase().includes(q);
        const matchesDef = t.definition.toLowerCase().includes(q);
        const matchesEx = (t.example || '').toLowerCase().includes(q);
        if (!matchesTerm && !matchesDef && !matchesEx) return false;
      }
      return true;
    });
  }, [terms, search, selectedModule, selectedLetter]);

  const handleCopy = (term: GlossaryTerm) => {
    navigator.clipboard.writeText(`${term.term}: ${term.definition}`);
    setCopiedId(term.id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const getModuleBadge = (id: string) => {
    if (id.startsWith('gl-sql-')) return { label: 'SQL', color: '#0284c7', bg: '#e0f2fe' };
    if (id.startsWith('gl-py-')) return { label: 'Python', color: '#16a34a', bg: '#dcfce7' };
    if (id.startsWith('gl-xl-')) return { label: 'Excel', color: '#15803d', bg: '#f0fdf4' };
    if (id.startsWith('gl-pbi-')) return { label: 'Power BI', color: '#d97706', bg: '#fef3c7' };
    if (id.startsWith('gl-stat-')) return { label: 'Statistics', color: '#9333ea', bg: '#f3e8ff' };
    if (id.startsWith('gl-biz-')) return { label: 'Business', color: '#ea580c', bg: '#ffedd5' };
    if (id.startsWith('gl-de-')) return { label: 'Data Eng', color: '#4f46e5', bg: '#e0e7ff' };
    return { label: 'General', color: '#4b5563', bg: '#f3f4f6' };
  };

  return (
    <div style={{ maxWidth: '64rem', margin: '0 auto', paddingBottom: '3rem' }}>
      {/* Search Input Bar */}
      <div style={{ position: 'relative', marginBottom: '1.25rem' }}>
        <input
          type="text"
          className="input"
          placeholder="Search 320+ analytics terms, formulas, definitions, or code idioms..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{
            width: '100%',
            padding: '0.85rem 1rem',
            fontSize: '1rem',
            borderRadius: '8px',
            border: '1px solid var(--border, #d1d5db)',
            background: 'var(--input-bg, #fff)',
          }}
        />
        {search && (
          <button
            type="button"
            onClick={() => setSearch('')}
            style={{
              position: 'absolute',
              right: '0.75rem',
              top: '50%',
              transform: 'translateY(-50%)',
              background: 'transparent',
              border: 'none',
              cursor: 'pointer',
              fontSize: '1rem',
              color: '#888',
            }}
          >
            ✕
          </button>
        )}
      </div>

      {/* Module Filter Pills */}
      <div style={{ display: 'flex', gap: '0.4rem', overflowX: 'auto', paddingBottom: '0.5rem', marginBottom: '0.75rem' }}>
        {MODULE_FILTERS.map((m) => (
          <button
            key={m.id}
            type="button"
            onClick={() => setSelectedModule(m.id)}
            style={{
              padding: '0.35rem 0.8rem',
              borderRadius: '999px',
              fontSize: '0.82rem',
              whiteSpace: 'nowrap',
              border: selectedModule === m.id ? '1px solid var(--accent, #2563eb)' : '1px solid var(--border, #e5e7eb)',
              background: selectedModule === m.id ? 'var(--accent, #2563eb)' : 'transparent',
              color: selectedModule === m.id ? '#fff' : 'inherit',
              cursor: 'pointer',
              fontWeight: selectedModule === m.id ? 600 : 400,
            }}
          >
            {m.label}
          </button>
        ))}
      </div>

      {/* A-Z Letter Bar */}
      <div style={{ display: 'flex', gap: '0.2rem', overflowX: 'auto', paddingBottom: '0.5rem', marginBottom: '1.5rem', alignItems: 'center' }}>
        <button
          type="button"
          onClick={() => setSelectedLetter(null)}
          style={{
            padding: '0.25rem 0.5rem',
            fontSize: '0.75rem',
            borderRadius: '4px',
            border: selectedLetter === null ? '1px solid var(--accent, #2563eb)' : '1px solid var(--border, #e5e7eb)',
            background: selectedLetter === null ? 'var(--accent, #2563eb)' : 'transparent',
            color: selectedLetter === null ? '#fff' : 'inherit',
            cursor: 'pointer',
            fontWeight: 600,
          }}
        >
          ALL
        </button>
        {ALPHABET.map((letter) => (
          <button
            key={letter}
            type="button"
            onClick={() => setSelectedLetter(selectedLetter === letter ? null : letter)}
            style={{
              padding: '0.25rem 0.45rem',
              fontSize: '0.75rem',
              borderRadius: '4px',
              border: selectedLetter === letter ? '1px solid var(--accent, #2563eb)' : '1px solid var(--border, #e5e7eb)',
              background: selectedLetter === letter ? 'var(--accent, #2563eb)' : 'transparent',
              color: selectedLetter === letter ? '#fff' : 'inherit',
              cursor: 'pointer',
              fontWeight: selectedLetter === letter ? 700 : 400,
            }}
          >
            {letter}
          </button>
        ))}
      </div>

      {/* Results Count */}
      <div style={{ marginBottom: '1rem', fontSize: '0.85rem', color: 'var(--muted, #666)' }}>
        Showing <strong>{filteredTerms.length}</strong> of {terms.length} terms
      </div>

      {/* Terms Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(18rem, 1fr))', gap: '1rem' }}>
        {filteredTerms.map((t) => {
          const badge = getModuleBadge(t.id);
          const isCopied = copiedId === t.id;
          return (
            <div
              key={t.id}
              className="card"
              style={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                padding: '1.25rem',
                borderRadius: '8px',
                border: '1px solid var(--border, #e5e7eb)',
                position: 'relative',
              }}
            >
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.6rem' }}>
                  <h3 style={{ margin: 0, fontSize: '1.05rem', fontWeight: 600 }}>{t.term}</h3>
                  <span
                    style={{
                      fontSize: '0.72rem',
                      fontWeight: 600,
                      padding: '0.15rem 0.5rem',
                      borderRadius: '4px',
                      color: badge.color,
                      background: badge.bg,
                    }}
                  >
                    {badge.label}
                  </span>
                </div>

                <p style={{ fontSize: '0.88rem', lineHeight: 1.5, margin: '0 0 0.75rem', color: 'var(--text, #374151)' }}>
                  {t.definition}
                </p>

                {t.example && (
                  <div
                    style={{
                      background: 'var(--code-bg, #f3f4f6)',
                      padding: '0.5rem 0.75rem',
                      borderRadius: '6px',
                      fontFamily: 'monospace',
                      fontSize: '0.78rem',
                      overflowX: 'auto',
                      marginBottom: '0.5rem',
                      color: 'var(--code-text, #1f2937)',
                    }}
                  >
                    {t.example}
                  </div>
                )}
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '0.5rem' }}>
                <button
                  type="button"
                  onClick={() => handleCopy(t)}
                  style={{
                    fontSize: '0.75rem',
                    padding: '0.2rem 0.5rem',
                    border: '1px solid var(--border, #d1d5db)',
                    borderRadius: '4px',
                    background: 'transparent',
                    cursor: 'pointer',
                    color: isCopied ? '#16a34a' : 'var(--muted, #666)',
                  }}
                >
                  {isCopied ? '✓ Copied' : 'Copy'}
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {filteredTerms.length === 0 && (
        <div className="card" style={{ textAlign: 'center', padding: '3rem 1.5rem', marginTop: '1rem' }}>
          <h3>No terms match your search</h3>
          <p className="muted" style={{ margin: '0.5rem 0 1rem' }}>
            Try clearing the search query or selecting "All Modules" and "ALL" letters.
          </p>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => {
              setSearch('');
              setSelectedModule('all');
              setSelectedLetter(null);
            }}
          >
            Reset Filters
          </button>
        </div>
      )}
    </div>
  );
}
