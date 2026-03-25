import { useState } from 'react';
import { EXAMPLE_SCANS } from '../data';

const CHETANA_URL = 'https://chetana.activemirror.ai';

function RiskBadge({ level }) {
  const colors = {
    HIGH: 'text-[var(--color-red)] border-[var(--color-red-dim)]',
    MEDIUM: 'text-[var(--color-amber)] border-[var(--color-amber-dim)]',
    LOW: 'text-[var(--color-green)] border-[var(--color-green-dim)]',
  };
  return (
    <span className={`text-xs border px-2 py-0.5 font-bold ${colors[level] || 'text-[var(--color-text-muted)] border-[var(--color-border)]'}`}>
      {level || 'UNKNOWN'}
    </span>
  );
}

export default function ScamScanner() {
  const [input, setInput] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const scan = async (message) => {
    const text = message || input;
    if (!text.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 10000);
      const res = await fetch(`${CHETANA_URL}/api/scan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
        signal: controller.signal,
      });
      clearTimeout(timeout);
      const data = await res.json();
      setResult(data);
    } catch {
      setError('Could not reach Chetana. Service may be running privately.');
    } finally {
      setLoading(false);
    }
  };

  const handleExample = (msg) => {
    setInput(msg);
    scan(msg);
  };

  return (
    <section id="scanner" className="px-4 py-16 max-w-4xl mx-auto">
      <h2 className="text-xs uppercase tracking-widest text-[var(--color-text-muted)] mb-6">
        Scam Scanner
      </h2>
      <div className="bg-[var(--color-bg-panel)] border border-[var(--color-border)] rounded-sm p-6">
        <p className="text-xs text-[var(--color-text-muted)] mb-4">
          Paste any suspicious message, SMS, or WhatsApp text. Chetana will analyze it for scam patterns.
        </p>

        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && scan()}
            placeholder="Paste a suspicious message..."
            className="flex-1 bg-[var(--color-bg-terminal)] border border-[var(--color-border)] rounded-sm px-3 py-2 text-sm text-[var(--color-text)] placeholder:text-[var(--color-text-muted)] outline-none focus:border-[var(--color-amber)] transition-colors font-[var(--font-mono)]"
          />
          <button
            onClick={() => scan()}
            disabled={loading || !input.trim()}
            className="text-xs border border-[var(--color-border)] px-4 py-2 bg-transparent text-[var(--color-text-muted)] hover:text-[var(--color-amber)] hover:border-[var(--color-amber)] transition-colors cursor-pointer disabled:opacity-30 disabled:cursor-not-allowed"
          >
            {loading ? 'scanning...' : 'scan'}
          </button>
        </div>

        <div className="flex gap-2 mt-3 flex-wrap">
          <span className="text-[10px] text-[var(--color-text-muted)]">try:</span>
          {EXAMPLE_SCANS.map((msg, i) => (
            <button
              key={i}
              onClick={() => handleExample(msg)}
              className="text-[10px] text-[var(--color-text-muted)] border border-[var(--color-border)] px-2 py-0.5 bg-transparent hover:border-[var(--color-amber)] hover:text-[var(--color-amber)] transition-colors cursor-pointer truncate max-w-[200px]"
            >
              {msg.slice(0, 40)}...
            </button>
          ))}
        </div>

        {error && (
          <div className="mt-4 p-3 border border-[var(--color-red-dim)] rounded-sm">
            <p className="text-xs text-[var(--color-red)]">{error}</p>
          </div>
        )}

        {result && (
          <div className="mt-4 p-4 border border-[var(--color-border)] rounded-sm bg-[var(--color-bg)]">
            <div className="flex items-center gap-3 mb-3">
              <RiskBadge level={result.risk_level || result.risk} />
              {result.risk_score !== undefined && (
                <span className="text-xs text-[var(--color-text-dim)]">
                  Score: {result.risk_score}
                </span>
              )}
            </div>
            {(result.signals || result.risk_signals || []).length > 0 && (
              <div className="mb-3">
                <p className="text-[10px] text-[var(--color-text-muted)] mb-1">Signals:</p>
                {(result.signals || result.risk_signals || []).map((s, i) => (
                  <p key={i} className="text-xs text-[var(--color-text-dim)] pl-2">- {s}</p>
                ))}
              </div>
            )}
            {result.recommendation && (
              <p className="text-xs text-[var(--color-amber)]">
                {result.recommendation}
              </p>
            )}
          </div>
        )}
      </div>
    </section>
  );
}
