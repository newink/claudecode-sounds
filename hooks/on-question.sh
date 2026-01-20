#!/bin/bash
# Plays question sound when AskUserQuestion is used
cat > /dev/null  # Consume stdin
exec "$CLAUDE_PLUGIN_ROOT/hooks/play-sound.sh" question
