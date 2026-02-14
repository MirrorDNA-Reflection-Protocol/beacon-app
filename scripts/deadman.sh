#!/usr/bin/env bash
# Truth-First Beacon — Dead Man's Protocol
# Monitors the "pulse" and triggers legacy export if stale for 30 days.

PULSE_FILE="/Users/mirror-admin/repos/truth-first-beacon/.last_pulse"
THRESHOLD_DAYS=30
VAULT_PATH="/Users/mirror-admin/MirrorDNA-Vault"
EXPORT_DIR="/Users/mirror-admin/.mirrordna/sandbox/ag/legacy_export"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
EXPORT_PATH="$EXPORT_DIR/vault_legacy_$TIMESTAMP.parquet"

mkdir -p "$EXPORT_DIR"

if [ ! -f "$PULSE_FILE" ]; then
    echo "⚠ Pulse file not found. Creating one now."
    date -Iseconds > "$PULSE_FILE"
    exit 0
fi

LAST_PULSE=$(cat "$PULSE_FILE")
LAST_PULSE_TS=$(date -j -f "%Y-%m-%dT%H:%M:%S%z" "$LAST_PULSE" +%s)
CURRENT_TS=$(date +%s)
DIFF_SECONDS=$((CURRENT_TS - LAST_PULSE_TS))
THRESHOLD_SECONDS=$((THRESHOLD_DAYS * 86400))

if [ $DIFF_SECONDS -gt $THRESHOLD_SECONDS ]; then
    echo "🚨 DEAD MAN'S PROTOCOL TRIGGERED"
    echo "   Last pulse: $LAST_PULSE"
    echo "   Staleness: $((DIFF_SECONDS / 86400)) days"
    
    echo "→ Running Legacy Export..."
    # Ensure pandas is available
    pip3 install pandas pyarrow --quiet
    
    python3 /Users/mirror-admin/repos/truth-first-beacon/scripts/legacy_export.py "$VAULT_PATH" "$EXPORT_PATH"
    
    if command -v ipfs &>/dev/null; then
        echo "→ Broadcasting to IPFS..."
        CID=$(ipfs add -Q "$EXPORT_PATH")
        echo "   Legacy CID: $CID"
    fi
    
    echo "⟡ Protocol Complete."
else
    echo "⟡ Heartbeat detected. $(( (THRESHOLD_SECONDS - DIFF_SECONDS) / 3600 )) hours until next threshold."
fi
