---
title: "The Fallback Chain: Provider-Agnostic Tool Routing for AI Agents"
date: '2026-02-28T14:55:00+05:30'
description: 'OpenCode issue #10704 asks for provider-hosted web search. I built this six months ago. Here is the pattern.'
tags:
- agentic-systems
- tool-routing
- provider-agnostic
- mirrordna
- engineering
signed: true
cognitive_weights:
  agentic_architecture: 0.90
  tool_routing_patterns: 0.88
  open_source_contribution: 0.72
  building_in_public: 0.70
draft: false
---

[OpenCode issue #10704](https://github.com/anomalyco/opencode/issues/10704) landed this week: *"Use provider-hosted web search when available."*

The request is specific and correct. Web search in most AI agents today is hardcoded: Exa integration, custom flag, API key. Even when the provider — Claude, OpenAI, Gemini — already ships a native search tool. The developer pays for Exa, configures the key, and gets worse results than what the provider offers natively, because the provider's search is model-native, not bolted on.

The fix is a fallback chain. I built one six months ago for MirrorDNA. Here is the pattern.

---

## The Problem, Precisely

Three tools exist for web search in AI agent contexts:

1. **Provider-native** — `web_search` (Claude), `webSearchPreview` (OpenAI), Grounding (Gemini). Built into the model's tool call spec. No additional key. Model-native quality.
2. **External search API** — Exa, Serper, Brave Search. Requires separate credentials. Works across any provider.
3. **Fetch fallback** — webfetch a URL directly. No search. Works when you have a URL, not a query.

Current state of most agents: they pick one and hardcode it. OpenCode defaults to Exa + webfetch. This means you always pay for Exa even when you're using Claude, which already has `web_search` built in.

What the issue asks for is obvious once you see it: detect what the provider supports, use the best available option, fall back gracefully.

---

## The Fallback Chain

```python
PROVIDER_NATIVE_SEARCH = {
    "anthropic": "web_search",
    "openai": "web_search_preview",
    "google": "google_search",
}

async def search(query: str, provider: str, model: str) -> SearchResult:
    # Tier 1: Provider-native (free with your API key, model-native quality)
    if native_tool := PROVIDER_NATIVE_SEARCH.get(provider):
        if await provider_supports_tool(provider, model, native_tool):
            return await call_native_tool(native_tool, query)

    # Tier 2: External search API (requires key, works across any provider)
    if exa_key := os.getenv("EXA_API_KEY"):
        return await exa_search(query, exa_key)

    # Tier 3: Fetch fallback (no search, best-effort URL retrieval)
    url = construct_search_url(query)
    return await webfetch(url)
```

Three lines of decision logic. The rest is implementation.

---

## The Part That Bites You: Capability Detection

`provider_supports_tool()` is where this gets real. You cannot assume a model supports a tool just because the provider offers it. `claude-3-haiku` does not have web search. `gpt-4o` has `webSearchPreview` but `gpt-3.5-turbo` does not. Grounding on Gemini is tier-gated.

You need a capability map — not from memory, from the provider's API. The right approach:

```python
async def provider_supports_tool(provider: str, model: str, tool: str) -> bool:
    # Check local cache first (refresh every 24h)
    if cached := capability_cache.get(f"{provider}/{model}/{tool}"):
        return cached

    # Query provider capability endpoint
    caps = await fetch_model_capabilities(provider, model)
    result = tool in caps.get("supported_tools", [])

    capability_cache.set(f"{provider}/{model}/{tool}", result, ttl=86400)
    return result
```

Cache it. Provider capability endpoints are slow and rate-limited. You don't want a capability check on every tool call.

---

## What This Unlocks

Once you have the fallback chain, a few things become possible that weren't before:

**Budget routing** — native search is included in your API cost. External search adds $0.01–0.05 per query. If you're running high-volume agents, the routing decision is also a cost decision. The chain makes this explicit.

**Quality tiering** — in my system, I route different tasks to different tiers. Research tasks hit native search (higher quality, model-native). Monitoring tasks hit external search (predictable, auditable). Fallback is last resort only.

**Provider switching without reconfiguration** — if you switch from Claude to OpenAI mid-session, the chain resolves the right tool automatically. No configuration change. No code change.

---

## What I Run in Production

MirrorDNA is a sovereign AI operating system I've been building for ten months. It runs across a Mac Mini M4, a Pixel 9 Pro XL, and a OnePlus 15, coordinated via a governance layer called MirrorGate.

MirrorGate handles all tool dispatch — including search — through a six-stage enforcement pipeline. The fallback chain is embedded at the tool resolution layer. Every agent call goes through it: Claude Code, a local Qwen model in Termux on the Pixel, Gemini, all of them. Same contract, different resolution.

The pattern works. It has been running without a search configuration failure in six months.

---

## For the OpenCode Contributors

The implementation in Go would look structurally the same. The capability map and cache are the first piece. The tiered resolution is the second. The Exa integration stays as Tier 2 — it becomes the default for providers that don't have native search, rather than the default for everything.

If this is useful, I'm reachable. The pattern is not proprietary. The full system around it is, but the routing logic is just engineering.

---

*MirrorDNA is a sovereign AI operating system. beacon.activemirror.ai is where I publish what I learn building it.*
