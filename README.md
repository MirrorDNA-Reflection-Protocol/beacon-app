# Truth-First Beacon

Sovereign, static-first publishing system. Content synthesized locally, signed cryptographically, pinned permanently.

## Architecture

```
┌─────────────────────────────────────────────────┐
│  EDGE (OnePlus 15 / Ray-Ban Meta)               │
│  ↓ Raw voice memos, cognitive shards            │
│  ↓ Sync via Tailscale/SSH (no clouds)           │
├─────────────────────────────────────────────────┤
│  CORE (Mac Mini M4)                             │
│  ┌─── Synthesis Engine ───────────────────┐     │
│  │ 1. REFLECT — analyze vault fragments   │     │
│  │ 2. DISSONANCE — check contradictions   │     │
│  │ 3. SYNTHESIZE — write in voice         │     │
│  └────────────────────────────────────────┘     │
│  ┌─── Hugo Static Site ──────────────────┐      │
│  │ Dark, minimalist, polymathic           │      │
│  │ PGP-signed posts + JSON-LD             │      │
│  │ Cognitive sidecars with embeddings     │      │
│  └────────────────────────────────────────┘      │
│  ↓ Publish: Build → Sign → IPFS Pin             │
├─────────────────────────────────────────────────┤
│  BEACON (Public)                                │
│  Static HTML + .well-known/ai-instructions.txt  │
│  Semantic sidecars for future AI discovery      │
│  IPFS CID for permanent availability            │
└─────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Dev server
hugo server --buildDrafts

# Run synthesis
cd engine && python synthesize.py --dry-run

# Extract voice DNA
cd engine && python voice_dna.py

# Generate sidecars
cd engine && python sidecar_gen.py

# Publish
./scripts/publish.sh

# Generate private alignment capsule (all-AI sync context)
./scripts/daily_alignment.py
```

## The 2050 Test

Every component passes: Hugo produces zero-dependency HTML. IPFS survives domain expiration. PGP proves authorship. Semantic sidecars enable future AI discovery.

## Daily AI Alignment Capsule

Private local context is generated daily to:

- Keep different AI copilots aligned to the same current state
- Track daily accomplishments from repo activity
- Surface open loops (dirty repos) and running sovereign services

Outputs:

- `/Users/mirror-admin/MirrorDNA-Vault/00_CANONICAL/AI_ALIGNMENT_CAPSULES/YYYY-MM-DD.md`
- `/Users/mirror-admin/MirrorDNA-Vault/00_CANONICAL/AI_ALIGNMENT_LATEST.md`

Scheduler template:

- `/Users/mirror-admin/repos/truth-first-beacon/scripts/com.pauldesai.alignment.daily.plist` (09:00 local)

⟡ Truth > Fluency
