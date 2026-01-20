#!/bin/bash
# Plays error sound on tool failures
input=$(cat)
# Check if tool result indicates an error
if echo "$input" | grep -qiE '"error"|"failed"|"exception"'; then
    exec "$CLAUDE_PLUGIN_ROOT/hooks/play-sound.sh" error
fi
exit 0
