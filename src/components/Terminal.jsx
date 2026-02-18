import { useState, useRef, useEffect, useCallback } from 'react';
import { SHIPPED_ITEMS, REFLECTIONS, IDENTITY_KERNEL, COGNITIVE_WEIGHTS, SYSTEM_STATS } from '../data';

const CHETANA_URL = 'https://chetana.activemirror.ai';

const HELP_TEXT = `Available commands:

  help        Show this help
  status      Service health overview
  scan <msg>  Scan a message for scam risk
  scan-url <url>  Check a URL for threats
  models      List available AI models
  identity    Show identity kernel
  weights     Show cognitive weight map
  brief       Sovereign briefing
  manifest    Build manifest
  shipped     Last 10 shipped items
  reflect     A random reflection
  about       System info
  clear       Clear terminal`;

const ABOUT_TEXT = `Active Mirror -- Sovereign AI Infrastructure
Built by Paul Desai in Goa, India

  Repos:          ${SYSTEM_STATS.repos}
  Models:         ${SYSTEM_STATS.models}
  Shipped:        ${SYSTEM_STATS.shipped_modules}+ modules
  Control Plane:  ${SYSTEM_STATS.control_plane_lines.toLocaleString()} lines
  Services:       ${SYSTEM_STATS.services}
  Guard Rules:    ${SYSTEM_STATS.guard_rules}

All code is sovereign. All data stays on-device.`;

function formatShipped() {
  return SHIPPED_ITEMS.slice(0, 10).map(item => {
    const name = item.name.padEnd(34);
    return `  ${item.date}  ${name} ${item.detail}`;
  }).join('\n');
}

function formatIdentity() {
  return JSON.stringify(IDENTITY_KERNEL, null, 2);
}

function formatWeights() {
  return COGNITIVE_WEIGHTS.map(w => {
    const filled = Math.round(w.value * 20);
    const empty = 20 - filled;
    const bar = '\u2588'.repeat(filled) + '\u2591'.repeat(empty);
    const label = w.label.padEnd(24);
    return `  ${label} ${bar}  ${w.value.toFixed(2)}`;
  }).join('\n');
}

