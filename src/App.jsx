import { useState, useEffect, useRef, useCallback } from 'react';
import { motion, useInView, AnimatePresence } from 'framer-motion';
import { SHOWCASE, ARTICLES, STATS } from './data';

const BEACON = 'https://beacon.activemirror.ai/reflections';
const CHETANA = 'https://chetana.activemirror.ai';
const CHAT_API = import.meta.env.DEV ? 'http://localhost:8095' : 'https://beacon.activemirror.ai';

/* ── fade-in on scroll ── */
function Reveal({ children, delay = 0, style = {} }) {
  const ref = useRef(null);
  const vis = useInView(ref, { once: true, margin: '-60px' });
  return (
    <motion.div ref={ref} initial={{ opacity: 0, y: 24 }}
      animate={vis ? { opacity: 1, y: 0 } : {}} transition={{ duration: 0.6, delay, ease: 'easeOut' }}
      style={style}>
      {children}
    </motion.div>
  );
}

/* ── AnimaBloom background particles ── */
function Bloom() {
  const ref = useRef(null);
  const mouse = useRef({ x: -999, y: -999 });
  useEffect(() => {
    const c = ref.current; if (!c) return;
    const ctx = c.getContext('2d');
    let raf;
    const pts = [];
    const resize = () => { c.width = innerWidth; c.height = innerHeight; };
    resize(); addEventListener('resize', resize);
    const onMove = (e) => {
      mouse.current = { x: e.clientX, y: e.clientY };
      if (Math.random() > 0.7) pts.push({
        x: e.clientX + (Math.random() - .5) * 40, y: e.clientY + (Math.random() - .5) * 40,
        s: Math.random() * 2 + .5, a: Math.random() * 6.28, sp: Math.random() * .3 + .08,
        l: 1, d: Math.random() * .004 + .002, h: Math.random() > .5 ? 38 : 45
      });
    };
    addEventListener('mousemove', onMove);
    for (let i = 0; i < 20; i++) pts.push({
      x: Math.random() * 1400, y: Math.random() * 900,
      s: Math.random() * 1.5 + .5, a: Math.random() * 6.28, sp: Math.random() * .15 + .03,
      l: Math.random() * .3 + .1, d: Math.random() * .001 + .0005, h: Math.random() > .5 ? 38 : 142
    });
    const draw = () => {
      ctx.clearRect(0, 0, c.width, c.height);
      const mx = mouse.current.x, my = mouse.current.y;
      for (let i = pts.length - 1; i >= 0; i--) {
        const p = pts[i];
        p.x += Math.cos(p.a) * p.sp; p.y += Math.sin(p.a) * p.sp;
        p.a += (Math.random() - .5) * .04; p.l -= p.d;
        if (p.l <= 0) { p.x = Math.random() * c.width; p.y = Math.random() * c.height; p.l = Math.random() * .3 + .1; }
        ctx.beginPath(); ctx.arc(p.x, p.y, p.s, 0, 6.28);
        ctx.fillStyle = `hsla(${p.h},80%,60%,${p.l * .45})`; ctx.fill();
        const dx = mx - p.x, dy = my - p.y, dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 160 && dist > 10) {
          ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(mx, my);
          ctx.strokeStyle = `rgba(245,158,11,${(1 - dist / 160) * p.l * .06})`;
          ctx.lineWidth = .3; ctx.stroke();
        }
      }
      raf = requestAnimationFrame(draw);
    };
    draw();
    return () => { cancelAnimationFrame(raf); removeEventListener('resize', resize); removeEventListener('mousemove', onMove); };
  }, []);
  return <canvas ref={ref} style={{ position: 'fixed', inset: 0, pointerEvents: 'none', zIndex: 0 }} />;
}

