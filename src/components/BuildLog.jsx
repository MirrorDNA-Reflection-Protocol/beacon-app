import { useState } from 'react';
import { SHIPPED_ITEMS } from '../data';

export default function BuildLog() {
  const [showAll, setShowAll] = useState(false);
  const items = showAll ? SHIPPED_ITEMS : SHIPPED_ITEMS.slice(0, 8);

  // Group by date
  const grouped = items.reduce((acc, item) => {
    if (!acc[item.date]) acc[item.date] = [];
    acc[item.date].push(item);
    return acc;
  }, {});

  return (
    <section id="buildlog" className="px-4 py-16 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xs uppercase tracking-widest text-[var(--color-text-muted)]">
          Build Log
        </h2>
        <span className="text-xs text-[var(--color-text-muted)]">
          {SHIPPED_ITEMS.length} shipped
        </span>
      </div>
      <div className="relative">
        {/* Timeline line */}
        <div className="absolute left-[5px] top-0 bottom-0 w-px bg-[var(--color-border)]" />

        {Object.entries(grouped).map(([date, dateItems]) => (
          <div key={date} className="mb-6">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-[11px] h-[11px] rounded-full bg-[var(--color-amber)] border-2 border-[var(--color-bg)] relative z-10" />
              <span className="text-xs text-[var(--color-amber)] font-bold">{date}</span>
            </div>
            <div className="ml-6 space-y-1">
              {dateItems.map((item, i) => (
                <div key={i} className="flex items-center justify-between py-1 px-3 bg-[var(--color-bg-panel)] border border-[var(--color-border)] rounded-sm">
                  <span className="text-xs text-[var(--color-text)]">{item.name}</span>
                  <span className="text-[10px] text-[var(--color-text-muted)] ml-2 shrink-0">{item.detail}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
      {SHIPPED_ITEMS.length > 8 && (
        <button
          onClick={() => setShowAll(!showAll)}
          className="mt-2 ml-6 text-xs text-[var(--color-text-muted)] hover:text-[var(--color-amber)] transition-colors border border-[var(--color-border)] px-3 py-1.5 bg-transparent cursor-pointer"
        >
          {showAll ? 'show recent' : `show all ${SHIPPED_ITEMS.length}`}
        </button>
      )}
    </section>
  );
}
