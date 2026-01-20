#!/bin/bash
# Plays complete sound when task finishes
cat > /dev/null  # Consume stdin
exec "$CLAUDE_PLUGIN_ROOT/hooks/play-sound.sh" complete
