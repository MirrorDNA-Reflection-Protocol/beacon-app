#!/usr/bin/env python3
"""
Generate dashboard mockup images — Cyberpunk Terminal Aesthetic.
Uses Playwright to render HTML → PNG screenshots.

All dashboards share the terminal/cyberpunk DNA:
- Dark background with CRT glow
- Scanline overlay
- Monospace typography (JetBrains Mono)
- Neon accent colors (green, amber, cyan, magenta)
- ASCII box-drawing characters
- Each persona is a CUSTOMIZATION of the same sovereign OS

This is a product showcase — "Your dashboard, your way."
"""

import asyncio
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "public" / "screenshots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Shared CSS for cyberpunk terminal aesthetic
SHARED_CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
@keyframes blink { 0%,50% { opacity:1; } 51%,100% { opacity:0; } }
@keyframes pulse { 0%,100% { opacity:0.6; } 50% { opacity:1; } }
@keyframes scan { 0% { top:-100%; } 100% { top:100%; } }
body { background:#000; overflow:hidden; }
.scanlines::after {
    content:'';
    position:absolute;
    top:0;left:0;right:0;bottom:0;
    background:repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,0,0,0.15) 2px,
        rgba(0,0,0,0.15) 4px
    );
    pointer-events:none;
    z-index:100;
}
.glow-green { text-shadow: 0 0 8px rgba(34,197,94,0.5); }
.glow-amber { text-shadow: 0 0 8px rgba(245,158,11,0.5); }
.glow-cyan { text-shadow: 0 0 8px rgba(6,182,212,0.5); }
.glow-magenta { text-shadow: 0 0 8px rgba(236,72,153,0.5); }
.border-glow-green { box-shadow: 0 0 12px rgba(34,197,94,0.15), inset 0 0 12px rgba(34,197,94,0.05); }
.border-glow-amber { box-shadow: 0 0 12px rgba(245,158,11,0.15), inset 0 0 12px rgba(245,158,11,0.05); }
.border-glow-cyan { box-shadow: 0 0 12px rgba(6,182,212,0.15), inset 0 0 12px rgba(6,182,212,0.05); }
"""

MOCKUPS = {
    "dashboard-neurodivergent.png": {
        "title": "Focus Mode — Neurodivergent Optimized",
        "html": """
        <div class="scanlines" style="background:#050508;color:#e0e0e0;font-family:'JetBrains Mono',monospace;padding:28px;width:1280px;height:800px;display:flex;flex-direction:column;gap:20px;position:relative">
            <!-- Header -->
            <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #1a1a1a;padding-bottom:12px">
                <div style="display:flex;align-items:center;gap:12px">
                    <span style="color:#f59e0b;font-size:20px" class="glow-amber">◇</span>
                    <span style="font-size:14px;font-weight:600;color:#f59e0b" class="glow-amber">FOCUS MODE</span>
                    <span style="font-size:9px;color:#333;letter-spacing:3px;margin-left:8px">━━━ SINGLE TASK · ZERO NOISE ━━━</span>
                </div>
                <div style="display:flex;align-items:center;gap:12px">
                    <span style="width:6px;height:6px;border-radius:50%;background:#22c55e;box-shadow:0 0 8px #22c55e"></span>
                    <span style="font-size:10px;color:#22c55e" class="glow-green">DEEP WORK</span>
                    <span style="font-size:10px;color:#333">│</span>
                    <span style="font-size:10px;color:#555">14:32 IST</span>
                </div>
            </div>

            <!-- Main -->
            <div style="flex:1;display:flex;gap:20px">
                <!-- Focus panel -->
                <div style="flex:2;display:flex;flex-direction:column;gap:14px">
                    <div class="border-glow-amber" style="background:#0a0a0d;border:1px solid #f59e0b33;border-radius:12px;padding:32px;flex:1;display:flex;flex-direction:column;justify-content:center">
                        <div style="font-size:9px;color:#f59e0b;letter-spacing:4px" class="glow-amber">┌── CURRENT TASK ──────────────────────────┐</div>
                        <div style="font-size:26px;font-weight:300;color:#fff;line-height:1.5;margin:16px 0;padding-left:16px;border-left:2px solid #f59e0b">Deploy beacon chat widget<br/>with cascading AI providers</div>
                        <div style="font-size:9px;color:#f59e0b;letter-spacing:4px" class="glow-amber">└──────────────────────────────────────────┘</div>
                        <div style="margin-top:24px;display:flex;gap:12px">
                            <div style="background:#111;border:1px solid #1a1a1a;border-radius:8px;padding:14px 20px;text-align:center">
                                <div style="font-size:28px;font-weight:700;color:#f59e0b" class="glow-amber">2.5h</div>
                                <div style="font-size:8px;color:#444;text-transform:uppercase;letter-spacing:2px;margin-top:4px">elapsed</div>
                            </div>
                            <div style="background:#111;border:1px solid #1a1a1a;border-radius:8px;padding:14px 20px;text-align:center">
                                <div style="font-size:28px;font-weight:700;color:#22c55e" class="glow-green">3/4</div>
                                <div style="font-size:8px;color:#444;text-transform:uppercase;letter-spacing:2px;margin-top:4px">subtasks</div>
                            </div>
                            <div style="background:#111;border:1px solid #1a1a1a;border-radius:8px;padding:14px 20px;text-align:center">
                                <div style="font-size:28px;font-weight:700;color:#555">0.6</div>
                                <div style="font-size:8px;color:#444;text-transform:uppercase;letter-spacing:2px;margin-top:4px">drift</div>
                            </div>
                        </div>
                    </div>
                    <!-- Terminal -->
                    <div style="background:#070709;border:1px solid #111;border-radius:8px;padding:14px 18px;display:flex;align-items:center;gap:10px">
                        <span style="color:#22c55e;font-size:12px" class="glow-green">▶</span>
                        <span style="color:#22c55e;font-size:11px" class="glow-green">$</span>
                        <span style="color:#888;font-size:11px">git push origin main</span>
                        <span style="color:#22c55e;animation:blink 1s infinite;margin-left:2px">█</span>
                        <span style="margin-left:auto;font-size:9px;color:#333">ESC to cancel</span>
                    </div>
                </div>

                <!-- Sidebar -->
                <div style="width:280px;display:flex;flex-direction:column;gap:12px">
                    <div style="background:#0a0a0d;border:1px solid #111;border-radius:10px;padding:18px;flex:1">
                        <div style="font-size:9px;color:#555;letter-spacing:3px;margin-bottom:14px">┌ QUEUE ─────────────┐</div>
                        <div style="font-size:10px;line-height:2.4">
                            <div style="color:#333;text-decoration:line-through">☑ Email service setup</div>
                            <div style="color:#333;text-decoration:line-through">☑ Chat API routing</div>
                            <div style="color:#333;text-decoration:line-through">☑ Rate limiting</div>
                            <div style="color:#f59e0b" class="glow-amber">▸ Dashboard mockups</div>
                            <div style="color:#444">○ Deploy to production</div>
                        </div>
                        <div style="font-size:9px;color:#555;letter-spacing:3px;margin-top:12px">└────────────────────┘</div>
                    </div>
                    <!-- Energy meter -->
                    <div style="background:#0a0a0d;border:1px solid #111;border-radius:10px;padding:18px">
                        <div style="font-size:9px;color:#555;letter-spacing:3px;margin-bottom:10px">COGNITIVE LOAD</div>
                        <div style="display:flex;gap:3px;margin-bottom:6px">
                            <div style="flex:1;height:8px;background:#22c55e;border-radius:2px;box-shadow:0 0 6px rgba(34,197,94,0.3)"></div>
                            <div style="flex:1;height:8px;background:#22c55e;border-radius:2px;box-shadow:0 0 6px rgba(34,197,94,0.3)"></div>
                            <div style="flex:1;height:8px;background:#22c55e;border-radius:2px;box-shadow:0 0 6px rgba(34,197,94,0.3)"></div>
                            <div style="flex:1;height:8px;background:#0a0a0a;border:1px solid #1a1a1a;border-radius:2px"></div>
                            <div style="flex:1;height:8px;background:#0a0a0a;border:1px solid #1a1a1a;border-radius:2px"></div>
                        </div>
                        <div style="font-size:9px;color:#22c55e" class="glow-green">LOW · PRODUCTIVE</div>
                    </div>
                </div>
            </div>

            <!-- Footer -->
            <div style="font-size:8px;color:#1a1a1a;text-align:center;letter-spacing:3px">◇ ACTIVE MIRROR · FOCUS MODE · CUSTOMIZABLE · NEURODIVERGENT OPTIMIZED ◇</div>
        </div>
        """,
    },
    "dashboard-sysadmin.png": {
        "title": "Sysadmin Terminal — Infrastructure Ops",
        "html": """
        <div class="scanlines" style="background:#020204;color:#e0e0e0;font-family:'JetBrains Mono',monospace;padding:0;width:1280px;height:800px;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:auto 1fr 1fr;gap:1px;background-color:#0a0a0a;position:relative">
            <!-- Top bar -->
            <div style="grid-column:span 2;background:#050508;padding:10px 18px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #22c55e22">
                <div style="display:flex;gap:16px;align-items:center">
                    <span style="color:#22c55e" class="glow-green">◇</span>
                    <span style="font-size:11px;font-weight:600;color:#22c55e" class="glow-green">ACTIVE MIRROR OPS</span>
                    <span style="font-size:9px;color:#22c55e44">│</span>
                    <span style="font-size:9px;color:#22c55e" class="glow-green">● 22/24 UP</span>
                    <span style="font-size:9px;color:#f59e0b" class="glow-amber">▲ 2 WARN</span>
                    <span style="font-size:9px;color:#333">│</span>
                    <span style="font-size:9px;color:#444">CPU:34%</span>
                    <span style="font-size:9px;color:#f59e0b">MEM:76%</span>
                    <span style="font-size:9px;color:#444">DISK:52%</span>
                    <span style="font-size:9px;color:#444">NET:↑2.1 ↓0.8 MB/s</span>
                </div>
                <div style="font-size:9px;color:#333">mac-mini-m4 · goa · 23:14:07 IST</div>
            </div>

            <!-- Service mesh -->
            <div style="background:#050508;padding:14px;overflow:hidden">
                <div style="font-size:8px;color:#22c55e44;letter-spacing:3px;margin-bottom:8px">┌── SERVICE MESH ────────────────────────┐</div>
                <div style="font-size:9px;line-height:2.2;color:#888">
                    <div><span style="color:#22c55e">●</span> chetana-api       <span style="color:#333">:8100</span> <span style="color:#22c55e;float:right" class="glow-green">12ms ✓</span></div>
                    <div><span style="color:#22c55e">●</span> beacon-chat       <span style="color:#333">:8095</span> <span style="color:#22c55e;float:right" class="glow-green">8ms ✓</span></div>
                    <div><span style="color:#22c55e">●</span> mirrordna-api     <span style="color:#333">:8088</span> <span style="color:#22c55e;float:right" class="glow-green">5ms ✓</span></div>
                    <div><span style="color:#22c55e">●</span> memory-bus        <span style="color:#333">:8200</span> <span style="color:#22c55e;float:right" class="glow-green">3ms ✓</span></div>
                    <div><span style="color:#22c55e">●</span> glyph-engine      <span style="color:#333">:8090</span> <span style="color:#22c55e;float:right" class="glow-green">7ms ✓</span></div>
                    <div><span style="color:#f59e0b">▲</span> <span style="color:#f59e0b">ollama</span>            <span style="color:#333">:11434</span> <span style="color:#f59e0b;float:right" class="glow-amber">HIGH MEM</span></div>
                    <div><span style="color:#22c55e">●</span> cloudflared       <span style="color:#333">tunnel</span> <span style="color:#22c55e;float:right" class="glow-green">ok ✓</span></div>
                    <div><span style="color:#22c55e">●</span> safety-proxy      <span style="color:#333">:8443</span> <span style="color:#22c55e;float:right" class="glow-green">4ms ✓</span></div>
                    <div><span style="color:#f59e0b">▲</span> <span style="color:#f59e0b">beacon-synth</span>      <span style="color:#333">cron</span> <span style="color:#f59e0b;float:right" class="glow-amber">STALE</span></div>
                    <div><span style="color:#22c55e">●</span> mirror-balance    <span style="color:#333">:8400</span> <span style="color:#22c55e;float:right" class="glow-green">6ms ✓</span></div>
                </div>
                <div style="font-size:8px;color:#22c55e44;letter-spacing:3px;margin-top:6px">└────────────────────────────────────────┘</div>
            </div>

            <!-- Live logs -->
            <div style="background:#050508;padding:14px;overflow:hidden">
                <div style="font-size:8px;color:#06b6d444;letter-spacing:3px;margin-bottom:8px">┌── LIVE LOG STREAM ─────────────────────┐</div>
                <div style="font-size:8px;line-height:2.2;color:#444">
                    <div><span style="color:#333">23:14:01</span> <span style="color:#06b6d4">[chetana]</span> scan: UPI fraud detected <span style="color:#ef4444">risk=HIGH</span></div>
                    <div><span style="color:#333">23:14:02</span> <span style="color:#22c55e">[beacon]</span> chat: groq resp 340ms provider=groq</div>
                    <div><span style="color:#333">23:14:03</span> <span style="color:#888">[bus]</span> session commit: 4 entries → bus/</div>
                    <div><span style="color:#333">23:14:04</span> <span style="color:#f59e0b">[ollama]</span> warn: llama3.1:8b mem 8.4G/24G</div>
                    <div><span style="color:#333">23:14:05</span> <span style="color:#22c55e">[glyph]</span> audit: AMGL rule #14 → ALLOW</div>
                    <div><span style="color:#333">23:14:06</span> <span style="color:#888">[bus]</span> heartbeat: drift=2.1% status=ok</div>
                    <div><span style="color:#333">23:14:07</span> <span style="color:#06b6d4">[chetana]</span> scan: phishing link → <span style="color:#f59e0b">MEDIUM</span></div>
                    <div><span style="color:#333">23:14:07</span> <span style="color:#22c55e">[factory]</span> batch-041: 6/6 agents complete</div>
                    <div><span style="color:#333">23:14:08</span> <span style="color:#888">[radar]</span> intel scan: 47 signals scored</div>
                </div>
                <div style="font-size:8px;color:#06b6d444;letter-spacing:3px;margin-top:6px">└─── tail -f /var/log/mirror/*.log ──────┘</div>
            </div>

            <!-- Resource meters -->
            <div style="background:#050508;padding:14px;overflow:hidden">
                <div style="font-size:8px;color:#f59e0b44;letter-spacing:3px;margin-bottom:10px">┌── RESOURCES ───────────────────────────┐</div>
                <div style="margin-top:4px">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px">
                        <span style="font-size:9px;color:#444;width:36px">CPU</span>
                        <div style="flex:1;height:10px;background:#0a0a0a;border:1px solid #111;border-radius:2px">
                            <div style="width:34%;height:100%;background:linear-gradient(90deg,#22c55e,#22c55e88);border-radius:1px;box-shadow:0 0 8px rgba(34,197,94,0.2)"></div>
                        </div>
                        <span style="font-size:9px;color:#22c55e;width:30px;text-align:right" class="glow-green">34%</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px">
                        <span style="font-size:9px;color:#444;width:36px">MEM</span>
                        <div style="flex:1;height:10px;background:#0a0a0a;border:1px solid #111;border-radius:2px">
                            <div style="width:76%;height:100%;background:linear-gradient(90deg,#f59e0b,#f59e0b88);border-radius:1px;box-shadow:0 0 8px rgba(245,158,11,0.2)"></div>
                        </div>
                        <span style="font-size:9px;color:#f59e0b;width:30px;text-align:right" class="glow-amber">76%</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px">
                        <span style="font-size:9px;color:#444;width:36px">DISK</span>
                        <div style="flex:1;height:10px;background:#0a0a0a;border:1px solid #111;border-radius:2px">
                            <div style="width:52%;height:100%;background:linear-gradient(90deg,#06b6d4,#06b6d488);border-radius:1px;box-shadow:0 0 8px rgba(6,182,212,0.2)"></div>
                        </div>
                        <span style="font-size:9px;color:#06b6d4;width:30px;text-align:right" class="glow-cyan">52%</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px">
                        <span style="font-size:9px;color:#444;width:36px">GPU</span>
                        <div style="flex:1;height:10px;background:#0a0a0a;border:1px solid #111;border-radius:2px">
                            <div style="width:41%;height:100%;background:linear-gradient(90deg,#8b5cf6,#8b5cf688);border-radius:1px;box-shadow:0 0 8px rgba(139,92,246,0.2)"></div>
                        </div>
                        <span style="font-size:9px;color:#8b5cf6;width:30px;text-align:right">41%</span>
                    </div>
                </div>
                <div style="font-size:8px;color:#444;letter-spacing:2px;margin-top:10px">OLLAMA MODELS LOADED</div>
                <div style="font-size:8px;color:#333;line-height:2;margin-top:4px">
                    llama3.1:8b <span style="color:#222">(4.7G)</span> · mistral:7b <span style="color:#222">(4.1G)</span> · qwen2:7b <span style="color:#222">(4.4G)</span>
                </div>
                <div style="font-size:8px;color:#f59e0b44;letter-spacing:3px;margin-top:8px">└────────────────────────────────────────┘</div>
            </div>

            <!-- Governance -->
            <div style="background:#050508;padding:14px;overflow:hidden">
                <div style="font-size:8px;color:#22c55e44;letter-spacing:3px;margin-bottom:10px">┌── AMGL GOVERNANCE · 23 RULES ─────────┐</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:8px">
                    <div style="background:#070709;border:1px solid #111;border-radius:4px;padding:7px 10px"><span style="color:#22c55e">✓</span> <span style="color:#666">Data sovereignty</span></div>
                    <div style="background:#070709;border:1px solid #111;border-radius:4px;padding:7px 10px"><span style="color:#22c55e">✓</span> <span style="color:#666">No cloud telemetry</span></div>
                    <div style="background:#070709;border:1px solid #111;border-radius:4px;padding:7px 10px"><span style="color:#22c55e">✓</span> <span style="color:#666">PGP signed outputs</span></div>
                    <div style="background:#070709;border:1px solid #111;border-radius:4px;padding:7px 10px"><span style="color:#22c55e">✓</span> <span style="color:#666">Audit trail active</span></div>
                    <div style="background:#070709;border:1px solid #111;border-radius:4px;padding:7px 10px"><span style="color:#22c55e">✓</span> <span style="color:#666">Memory isolation</span></div>
                    <div style="background:#070709;border:1px solid #111;border-radius:4px;padding:7px 10px"><span style="color:#22c55e">✓</span> <span style="color:#666">Agent sandboxing</span></div>
                    <div style="background:#070709;border:1px solid #111;border-radius:4px;padding:7px 10px"><span style="color:#22c55e">✓</span> <span style="color:#666">Fail-open routing</span></div>
                    <div style="background:#070709;border:1px solid #111;border-radius:4px;padding:7px 10px"><span style="color:#22c55e">✓</span> <span style="color:#666">Token scoping</span></div>
                </div>
                <div style="margin-top:10px;font-size:8px;color:#444">
                    Last audit: 23:14:05 · <span style="color:#22c55e">23/23 PASS</span> · 0 violations (30d)
                </div>
                <div style="font-size:8px;color:#22c55e44;letter-spacing:3px;margin-top:8px">└────────────────────────────────────────┘</div>
            </div>
        </div>
        """,
    },
    "dashboard-enterprise.png": {
        "title": "Enterprise Command Center",
        "html": """
        <div class="scanlines" style="background:#06060c;color:#e0e0e0;font-family:'JetBrains Mono',monospace;padding:0;width:1280px;height:800px;display:flex;flex-direction:column;position:relative">
            <!-- Top bar -->
            <div style="background:#08080f;padding:12px 24px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #818cf822">
                <div style="display:flex;align-items:center;gap:16px">
                    <span style="color:#818cf8;font-size:18px" class="glow-cyan">◇</span>
                    <span style="font-size:13px;font-weight:600;color:#818cf8" class="glow-cyan">ENTERPRISE AI COMMAND</span>
                    <span style="font-size:9px;color:#333">━━━</span>
                    <div style="display:flex;gap:20px;font-size:9px">
                        <span style="color:#818cf8;border-bottom:1px solid #818cf8;padding-bottom:4px">Overview</span>
                        <span style="color:#444">Teams</span>
                        <span style="color:#444">Compliance</span>
                        <span style="color:#444">Audit</span>
                        <span style="color:#444">Costs</span>
                    </div>
                </div>
                <div style="display:flex;align-items:center;gap:12px">
                    <div style="background:#22c55e11;border:1px solid #22c55e33;color:#22c55e;font-size:8px;padding:4px 10px;border-radius:3px" class="glow-green">ALL SYSTEMS COMPLIANT</div>
                    <span style="font-size:9px;color:#333">Q1 2026</span>
                </div>
            </div>

            <!-- KPI strip -->
            <div style="background:#08080f;padding:14px 24px;display:flex;gap:16px;border-bottom:1px solid #0a0a14">
                <div style="flex:1;background:#0a0a14;border:1px solid #12121e;border-radius:8px;padding:14px;text-align:center">
                    <div style="font-size:30px;font-weight:700;color:#818cf8" class="glow-cyan">47</div>
                    <div style="font-size:8px;color:#444;text-transform:uppercase;letter-spacing:2px;margin-top:4px">Active Agents</div>
                </div>
                <div style="flex:1;background:#0a0a14;border:1px solid #12121e;border-radius:8px;padding:14px;text-align:center">
                    <div style="font-size:30px;font-weight:700;color:#22c55e" class="glow-green">99.7%</div>
                    <div style="font-size:8px;color:#444;text-transform:uppercase;letter-spacing:2px;margin-top:4px">Uptime (30d)</div>
                </div>
                <div style="flex:1;background:#0a0a14;border:1px solid #12121e;border-radius:8px;padding:14px;text-align:center">
                    <div style="font-size:30px;font-weight:700;color:#f59e0b" class="glow-amber">$2.4k</div>
                    <div style="font-size:8px;color:#444;text-transform:uppercase;letter-spacing:2px;margin-top:4px">Monthly Cost</div>
                </div>
                <div style="flex:1;background:#0a0a14;border:1px solid #12121e;border-radius:8px;padding:14px;text-align:center">
                    <div style="font-size:30px;font-weight:700;color:#fff">0</div>
                    <div style="font-size:8px;color:#444;text-transform:uppercase;letter-spacing:2px;margin-top:4px">Policy Violations</div>
                </div>
            </div>

            <!-- Main grid -->
            <div style="flex:1;display:grid;grid-template-columns:1fr 1fr;gap:1px;background:#0a0a14;padding:1px">
                <!-- Team performance -->
                <div style="background:#08080f;padding:18px">
                    <div style="font-size:8px;color:#818cf844;letter-spacing:3px;margin-bottom:14px">┌── TEAM PERFORMANCE ────────────────────┐</div>
                    <div style="font-size:9px;line-height:3">
                        <div style="display:flex;align-items:center;gap:8px">
                            <span style="width:80px;color:#666">Engineering</span>
                            <div style="flex:1;height:8px;background:#0a0a14;border:1px solid #111;border-radius:2px"><div style="width:87%;height:100%;background:linear-gradient(90deg,#818cf8,#818cf888);border-radius:1px;box-shadow:0 0 6px rgba(129,140,248,0.2)"></div></div>
                            <span style="color:#818cf8;width:30px;text-align:right">87%</span>
                        </div>
                        <div style="display:flex;align-items:center;gap:8px">
                            <span style="width:80px;color:#666">Security</span>
                            <div style="flex:1;height:8px;background:#0a0a14;border:1px solid #111;border-radius:2px"><div style="width:94%;height:100%;background:linear-gradient(90deg,#22c55e,#22c55e88);border-radius:1px;box-shadow:0 0 6px rgba(34,197,94,0.2)"></div></div>
                            <span style="color:#22c55e;width:30px;text-align:right">94%</span>
                        </div>
                        <div style="display:flex;align-items:center;gap:8px">
                            <span style="width:80px;color:#666">Data Science</span>
                            <div style="flex:1;height:8px;background:#0a0a14;border:1px solid #111;border-radius:2px"><div style="width:72%;height:100%;background:linear-gradient(90deg,#f59e0b,#f59e0b88);border-radius:1px;box-shadow:0 0 6px rgba(245,158,11,0.2)"></div></div>
                            <span style="color:#f59e0b;width:30px;text-align:right">72%</span>
                        </div>
                        <div style="display:flex;align-items:center;gap:8px">
                            <span style="width:80px;color:#666">Operations</span>
                            <div style="flex:1;height:8px;background:#0a0a14;border:1px solid #111;border-radius:2px"><div style="width:91%;height:100%;background:linear-gradient(90deg,#818cf8,#818cf888);border-radius:1px;box-shadow:0 0 6px rgba(129,140,248,0.2)"></div></div>
                            <span style="color:#818cf8;width:30px;text-align:right">91%</span>
                        </div>
                    </div>
                </div>

                <!-- Compliance -->
                <div style="background:#08080f;padding:18px">
                    <div style="font-size:8px;color:#22c55e44;letter-spacing:3px;margin-bottom:14px">┌── COMPLIANCE STATUS ───────────────────┐</div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:8px">
                        <div style="background:#0a0a14;border:1px solid #12121e;border-radius:4px;padding:8px 10px"><span style="color:#22c55e">●</span> SOC 2 Type II <span style="float:right;color:#22c55e" class="glow-green">PASS</span></div>
                        <div style="background:#0a0a14;border:1px solid #12121e;border-radius:4px;padding:8px 10px"><span style="color:#22c55e">●</span> GDPR <span style="float:right;color:#22c55e" class="glow-green">PASS</span></div>
                        <div style="background:#0a0a14;border:1px solid #12121e;border-radius:4px;padding:8px 10px"><span style="color:#22c55e">●</span> ISO 27001 <span style="float:right;color:#22c55e" class="glow-green">PASS</span></div>
                        <div style="background:#0a0a14;border:1px solid #12121e;border-radius:4px;padding:8px 10px"><span style="color:#22c55e">●</span> HIPAA <span style="float:right;color:#22c55e" class="glow-green">PASS</span></div>
                        <div style="background:#0a0a14;border:1px solid #12121e;border-radius:4px;padding:8px 10px"><span style="color:#22c55e">●</span> PCI DSS <span style="float:right;color:#22c55e" class="glow-green">PASS</span></div>
                        <div style="background:#0a0a14;border:1px solid #12121e;border-radius:4px;padding:8px 10px"><span style="color:#22c55e">●</span> AI Act (EU) <span style="float:right;color:#22c55e" class="glow-green">PASS</span></div>
                    </div>
                </div>

                <!-- Model routing -->
                <div style="background:#08080f;padding:18px">
                    <div style="font-size:8px;color:#f59e0b44;letter-spacing:3px;margin-bottom:14px">┌── MODEL ROUTING ───────────────────────┐</div>
                    <div style="font-size:9px;line-height:2.6;color:#666">
                        <div>Tier 1 → <span style="color:#818cf8" class="glow-cyan">Claude Opus</span> · reasoning, arch <span style="color:#333;float:right">$0.08/call</span></div>
                        <div>Tier 2 → <span style="color:#22c55e" class="glow-green">Gemini Pro</span> · bulk, summaries <span style="color:#333;float:right">$0.02/call</span></div>
                        <div>Tier 3 → <span style="color:#f59e0b" class="glow-amber">Local Llama</span> · PII, always-on <span style="color:#333;float:right">$0.00</span></div>
                    </div>
                    <div style="font-size:8px;color:#444;margin-top:8px">Total API spend (30d): <span style="color:#f59e0b" class="glow-amber">$2,412</span> · ↓14% vs prev month</div>
                </div>

                <!-- Decisions log -->
                <div style="background:#08080f;padding:18px">
                    <div style="font-size:8px;color:#06b6d444;letter-spacing:3px;margin-bottom:14px">┌── GOVERNANCE DECISIONS ────────────────┐</div>
                    <div style="font-size:9px;line-height:2.4;color:#444">
                        <div><span style="color:#22c55e" class="glow-green">ALLOW</span> agent-041 → deploy staging <span style="color:#222;float:right">14:31</span></div>
                        <div><span style="color:#22c55e" class="glow-green">ALLOW</span> agent-038 → read customer DB <span style="color:#222;float:right">14:28</span></div>
                        <div><span style="color:#f59e0b" class="glow-amber">ASK  </span> agent-042 → write prod config <span style="color:#222;float:right">14:25</span></div>
                        <div><span style="color:#ef4444">BLOCK</span> agent-039 → ext API no auth <span style="color:#222;float:right">14:20</span></div>
                    </div>
                </div>
            </div>
        </div>
        """,
    },
    "dashboard-creative.png": {
        "title": "Creative Studio — Visual AI Workspace",
        "html": """
        <div class="scanlines" style="background:#06060a;color:#e0e0e0;font-family:'JetBrains Mono',monospace;padding:24px;width:1280px;height:800px;display:flex;flex-direction:column;gap:18px;position:relative">
            <!-- Header -->
            <div style="display:flex;justify-content:space-between;align-items:center">
                <div style="display:flex;align-items:center;gap:12px">
                    <span style="color:#ec4899;font-size:20px" class="glow-magenta">◇</span>
                    <span style="font-size:14px;font-weight:300;color:#ec4899;letter-spacing:3px" class="glow-magenta">CREATIVE STUDIO</span>
                </div>
                <div style="display:flex;gap:6px">
                    <div style="width:16px;height:16px;border-radius:50%;background:#ec4899;box-shadow:0 0 12px rgba(236,72,153,0.4)"></div>
                    <div style="width:16px;height:16px;border-radius:50%;background:#8b5cf6;box-shadow:0 0 12px rgba(139,92,246,0.4)"></div>
                    <div style="width:16px;height:16px;border-radius:50%;background:#06b6d4;box-shadow:0 0 12px rgba(6,182,212,0.4)"></div>
                    <div style="width:16px;height:16px;border-radius:50%;background:#f59e0b;box-shadow:0 0 12px rgba(245,158,11,0.4)"></div>
                </div>
            </div>

            <!-- Main -->
            <div style="flex:1;display:grid;grid-template-columns:2fr 1fr;grid-template-rows:1fr 1fr;gap:14px">
                <!-- Canvas -->
                <div style="grid-row:span 2;background:#08080e;border:1px solid #ec489922;border-radius:12px;padding:20px;display:flex;flex-direction:column" class="border-glow-cyan">
                    <div style="font-size:8px;color:#8b5cf644;letter-spacing:4px;margin-bottom:12px">┌── GENERATION CANVAS ───────────────────────────────────────┐</div>
                    <div style="flex:1;background:#050508;border:1px solid #0a0a14;border-radius:8px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden">
                        <!-- Glow orbs -->
                        <div style="position:absolute;width:220px;height:220px;background:radial-gradient(circle,rgba(139,92,246,0.12),transparent);top:15%;left:15%"></div>
                        <div style="position:absolute;width:180px;height:180px;background:radial-gradient(circle,rgba(236,72,153,0.08),transparent);bottom:15%;right:25%"></div>
                        <div style="position:absolute;width:160px;height:160px;background:radial-gradient(circle,rgba(6,182,212,0.06),transparent);top:50%;right:10%"></div>
                        <div style="text-align:center;z-index:1">
                            <div style="font-size:48px;color:#1a1a2e;margin-bottom:16px">◇</div>
                            <div style="font-size:9px;color:#333;letter-spacing:3px">DESCRIBE · DRAG · GENERATE</div>
                            <div style="font-size:8px;color:#222;letter-spacing:2px;margin-top:8px">ALL PROCESSING ON-DEVICE</div>
                        </div>
                    </div>
                    <div style="display:flex;gap:6px;margin-top:14px">
                        <div style="flex:1;background:#0a0a14;border:1px solid #12121e;border-radius:6px;padding:10px;font-size:9px;color:#666;text-align:center">Generate</div>
                        <div style="flex:1;background:#0a0a14;border:1px solid #12121e;border-radius:6px;padding:10px;font-size:9px;color:#666;text-align:center">Remix</div>
                        <div style="flex:1;background:#0a0a14;border:1px solid #12121e;border-radius:6px;padding:10px;font-size:9px;color:#666;text-align:center">Upscale</div>
                        <div style="flex:1;background:#8b5cf611;border:1px solid #8b5cf633;border-radius:6px;padding:10px;font-size:9px;color:#8b5cf6;text-align:center;box-shadow:0 0 8px rgba(139,92,246,0.1)" class="glow-magenta">Synthesize</div>
                    </div>
                    <div style="font-size:8px;color:#8b5cf644;letter-spacing:4px;margin-top:10px">└────────────────────────────────────────────────────────────┘</div>
                </div>

                <!-- Mood / style -->
                <div style="background:#08080e;border:1px solid #12121e;border-radius:12px;padding:18px">
                    <div style="font-size:8px;color:#ec489944;letter-spacing:4px;margin-bottom:10px">┌── MOOD & STYLE ─────┐</div>
                    <div style="display:flex;flex-wrap:wrap;gap:5px;font-size:8px">
                        <span style="background:#ec489916;color:#ec4899;padding:4px 10px;border-radius:10px;border:1px solid #ec489933;box-shadow:0 0 6px rgba(236,72,153,0.15)">ethereal</span>
                        <span style="background:#8b5cf616;color:#8b5cf6;padding:4px 10px;border-radius:10px;border:1px solid #8b5cf633;box-shadow:0 0 6px rgba(139,92,246,0.15)">cosmic</span>
                        <span style="background:#22c55e16;color:#22c55e;padding:4px 10px;border-radius:10px;border:1px solid #22c55e33">organic</span>
                        <span style="background:#0a0a14;color:#444;padding:4px 10px;border-radius:10px;border:1px solid #12121e">minimal</span>
                        <span style="background:#0a0a14;color:#444;padding:4px 10px;border-radius:10px;border:1px solid #12121e">brutal</span>
                    </div>
                    <div style="font-size:8px;color:#f59e0b44;letter-spacing:4px;margin:16px 0 8px">PALETTE</div>
                    <div style="display:flex;gap:5px">
                        <div style="width:28px;height:28px;border-radius:6px;background:#8b5cf6;box-shadow:0 0 8px rgba(139,92,246,0.3)"></div>
                        <div style="width:28px;height:28px;border-radius:6px;background:#ec4899;box-shadow:0 0 8px rgba(236,72,153,0.3)"></div>
                        <div style="width:28px;height:28px;border-radius:6px;background:#06060a;border:1px solid #1a1a2e"></div>
                        <div style="width:28px;height:28px;border-radius:6px;background:#f0f0f0"></div>
                        <div style="width:28px;height:28px;border-radius:6px;background:#f59e0b;box-shadow:0 0 8px rgba(245,158,11,0.3)"></div>
                    </div>
                    <div style="font-size:8px;color:#444;letter-spacing:3px;margin:16px 0 6px">MODEL</div>
                    <div style="font-size:10px;color:#8b5cf6" class="glow-magenta">Stable Diffusion XL</div>
                    <div style="font-size:8px;color:#333;margin-top:3px">On-device · No cloud · Your IP</div>
                    <div style="font-size:8px;color:#ec489944;letter-spacing:4px;margin-top:12px">└─────────────────────┘</div>
                </div>

                <!-- Recent grid -->
                <div style="background:#08080e;border:1px solid #12121e;border-radius:12px;padding:18px">
                    <div style="font-size:8px;color:#06b6d444;letter-spacing:4px;margin-bottom:10px">┌── RECENT ───────────┐</div>
                    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:5px">
                        <div style="aspect-ratio:1;background:#8b5cf608;border:1px solid #8b5cf622;border-radius:6px;box-shadow:inset 0 0 20px rgba(139,92,246,0.05)"></div>
                        <div style="aspect-ratio:1;background:#ec489908;border:1px solid #ec489922;border-radius:6px;box-shadow:inset 0 0 20px rgba(236,72,153,0.05)"></div>
                        <div style="aspect-ratio:1;background:#f59e0b08;border:1px solid #f59e0b22;border-radius:6px;box-shadow:inset 0 0 20px rgba(245,158,11,0.05)"></div>
                        <div style="aspect-ratio:1;background:#22c55e08;border:1px solid #22c55e22;border-radius:6px;box-shadow:inset 0 0 20px rgba(34,197,94,0.05)"></div>
                        <div style="aspect-ratio:1;background:#06b6d408;border:1px solid #06b6d422;border-radius:6px;box-shadow:inset 0 0 20px rgba(6,182,212,0.05)"></div>
                        <div style="aspect-ratio:1;background:#08080e;border:1px solid #12121e;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:14px;color:#222">+</div>
                    </div>
                    <div style="font-size:8px;color:#06b6d444;letter-spacing:4px;margin-top:10px">└─────────────────────┘</div>
                </div>
            </div>

            <!-- Footer -->
            <div style="font-size:7px;color:#111;text-align:center;letter-spacing:3px">◇ ACTIVE MIRROR · CREATIVE STUDIO · ALL GENERATION ON-DEVICE · YOUR ART STAYS YOURS · CUSTOMIZABLE ◇</div>
        </div>
        """,
    },
    "dashboard-teams.png": {
        "title": "Teams — Async Ops, Shared Context",
        "html": """
        <div class="scanlines" style="background:#030305;color:#e0e0e0;font-family:'JetBrains Mono',monospace;padding:0;width:1280px;height:800px;display:flex;flex-direction:column;gap:1px;background-color:#0a0a0a;position:relative">
            <!-- Top bar -->
            <div style="background:#050508;padding:10px 18px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #06b6d422">
                <div style="display:flex;gap:16px;align-items:center">
                    <span style="color:#06b6d4" class="glow-cyan">◇</span>
                    <span style="font-size:11px;font-weight:600;color:#06b6d4" class="glow-cyan">TEAM MESH</span>
                    <span style="font-size:9px;color:#06b6d444">│</span>
                    <span style="font-size:9px;color:#22c55e" class="glow-green">● 5/6 ONLINE</span>
                    <span style="font-size:9px;color:#06b6d444">│</span>
                    <span style="font-size:9px;color:#555">DRIFT 2.3% · VELOCITY HIGH</span>
                </div>
                <div style="display:flex;gap:12px;font-size:9px;color:#444">
                    <span style="color:#06b6d4" class="glow-cyan">Overview</span>
                    <span>Standups</span><span>Context</span><span>Blockers</span><span>Decisions</span>
                    <span style="margin-left:12px;color:#555">14:47 IST</span>
                </div>
            </div>
            <!-- Body -->
            <div style="flex:1;display:grid;grid-template-columns:1fr 1fr;gap:1px;background:#0a0a0a">
                <!-- Left: Team presence -->
                <div style="background:#030305;padding:18px;display:flex;flex-direction:column;gap:14px">
                    <div style="font-size:9px;color:#06b6d4;letter-spacing:3px" class="glow-cyan">┌── PRESENCE ─────────────────────────────┐</div>
                    <div style="display:flex;flex-direction:column;gap:10px">
                        <div style="display:flex;align-items:center;gap:12px;padding:10px 14px;background:#070709;border:1px solid #06b6d422;border-radius:8px">
                            <span style="width:8px;height:8px;border-radius:50%;background:#22c55e;box-shadow:0 0 8px #22c55e;flex-shrink:0"></span>
                            <span style="font-size:11px;color:#e0e0e0;width:90px">priya</span>
                            <span style="font-size:10px;color:#555;flex:1">Refactoring auth middleware</span>
                            <span style="font-size:9px;color:#22c55e" class="glow-green">FLOW · 1.8h</span>
                        </div>
                        <div style="display:flex;align-items:center;gap:12px;padding:10px 14px;background:#070709;border:1px solid #06b6d422;border-radius:8px">
                            <span style="width:8px;height:8px;border-radius:50%;background:#22c55e;box-shadow:0 0 8px #22c55e;flex-shrink:0"></span>
                            <span style="font-size:11px;color:#e0e0e0;width:90px">arjun</span>
                            <span style="font-size:10px;color:#555;flex:1">API gateway latency tests</span>
                            <span style="font-size:9px;color:#22c55e" class="glow-green">FLOW · 0.4h</span>
                        </div>
                        <div style="display:flex;align-items:center;gap:12px;padding:10px 14px;background:#070709;border:1px solid #f59e0b22;border-radius:8px">
                            <span style="width:8px;height:8px;border-radius:50%;background:#f59e0b;box-shadow:0 0 8px #f59e0b;flex-shrink:0"></span>
                            <span style="font-size:11px;color:#e0e0e0;width:90px">sam</span>
                            <span style="font-size:10px;color:#f59e0b;flex:1">Blocked — needs design review</span>
                            <span style="font-size:9px;color:#f59e0b" class="glow-amber">BLOCKED</span>
                        </div>
                        <div style="display:flex;align-items:center;gap:12px;padding:10px 14px;background:#070709;border:1px solid #06b6d422;border-radius:8px">
                            <span style="width:8px;height:8px;border-radius:50%;background:#22c55e;box-shadow:0 0 8px #22c55e;flex-shrink:0"></span>
                            <span style="font-size:11px;color:#e0e0e0;width:90px">mei</span>
                            <span style="font-size:10px;color:#555;flex:1">Drafting compliance brief</span>
                            <span style="font-size:9px;color:#06b6d4" class="glow-cyan">DEEP · 2.1h</span>
                        </div>
                        <div style="display:flex;align-items:center;gap:12px;padding:10px 14px;background:#070709;border:1px solid #06b6d422;border-radius:8px">
                            <span style="width:8px;height:8px;border-radius:50%;background:#22c55e;box-shadow:0 0 8px #22c55e;flex-shrink:0"></span>
                            <span style="font-size:11px;color:#e0e0e0;width:90px">ravi</span>
                            <span style="font-size:10px;color:#555;flex:1">Deploying staging environment</span>
                            <span style="font-size:9px;color:#22c55e" class="glow-green">ACTIVE</span>
                        </div>
                        <div style="display:flex;align-items:center;gap:12px;padding:10px 14px;background:#070709;border:1px solid #1a1a1a;border-radius:8px">
                            <span style="width:8px;height:8px;border-radius:50%;background:#222;flex-shrink:0"></span>
                            <span style="font-size:11px;color:#333;width:90px">tom</span>
                            <span style="font-size:10px;color:#222;flex:1">offline</span>
                            <span style="font-size:9px;color:#222">OFFLINE</span>
                        </div>
                    </div>
                    <div style="font-size:9px;color:#06b6d4;letter-spacing:3px" class="glow-cyan">└─────────────────────────────────────────┘</div>
                    <!-- Shared context drift -->
                    <div style="background:#070709;border:1px solid #06b6d422;border-radius:8px;padding:14px">
                        <div style="font-size:9px;color:#555;letter-spacing:2px;margin-bottom:10px">CONTEXT DRIFT PER MEMBER</div>
                        <div style="display:flex;flex-direction:column;gap:6px;font-size:10px">
                            <div style="display:flex;align-items:center;gap:10px"><span style="width:50px;color:#666">priya</span><div style="flex:1;height:4px;background:#111;border-radius:2px"><div style="width:12%;height:100%;background:#22c55e;border-radius:2px"></div></div><span style="color:#22c55e;width:30px">1.2%</span></div>
                            <div style="display:flex;align-items:center;gap:10px"><span style="width:50px;color:#666">arjun</span><div style="flex:1;height:4px;background:#111;border-radius:2px"><div style="width:22%;height:100%;background:#22c55e;border-radius:2px"></div></div><span style="color:#22c55e;width:30px">2.2%</span></div>
                            <div style="display:flex;align-items:center;gap:10px"><span style="width:50px;color:#666">sam</span><div style="flex:1;height:4px;background:#111;border-radius:2px"><div style="width:58%;height:100%;background:#f59e0b;border-radius:2px"></div></div><span style="color:#f59e0b;width:30px">5.8%</span></div>
                            <div style="display:flex;align-items:center;gap:10px"><span style="width:50px;color:#666">mei</span><div style="flex:1;height:4px;background:#111;border-radius:2px"><div style="width:9%;height:100%;background:#22c55e;border-radius:2px"></div></div><span style="color:#22c55e;width:30px">0.9%</span></div>
                        </div>
                    </div>
                </div>
                <!-- Right: Shared context + decisions -->
                <div style="background:#030305;padding:18px;display:flex;flex-direction:column;gap:14px">
                    <div style="font-size:9px;color:#06b6d4;letter-spacing:3px" class="glow-cyan">┌── SHARED CONTEXT ───────────────────────┐</div>
                    <div style="background:#070709;border:1px solid #06b6d422;border-radius:8px;padding:14px;flex:1">
                        <div style="font-size:9px;color:#555;margin-bottom:10px;letter-spacing:2px">LAST 24H DECISIONS</div>
                        <div style="display:flex;flex-direction:column;gap:8px;font-size:10px">
                            <div style="display:flex;gap:10px;align-items:baseline"><span style="color:#22c55e;width:50px" class="glow-green">SHIPPED</span><span style="color:#666">priya · auth v2 merged to main</span><span style="margin-left:auto;color:#333">2h</span></div>
                            <div style="display:flex;gap:10px;align-items:baseline"><span style="color:#f59e0b;width:50px" class="glow-amber">BLOCKED</span><span style="color:#666">sam · design review needed on onboarding</span><span style="margin-left:auto;color:#333">3h</span></div>
                            <div style="display:flex;gap:10px;align-items:baseline"><span style="color:#22c55e;width:50px" class="glow-green">SHIPPED</span><span style="color:#666">ravi · staging env deployed, tests green</span><span style="margin-left:auto;color:#333">4h</span></div>
                            <div style="display:flex;gap:10px;align-items:baseline"><span style="color:#06b6d4;width:50px" class="glow-cyan">CONTEXT</span><span style="color:#666">mei · compliance brief draft ready for review</span><span style="margin-left:auto;color:#333">5h</span></div>
                            <div style="display:flex;gap:10px;align-items:baseline"><span style="color:#06b6d4;width:50px" class="glow-cyan">CONTEXT</span><span style="color:#666">arjun · p95 latency 180ms → target 120ms</span><span style="margin-left:auto;color:#333">6h</span></div>
                        </div>
                    </div>
                    <div style="font-size:9px;color:#06b6d4;letter-spacing:3px" class="glow-cyan">┌── BLOCKERS ─────────────────────────────┐</div>
                    <div style="background:#070709;border:1px solid #f59e0b22;border-radius:8px;padding:14px">
                        <div style="display:flex;flex-direction:column;gap:8px;font-size:10px">
                            <div style="display:flex;gap:10px;align-items:baseline">
                                <span style="color:#f59e0b" class="glow-amber">▸</span>
                                <span style="color:#888">sam needs design sign-off on onboarding modal</span>
                                <span style="margin-left:auto;color:#f59e0b;font-size:9px">URGENT</span>
                            </div>
                            <div style="display:flex;gap:10px;align-items:baseline">
                                <span style="color:#333">▸</span>
                                <span style="color:#555">arjun blocked on gateway creds (infra)</span>
                                <span style="margin-left:auto;color:#444;font-size:9px">LOW</span>
                            </div>
                        </div>
                    </div>
                    <div style="background:#070709;border:1px solid #06b6d422;border-radius:8px;padding:14px">
                        <div style="font-size:9px;color:#555;margin-bottom:10px;letter-spacing:2px">VELOCITY THIS WEEK</div>
                        <div style="display:flex;gap:6px;align-items:flex-end;height:50px">
                            <div style="flex:1;background:#06b6d4;border-radius:2px 2px 0 0;height:40%;opacity:0.6"></div>
                            <div style="flex:1;background:#06b6d4;border-radius:2px 2px 0 0;height:65%;opacity:0.7"></div>
                            <div style="flex:1;background:#06b6d4;border-radius:2px 2px 0 0;height:50%;opacity:0.7"></div>
                            <div style="flex:1;background:#06b6d4;border-radius:2px 2px 0 0;height:80%;opacity:0.8"></div>
                            <div style="flex:1;background:#22c55e;border-radius:2px 2px 0 0;height:95%;box-shadow:0 0 8px rgba(34,197,94,0.3)"></div>
                        </div>
                        <div style="display:flex;gap:6px;font-size:8px;color:#333;margin-top:4px">
                            <div style="flex:1;text-align:center">M</div><div style="flex:1;text-align:center">T</div><div style="flex:1;text-align:center">W</div><div style="flex:1;text-align:center">T</div><div style="flex:1;text-align:center;color:#22c55e">F</div>
                        </div>
                    </div>
                </div>
            </div>
            <div style="background:#050508;padding:6px 18px;font-size:8px;color:#1a1a1a;letter-spacing:3px;text-align:center">◇ ACTIVE MIRROR · TEAM MESH · ASYNC-FIRST · SOVEREIGN COLLABORATION ◇</div>
        </div>
        """,
    },
    "dashboard-founder.png": {
        "title": "Solo Founder — Revenue, Runway, Focus",
        "html": """
        <div class="scanlines" style="background:#03010a;color:#e0e0e0;font-family:'JetBrains Mono',monospace;padding:0;width:1280px;height:800px;display:flex;flex-direction:column;position:relative">
            <!-- Top bar -->
            <div style="background:#060309;padding:10px 18px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #ec489922">
                <div style="display:flex;gap:16px;align-items:center">
                    <span style="color:#ec4899" class="glow-magenta">◇</span>
                    <span style="font-size:11px;font-weight:600;color:#ec4899" class="glow-magenta">FOUNDER OS</span>
                    <span style="font-size:9px;color:#ec489944">│</span>
                    <span style="font-size:9px;color:#22c55e" class="glow-green">● BUILDING</span>
                    <span style="font-size:9px;color:#ec489944">│</span>
                    <span style="font-size:9px;color:#555">DAY 294 · STREAK 12</span>
                </div>
                <div style="display:flex;gap:16px;font-size:9px;color:#444">
                    <span style="color:#ec4899" class="glow-magenta">Today</span>
                    <span>Revenue</span><span>Runway</span><span>Pipeline</span>
                    <span style="margin-left:12px;color:#555">09:14 IST</span>
                </div>
            </div>
            <!-- Body -->
            <div style="flex:1;display:grid;grid-template-columns:2fr 1fr;gap:1px;background:#0a0a0a">
                <!-- Left -->
                <div style="background:#04020a;padding:20px;display:flex;flex-direction:column;gap:16px">
                    <!-- Today's one thing -->
                    <div class="border-glow-magenta" style="background:#07040f;border:1px solid #ec489933;border-radius:12px;padding:24px">
                        <div style="font-size:9px;color:#ec4899;letter-spacing:4px;margin-bottom:12px" class="glow-magenta">┌── TODAY'S ONE THING ──────────────────────┐</div>
                        <div style="font-size:22px;font-weight:300;color:#fff;line-height:1.5;padding-left:14px;border-left:2px solid #ec4899">Ship the onboarding flow.<br/>Everything else is noise.</div>
                        <div style="font-size:9px;color:#ec4899;letter-spacing:4px;margin-top:12px" class="glow-magenta">└──────────────────────────────────────────┘</div>
                        <div style="margin-top:16px;display:flex;gap:12px">
                            <div style="background:#0a0a0f;border:1px solid #1a1a1a;border-radius:8px;padding:12px 18px;text-align:center">
                                <div style="font-size:24px;font-weight:700;color:#ec4899" class="glow-magenta">3.2h</div>
                                <div style="font-size:8px;color:#444;text-transform:uppercase;letter-spacing:2px;margin-top:4px">deep work today</div>
                            </div>
                            <div style="background:#0a0a0f;border:1px solid #1a1a1a;border-radius:8px;padding:12px 18px;text-align:center">
                                <div style="font-size:24px;font-weight:700;color:#22c55e" class="glow-green">0.8%</div>
                                <div style="font-size:8px;color:#444;text-transform:uppercase;letter-spacing:2px;margin-top:4px">drift</div>
                            </div>
                            <div style="background:#0a0a0f;border:1px solid #1a1a1a;border-radius:8px;padding:12px 18px;text-align:center">
                                <div style="font-size:24px;font-weight:700;color:#f59e0b" class="glow-amber">HIGH</div>
                                <div style="font-size:8px;color:#444;text-transform:uppercase;letter-spacing:2px;margin-top:4px">momentum</div>
                            </div>
                        </div>
                    </div>
                    <!-- Key metrics -->
                    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px">
                        <div style="background:#07040f;border:1px solid #ec489922;border-radius:10px;padding:16px">
                            <div style="font-size:9px;color:#555;letter-spacing:2px;margin-bottom:8px">MRR</div>
                            <div style="font-size:28px;font-weight:700;color:#22c55e" class="glow-green">$4.2k</div>
                            <div style="font-size:9px;color:#22c55e;margin-top:4px">↑ +$800 this month</div>
                        </div>
                        <div style="background:#07040f;border:1px solid #ec489922;border-radius:10px;padding:16px">
                            <div style="font-size:9px;color:#555;letter-spacing:2px;margin-bottom:8px">RUNWAY</div>
                            <div style="font-size:28px;font-weight:700;color:#f59e0b" class="glow-amber">14mo</div>
                            <div style="font-size:9px;color:#555;margin-top:4px">burn $3.1k/mo</div>
                        </div>
                        <div style="background:#07040f;border:1px solid #ec489922;border-radius:10px;padding:16px">
                            <div style="font-size:9px;color:#555;letter-spacing:2px;margin-bottom:8px">PIPELINE</div>
                            <div style="font-size:28px;font-weight:700;color:#06b6d4" class="glow-cyan">$28k</div>
                            <div style="font-size:9px;color:#555;margin-top:4px">6 prospects active</div>
                        </div>
                    </div>
                    <!-- Revenue sparkline -->
                    <div style="background:#07040f;border:1px solid #ec489922;border-radius:10px;padding:16px">
                        <div style="font-size:9px;color:#555;letter-spacing:2px;margin-bottom:12px">MRR TRAJECTORY · 6 MONTHS</div>
                        <div style="display:flex;gap:4px;align-items:flex-end;height:60px">
                            <div style="flex:1;background:#ec489933;border-radius:2px 2px 0 0;height:30%"></div>
                            <div style="flex:1;background:#ec489944;border-radius:2px 2px 0 0;height:40%"></div>
                            <div style="flex:1;background:#ec489955;border-radius:2px 2px 0 0;height:52%"></div>
                            <div style="flex:1;background:#ec489966;border-radius:2px 2px 0 0;height:63%"></div>
                            <div style="flex:1;background:#ec489977;border-radius:2px 2px 0 0;height:78%"></div>
                            <div style="flex:1;background:#ec4899;border-radius:2px 2px 0 0;height:100%;box-shadow:0 0 12px rgba(236,72,153,0.4)"></div>
                        </div>
                        <div style="display:flex;gap:4px;font-size:8px;color:#333;margin-top:4px">
                            <div style="flex:1;text-align:center">Sep</div><div style="flex:1;text-align:center">Oct</div><div style="flex:1;text-align:center">Nov</div><div style="flex:1;text-align:center">Dec</div><div style="flex:1;text-align:center">Jan</div><div style="flex:1;text-align:center;color:#ec4899">Feb</div>
                        </div>
                    </div>
                </div>
                <!-- Right sidebar -->
                <div style="background:#04020a;padding:18px;display:flex;flex-direction:column;gap:14px">
                    <div style="font-size:9px;color:#ec4899;letter-spacing:3px" class="glow-magenta">┌── PIPELINE ─────────────┐</div>
                    <div style="display:flex;flex-direction:column;gap:8px;font-size:10px">
                        <div style="padding:10px 12px;background:#07040f;border:1px solid #22c55e33;border-radius:8px">
                            <div style="color:#22c55e;font-size:9px" class="glow-green">CLOSING · $8k</div>
                            <div style="color:#888;margin-top:3px">Acme Corp — contract sent</div>
                        </div>
                        <div style="padding:10px 12px;background:#07040f;border:1px solid #06b6d422;border-radius:8px">
                            <div style="color:#06b6d4;font-size:9px" class="glow-cyan">DEMO · $5k</div>
                            <div style="color:#888;margin-top:3px">Bright Labs — call Thu</div>
                        </div>
                        <div style="padding:10px 12px;background:#07040f;border:1px solid #ec489922;border-radius:8px">
                            <div style="color:#ec4899;font-size:9px" class="glow-magenta">NURTURE · $15k</div>
                            <div style="color:#888;margin-top:3px">4 prospects in sequence</div>
                        </div>
                    </div>
                    <div style="font-size:9px;color:#ec4899;letter-spacing:3px" class="glow-magenta">┌── ENERGY ───────────────┐</div>
                    <div style="background:#07040f;border:1px solid #ec489922;border-radius:8px;padding:14px">
                        <div style="font-size:9px;color:#555;margin-bottom:10px">TODAY'S CAPACITY</div>
                        <div style="display:flex;gap:3px;margin-bottom:6px">
                            <div style="flex:1;height:10px;background:#ec4899;border-radius:2px;box-shadow:0 0 6px rgba(236,72,153,0.3)"></div>
                            <div style="flex:1;height:10px;background:#ec4899;border-radius:2px;box-shadow:0 0 6px rgba(236,72,153,0.3)"></div>
                            <div style="flex:1;height:10px;background:#ec4899;border-radius:2px;box-shadow:0 0 6px rgba(236,72,153,0.3)"></div>
                            <div style="flex:1;height:10px;background:#ec4899;border-radius:2px;box-shadow:0 0 6px rgba(236,72,153,0.3)"></div>
                            <div style="flex:1;height:10px;background:#111;border:1px solid #1a1a1a;border-radius:2px"></div>
                        </div>
                        <div style="font-size:9px;color:#ec4899" class="glow-magenta">FULL · SHIP SOMETHING</div>
                    </div>
                    <div style="background:#07040f;border:1px solid #ec489922;border-radius:8px;padding:14px;flex:1">
                        <div style="font-size:9px;color:#555;margin-bottom:10px;letter-spacing:2px">RECENT SHIPS</div>
                        <div style="display:flex;flex-direction:column;gap:6px;font-size:9px;color:#555">
                            <div>✓ Landing page v3</div>
                            <div>✓ Payment integration</div>
                            <div>✓ Email sequences</div>
                            <div>✓ Analytics dashboard</div>
                            <div style="color:#333">○ Onboarding flow</div>
                        </div>
                    </div>
                </div>
            </div>
            <div style="background:#060309;padding:6px 18px;font-size:8px;color:#1a1a1a;letter-spacing:3px;text-align:center">◇ ACTIVE MIRROR · FOUNDER OS · REVENUE-FIRST · SOVEREIGN MOMENTUM ◇</div>
        </div>
        """,
    },
}


async def render_mockups(targets=None):
    from playwright.async_api import async_playwright

    to_render = {k: v for k, v in MOCKUPS.items() if targets is None or any(t in k for t in targets)}

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 800})

        for filename, mockup in to_render.items():
            html = f"""<!DOCTYPE html>
            <html><head>
            <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&display=swap" rel="stylesheet">
            <style>{SHARED_CSS}</style>
            </head><body>{mockup['html']}</body></html>"""

            await page.set_content(html)
            await page.wait_for_load_state("networkidle")
            output = OUTPUT_DIR / filename
            await page.screenshot(path=str(output))
            print(f"Rendered: {output} ({output.stat().st_size // 1024}KB)")

        await browser.close()
    print(f"Done — {len(to_render)} mockup(s) rendered.")


if __name__ == "__main__":
    import sys
    targets = sys.argv[1:] if len(sys.argv) > 1 else None
    if targets is None:
        print(f"Available: {', '.join(k.replace('.png','') for k in MOCKUPS)}")
        print("Rendering all...")
    asyncio.run(render_mockups(targets))
