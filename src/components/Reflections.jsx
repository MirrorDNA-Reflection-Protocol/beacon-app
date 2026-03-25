import { useState, useEffect } from 'react';
import { REFLECTIONS } from '../data';

export default function Reflections() {
  const [index, setIndex] = useState(0);
  const [fade, setFade] = useState(true);

  useEffect(() => {
    const interval = setInterval(() => {
      setFade(false);
      setTimeout(() => {
        setIndex((prev) => (prev + 1) % REFLECTIONS.length);
        setFade(true);
      }, 400);
    }, 8000);
    return () => clearInterval(interval);
  }, []);

  const next = () => {
    setFade(false);
    setTimeout(() => {
      setIndex((prev) => (prev + 1) % REFLECTIONS.length);
      setFade(true);
    }, 200);
  };

  return (
    <section id="reflections" className="px-4 py-16 max-w-4xl mx-auto">
      <h2 className="text-xs uppercase tracking-widest text-[var(--color-text-muted)] mb-6">
        Reflections
      </h2>
      <div className="bg-[var(--color-bg-panel)] border border-[var(--color-border)] rounded-sm p-8 min-h-[120px] flex flex-col justify-center">
        <blockquote
          className={`text-sm sm:text-base text-[var(--color-text)] italic leading-relaxed transition-opacity duration-400 ${fade ? 'opacity-100' : 'opacity-0'}`}
        >
          "{REFLECTIONS[index]}"
        </blockquote>
        <div className="flex items-center justify-between mt-6">
          <span className="text-[10px] text-[var(--color-text-muted)]">
            {index + 1} / {REFLECTIONS.length}
          </span>
          <button
            onClick={next}
            className="text-xs text-[var(--color-text-muted)] hover:text-[var(--color-amber)] transition-colors border border-[var(--color-border)] px-2 py-1 bg-transparent cursor-pointer"
          >
            next
          </button>
        </div>
      </div>
    </section>
  );
}
