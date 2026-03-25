import { useState, useEffect, useRef } from 'react';
import { COGNITIVE_WEIGHTS } from '../data';

function WeightBar({ label, value, onChange }) {
  const [animated, setAnimated] = useState(0);
  const barRef = useRef(null);

  useEffect(() => {
    const timer = setTimeout(() => setAnimated(value), 200);
    return () => clearTimeout(timer);
  }, [value]);

  const handleSliderChange = (e) => {
    onChange(parseFloat(e.target.value));
  };

  return (
    <div className="mb-3">
      <div className="flex items-center justify-between mb-1">
        <span className="text-xs text-[var(--color-text-dim)]">{label}</span>
        <span className="text-xs text-[var(--color-amber)] font-bold tabular-nums">{value.toFixed(2)}</span>
      </div>
      <div className="relative">
        <div
          ref={barRef}
          className="h-3 bg-[var(--color-bg)] rounded-sm overflow-hidden border border-[var(--color-border)]"
        >
          <div
            className="h-full transition-all duration-700 ease-out rounded-sm"
            style={{
              width: `${animated * 100}%`,
              backgroundColor: value > 0.7 ? 'var(--color-amber)' : value > 0.4 ? 'var(--color-green)' : 'var(--color-text-muted)',
            }}
          />
        </div>
        <input
          type="range"
          min="0"
          max="1"
          step="0.01"
          value={value}
          onChange={handleSliderChange}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />
      </div>
    </div>
  );
}

export default function CognitiveWeights() {
  const [weights, setWeights] = useState(COGNITIVE_WEIGHTS.map(w => ({ ...w })));

  const handleChange = (index, newValue) => {
    setWeights(prev => {
      const next = [...prev];
      next[index] = { ...next[index], value: newValue };
      return next;
    });
  };

  const handleReset = () => {
    setWeights(COGNITIVE_WEIGHTS.map(w => ({ ...w })));
  };

  return (
    <section id="weights" className="px-4 py-16 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xs uppercase tracking-widest text-[var(--color-text-muted)]">
          Cognitive Weight Map
        </h2>
        <button
          onClick={handleReset}
          className="text-xs text-[var(--color-text-muted)] hover:text-[var(--color-amber)] transition-colors border border-[var(--color-border)] px-2 py-1 bg-transparent cursor-pointer"
        >
          reset
        </button>
      </div>
      <div className="bg-[var(--color-bg-panel)] border border-[var(--color-border)] rounded-sm p-6">
        <p className="text-xs text-[var(--color-text-muted)] mb-6">
          Real-time cognitive weight distribution. Drag sliders to explore state space.
        </p>
        {weights.map((w, i) => (
          <WeightBar
            key={w.key}
            label={w.label}
            value={w.value}
            onChange={(val) => handleChange(i, val)}
          />
        ))}
      </div>
    </section>
  );
}
