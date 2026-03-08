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

# Load API keys (set -a exports all vars so python child process can see them)
set -a
source "$HOME/.mirrordna/secrets.env" 2>/dev/null || true
set +a

# Check Ollama is up (stages 1-2 need it)
if ! curl -sf http://localhost:11434/api/tags > /dev/null 2>&1; then
    notify_failure "Ollama not running"
    exit 1
fi

# Run synthesis (14 day window for variety)
cd "$ENGINE_DIR"
if ! /usr/bin/python3 synthesize.py --days 14 >> "$LOG" 2>&1; then
    notify_failure "Synthesis pipeline failed"
    exit 1
fi

# Find the newest post (just created, within last 5 minutes)
NEWEST=$(find "$BEACON_DIR/content/reflections/" -name "*.md" -not -name "_index*" -mmin -5 -print | head -1)
if [ -z "$NEWEST" ]; then
    notify_failure "No post generated in last 5 minutes"
    exit 1
fi

# Guard: reject empty or untitled posts
TITLE=$(grep '^title:' "$NEWEST" | head -1 | sed 's/^title: *//' | tr -d "'" | tr -d '"')
BODY_LINES=$(sed '1,/^---$/d' "$NEWEST" | sed '/^$/d' | wc -l | tr -d ' ')

if [ "$TITLE" = "Untitled Reflection" ] || [ "$TITLE" = "Untitled" ] || [ -z "$TITLE" ]; then
    notify_failure "Rejected: untitled post ($(basename $NEWEST))"
    rm "$NEWEST"
    echo "$(date -Iseconds) — Rejected untitled: $(basename $NEWEST)" >> "$LOG"
    exit 1
fi

if [ "$BODY_LINES" -lt 3 ]; then
    notify_failure "Rejected: empty post ($(basename $NEWEST), $BODY_LINES body lines)"
    rm "$NEWEST"
    echo "$(date -Iseconds) — Rejected empty: $(basename $NEWEST)" >> "$LOG"
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
