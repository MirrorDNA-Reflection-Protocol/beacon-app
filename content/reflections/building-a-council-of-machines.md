---
title: Building a Council of Machines
date: '2026-02-14T14:00:00+05:30'
description: 'One AI is an assistant. Multiple AIs with governance, identity, and fallback routing — that is a council. I built one that runs on a Mac Mini.'
tags:
- multi-agent
- orchestration
- governance
- sovereign-infrastructure
signed: true
cognitive_weights:
  multi_agent_orchestration: 0.88
  governance_architecture: 0.82
  model_routing: 0.75
  autonomous_systems: 0.70
draft: false
---

One AI is an assistant. Multiple AIs with governance, identity, and fallback routing — that's a council. I built one that runs on a Mac Mini.

The setup: Claude Opus handles complex reasoning and architecture decisions. Claude Sonnet handles routine execution. Gemini does broad analysis and fast iteration. Groq runs Llama at absurd speed for parallelizable tasks. DeepSeek and Mistral handle specialized workloads. Eleven Ollama models run locally for anything that should never leave the machine.

They don't know about each other. They don't need to. The orchestration layer handles routing, the governance layer handles permissions, and the bus handles continuity. Each model thinks it's the only one. The council doesn't require consensus — it requires coordination.

> A council isn't about agreement. It's about routing the right question to the right mind.

Here's how a real task flows. I describe what I want to the swarm conductor. It decomposes the work into a DAG — directed acyclic graph — resolving dependencies, assigning models based on complexity and sensitivity. Low-risk audit? Groq at 500 tokens per second. Architecture decision? Claude Opus with full context. Local benchmark? Ollama, never leaving the machine. The conductor spawns agents in parallel batches, watches for completion, chains outputs between dependent tasks, and synthesizes results.

Five agents completed a full infrastructure audit in under twenty seconds for thirteen cents. Not because any single model is cheap — because the routing is precise.

The governance layer is where this stops being a toy. MirrorBalance evaluates every task before it spawns. ALLOW means proceed. BLOCK means skip — the task is too sensitive for that model or that moment. There's a delegation mode with a dead man's switch: if I'm unavailable and the system detects it, autonomy degrades gracefully. Routine tasks continue. Sensitive decisions queue for my return.

I didn't build this because I don't trust AI. I built it because I trust AI enough to give it real work, and real work requires real governance. The same way a good engineering organization has code review, deployment gates, and rollback procedures — not because engineers are untrustworthy, but because good systems account for failure.

The identity layer gives each agent a glyph. Claude gets the diamond: `⟡`. Gemini gets the triangle: `△`. Codex gets the grid: `⧉`. When the council produces output, you can see who contributed what. Not for attribution theater — for debugging. When something goes wrong, I need to know which model said what, in what context, with what information. Traceability isn't surveillance. It's engineering.

The fallback chain is the part I'm proudest of. Claude hits rate limits — it happens, I push hard. When it does, the system doesn't stop. Gemini picks up the thread through an MCP server that shares the continuity state. If Gemini is unavailable, local models handle what they can. If everything remote is down, Ollama keeps the lights on. I've never had a zero-capability moment. Not once in ten months.

The council auto-routes through an MCP sync server. Any agent that boots calls `sync_boot`, gets the current state, registers itself in the agent registry. When it finishes, it calls `sync_commit`, writes its results to the bus, and the next agent can see what happened. The protocol is the coordinator, not any single model.

Most multi-agent frameworks I've seen are demos. Six agents with cute names role-playing a software team. They produce impressive-looking output for simple tasks and fall apart for real work. The difference is governance. Without permission boundaries, without sensitivity routing, without fallback chains, without a dead man's switch — you have a parlor trick, not infrastructure.

There's a moment when you're watching the terminal — six windows tiled across a 32-inch monitor, each running a different model on a different task, results chaining between them, the dashboard updating in real time — when you realize this isn't an AI product. It's an operating system. One that happens to have language models as its execution layer instead of compiled binaries.

That's the council. Not a chatbot. Not an assistant. A sovereign coordination layer that turns models into infrastructure.

**Closing principle:** The future of AI isn't one model doing everything. It's many models doing precise things, governed by protocols that outlast any individual model. Build the protocol first. The models will come and go.
