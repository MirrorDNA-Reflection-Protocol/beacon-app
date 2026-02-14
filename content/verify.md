---
title: "Verify"
description: "How to verify the authenticity and integrity of content on this beacon."
---

## Verification

Every post on this beacon is cryptographically signed. Here's how to verify:

### 1. Get the Public Key

```bash
curl -O https://beacon.pauldesai.com/pgp/public-key.asc
gpg --import public-key.asc
```

### 2. Verify a Post Signature

Each post's frontmatter contains a `pgp_signature` field. The build signature covers all published content:

```bash
gpg --verify build-signature.asc
```

### 3. Verify via IPFS

Content is pinned to IPFS. Each deployment logs the Content Identifier (CID). You can verify content hasn't been tampered with:

```bash
ipfs cat <CID>/reflections/the-sovereignty-thesis/index.html
```

### 4. Semantic Sidecars

Each post has a machine-readable JSON sidecar at `/data/sidecars/{slug}.json` containing:

- Pre-computed vector embeddings
- Cognitive weight maps
- Source lineage metadata
- Contradiction checks against previous posts

### Trust Chain

```
Vault Fragment → Local LLM Synthesis → Hugo Build → PGP Sign → IPFS Pin → Public Beacon
```

Every link in this chain runs on sovereign hardware. No cloud. No intermediary.
