---
title: Systems That Heal Themselves
date: '2026-02-14T13:00:00+05:30'
description: 'Monitoring tells you something broke. Self-healing fixes it before you notice. I built a system that uses a local LLM to diagnose its own failures.'
tags:
- self-healing
- infrastructure
- resilience
- autonomous-systems
signed: false
cognitive_weights:
  infrastructure_resilience: 0.90
  autonomous_remediation: 0.82
  llm_as_diagnostician: 0.75
  system_design: 0.68
draft: false
---

Monitoring tells you something broke. Self-healing fixes it before you notice.

I got tired of waking up to dead services. Not catastrophic failures — the annoying kind. Ollama OOM'd at 3am and didn't restart. A LaunchAgent lost its environment variable after a macOS update. A log file grew to 2GB because something was chatty. Small things that compound into a morning spent debugging instead of building.

So I built a system that checks everything every five minutes and fixes what it can.

> The best infrastructure is the kind you forget exists because it never breaks.

The monitor checks five services, four LaunchAgents, seven critical files, every log for error spikes, disk space, Ollama model availability, and the freshness of the continuity file. Each check has a criticality flag. Core services like Ollama and the cloudflare tunnel are critical — if they're down, the system is degraded. Optional services like the cognitive dashboard are noted but don't trigger alerts.

When something is wrong, it tries to fix it first. Ollama down? Restart it. LaunchAgent not loaded? Reload it. Missing directory? Create it. Only after attempting remediation does it log the issue. Most of the time, by the time I look at the health report, the problem has already been resolved.

The part that surprised me was how useful an LLM is for diagnosis. After collecting all the issues, the monitor sends the critical ones to a local model — Qwen 2.5 running on Ollama — and asks for a diagnosis. Not a fix. A diagnosis. "Here are the symptoms. What's the likely root cause? What should the operator check?"

The LLM's diagnosis isn't always right. But it's right often enough to save fifteen minutes of investigation. When three services failed simultaneously last week, the LLM correctly identified that they all depended on a PATH variable that had been clobbered by a shell config change. I would have found that eventually. The LLM found it in two seconds.

This only works because the LLM runs locally. The health of my infrastructure isn't something I want to send to a cloud API. The diagnosis happens on the same machine that's being diagnosed, using a model that's always available, with zero network dependency. If the internet is down, the self-healer still runs. It just can't fix the tunnel.

The architecture is deliberately simple. A Python script. A LaunchAgent that triggers it every 300 seconds. A JSON output that persists to disk. A bus alert if something is critical. No framework. No container orchestration. No Kubernetes. Just a script that checks things and fixes what it can.

I've seen infrastructure teams spend months building observability platforms with Grafana dashboards, PagerDuty integrations, and runbook automation. For a sovereign single-operator stack, that's over-engineering on an absurd scale. I need to know if things are broken and I need them fixed. A 400-line Python script does both.

The self-heal monitor now catches things I used to miss for days. A log file with 50+ errors per hour that indicates a retry loop. A LaunchAgent that's loaded but whose process actually died. A model that was pulled from Ollama's registry but never replaced. These aren't emergencies. They're the slow decay that eventually becomes one.

The design philosophy is fail-open. If the monitor itself crashes, nothing else is affected. If the LLM diagnosis fails, the raw issues are still logged. If a remediation attempt fails, it's logged and I get the alert. The system never makes things worse by trying to make them better.

Three design decisions that matter:

First, the monitor distinguishes between critical and optional services. Early versions triggered false alarms because the cognitive dashboard being slow isn't the same kind of problem as Ollama being dead. Severity classification is half the battle.

Second, the LLM diagnosis only gets critical issues. Feeding it fifty warnings about log verbosity overwhelms the context and produces useless output. Filter first, then diagnose.

Third, remediation attempts are idempotent. Restarting an already-running service is harmless. Reloading an already-loaded LaunchAgent is harmless. Creating an already-existing directory is harmless. Every fix action can run repeatedly without side effects.

The system healed itself fourteen times last week. I noticed zero of those incidents in real time. That's the point.

**Closing principle:** Don't just monitor your systems — teach them to fix themselves. The gap between observability and remediation is where operational pain lives. Close it with automation, close it with local LLMs, close it with scripts that run every five minutes and fix what they find. Perfect infrastructure isn't infrastructure that never breaks. It's infrastructure that breaks and heals before you notice.
