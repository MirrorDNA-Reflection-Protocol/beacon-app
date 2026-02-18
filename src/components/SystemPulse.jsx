import { useState, useEffect, useCallback } from 'react';

const CHETANA_URL = 'https://chetana.activemirror.ai';

const SERVICES = [
  { key: 'chetana', label: 'Chetana', url: `${CHETANA_URL}/api/health`, public: true },
  { key: 'beacon', label: 'Beacon', url: null, public: true },
  { key: 'brain', label: 'MirrorBrain', url: 'https://brain.activemirror.ai/status', public: true },
  { key: 'site', label: 'activemirror.ai', url: 'https://activemirror.ai', public: true },
  { key: 'dashboard', label: 'Dashboard', url: null, public: false },
  { key: 'factory', label: 'Factory', url: null, public: false },
  { key: 'ollama', label: 'Ollama (14 models)', url: null, public: false },
  { key: 'bus', label: 'Memory Bus', url: null, public: false },
];

function StatusDot({ status }) {
  const colors = {
    online: 'bg-[var(--color-green)]',
    offline: 'bg-[var(--color-red)]',
    private: 'bg-[var(--color-text-muted)]',
    checking: 'bg-[var(--color-amber)]',
  };
  return (
    <span className={`inline-block w-2 h-2 rounded-full ${colors[status] || colors.private}`} />
  );
}

export default function SystemPulse() {
  const [statuses, setStatuses] = useState(() =>
    Object.fromEntries(SERVICES.map(s => [s.key, s.public && s.url ? 'checking' : 'private']))
  );
  const [lastCheck, setLastCheck] = useState(null);

  const checkServices = useCallback(async () => {
    const results = { ...statuses };

    for (const svc of SERVICES) {
      if (!svc.url || !svc.public) {
        results[svc.key] = svc.public ? 'online' : 'private';
        continue;
      }
      try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 5000);
        const res = await fetch(svc.url, { signal: controller.signal, mode: 'cors' });
        clearTimeout(timeout);
        results[svc.key] = res.ok ? 'online' : 'offline';
      } catch {
        results[svc.key] = 'offline';
      }
    }

    // Beacon is this app — always online
    results.beacon = 'online';

    setStatuses(results);
    setLastCheck(new Date());
  }, []);

  useEffect(() => {
    checkServices();
    const interval = setInterval(checkServices, 60000);
    return () => clearInterval(interval);
  }, [checkServices]);

  const onlineCount = Object.values(statuses).filter(s => s === 'online').length;
  const privateCount = Object.values(statuses).filter(s => s === 'private').length;

  return (
    <section id="pulse" className="px-4 py-16 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xs uppercase tracking-widest text-[var(--color-text-muted)]">
          System Pulse
        </h2>
        <span className="text-xs text-[var(--color-text-muted)]">
          {onlineCount} online / {privateCount} private
        </span>
      </div>
      <div className="bg-[var(--color-bg-panel)] border border-[var(--color-border)] rounded-sm p-6">
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {SERVICES.map((svc) => (
            <div key={svc.key} className="flex items-center gap-2">
              <StatusDot status={statuses[svc.key]} />
              <span className="text-xs text-[var(--color-text-dim)]">{svc.label}</span>
            </div>
          ))}
        </div>
        {lastCheck && (
          <p className="text-[10px] text-[var(--color-text-muted)] mt-4">
            Last checked: {lastCheck.toLocaleTimeString()}
          </p>
        )}
      </div>
    </section>
  );
}
