import React, { useState, useEffect, useMemo } from 'react';
import { useProgress, useMounted } from '../../lib/progress-react';
import { reviewFlashcard, dueFlashcards } from '../../lib/progress';

export type Flashcard = {
  id: string;
  topic: string;
  front: string;
  back: string;
};

type Props = {
  cards: Flashcard[];
};

const TOPICS = [
  { id: 'all', label: 'All Topics' },
  { id: 'sql', label: 'SQL' },
  { id: 'python', label: 'Python & Pandas' },
  { id: 'excel', label: 'Excel' },
  { id: 'power-bi', label: 'Power BI & DAX' },
  { id: 'statistics', label: 'Statistics & A/B' },
  { id: 'business', label: 'Business & Metrics' },
  { id: 'aptitude', label: 'Aptitude & Logic' },
];

export default function FlashcardPlayer({ cards }: Props) {
  const store = useProgress();
  const mounted = useMounted();
  const [selectedTopic, setSelectedTopic] = useState('all');
  const [filterMode, setFilterMode] = useState<'due' | 'all'>('due');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [sessionReviewed, setSessionReviewed] = useState(0);

  // Filter cards by topic
  const topicCards = useMemo(() => {
    if (selectedTopic === 'all') return cards;
    return cards.filter((c) => c.topic === selectedTopic);
  }, [cards, selectedTopic]);

  // Due card IDs from store
  const activeDeck = useMemo(() => {
    if (!mounted || filterMode === 'all') return topicCards;
    const dueIds = new Set(dueFlashcards(topicCards.map((c) => c.id), store));
    const filtered = topicCards.filter((c) => dueIds.has(c.id));
    return filtered.length > 0 ? filtered : topicCards;
  }, [topicCards, filterMode, store, mounted]);

  // Clamp current index when deck changes
  useEffect(() => {
    setCurrentIndex(0);
    setIsFlipped(false);
  }, [selectedTopic, filterMode]);

  const currentCard = activeDeck[currentIndex] || activeDeck[0];

  // Box statistics
  const boxStats = useMemo(() => {
    if (!mounted) return { b1: 0, b2: 0, b3: 0, b4: 0, b5: 0, total: cards.length };
    const counts = { b1: 0, b2: 0, b3: 0, b4: 0, b5: 0, total: cards.length };
    for (const c of cards) {
      const rec = store.flashcards[c.id];
      if (!rec || rec.box === 1) counts.b1++;
      else if (rec.box === 2) counts.b2++;
      else if (rec.box === 3) counts.b3++;
      else if (rec.box === 4) counts.b4++;
      else if (rec.box >= 5) counts.b5++;
    }
    return counts;
  }, [cards, store, mounted]);

  const handleReview = (correct: boolean) => {
    if (!currentCard) return;
    reviewFlashcard(currentCard.id, correct);
    setSessionReviewed((prev) => prev + 1);
    setIsFlipped(false);
    if (currentIndex < activeDeck.length - 1) {
      setCurrentIndex((prev) => prev + 1);
    } else {
      setCurrentIndex(0);
    }
  };

  const handleShuffle = () => {
    setIsFlipped(false);
    setCurrentIndex(Math.floor(Math.random() * activeDeck.length));
  };

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
      if (e.code === 'Space') {
        e.preventDefault();
        setIsFlipped((f) => !f);
      } else if (e.code === 'ArrowLeft' || e.key === '1') {
        e.preventDefault();
        handleReview(false);
      } else if (e.code === 'ArrowRight' || e.key === '2') {
        e.preventDefault();
        handleReview(true);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentCard, currentIndex, activeDeck.length]);

  const currentBox = mounted && currentCard ? store.flashcards[currentCard.id]?.box || 1 : 1;

  return (
    <div style={{ maxWidth: '48rem', margin: '0 auto', paddingBottom: '3rem' }}>
      {/* Header Controls */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.25rem' }}>
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          <button
            type="button"
            className={`btn ${filterMode === 'due' ? 'btn-primary' : 'btn-secondary'}`}
            style={{ fontSize: '0.85rem', padding: '0.4rem 0.85rem' }}
            onClick={() => setFilterMode('due')}
          >
            Due Today ({activeDeck.length})
          </button>
          <button
            type="button"
            className={`btn ${filterMode === 'all' ? 'btn-primary' : 'btn-secondary'}`}
            style={{ fontSize: '0.85rem', padding: '0.4rem 0.85rem' }}
            onClick={() => setFilterMode('all')}
          >
            All Cards ({topicCards.length})
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            style={{ fontSize: '0.85rem', padding: '0.4rem 0.85rem' }}
            onClick={handleShuffle}
            title="Jump to a random card in this deck"
          >
            Shuffle
          </button>
        </div>

        <div style={{ fontSize: '0.85rem', color: 'var(--muted, #666)' }}>
          Reviewed this session: <strong>{sessionReviewed}</strong>
        </div>
      </div>

      {/* Topic Filter Pills */}
      <div style={{ display: 'flex', gap: '0.4rem', overflowX: 'auto', paddingBottom: '0.5rem', marginBottom: '1.25rem' }}>
        {TOPICS.map((t) => (
          <button
            key={t.id}
            type="button"
            onClick={() => setSelectedTopic(t.id)}
            style={{
              padding: '0.3rem 0.75rem',
              borderRadius: '999px',
              fontSize: '0.82rem',
              whiteSpace: 'nowrap',
              border: selectedTopic === t.id ? '1px solid var(--accent, #2563eb)' : '1px solid var(--border, #e5e7eb)',
              background: selectedTopic === t.id ? 'var(--accent, #2563eb)' : 'transparent',
              color: selectedTopic === t.id ? '#fff' : 'inherit',
              cursor: 'pointer',
              fontWeight: selectedTopic === t.id ? 600 : 400,
            }}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Leitner Box Status Indicator */}
      <div
        className="card"
        style={{
          padding: '0.75rem 1rem',
          marginBottom: '1.5rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '0.5rem',
          fontSize: '0.82rem',
          background: 'var(--surface-2)',
        }}
      >
        <span style={{ fontWeight: 600 }}>Leitner Spaced Repetition:</span>
        <div style={{ display: 'flex', gap: '0.6rem', flexWrap: 'wrap' }}>
          <span title="Box 1: Review every 1 day">Box 1 (Daily): <strong>{boxStats.b1}</strong></span>
          <span title="Box 2: Review every 2 days">Box 2 (2d): <strong>{boxStats.b2}</strong></span>
          <span title="Box 3: Review every 4 days">Box 3 (4d): <strong>{boxStats.b3}</strong></span>
          <span title="Box 4: Review every 8 days">Box 4 (8d): <strong>{boxStats.b4}</strong></span>
          <span title="Box 5: Review every 16 days">Box 5 (Mastered): <strong>{boxStats.b5}</strong></span>
        </div>
      </div>

      {/* Card Arena */}
      {currentCard ? (
        <div>
          {/* Card Meta & Progress */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem', fontSize: '0.85rem' }}>
            <span style={{ textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 600, color: 'var(--accent, #2563eb)' }}>
              {currentCard.topic} • Box {currentBox}
            </span>
            <span style={{ color: 'var(--muted, #666)' }}>
              Card {currentIndex + 1} of {activeDeck.length}
            </span>
          </div>

          {/* Progress Bar */}
          <div style={{ height: '4px', background: 'var(--border, #e5e7eb)', borderRadius: '2px', marginBottom: '1.25rem', overflow: 'hidden' }}>
            <div
              style={{
                height: '100%',
                background: 'var(--accent, #2563eb)',
                width: `${((currentIndex + 1) / activeDeck.length) * 100}%`,
                transition: 'width 0.2s ease',
              }}
            />
          </div>

          {/* Flashcard Component */}
          <div
            onClick={() => setIsFlipped((f) => !f)}
            style={{
              minHeight: '260px',
              padding: '2.5rem 2rem',
              borderRadius: '12px',
              border: isFlipped ? '2px solid #10b981' : '2px solid var(--border, #e5e7eb)',
              background: isFlipped ? 'var(--surface-2)' : 'var(--surface)',
              boxShadow: '0 4px 14px rgba(0,0,0,0.06)',
              cursor: 'pointer',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'center',
              alignItems: 'center',
              textAlign: 'center',
              transition: 'all 0.2s ease',
              position: 'relative',
              userSelect: 'none',
            }}
          >
            <div style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.1em', color: isFlipped ? '#10b981' : 'var(--muted, #888)', marginBottom: '1rem' }}>
              {isFlipped ? 'Answer / Explanation (Click or Space to flip back)' : 'Question (Click or Space to flip)'}
            </div>

            <div style={{ fontSize: isFlipped ? '1.15rem' : '1.35rem', fontWeight: isFlipped ? 400 : 600, lineHeight: 1.5, color: 'inherit' }}>
              {isFlipped ? currentCard.back : currentCard.front}
            </div>

            <div style={{ marginTop: '1.5rem', fontSize: '0.78rem', color: 'var(--muted, #888)' }}>
              Press <strong>Space</strong> to flip • <strong>1 / Left Arrow</strong> Need Practice • <strong>2 / Right Arrow</strong> Mastered
            </div>
          </div>

          {/* Rating Action Buttons */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginTop: '1.5rem' }}>
            <button
              type="button"
              onClick={() => handleReview(false)}
              style={{
                padding: '0.9rem 1.25rem',
                borderRadius: '8px',
                border: '1px solid #ef4444',
                background: 'rgba(239, 68, 68, 0.1)',
                color: '#ef4444',
                fontSize: '1rem',
                fontWeight: 600,
                cursor: 'pointer',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: '0.2rem',
              }}
            >
              <span>Need Practice</span>
              <span style={{ fontSize: '0.75rem', fontWeight: 400, opacity: 0.85 }}>Resets to Box 1 (Key 1 or Left)</span>
            </button>

            <button
              type="button"
              onClick={() => handleReview(true)}
              style={{
                padding: '0.9rem 1.25rem',
                borderRadius: '8px',
                border: '1px solid #10b981',
                background: 'rgba(16, 185, 129, 0.1)',
                color: '#10b981',
                fontSize: '1rem',
                fontWeight: 600,
                cursor: 'pointer',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: '0.2rem',
              }}
            >
              <span>Mastered / Knew It</span>
              <span style={{ fontSize: '0.75rem', fontWeight: 400, opacity: 0.85 }}>Advances Box (Key 2 or Right)</span>
            </button>
          </div>
        </div>
      ) : (
        <div className="card" style={{ textAlign: 'center', padding: '3rem 1.5rem' }}>
          <h3>All caught up! 🎉</h3>
          <p className="muted" style={{ maxWidth: '28rem', margin: '0.5rem auto 1.5rem' }}>
            You have reviewed all due flashcards in this topic. You can switch to "All Cards" mode to drill the entire deck anytime.
          </p>
          <button type="button" className="btn btn-primary" onClick={() => setFilterMode('all')}>
            Browse All Cards
          </button>
        </div>
      )}
    </div>
  );
}