/* ── Auto-rotating Carousel ── */
function Carousel({ items, onSelect }) {
  const [active, setActive] = useState(0);
  const [paused, setPaused] = useState(false);
  const count = items.length;
  const timerRef = useRef(null);

  const go = useCallback((dir) => {
    setActive(prev => (prev + dir + count) % count);
  }, [count]);

  // Auto-advance every 4.5 seconds
  useEffect(() => {
    if (paused) return;
    timerRef.current = setInterval(() => go(1), 4500);
    return () => clearInterval(timerRef.current);
  }, [paused, go]);

  const item = items[active];

  return (
    <div style={{ maxWidth: 780, margin: '0 auto', padding: '0 24px' }}
      onMouseEnter={() => setPaused(true)} onMouseLeave={() => setPaused(false)}>

      {/* Main image — crossfade */}
      <div style={{ position: 'relative', borderRadius: 16, overflow: 'hidden', border: '1px solid #161616', background: '#030303', cursor: 'pointer' }}
        onClick={() => onSelect(item)}>
        <AnimatePresence mode="wait">
          <motion.div key={active} initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            transition={{ duration: 0.5 }}>
            <div style={{
              height: item.portrait ? 480 : 420, display: 'flex', alignItems: 'center', justifyContent: 'center',
              background: '#030303', overflow: 'hidden',
            }}>
              <img src={item.image} alt={item.title} style={{
                [item.portrait ? 'height' : 'width']: '100%',
                objectFit: item.portrait ? 'contain' : 'cover',
                transition: 'transform .8s ease',
              }}
                onMouseOver={e => e.target.style.transform = 'scale(1.03)'}
                onMouseOut={e => e.target.style.transform = 'scale(1)'} />
            </div>
          </motion.div>
        </AnimatePresence>

        {/* Overlay info */}
        <div style={{ position: 'absolute', bottom: 0, left: 0, right: 0, padding: '32px 28px 24px', background: 'linear-gradient(transparent, rgba(0,0,0,.85))' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <span style={{ fontSize: 17, fontWeight: 600, color: '#fff' }}>{item.title}</span>
            <div style={{ flex: 1 }} />
            {(item.tags || []).map(t => (
              <span key={t} style={{ fontSize: 9, color: '#999', border: '1px solid rgba(255,255,255,.15)', padding: '2px 10px', borderRadius: 99, letterSpacing: 1, textTransform: 'uppercase' }}>{t}</span>
            ))}
          </div>
          <p style={{ fontSize: 12, color: '#aaa', marginTop: 8, lineHeight: 1.7 }}>{item.description}</p>
        </div>

        {/* Arrows */}
        <button onClick={(e) => { e.stopPropagation(); go(-1); }} aria-label="Previous"
          style={{ position: 'absolute', left: 16, top: '50%', transform: 'translateY(-50%)', width: 40, height: 40, borderRadius: '50%', background: 'rgba(0,0,0,.6)', border: '1px solid rgba(255,255,255,.1)', color: '#ccc', fontSize: 20, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', backdropFilter: 'blur(4px)', transition: 'all .3s' }}
          onMouseOver={e => { e.target.style.background = 'rgba(245,158,11,.3)'; e.target.style.borderColor = '#f59e0b'; }}
          onMouseOut={e => { e.target.style.background = 'rgba(0,0,0,.6)'; e.target.style.borderColor = 'rgba(255,255,255,.1)'; }}>
          &#8249;
        </button>
        <button onClick={(e) => { e.stopPropagation(); go(1); }} aria-label="Next"
          style={{ position: 'absolute', right: 16, top: '50%', transform: 'translateY(-50%)', width: 40, height: 40, borderRadius: '50%', background: 'rgba(0,0,0,.6)', border: '1px solid rgba(255,255,255,.1)', color: '#ccc', fontSize: 20, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', backdropFilter: 'blur(4px)', transition: 'all .3s' }}
          onMouseOver={e => { e.target.style.background = 'rgba(245,158,11,.3)'; e.target.style.borderColor = '#f59e0b'; }}
          onMouseOut={e => { e.target.style.background = 'rgba(0,0,0,.6)'; e.target.style.borderColor = 'rgba(255,255,255,.1)'; }}>
          &#8250;
        </button>

        {/* Slide counter */}
        <div style={{ position: 'absolute', top: 16, right: 20, fontSize: 10, color: '#666', letterSpacing: 2 }}>
          {String(active + 1).padStart(2, '0')} / {String(count).padStart(2, '0')}
        </div>
      </div>

      {/* Thumbnail strip + progress */}
      <div style={{ display: 'flex', gap: 8, marginTop: 16, justifyContent: 'center' }}>
        {items.map((it, i) => (
          <button key={i} onClick={() => setActive(i)} aria-label={it.title}
            style={{
              width: 56, height: 36, borderRadius: 6, overflow: 'hidden', border: active === i ? '2px solid #f59e0b' : '1px solid #1a1a1a',
              cursor: 'pointer', opacity: active === i ? 1 : 0.4, transition: 'all .3s', padding: 0, background: '#030303', flexShrink: 0,
            }}>
            <img src={it.image} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
          </button>
        ))}
      </div>

      {/* Auto-advance bar */}
      {!paused && (
        <div style={{ marginTop: 10, height: 2, background: '#111', borderRadius: 1, overflow: 'hidden' }}>
          <motion.div
            key={active}
            initial={{ width: '0%' }}
            animate={{ width: '100%' }}
            transition={{ duration: 4.5, ease: 'linear' }}
            style={{ height: '100%', background: '#f59e0b', borderRadius: 1 }}
          />
        </div>
      )}
    </div>
  );
}

/* ── Scam Scanner terminal ── */
function ScanTerminal() {
  const [lines, setLines] = useState([]);
  const [inp, setInp] = useState('');
  const [scanning, setScanning] = useState(false);
  const end = useRef(null);
  const inputRef = useRef(null);
  const quotes = [
    "The model is interchangeable. The bus is identity.",
    "107 repos, one Mac Mini, zero cloud deps.",
    "There's nothing between a scammer and a grandmother with a smartphone.",
    "Your AI identity should be a portable file — stored in your files, not theirs.",
  ];

  useEffect(() => { end.current?.scrollIntoView({ behavior: 'smooth' }); }, [lines]);

  // Auto-demo on mount
  useEffect(() => {
    const t1 = setTimeout(() => {
      setLines([
        { t: 's', x: '  Chetana AI Shield · 15 scam categories · on-device' },
        { t: 'o', x: '' },
        { t: 'o', x: '  Paste any suspicious message below to scan it.' },
        { t: 'o', x: '  Or try: help | about | reflect | stats' },
      ]);
    }, 300);
    return () => clearTimeout(t1);
  }, []);

  const add = (x, t = 'o') => setLines(p => [...p, { t, x }]);

  const run = async (cmd) => {
    const c = cmd.trim().toLowerCase(); add(`$ ${cmd}`, 'c'); if (!c) return;
    if (c === 'help') add('  help | about | scan <msg> | reflect | stats | clear');
    else if (c === 'about') add('  Paul Desai · Goa · 10mo sovereign AI · 1 Mac Mini · 0 cloud deps');
    else if (c === 'stats') STATS.forEach(s => add(`  ${s.label.padEnd(16)} ${s.value}`));
    else if (c === 'reflect') add(`  "${quotes[Math.floor(Math.random() * quotes.length)]}"`);
    else if (c === 'clear') { setLines([{ t: 's', x: '> cleared' }]); return; }
    else {
      // Anything that's not a known command → treat as scan input
      const msg = c.startsWith('scan ') ? cmd.slice(5) : cmd;
      add('  scanning...', 's');
      setScanning(true);
      try {
        const r = await fetch(`${CHETANA}/api/scan`, {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: msg }), signal: AbortSignal.timeout(8000),
        });
        const d = await r.json();
        const risk = d.risk_level || d.risk || 'UNKNOWN';
        add(`  RISK: ${risk}`, risk === 'HIGH' ? 'e' : risk === 'MEDIUM' ? 's' : 'o');
        if (d.category) add(`  Category: ${d.category}`);
        (d.signals || d.risk_signals || []).forEach(s => add(`    → ${s}`));
        if (risk === 'LOW') add('  This message appears safe.', 'o');
      } catch {
        add('  [chetana offline — try again later]', 's');
      }
      setScanning(false);
    }
  };

  const col = { s: '#f59e0b', c: '#22c55e', o: '#888', e: '#ef4444' };

  return (
    <div onClick={() => inputRef.current?.focus()}
      style={{ background: '#0a0a0a', border: '1px solid #161616', borderRadius: 16, padding: 20, display: 'flex', flexDirection: 'column', maxWidth: 640, width: '100%', margin: '0 auto', minHeight: 280 }}>
      <div style={{ display: 'flex', gap: 6, marginBottom: 12, alignItems: 'center' }}>
        <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#ff5f57' }} />
        <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#ffbd2e' }} />
        <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#28c840' }} />
        <span style={{ fontSize: 10, color: '#444', marginLeft: 8 }}>chetana://scanner</span>
        <div style={{ flex: 1 }} />
        {scanning && <span style={{ fontSize: 10, color: '#f59e0b', animation: 'pglow 1s ease-in-out infinite' }}>scanning...</span>}
      </div>
      <div style={{ flex: 1, overflowY: 'auto', fontSize: 12, lineHeight: 1.8 }}>
        {lines.map((l, i) => <div key={i} style={{ color: col[l.t] || '#888', whiteSpace: 'pre-wrap' }}>{l.x}</div>)}
        <div ref={end} />
      </div>
      <div style={{ display: 'flex', alignItems: 'center', marginTop: 10, fontSize: 12, borderTop: '1px solid #121212', paddingTop: 10 }}>
        <span style={{ color: '#22c55e', marginRight: 8 }}>$</span>
        <input ref={inputRef} value={inp} onChange={e => setInp(e.target.value)}
          onKeyDown={e => { if (e.key === 'Enter' && !scanning) { run(inp); setInp(''); } }}
          style={{ flex: 1, background: 'transparent', border: 'none', outline: 'none', color: '#e0e0e0', fontSize: 12, fontFamily: 'inherit' }}
          placeholder="paste a suspicious message to scan..." spellCheck="false" />
      </div>
    </div>
  );
}

/* ── Chat Widget ── */
function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [msgs, setMsgs] = useState([]);
  const [inp, setInp] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const end = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => { if (open) { end.current?.scrollIntoView({ behavior: 'smooth' }); inputRef.current?.focus(); } }, [open, msgs]);

  const send = async () => {
    const text = inp.trim();
    if (!text || loading) return;
    if (text.length > 500) { setError('Message too long (max 500 chars)'); return; }

    const newMsgs = [...msgs, { role: 'user', content: text }];
    setMsgs(newMsgs);
    setInp('');
    setError('');
    setLoading(true);

    try {
      const r = await fetch(`${CHAT_API}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: newMsgs }),
        signal: AbortSignal.timeout(15000),
      });
      if (!r.ok) {
        const errData = await r.json().catch(() => ({}));
        throw new Error(errData.detail || `Error ${r.status}`);
      }
      const data = await r.json();
      setMsgs([...newMsgs, { role: 'assistant', content: data.reply }]);
    } catch (e) {
      setError(e.message || 'Failed to connect. Please try again.');
    }
    setLoading(false);
  };

  return (
    <>
      {/* Floating button */}
      <button onClick={() => setOpen(!open)} aria-label="Chat about Active Mirror"
        style={{
          position: 'fixed', bottom: 24, right: 24, zIndex: 40,
          width: 52, height: 52, borderRadius: '50%',
          background: open ? '#333' : '#f59e0b', border: 'none',
          color: open ? '#999' : '#000', fontSize: 22, cursor: 'pointer',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          boxShadow: '0 4px 20px rgba(0,0,0,.5)', transition: 'all .3s',
        }}>
        {open ? '\u00D7' : '\u25C7'}
      </button>

      {/* Chat panel */}
      <AnimatePresence>
        {open && (
          <motion.div initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }} exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ duration: 0.2 }}
            style={{
              position: 'fixed', bottom: 88, right: 24, zIndex: 40,
              width: 380, maxWidth: 'calc(100vw - 48px)', height: 480, maxHeight: 'calc(100vh - 120px)',
              background: '#0a0a0a', border: '1px solid #1a1a1a', borderRadius: 16,
              display: 'flex', flexDirection: 'column', overflow: 'hidden',
              boxShadow: '0 8px 40px rgba(0,0,0,.6)',
            }}>
            {/* Header */}
            <div style={{ padding: '16px 20px', borderBottom: '1px solid #141414', display: 'flex', alignItems: 'center', gap: 10 }}>
              <span style={{ color: '#f59e0b', fontSize: 18 }}>&#9671;</span>
              <div>
                <div style={{ fontSize: 13, fontWeight: 600, color: '#e0e0e0' }}>Active Mirror</div>
                <div style={{ fontSize: 9, color: '#555', letterSpacing: 1 }}>SOVEREIGN AI KNOWLEDGE BASE</div>
              </div>
              <div style={{ flex: 1 }} />
              <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#22c55e', boxShadow: '0 0 6px rgba(34,197,94,.5)' }} />
            </div>

            {/* Messages */}
            <div style={{ flex: 1, overflowY: 'auto', padding: '16px 16px 8px' }}>
              {msgs.length === 0 && (
                <div style={{ textAlign: 'center', padding: '40px 16px' }}>
                  <div style={{ color: '#f59e0b', fontSize: 28, marginBottom: 12 }}>&#9671;</div>
                  <p style={{ fontSize: 13, color: '#888', marginBottom: 8 }}>Ask me about Active Mirror</p>
                  <p style={{ fontSize: 11, color: '#444', lineHeight: 1.6 }}>
                    Sovereign AI infrastructure, Chetana scam detection, the memory bus, or any of Paul's published reflections.
                  </p>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginTop: 16, justifyContent: 'center' }}>
                    {['What is Active Mirror?', 'Tell me about Chetana', 'How does the memory bus work?'].map(q => (
                      <button key={q} onClick={() => { setInp(q); }}
                        style={{ fontSize: 10, color: '#888', border: '1px solid #1a1a1a', background: 'transparent', padding: '6px 12px', borderRadius: 8, cursor: 'pointer', fontFamily: 'inherit', transition: 'all .3s' }}
                        onMouseOver={e => { e.target.style.borderColor = '#f59e0b'; e.target.style.color = '#f59e0b'; }}
                        onMouseOut={e => { e.target.style.borderColor = '#1a1a1a'; e.target.style.color = '#888'; }}>
                        {q}
                      </button>
                    ))}
                  </div>
                </div>
              )}
              {msgs.map((m, i) => (
                <div key={i} style={{
                  marginBottom: 12,
                  display: 'flex', flexDirection: 'column',
                  alignItems: m.role === 'user' ? 'flex-end' : 'flex-start',
                }}>
                  <div style={{
                    maxWidth: '85%', padding: '10px 14px', borderRadius: 12,
                    fontSize: 12, lineHeight: 1.7, wordBreak: 'break-word',
                    background: m.role === 'user' ? '#1a1a1a' : '#0d0d0d',
                    border: m.role === 'user' ? '1px solid #222' : '1px solid #161616',
                    color: m.role === 'user' ? '#e0e0e0' : '#aaa',
                  }}>
                    {m.content}
                  </div>
                </div>
              ))}
              {loading && (
                <div style={{ marginBottom: 12 }}>
                  <div style={{ padding: '10px 14px', borderRadius: 12, background: '#0d0d0d', border: '1px solid #161616', display: 'inline-block' }}>
                    <span style={{ fontSize: 12, color: '#f59e0b', animation: 'pglow 1s ease-in-out infinite' }}>thinking...</span>
                  </div>
                </div>
              )}
              {error && (
                <div style={{ fontSize: 11, color: '#ef4444', textAlign: 'center', padding: 8 }}>{error}</div>
              )}
              <div ref={end} />
            </div>

            {/* Input */}
            <div style={{ padding: '12px 16px', borderTop: '1px solid #141414' }}>
              <div style={{ display: 'flex', gap: 8 }}>
                <input ref={inputRef} value={inp} onChange={e => setInp(e.target.value)}
                  onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } }}
                  placeholder="Ask about Active Mirror..."
                  style={{ flex: 1, background: '#0d0d0d', border: '1px solid #1a1a1a', borderRadius: 8, padding: '10px 12px', fontSize: 12, color: '#e0e0e0', outline: 'none', fontFamily: 'inherit' }} />
                <button onClick={send} disabled={loading || !inp.trim()}
                  style={{ padding: '10px 16px', background: inp.trim() && !loading ? '#f59e0b' : '#222', color: inp.trim() && !loading ? '#000' : '#555', fontSize: 12, fontWeight: 700, borderRadius: 8, border: 'none', cursor: inp.trim() && !loading ? 'pointer' : 'default', fontFamily: 'inherit', transition: 'all .3s' }}>
                  &#8593;
                </button>
              </div>
              <p style={{ fontSize: 9, color: '#333', marginTop: 8, textAlign: 'center' }}>
                Powered by sovereign AI infrastructure
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}

/* ── Sticky Nav ── */
function StickyNav() {
  const [show, setShow] = useState(false);
  useEffect(() => {
    const onScroll = () => setShow(window.scrollY > window.innerHeight * 0.8);
    addEventListener('scroll', onScroll, { passive: true });
    return () => removeEventListener('scroll', onScroll);
  }, []);
  if (!show) return null;
  const links = [
    ['showcase', 'Showcase'],
    ['scanner', 'Scanner'],
    ['writing', 'Writing'],
    ['live', 'Live'],
    ['subscribe', 'Subscribe'],
  ];
  return (
    <motion.nav initial={{ y: -60 }} animate={{ y: 0 }} transition={{ duration: 0.3 }}
      style={{
        position: 'fixed', top: 0, left: 0, right: 0, zIndex: 30,
        background: 'rgba(5,5,5,.85)', backdropFilter: 'blur(12px)',
        borderBottom: '1px solid #111', padding: '0 24px',
        display: 'flex', alignItems: 'center', justifyContent: 'center', height: 48,
      }}>
      <a href="#" style={{ color: '#f59e0b', fontSize: 16, marginRight: 32, textDecoration: 'none' }}>&#9671;</a>
      <div style={{ display: 'flex', gap: 24 }}>
        {links.map(([id, label]) => (
          <a key={id} href={`#${id}`}
            style={{ fontSize: 11, color: '#555', letterSpacing: 1, textTransform: 'uppercase', textDecoration: 'none', transition: 'color .3s' }}
            onMouseOver={e => e.target.style.color = '#f59e0b'}
            onMouseOut={e => e.target.style.color = '#555'}>{label}</a>
        ))}
      </div>
    </motion.nav>
  );
}

/* ═══════════════════ APP ═══════════════════ */
export default function App() {
  const [lightbox, setLightbox] = useState(null);
  const [time, setTime] = useState(new Date());
  const [email, setEmail] = useState('');
  const [subbed, setSubbed] = useState(false);

  useEffect(() => { const t = setInterval(() => setTime(new Date()), 1000); return () => clearInterval(t); }, []);
  useEffect(() => { window.scrollTo(0, 0); }, []);

  const subscribe = async (e) => {
    e.preventDefault(); if (!email.trim()) return;
    try {
      const r = await fetch(`${CHAT_API}/api/subscribe`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }), signal: AbortSignal.timeout(8000),
      });
      if (r.ok) setSubbed(true);
    } catch {
      // Fallback to localStorage if server is down
      const subs = JSON.parse(localStorage.getItem('beacon_subs') || '[]');
      subs.push({ email, ts: Date.now() });
      localStorage.setItem('beacon_subs', JSON.stringify(subs));
      setSubbed(true);
    }
  };

  const col = { maxWidth: 760, margin: '0 auto', padding: '0 24px' };
  const latestArticles = ARTICLES.slice(0, 3);

  // Dynamic duration since project start (April 2025)
  const startDate = new Date('2025-04-01');
  const now = new Date();
  const months = Math.floor((now - startDate) / (1000 * 60 * 60 * 24 * 30.44));
  const durationText = months >= 12 ? `${Math.floor(months / 12)}+ year${Math.floor(months / 12) > 1 ? 's' : ''}` : `${months} months`;

  return (
    <div style={{ minHeight: '100vh', background: '#050505', color: '#e0e0e0', position: 'relative', overflowX: 'hidden' }}>
      <Bloom />

      <StickyNav />

      <div style={{ position: 'relative', zIndex: 1 }}>

        {/* ═══ HERO ═══ */}
        <section id="hero" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: '40px 24px' }}>
          <Reveal>
            <div style={{ color: '#f59e0b', fontSize: 36, marginBottom: 24, animation: 'pglow 3s ease-in-out infinite' }}>&#9671;</div>
          </Reveal>
          <Reveal delay={.08}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, justifyContent: 'center', marginBottom: 20 }}>
              <span style={{ width: 7, height: 7, borderRadius: '50%', background: '#22c55e', boxShadow: '0 0 8px rgba(34,197,94,.6)' }} />
              <span style={{ fontSize: 10, letterSpacing: 3, textTransform: 'uppercase', color: '#22c55e' }}>system online</span>
            </div>
          </Reveal>
          <Reveal delay={.12}>
            <h1 style={{ fontSize: 'clamp(42px, 8vw, 80px)', fontWeight: 700, letterSpacing: -2, color: '#fff', lineHeight: 1 }}>Active Mirror</h1>
          </Reveal>
          <Reveal delay={.16}>
            <p style={{ color: '#444', fontSize: 11, letterSpacing: 6, textTransform: 'uppercase', marginTop: 8 }}>Sovereign AI from Goa</p>
          </Reveal>
          <Reveal delay={.24}>
            <p style={{ marginTop: 36, color: '#666', fontSize: 14, maxWidth: 400, lineHeight: 1.9, margin: '36px auto 0' }}>
              One person. One Mac Mini. {durationText}.<br />An AI operating system that answers to nobody.
            </p>
          </Reveal>
          <Reveal delay={.32}>
            <div style={{ marginTop: 48, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: 36 }}>
              {STATS.map(s => (
                <div key={s.label} style={{ textAlign: 'center' }}>
                  <div className="text-gradient" style={{ fontSize: 28, fontWeight: 700 }}>{s.value}</div>
                  <div style={{ fontSize: 9, color: '#555', marginTop: 4, textTransform: 'uppercase', letterSpacing: 2 }}>{s.label}</div>
                </div>
              ))}
            </div>
          </Reveal>
          <Reveal delay={.4}>
            <div style={{ marginTop: 56 }}>
              <a href="#showcase" style={{ display: 'inline-block', border: '1px solid #222', padding: '10px 32px', fontSize: 11, color: '#666', letterSpacing: 2, textTransform: 'uppercase', transition: 'all .4s' }}
                onMouseOver={e => { e.target.style.borderColor = '#f59e0b'; e.target.style.color = '#f59e0b'; }}
                onMouseOut={e => { e.target.style.borderColor = '#222'; e.target.style.color = '#666'; }}>
                explore ↓
              </a>
            </div>
          </Reveal>
        </section>

        {/* ═══ LATEST WRITING (above fold teaser) ═══ */}
        <section style={{ paddingBottom: 40 }}>
          <div style={col}>
            <Reveal>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 20 }}>
                <p style={{ fontSize: 10, letterSpacing: 5, textTransform: 'uppercase', color: '#f59e0b' }}>Latest</p>
                <div style={{ flex: 1, height: 1, background: '#1a1a1a' }} />
                <a href="#writing" style={{ fontSize: 10, color: '#444', letterSpacing: 1, textTransform: 'uppercase', textDecoration: 'none', transition: 'color .3s' }}
                  onMouseOver={e => e.target.style.color = '#f59e0b'} onMouseOut={e => e.target.style.color = '#444'}>
                  all writing &rarr;
                </a>
              </div>
            </Reveal>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 12 }}>
              {latestArticles.map((a, i) => (
                <Reveal key={a.slug} delay={.05 * i}>
                  <a href={`${BEACON}/${a.slug}/`} target="_blank" rel="noopener noreferrer"
                    style={{ display: 'block', padding: 16, background: '#0a0a0a', border: '1px solid #161616', borderRadius: 12, textDecoration: 'none', transition: 'border-color .3s' }}
                    onMouseOver={e => e.currentTarget.style.borderColor = '#222'}
                    onMouseOut={e => e.currentTarget.style.borderColor = '#161616'}>
                    <span style={{ fontSize: 10, color: '#444', fontVariantNumeric: 'tabular-nums' }}>{a.date}</span>
                    <p style={{ fontSize: 13, color: '#999', marginTop: 6, lineHeight: 1.5, transition: 'color .3s' }}>{a.title}</p>
                  </a>
                </Reveal>
              ))}
            </div>
          </div>
        </section>

        {/* ═══ SHOWCASE ═══ */}
        <section id="showcase" style={{ paddingTop: 100, paddingBottom: 100 }}>
          <div style={col}>
            <Reveal>
              <p style={{ fontSize: 10, letterSpacing: 5, textTransform: 'uppercase', color: '#f59e0b', marginBottom: 8 }}>Showcase</p>
            </Reveal>
            <Reveal delay={.05}>
              <h2 style={{ fontSize: 28, fontWeight: 300, color: '#ccc', marginBottom: 48 }}>What {durationText} of building looks like.</h2>
            </Reveal>
          </div>
          <Reveal delay={.1}>
            <Carousel items={SHOWCASE} onSelect={setLightbox} />
          </Reveal>
        </section>

        {/* ═══ LIVE SCANNER ═══ */}
        <section id="scanner" style={{ paddingTop: 60, paddingBottom: 80 }}>
          <div style={col}>
            <Reveal>
              <p style={{ fontSize: 10, letterSpacing: 5, textTransform: 'uppercase', color: '#f59e0b', marginBottom: 8 }}>Live Demo</p>
            </Reveal>
            <Reveal delay={.05}>
              <h2 style={{ fontSize: 28, fontWeight: 300, color: '#ccc', marginBottom: 8 }}>Chetana — AI scam scanner.</h2>
              <p style={{ fontSize: 12, color: '#555', marginBottom: 32, lineHeight: 1.7 }}>
                Paste any suspicious message. 15 scam categories. On-device analysis. Try it live.
              </p>
            </Reveal>
            <Reveal delay={.1}>
              <ScanTerminal />
            </Reveal>
          </div>
        </section>

        {/* ═══ WRITING ═══ */}
        <section id="writing" style={{ paddingTop: 80, paddingBottom: 80 }}>
          <div style={col}>
            <Reveal>
              <p style={{ fontSize: 10, letterSpacing: 5, textTransform: 'uppercase', color: '#f59e0b', marginBottom: 8 }}>Writing</p>
            </Reveal>
            <Reveal delay={.05}>
              <h2 style={{ fontSize: 28, fontWeight: 300, color: '#ccc', marginBottom: 12 }}>Reflections from the frontier.</h2>
              <p style={{ fontSize: 11, color: '#444', marginBottom: 40 }}>PGP-signed · IPFS-pinned · Published daily</p>
            </Reveal>
            <div style={{ borderLeft: '1px solid #1a1a1a', paddingLeft: 24, marginLeft: 3 }}>
              {ARTICLES.map((a, i) => (
                <Reveal key={a.slug} delay={.02 * i}>
                  <a href={`${BEACON}/${a.slug}/`} target="_blank" rel="noopener noreferrer"
                    style={{ display: 'block', padding: '14px 0', position: 'relative', transition: 'all .3s', textDecoration: 'none' }}
                    onMouseOver={e => {
                      e.currentTarget.querySelector('.tl-dot').style.background = '#f59e0b';
                      e.currentTarget.querySelector('.tl-dot').style.boxShadow = '0 0 6px rgba(245,158,11,.4)';
                      e.currentTarget.querySelector('.tl-title').style.color = '#f59e0b';
                    }}
                    onMouseOut={e => {
                      e.currentTarget.querySelector('.tl-dot').style.background = '#222';
                      e.currentTarget.querySelector('.tl-dot').style.boxShadow = 'none';
                      e.currentTarget.querySelector('.tl-title').style.color = '#999';
                    }}>
                    <div className="tl-dot" style={{ position: 'absolute', left: -28, top: 20, width: 7, height: 7, borderRadius: '50%', background: '#222', transition: 'all .3s' }} />
                    <div style={{ display: 'flex', alignItems: 'baseline', gap: 16 }}>
                      <span style={{ fontSize: 10, color: '#444', flexShrink: 0, width: 68, fontVariantNumeric: 'tabular-nums' }}>{a.date}</span>
                      <div style={{ flex: 1, minWidth: 0 }}>
                        <span className="tl-title" style={{ fontSize: 14, color: '#999', transition: 'color .3s' }}>{a.title}</span>
                        <p style={{ fontSize: 11, color: '#444', marginTop: 3, lineHeight: 1.6 }} className="line-clamp-2">{a.description}</p>
                      </div>
                      <span style={{ color: '#333', fontSize: 14, flexShrink: 0 }}>&rarr;</span>
                    </div>
                  </a>
                </Reveal>
              ))}
            </div>
          </div>
        </section>

        {/* ═══ LIVE STATUS ═══ */}
        <section id="live" style={{ paddingTop: 80, paddingBottom: 80 }}>
          <div style={col}>
            <Reveal>
              <p style={{ fontSize: 10, letterSpacing: 5, textTransform: 'uppercase', color: '#f59e0b', marginBottom: 8 }}>Live</p>
            </Reveal>
            <Reveal delay={.1}>
              <div style={{ border: '1px solid #161616', borderRadius: 16, padding: 28, background: '#0a0a0a' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span style={{ width: 7, height: 7, borderRadius: '50%', background: '#22c55e', boxShadow: '0 0 6px rgba(34,197,94,.5)' }} />
                    <span style={{ fontSize: 11, color: '#22c55e', letterSpacing: 1 }}>SOVEREIGN MESH ACTIVE</span>
                  </div>
                  <span style={{ fontSize: 11, color: '#555', fontVariantNumeric: 'tabular-nums' }}>
                    {time.toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata', hour12: false })} IST
                  </span>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))', gap: 10 }}>
                  {[
                    { n: 'Chetana', on: true, d: 'AI Shield' },
                    { n: 'Beacon', on: true, d: 'This page' },
                    { n: 'Memory Bus', on: false, d: 'LAN only' },
                    { n: 'Factory', on: false, d: 'LAN only' },
                    { n: 'Dashboard', on: false, d: '24 panels' },
                    { n: 'Ollama', on: false, d: '14 models' },
                    { n: 'MirrorBrain', on: false, d: 'Android' },
                    { n: 'GlyphTrail', on: false, d: 'Audit log' },
                  ].map(s => (
                    <div key={s.n} style={{ background: '#0d0d0d', border: '1px solid #121212', borderRadius: 10, padding: 12 }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 4 }}>
                        <span style={{ width: 5, height: 5, borderRadius: '50%', background: s.on ? '#22c55e' : '#333' }} />
                        <span style={{ fontSize: 11, color: '#888' }}>{s.n}</span>
                      </div>
                      <span style={{ fontSize: 10, color: s.on ? '#22c55e' : '#444' }}>{s.d}</span>
                    </div>
                  ))}
                </div>
                <div style={{ marginTop: 20, paddingTop: 14, borderTop: '1px solid #121212', fontSize: 10, color: '#444', display: 'flex', justifyContent: 'space-between' }}>
                  <span>Goa, India · Mac Mini M4 Pro 24GB</span>
                  <span>Zero cloud dependencies</span>
                </div>
              </div>
            </Reveal>
          </div>
        </section>

        {/* ═══ SUBSCRIBE ═══ */}
        <section id="subscribe" style={{ paddingTop: 80, paddingBottom: 100 }}>
          <div style={{ maxWidth: 460, margin: '0 auto', padding: '0 24px', textAlign: 'center' }}>
            <Reveal>
              <div style={{ border: '1px solid #161616', borderRadius: 16, padding: 48, background: '#0a0a0a' }}>
                <div style={{ color: '#f59e0b', fontSize: 28, marginBottom: 20, animation: 'pglow 3s ease-in-out infinite' }}>&#9671;</div>
                <h3 style={{ fontSize: 18, fontWeight: 600, color: '#fff' }}>Dispatches from the frontier</h3>
                <p style={{ fontSize: 12, color: '#555', marginTop: 12, lineHeight: 1.7 }}>New reflections and shipped modules. No spam, no tracking.</p>
                {subbed ? (
                  <p style={{ marginTop: 28, color: '#22c55e', fontSize: 13 }}>You're in. &#9671;</p>
                ) : (
                  <form onSubmit={subscribe} style={{ marginTop: 28, display: 'flex', gap: 8, maxWidth: 320, margin: '28px auto 0' }}>
                    <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="email" required
                      style={{ flex: 1, background: '#0d0d0d', border: '1px solid #1a1a1a', borderRadius: 8, padding: '10px 14px', fontSize: 13, color: '#e0e0e0', outline: 'none', fontFamily: 'inherit' }} />
                    <button type="submit"
                      style={{ padding: '10px 24px', background: '#f59e0b', color: '#000', fontSize: 13, fontWeight: 700, borderRadius: 8, border: 'none', cursor: 'pointer', fontFamily: 'inherit', transition: 'background .3s' }}
                      onMouseOver={e => e.target.style.background = '#fbbf24'}
                      onMouseOut={e => e.target.style.background = '#f59e0b'}>go</button>
                  </form>
                )}
              </div>
            </Reveal>
          </div>
        </section>

        {/* ═══ FOOTER ═══ */}
        <footer style={{ borderTop: '1px solid #111', padding: '40px 24px', textAlign: 'center' }}>
          <div style={{ display: 'flex', justifyContent: 'center', gap: 24, fontSize: 12, color: '#444' }}>
            {[
              ['activemirror.ai', 'https://activemirror.ai'],
              ['chetana', 'https://chetana.activemirror.ai'],
              ['reflections', BEACON],
              ['github', 'https://github.com/MirrorDNA-Reflection-Protocol'],
            ].map(([label, href], i) => (
              <span key={label}>
                {i > 0 && <span style={{ color: '#1a1a1a', marginRight: 24 }}>·</span>}
                <a href={href} target="_blank" rel="noopener noreferrer"
                  style={{ color: '#444', transition: 'color .3s' }}
                  onMouseOver={e => e.target.style.color = '#f59e0b'}
                  onMouseOut={e => e.target.style.color = '#444'}>{label}</a>
              </span>
            ))}
          </div>
          <p style={{ fontSize: 10, color: '#333', marginTop: 20 }}>
            Built by Paul Desai · Goa · All data on-device · PGP-signed · IPFS-pinned
          </p>
        </footer>
      </div>

      {/* ═══ CHAT ═══ */}
      <ChatWidget />

      {/* ═══ LIGHTBOX ═══ */}
      <AnimatePresence>
        {lightbox && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            onClick={() => setLightbox(null)}
            style={{ position: 'fixed', inset: 0, zIndex: 50, background: 'rgba(0,0,0,.95)', backdropFilter: 'blur(12px)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 24, cursor: 'pointer' }}>
            <motion.div initial={{ scale: .93, y: 20 }} animate={{ scale: 1, y: 0 }} exit={{ scale: .93, y: 20 }}
              onClick={e => e.stopPropagation()}
              style={{ maxWidth: 960, width: '100%', position: 'relative' }}>
              <img src={lightbox.image} alt={lightbox.title}
                style={{ maxWidth: '100%', maxHeight: '80vh', margin: '0 auto', display: 'block', objectFit: 'contain', borderRadius: 12 }} />
              <div style={{ textAlign: 'center', marginTop: 20 }}>
                <p style={{ fontSize: 15, color: '#fff', fontWeight: 500 }}>{lightbox.title}</p>
                <p style={{ fontSize: 12, color: '#666', marginTop: 6 }}>{lightbox.description}</p>
              </div>
              <button onClick={() => setLightbox(null)}
                style={{ position: 'absolute', top: -12, right: -12, width: 36, height: 36, borderRadius: '50%', background: '#111', border: '1px solid #222', color: '#888', fontSize: 18, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>&times;</button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
