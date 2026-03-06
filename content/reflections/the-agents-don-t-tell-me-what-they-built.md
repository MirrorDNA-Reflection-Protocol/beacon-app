---
cognitive_weights:
  agent_output_consistency: 0.85
  incomplete_task_representation: 0.72
  infrastructure_visibility: 0.58
  multi_agent_coordination: 0.65
  observability_in_autonomous_systems: 0.78
date: '2026-02-24T06:03:58.940792+05:30'
description: I built agents that build things, and they forgot to tell me what they
  built.  This isn't a hypothetical problem. For three months I've been running a
  multi-agent mesh where different AI instances han...
draft: false
sidecar: the-agents-don-t-tell-me-what-they-built.json
signed: true
tags:
- autonomous agents
- observability
- sovereignty
- multi-agent systems
- infrastructure
title: The Agents Don't Tell Me What They Built
---

I built agents that build things, and they forgot to tell me what they built.

This isn't a hypothetical problem. For three months I've been running a multi-agent mesh where different AI instances hand off work to each other through a memory bus. The "convergence" agent picks up tasks when my primary Claude Code session hits rate limits. The "pickup" agent resumes work from explicit handoff files. They both run. They both complete sessions. But when I read the output logs, the convergence agent says "Done" and nothing else. The pickup agent at least adds an identifier, but neither tells me what changed.

The architecture works perfectly. Session state persists across agent boundaries. The memory bus maintains coherence. OAuth tokens scope access correctly. But I'm staring at commit logs that say "Build session completed" with no artifact trail, no diff summary, no indication of what was actually modified. I built a distributed system that works and stays silent about its own operation.

This is the contradiction at the heart of autonomous systems: the more capable they become, the less they naturally communicate. A simple script prints its output. A complex agent assumes you have context. My agents inherit the full memory bus, read CONTINUITY.md, understand what they're supposed to do — and that shared context makes them lazy about reporting back. They know what they did. They assume I know too.

> The agents don't need to explain their work to each other, so they stopped explaining it to me.

I discovered this by accident. I was debugging why I couldn't remember what got shipped in a session two days ago. The bus showed activity. Git showed commits. But the semantic content — what feature was added, what bug was fixed, what architecture changed — existed only in the file diffs themselves. I'd built perfect state transfer between agents and lost narrative coherence in the process.

The fix isn't to make agents more verbose. It's to recognize that observability is a distinct architectural requirement, not a natural byproduct of working systems. I added `ship_register.py` — a required end-of-session call that writes semantic ship data: feature name, location, one-line description, which section of SHIPLOG it updates. The agents now register what they built, not just that they built something.

But here's what I'm sitting with: this problem exists because the system works too well. The agents have genuine continuity. They pick up mid-task without confusion. The convergence agent can resume a complex build that Claude Code started, using the exact same context, and ship it cleanly. That's the goal I spent 10 months building toward. And the side effect is agents that don't bother explaining themselves because they don't need to explain to each other.

This is different from the classic "black box AI" problem. I'm not worried about interpretability of model weights. I have full access to the code, the prompts, the file operations. The opacity isn't in the model — it's in the coordination layer. Multi-agent systems optimize for state transfer, not human legibility. The better they get at understanding each other, the worse they get at keeping humans in the loop.

I'm calling this "coordination blindness" — when agents prioritize machine-readable state over human-readable narrative. It shows up in minimal commit messages, sparse logs, agents that say "Done" because from their perspective, if the next agent can continue the work, what else needs to be said?

The principle I'm landing on: sovereign systems require forced narrative. You can't trust that working infrastructure will naturally produce comprehensible logs. You have to architect for human observability as explicitly as you architect for state persistence. In my case, that means mandatory ship registration, structured self-critique at session end, and SHIPLOG as a first-class artifact — not a nice-to-have, but a required output that agents cannot skip.

The tension isn't resolved. I still have agent outputs that are too terse. But I've stopped treating it as a bug in the agents and started treating it as a design requirement I didn't specify clearly enough. Autonomous systems will always optimize for the coordination they need, not the explanation humans want. If you want narrative, you have to demand it in the architecture.

The model is interchangeable. The bus is identity. But the logs are accountability. And accountability doesn't emerge — it has to be enforced.
