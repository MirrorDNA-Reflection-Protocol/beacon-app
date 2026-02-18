import { DEV_LINKS, SYSTEM_STATS } from '../data';

export default function DevSection() {
  return (
    <section id="dev" className="px-4 py-16 max-w-4xl mx-auto">
      <h2 className="text-xs uppercase tracking-widest text-[var(--color-text-muted)] mb-6">
        For Developers
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="bg-[var(--color-bg-panel)] border border-[var(--color-border)] rounded-sm p-6">
          <h3 className="text-xs text-[var(--color-amber)] mb-4">Resources</h3>
          <div className="space-y-2">
            {DEV_LINKS.map((link) => (
              <a
                key={link.label}
                href={link.href}
                className="flex items-center justify-between text-xs text-[var(--color-text-dim)] hover:text-[var(--color-amber)] transition-colors py-1"
              >
                <span>{link.label}</span>
                {link.arrow && <span className="text-[var(--color-text-muted)]">&rarr;</span>}
              </a>
            ))}
          </div>
        </div>
        <div className="bg-[var(--color-bg-panel)] border border-[var(--color-border)] rounded-sm p-6">
          <h3 className="text-xs text-[var(--color-amber)] mb-4">System</h3>
          <div className="space-y-2 text-xs">
            <div className="flex justify-between text-[var(--color-text-dim)]">
              <span>Repositories</span>
              <span className="text-[var(--color-text)]">{SYSTEM_STATS.repos}</span>
            </div>
            <div className="flex justify-between text-[var(--color-text-dim)]">
              <span>Active Models</span>
              <span className="text-[var(--color-text)]">{SYSTEM_STATS.models}</span>
            </div>
            <div className="flex justify-between text-[var(--color-text-dim)]">
              <span>Shipped Modules</span>
              <span className="text-[var(--color-text)]">{SYSTEM_STATS.shipped_modules}+</span>
            </div>
            <div className="flex justify-between text-[var(--color-text-dim)]">
              <span>Control Plane</span>
              <span className="text-[var(--color-text)]">{SYSTEM_STATS.control_plane_lines.toLocaleString()} lines</span>
            </div>
            <div className="flex justify-between text-[var(--color-text-dim)]">
              <span>Services</span>
              <span className="text-[var(--color-text)]">{SYSTEM_STATS.services}</span>
            </div>
            <div className="flex justify-between text-[var(--color-text-dim)]">
              <span>Guard Rules</span>
              <span className="text-[var(--color-text)]">{SYSTEM_STATS.guard_rules}</span>
            </div>
            <div className="flex justify-between text-[var(--color-text-dim)]">
              <span>Scam Categories</span>
              <span className="text-[var(--color-text)]">{SYSTEM_STATS.scam_categories}</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
