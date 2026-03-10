---
name: claudecode-sounds:soundpack-set
description: Change the active soundpack
prefix-required: true
argument-hint: "<soundpack-name>"
allowed-tools:
  - Read
  - Write
  - Bash
---

# Set Active Soundpack

Change which soundpack is used for notifications globally (applies to all projects).

## Instructions

1. If no argument provided, list available soundpacks and ask user to choose
2. Validate the soundpack exists in `$CLAUDE_PLUGIN_ROOT/soundpacks/`
3. Create or update the global settings file at `$CLAUDE_CONFIG_DIR/claudecode-sounds.json` (fallback to `~/.claude/` if not set)

## Settings File Format

Create/update `$CLAUDE_CONFIG_DIR/claudecode-sounds.json` (or `~/.claude/claudecode-sounds.json`):

```json
{
  "soundpack": "warcraft3-en"
}
```

## Available Soundpacks

List available soundpacks:
```bash
node "$CLAUDE_PLUGIN_ROOT/hooks/cli.mjs" soundpack list || python3 "$CLAUDE_PLUGIN_ROOT/hooks/cli.py" soundpack list || python "$CLAUDE_PLUGIN_ROOT/hooks/cli.py" soundpack list || py -3 "$CLAUDE_PLUGIN_ROOT/hooks/cli.py" soundpack list
```

## After Setting

Play a test sound to confirm:
```bash
node "$CLAUDE_PLUGIN_ROOT/hooks/cli.mjs" play complete || python3 "$CLAUDE_PLUGIN_ROOT/hooks/cli.py" play complete || python "$CLAUDE_PLUGIN_ROOT/hooks/cli.py" play complete || py -3 "$CLAUDE_PLUGIN_ROOT/hooks/cli.py" play complete
```
