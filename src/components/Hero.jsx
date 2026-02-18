export default function Hero() {
  return (
    <section id="hero" className="min-h-[60vh] flex flex-col items-center justify-center px-4">
      <div className="text-center">
        <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold tracking-tight text-[var(--color-text)]">
          Active Mirror<span className="text-[var(--color-text-muted)] text-lg align-super ml-1">TM</span> Beacon
        </h1>
        <p className="mt-4 text-[var(--color-text-dim)] text-sm sm:text-base max-w-xl mx-auto">
          Daily reflections, live scam scanning, and a build log from a sovereign AI stack — 107 repos, 14 models, zero cloud dependencies.
        </p>
        <div className="mt-8 flex gap-3 justify-center text-xs text-[var(--color-text-muted)] flex-wrap">
          <a href="#articles" className="border border-[var(--color-border)] px-3 py-1.5 hover:border-[var(--color-amber)] hover:text-[var(--color-amber)] transition-colors">
            reflections
          </a>
          <a href="#terminal" className="border border-[var(--color-border)] px-3 py-1.5 hover:border-[var(--color-amber)] hover:text-[var(--color-amber)] transition-colors">
            terminal
          </a>
          <a href="#scanner" className="border border-[var(--color-border)] px-3 py-1.5 hover:border-[var(--color-amber)] hover:text-[var(--color-amber)] transition-colors">
            scan
          </a>
          <a href="#pulse" className="border border-[var(--color-border)] px-3 py-1.5 hover:border-[var(--color-amber)] hover:text-[var(--color-amber)] transition-colors">
            pulse
          </a>
          <a href="#buildlog" className="border border-[var(--color-border)] px-3 py-1.5 hover:border-[var(--color-amber)] hover:text-[var(--color-amber)] transition-colors">
            build log
          </a>
        </div>
      </div>
    </section>
  );
}
