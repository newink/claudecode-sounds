---
name: claudecode-sounds:test-sounds
description: Play all notification sounds to test your soundpack
prefix-required: true
allowed-tools:
  - Bash
  - AskUserQuestion
---

# Test All Sounds

Test sounds by running the plugin playback commands directly.

## Instructions

Run the sound test commands directly so each sound can be verified deterministically without depending on hook timing.

1. Run these commands in order:
   ```bash
   node "$CLAUDE_PLUGIN_ROOT/hooks/cli.mjs" soundpack get || python3 "$CLAUDE_PLUGIN_ROOT/hooks/cli.py" soundpack get || python "$CLAUDE_PLUGIN_ROOT/hooks/cli.py" soundpack get || py -3 "$CLAUDE_PLUGIN_ROOT/hooks/cli.py" soundpack get
   node "$CLAUDE_PLUGIN_ROOT/hooks/cli.mjs" play question || python3 "$CLAUDE_PLUGIN_ROOT/hooks/cli.py" play question || python "$CLAUDE_PLUGIN_ROOT/hooks/cli.py" play question || py -3 "$CLAUDE_PLUGIN_ROOT/hooks/cli.py" play question
   node "$CLAUDE_PLUGIN_ROOT/hooks/cli.mjs" play permission || python3 "$CLAUDE_PLUGIN_ROOT/hooks/cli.py" play permission || python "$CLAUDE_PLUGIN_ROOT/hooks/cli.py" play permission || py -3 "$CLAUDE_PLUGIN_ROOT/hooks/cli.py" play permission
   node "$CLAUDE_PLUGIN_ROOT/hooks/cli.mjs" play complete || python3 "$CLAUDE_PLUGIN_ROOT/hooks/cli.py" play complete || python "$CLAUDE_PLUGIN_ROOT/hooks/cli.py" play complete || py -3 "$CLAUDE_PLUGIN_ROOT/hooks/cli.py" play complete
   node "$CLAUDE_PLUGIN_ROOT/hooks/cli.mjs" play error || python3 "$CLAUDE_PLUGIN_ROOT/hooks/cli.py" play error || python "$CLAUDE_PLUGIN_ROOT/hooks/cli.py" play error || py -3 "$CLAUDE_PLUGIN_ROOT/hooks/cli.py" play error
   ```
2. Then ask the user which sounds they heard and whether any were missing or incorrect.
