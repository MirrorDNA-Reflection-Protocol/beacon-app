#!/usr/bin/env bash
# Truth-First Beacon — Publish Pipeline
# Build → Sign → Pin → Deploy
set -euo pipefail

BEACON_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PUBLIC_DIR="$BEACON_DIR/public"
DEPLOY_LOG="$BEACON_DIR/deploy.log"
GPG_KEY="${GPG_KEY:-paul@n1.agency}"
STRICT_SIGNING="${STRICT_SIGNING:-0}"
STRICT_IPFS="${STRICT_IPFS:-0}"
REQUIRE_SIGN_AND_PIN="${REQUIRE_SIGN_AND_PIN:-0}"

if [ "$REQUIRE_SIGN_AND_PIN" = "1" ]; then
    STRICT_SIGNING=1
    STRICT_IPFS=1
fi

echo "⟡ Truth-First Beacon — Publish"
echo "  Dir: $BEACON_DIR"
echo ""

# Step 1: Hugo Build
echo "→ Building site..."
cd "$BEACON_DIR"
hugo --minify
echo "  ✓ Hugo build complete"

# Step 2: Hash the build
echo "→ Computing content hash..."
CONTENT_HASH=$(find "$PUBLIC_DIR" -type f -exec shasum -a 256 {} + | sort | shasum -a 256 | cut -d' ' -f1)
echo "  Hash: $CONTENT_HASH"

# Step 3: PGP Sign
if command -v gpg &>/dev/null; then
    echo "→ Signing build..."
    if echo "$CONTENT_HASH" | gpg --clearsign --armor --local-user "$GPG_KEY" > "$PUBLIC_DIR/build-signature.asc" 2>/dev/null; then
        echo "  ✓ Signed with key: $GPG_KEY"
    else
        if [ "$STRICT_SIGNING" = "1" ]; then
            echo "  ✗ GPG signing failed and STRICT_SIGNING=1"
            exit 1
        fi
        echo "  ⚠ GPG signing failed (check keyring)"
    fi
else
    if [ "$STRICT_SIGNING" = "1" ]; then
        echo "  ✗ GPG not available and STRICT_SIGNING=1"
        exit 1
    fi
    echo "  ⚠ GPG not available, skipping signing"
fi

# Step 4: IPFS Pin
if command -v ipfs &>/dev/null; then
    echo "→ Pinning to IPFS..."
    if CID=$(ipfs add -r -Q --pin "$PUBLIC_DIR" 2>/dev/null); then
        echo "  CID: $CID"
        echo "$(date -Iseconds) | CID: $CID | Hash: $CONTENT_HASH" >> "$DEPLOY_LOG"
    else
        if [ "$STRICT_IPFS" = "1" ]; then
            echo "  ✗ IPFS pin failed and STRICT_IPFS=1"
            exit 1
        fi
        echo "  ⚠ IPFS pin failed, continuing local-only"
        echo "$(date -Iseconds) | LOCAL_ONLY(pin_failed) | Hash: $CONTENT_HASH" >> "$DEPLOY_LOG"
    fi
else
    if [ "$STRICT_IPFS" = "1" ]; then
        echo "  ✗ IPFS not available and STRICT_IPFS=1"
        exit 1
    fi
    echo "  ⚠ IPFS not available, skipping pin"
    echo "$(date -Iseconds) | LOCAL_ONLY | Hash: $CONTENT_HASH" >> "$DEPLOY_LOG"
fi

# Step 5: Record pulse (for Dead Man's Protocol)
PULSE_FILE="$BEACON_DIR/.last_pulse"
date -Iseconds > "$PULSE_FILE"
echo ""
echo "⟡ Publish complete"
echo "  Hash: $CONTENT_HASH"
echo "  Pulse: $(cat "$PULSE_FILE")"
[ -n "${CID:-}" ] && echo "  IPFS: $CID"
