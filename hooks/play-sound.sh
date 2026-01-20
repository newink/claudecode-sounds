#!/bin/bash
# Cross-platform sound player for claudecode-sounds plugin
# Usage: play-sound.sh <sound_type>
# Sound types: question, complete, error, permission
# Supports multiple sounds per event with random selection

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

# Get sound file from soundpack, handling both string and array formats
# Args: soundpack_dir, sound_type
# Returns: resolved sound file path (empty if not found)
get_sound_file() {
    local pack_dir="$1"
    local stype="$2"
    local json_file="$pack_dir/soundpack.json"

    # If no soundpack.json, try direct file
    if [ ! -f "$json_file" ]; then
        local direct="$pack_dir/$stype.wav"
        if [ -f "$direct" ]; then
            echo "$direct"
        fi
        return
    fi

    # Check if jq is available for proper JSON parsing
    if command -v jq &> /dev/null; then
        local sound_value
        sound_value=$(jq -r ".sounds[\"$stype\"] // empty" "$json_file" 2>/dev/null)

        if [ -z "$sound_value" ]; then
            return
        fi

        # Check if it's an array
        local is_array
        is_array=$(jq -r ".sounds[\"$stype\"] | if type == \"array\" then \"yes\" else \"no\" end" "$json_file" 2>/dev/null)

        if [ "$is_array" = "yes" ]; then
            # Get array length and select random element
            local count
            count=$(jq -r ".sounds[\"$stype\"] | length" "$json_file" 2>/dev/null)
            if [ "$count" -gt 0 ]; then
                local index=$((RANDOM % count))
                local filename
                filename=$(jq -r ".sounds[\"$stype\"][$index]" "$json_file" 2>/dev/null)
                local resolved="$pack_dir/$filename"
                if [ -f "$resolved" ]; then
                    echo "$resolved"
                fi
            fi
        else
            # Single string value
            local resolved="$pack_dir/$sound_value"
            if [ -f "$resolved" ]; then
                echo "$resolved"
            fi
        fi
    else
        # Fallback without jq: try simple grep/sed parsing (string format only)
        local filename
        filename=$(grep -o "\"$stype\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" "$json_file" 2>/dev/null | sed 's/.*:[[:space:]]*"\([^"]*\)"/\1/' | head -1)
        if [ -n "$filename" ]; then
            local resolved="$pack_dir/$filename"
            if [ -f "$resolved" ]; then
                echo "$resolved"
            fi
        else
            # Try direct file as last resort
            local direct="$pack_dir/$stype.wav"
            if [ -f "$direct" ]; then
                echo "$direct"
            fi
        fi
    fi
}

# Try to get sound file from configured soundpack
SOUND_FILE=$(get_sound_file "$PLUGIN_ROOT/soundpacks/$SOUNDPACK" "$SOUND_TYPE")

# Fallback to warcraft3-en if not found
if [ -z "$SOUND_FILE" ] && [ "$SOUNDPACK" != "warcraft3-en" ]; then
    SOUND_FILE=$(get_sound_file "$PLUGIN_ROOT/soundpacks/warcraft3-en" "$SOUND_TYPE")
fi

# Exit if no sound file found
if [ -z "$SOUND_FILE" ]; then
    exit 0
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
            # Convert Unix path to Windows path for PowerShell
            WIN_SOUND_FILE=$(cygpath -w "$SOUND_FILE")
            powershell.exe -c "(New-Object Media.SoundPlayer '$WIN_SOUND_FILE').PlaySync()" &
        elif command -v mpv &> /dev/null; then
            mpv --no-video --really-quiet "$SOUND_FILE" &
        fi
        ;;
esac

# Don't wait for sound to finish
disown 2>/dev/null || true
exit 0
