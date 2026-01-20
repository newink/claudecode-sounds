#!/bin/bash
# Check if session ended with error and play appropriate sound
# Used as Stop hook

set -euo pipefail

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$0")")}"

# Read stdin JSON
INPUT=$(cat)

# Check for error indicators in the stop context
# Look for: error messages, failed operations, non-zero exit codes
if echo "$INPUT" | grep -qiE '(error|failed|exception|exit code [1-9]|exit status [1-9]|cannot |fatal:|denied|not found)'; then
    SOUND_TYPE="error"
else
    SOUND_TYPE="complete"
fi

# Play sound
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    powershell -NoProfile -ExecutionPolicy Bypass -File "$PLUGIN_ROOT/hooks/play-sound.ps1" "$SOUND_TYPE" 2>/dev/null &
else
    bash "$PLUGIN_ROOT/hooks/play-sound.sh" "$SOUND_TYPE" &
fi

disown 2>/dev/null || true
exit 0
