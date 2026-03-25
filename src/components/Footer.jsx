export default function Footer() {
  return (
    <footer className="px-4 py-12 max-w-4xl mx-auto border-t border-[var(--color-border)]">
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="text-xs text-[var(--color-text-muted)]">
          <span className="text-[var(--color-text-dim)]">Active Mirror</span>
          <span className="mx-2">/</span>
          <span>Sovereign AI Infrastructure</span>
        </div>
        <div className="flex gap-4 text-xs text-[var(--color-text-muted)]">
          <a href="https://activemirror.ai" target="_blank" rel="noopener noreferrer" className="hover:text-[var(--color-amber)] transition-colors">
            activemirror.ai
          </a>
          <a href="https://chetana.activemirror.ai" target="_blank" rel="noopener noreferrer" className="hover:text-[var(--color-amber)] transition-colors">
            chetana
          </a>
          <a href="https://github.com/MirrorDNA-Reflection-Protocol" target="_blank" rel="noopener noreferrer" className="hover:text-[var(--color-amber)] transition-colors">
            github
          </a>
        </div>
      </div>
      <p className="text-center text-[10px] text-[var(--color-text-muted)] mt-6">
        Built by Paul Desai in Goa, India. All data stays on-device.
      </p>
    </footer>
  );
}
