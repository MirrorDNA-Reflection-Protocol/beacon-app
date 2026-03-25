import { useState } from 'react';
import { ARTICLES } from '../data';

const BEACON_BASE = 'https://beacon.activemirror.ai/reflections';

export default function Articles() {
  const [expanded, setExpanded] = useState(false);
  const visible = expanded ? ARTICLES : ARTICLES.slice(0, 6);

  return (
    <section id="articles" className="px-4 py-16 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xs uppercase tracking-widest text-[var(--color-text-muted)]">
          Beacon Reflections
        </h2>
        <span className="text-xs text-[var(--color-text-muted)]">
          {ARTICLES.length} published
        </span>
      </div>
      <div className="space-y-3">
        {visible.map((article) => (
          <a
            key={article.slug}
            href={`${BEACON_BASE}/${article.slug}/`}
            target="_blank"
            rel="noopener noreferrer"
            className="block bg-[var(--color-bg-panel)] border border-[var(--color-border)] rounded-sm p-4 hover:border-[var(--color-amber)] transition-colors group"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <h3 className="text-sm text-[var(--color-text)] group-hover:text-[var(--color-amber)] transition-colors">
                  {article.title}
                </h3>
                <p className="text-xs text-[var(--color-text-dim)] mt-1 line-clamp-2">
                  {article.description}
                </p>
                <div className="flex gap-2 mt-2 flex-wrap">
                  {article.tags.slice(0, 3).map((tag) => (
                    <span
                      key={tag}
                      className="text-[10px] text-[var(--color-text-muted)] border border-[var(--color-border)] px-1.5 py-0.5"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
              <span className="text-xs text-[var(--color-text-muted)] whitespace-nowrap shrink-0">
                {article.date}
              </span>
            </div>
          </a>
        ))}
      </div>
      {ARTICLES.length > 6 && (
        <button
          onClick={() => setExpanded(!expanded)}
          className="mt-4 text-xs text-[var(--color-text-muted)] hover:text-[var(--color-amber)] transition-colors border border-[var(--color-border)] px-3 py-1.5 bg-transparent cursor-pointer"
        >
          {expanded ? 'show less' : `show all ${ARTICLES.length}`}
        </button>
      )}
    </section>
  );
}