export default function Terminal() {
  const [lines, setLines] = useState([
    { type: 'system', text: 'Active Mirror Beacon v1.0' },
    { type: 'system', text: 'Type "help" for available commands.' },
    { type: 'system', text: '' },
  ]);
  const [input, setInput] = useState('');
  const [history, setHistory] = useState([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const isAnimating = false;
  const termRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = useCallback(() => {
    if (termRef.current) {
      termRef.current.scrollTop = termRef.current.scrollHeight;
    }
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [lines, scrollToBottom]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const addLines = useCallback((newLines) => {
    setLines(prev => [...prev, ...newLines]);
  }, []);

  const typeOutput = useCallback((text, type = 'output') => {
    const outputLines = text.split('\n').map(line => ({ type, text: line }));
    addLines(outputLines);
  }, [addLines]);

  const fetchWithTimeout = async (url, options = {}, timeout = 5000) => {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);
    try {
      const res = await fetch(url, { ...options, signal: controller.signal, mode: 'cors' });
      clearTimeout(id);
      return res;
    } catch (e) {
      clearTimeout(id);
      throw e;
    }
  };

  const executeCommand = useCallback(async (cmd) => {
    const trimmed = cmd.trim();
    if (!trimmed) return;

    setLines(prev => [...prev, { type: 'prompt', text: `mirror@beacon ~ $ ${trimmed}` }]);

    const parts = trimmed.split(/\s+/);
    const command = parts[0].toLowerCase();
    const args = parts.slice(1).join(' ');

    switch (command) {
      case 'help':
        typeOutput(HELP_TEXT);
        break;

      case 'clear':
        setLines([]);
        break;

      case 'about':
        typeOutput(ABOUT_TEXT);
        break;

      case 'shipped':
        typeOutput('Last 10 shipped items:\n\n' + formatShipped());
        break;

      case 'reflect': {
        const idx = Math.floor(Math.random() * REFLECTIONS.length);
        typeOutput('\n  "' + REFLECTIONS[idx] + '"\n');
        break;
      }

      case 'identity':
        typeOutput(formatIdentity());
        break;

      case 'weights':
        typeOutput('Cognitive Weight Map:\n\n' + formatWeights());
        break;

      case 'scan': {
        if (!args) {
          typeOutput('Usage: scan <message to check for scams>');
          break;
        }
        typeOutput('Scanning...');
        try {
          const res = await fetchWithTimeout(`${CHETANA_URL}/api/scan`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: args }),
          }, 8000);
          const data = await res.json();
          const risk = data.risk_level || data.risk || 'UNKNOWN';
          const score = data.risk_score !== undefined ? data.risk_score : '?';
          const signals = data.signals || data.risk_signals || [];
          let output = `\n  Risk Level: ${risk}`;
          output += `\n  Score:      ${score}`;
          if (signals.length > 0) {
            output += '\n  Signals:';
            signals.forEach(s => { output += `\n    - ${s}`; });
          }
          if (data.recommendation) {
            output += `\n  Action:     ${data.recommendation}`;
          }
          typeOutput(output + '\n');
        } catch (e) {
          typeOutput('  [!] Could not reach Chetana. Service may be running privately.');
        }
        break;
      }

      case 'scan-url': {
        if (!args) {
          typeOutput('Usage: scan-url <url to check>');
          break;
        }
        typeOutput('Checking URL...');
        try {
          const res = await fetchWithTimeout(`${CHETANA_URL}/api/url/check`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: args }),
          }, 8000);
          const data = await res.json();
          const risk = data.risk_level || data.risk || 'UNKNOWN';
          let output = `\n  URL:   ${args}`;
          output += `\n  Risk:  ${risk}`;
          if (data.signals && data.signals.length > 0) {
            output += '\n  Flags:';
            data.signals.forEach(s => { output += `\n    - ${s}`; });
          }
          typeOutput(output + '\n');
        } catch (e) {
          typeOutput('  [!] Could not reach Chetana. Service may be running privately.');
        }
        break;
      }

      case 'status': {
        typeOutput('Fetching service status...');
        try {
          const res = await fetchWithTimeout('https://brain.activemirror.ai/status', {}, 5000);
          const data = await res.json();
          typeOutput(JSON.stringify(data, null, 2));
        } catch (e) {
          // Fall back to chetana health
          try {
            const res = await fetchWithTimeout(`${CHETANA_URL}/api/health`, {}, 5000);
            const data = await res.json();
            let output = '\n  System Status (partial):\n';
            output += `  chetana:  ONLINE\n`;
            if (data.model) output += `  model:    ${data.model}\n`;
            if (data.uptime) output += `  uptime:   ${data.uptime}\n`;
            output += `\n  [Other services running privately on LAN]`;
            typeOutput(output);
          } catch (e2) {
            typeOutput(`\n  System running privately.
  Services are accessible on the local network only.

  Known services: 24
  Scheduled tasks: 5
  Guard rules: 23`);
          }
        }
        break;
      }

      case 'models': {
        typeOutput('Querying model registry...');
        try {
          const res = await fetchWithTimeout('http://localhost:11434/api/tags', {}, 3000);
          const data = await res.json();
          if (data.models && data.models.length > 0) {
            const output = data.models.map(m => `  ${m.name}`).join('\n');
            typeOutput('\n  Loaded models:\n\n' + output + '\n');
          } else {
            typeOutput('  No models loaded.');
          }
        } catch (e) {
          typeOutput(`\n  Model registry not accessible from public network.
  Running locally: 14 models via Ollama

  Known models:
    llama3.2:3b
    llama3.1:8b
    qwen2.5-coder:7b
    deepseek-r1:7b
    mistral:7b
    gemma2:9b
    nomic-embed-text
    phi3:mini
    codellama:7b
    ... and more`);
        }
        break;
      }

      case 'brief': {
        typeOutput('Loading sovereign briefing...');
        try {
          const res = await fetchWithTimeout('http://localhost:8401/brief', {}, 5000);
          const data = await res.json();
          typeOutput(JSON.stringify(data, null, 2));
        } catch (e) {
          typeOutput(`\n  Briefing not accessible from public network.
  The sovereign briefing contains:
    - Current system phase
    - Active priorities
    - Open loops
    - Factory status
    - Drift score

  Access requires LAN or Tailscale mesh.`);
        }
        break;
      }

      case 'manifest': {
        typeOutput('Loading build manifest...');
        try {
          const res = await fetchWithTimeout('http://localhost:8401/manifest', {}, 5000);
          const data = await res.json();
          typeOutput(JSON.stringify(data, null, 2));
        } catch (e) {
          typeOutput(`\n  Manifest not accessible from public network.
  Current build manifest includes:
    - ${SYSTEM_STATS.repos} active repositories
    - ${SYSTEM_STATS.shipped_modules}+ shipped modules
    - ${SYSTEM_STATS.control_plane_lines.toLocaleString()} lines in control plane
    - ${SYSTEM_STATS.guard_rules} guard rules
    - ${SYSTEM_STATS.services} running services

  Access requires LAN or Tailscale mesh.`);
        }
        break;
      }

      default:
        typeOutput(`  command not found: ${command}\n  Type "help" for available commands.`);
    }
  }, [typeOutput]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !isAnimating) {
      const cmd = input;
      setInput('');
      setHistory(prev => [cmd, ...prev]);
      setHistoryIndex(-1);
      executeCommand(cmd);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (history.length > 0) {
        const newIndex = Math.min(historyIndex + 1, history.length - 1);
        setHistoryIndex(newIndex);
        setInput(history[newIndex]);
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (historyIndex > 0) {
        const newIndex = historyIndex - 1;
        setHistoryIndex(newIndex);
        setInput(history[newIndex]);
      } else {
        setHistoryIndex(-1);
        setInput('');
      }
    }
  };

  const handleTerminalClick = () => {
    inputRef.current?.focus();
  };

  return (
    <section id="terminal" className="px-4 py-16 max-w-4xl mx-auto">
      <h2 className="text-xs uppercase tracking-widest text-[var(--color-text-muted)] mb-4">
        Terminal
      </h2>
      <div
        ref={termRef}
        onClick={handleTerminalClick}
        className="bg-[var(--color-bg-terminal)] border border-[var(--color-border)] rounded-sm p-4 min-h-[400px] max-h-[600px] overflow-y-auto cursor-text font-mono text-sm leading-relaxed"
      >
        {lines.map((line, i) => (
          <div key={i} className="whitespace-pre-wrap break-words">
            {line.type === 'prompt' ? (
              <span>
                <span className="text-[var(--color-green)]">mirror@beacon</span>
                <span className="text-[var(--color-text-dim)]"> ~ $ </span>
                <span className="text-[var(--color-text)]">{line.text.replace(/^mirror@beacon ~ \$ /, '')}</span>
              </span>
            ) : line.type === 'system' ? (
              <span className="text-[var(--color-amber)]">{line.text}</span>
            ) : line.type === 'error' ? (
              <span className="text-[var(--color-red)]">{line.text}</span>
            ) : (
              <span className="text-[var(--color-text-dim)]">{line.text}</span>
            )}
          </div>
        ))}
        <div className="flex items-center">
          <span className="text-[var(--color-green)]">mirror@beacon</span>
          <span className="text-[var(--color-text-dim)]">&nbsp;~&nbsp;$&nbsp;</span>
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            className="flex-1 bg-transparent border-none outline-none text-[var(--color-text)] font-mono text-sm caret-[var(--color-green)]"
            spellCheck={false}
            autoComplete="off"
            autoCapitalize="off"
            disabled={isAnimating}
          />
        </div>
      </div>
    </section>
  );
}
