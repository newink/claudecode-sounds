#!/bin/bash
# Cross-platform sound player for claudecode-sounds plugin
# Usage: play-sound.sh <sound_type>
# Sound types: question, complete, error, permission

set -euo pipefail

SOUND_TYPE="${1:-}"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$0")")}"
SETTINGS_FILE="${CLAUDE_PROJECT_DIR:-.}/.claude/claudecode-sounds.local.md"

# Default soundpack
SOUNDPACK="warcraft3-en"

# Read soundpack from settings if exists
if [ -f "$SETTINGS_FILE" ]; then
    # Extract soundpack from YAML frontmatter
    CONFIGURED_PACK=$(sed -n '/^---$/,/^---$/p' "$SETTINGS_FILE" | grep "^soundpack:" | cut -d':' -f2 | tr -d ' "'"'" | head -1)
    if [ -n "$CONFIGURED_PACK" ]; then
        SOUNDPACK="$CONFIGURED_PACK"
    fi
fi

# Validate sound type
if [ -z "$SOUND_TYPE" ]; then
    exit 0
fi

# Build sound file path
SOUND_FILE="$PLUGIN_ROOT/soundpacks/$SOUNDPACK/$SOUND_TYPE.wav"

# Check if sound file exists
if [ ! -f "$SOUND_FILE" ]; then
    # Try fallback to warcraft3-en
    SOUND_FILE="$PLUGIN_ROOT/soundpacks/warcraft3-en/$SOUND_TYPE.wav"
    if [ ! -f "$SOUND_FILE" ]; then
        exit 0
    fi
fi

# Play sound based on OS (in background, don't block)
case "$(uname -s)" in
    Darwin)
        # macOS
        afplay "$SOUND_FILE" &
        ;;
    Linux)
        # Linux - try multiple players
        if command -v paplay &> /dev/null; then
            paplay "$SOUND_FILE" &
        elif command -v aplay &> /dev/null; then
            aplay -q "$SOUND_FILE" &
        elif command -v mpv &> /dev/null; then
            mpv --no-video --really-quiet "$SOUND_FILE" &
        elif command -v ffplay &> /dev/null; then
            ffplay -nodisp -autoexit -loglevel quiet "$SOUND_FILE" &
        fi
        ;;
    MINGW*|MSYS*|CYGWIN*)
        # Windows (Git Bash, MSYS2, Cygwin)
        if command -v powershell.exe &> /dev/null; then
            powershell.exe -c "(New-Object Media.SoundPlayer '$SOUND_FILE').PlaySync()" &
        elif command -v mpv &> /dev/null; then
            mpv --no-video --really-quiet "$SOUND_FILE" &
        fi
        ;;
esac

# Don't wait for sound to finish
disown 2>/dev/null || true
exit 0
