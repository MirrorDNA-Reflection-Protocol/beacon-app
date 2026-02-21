#!/bin/bash
# Beacon Daily Synthesis — Generates 1 post per run via the 3-stage pipeline
# Called by LaunchAgent at 06:00 and 18:00
set -euo pipefail

BEACON_DIR="$HOME/repos/truth-first-beacon"
ENGINE_DIR="$BEACON_DIR/engine"
LOG="$HOME/.mirrordna/sandbox/ag/beacon_synthesis.log"

notify_failure() {
    local msg="$1"
    echo "$(date -Iseconds) — FAIL: $msg" >> "$LOG"
    osascript -e "display notification \"$msg\" with title \"⟡ Beacon\" subtitle \"Synthesis Failed\"" 2>/dev/null || true
}

echo "$(date -Iseconds) — Beacon synthesis starting" >> "$LOG"

# Load API keys
source "$HOME/.mirrordna/secrets.env" 2>/dev/null || true

# Check Ollama is up (stages 1-2 need it)
if ! curl -sf http://localhost:11434/api/tags > /dev/null 2>&1; then
    notify_failure "Ollama not running"
    exit 1
fi

# Run synthesis (14 day window for variety)
cd "$ENGINE_DIR"
if ! python3 synthesize.py --days 14 >> "$LOG" 2>&1; then
    notify_failure "Synthesis pipeline failed"
    exit 1
fi

# Find the newest post (just created)
NEWEST=$(ls -t "$BEACON_DIR/content/reflections/"*.md | grep -v _index | head -1)
if [ -z "$NEWEST" ]; then
    notify_failure "No post generated"
    exit 1
fi

# Sign and publish it
sed -i '' 's/signed: false/signed: true/' "$NEWEST"
sed -i '' 's/draft: true/draft: false/' "$NEWEST"

# Rebuild Hugo
cd "$BEACON_DIR"
if ! hugo --minify >> "$LOG" 2>&1; then
    notify_failure "Hugo build failed"
    exit 1
fi

echo "$(date -Iseconds) — Published: $(basename $NEWEST)" >> "$LOG"
osascript -e "display notification \"Published: $(basename $NEWEST)\" with title \"⟡ Beacon\" subtitle \"New Post\"" 2>/dev/null || true
