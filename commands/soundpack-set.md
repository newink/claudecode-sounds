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

Change which soundpack is used for notifications.

## Instructions

1. If no argument provided, list available soundpacks and ask user to choose
2. Validate the soundpack exists in `$CLAUDE_PLUGIN_ROOT/soundpacks/`
3. Create or update `.claude/claudecode-sounds.local.md` with the new setting

## Settings File Format

Create/update `.claude/claudecode-sounds.local.md`:

```markdown
---
soundpack: warcraft3-en
---

# Claude Code Sounds Settings

Active soundpack for audio notifications.
```

## Available Soundpacks

Check `$CLAUDE_PLUGIN_ROOT/soundpacks/` for available options:
- `warcraft3-en` - Warcraft 3 (English)
- `warcraft3-ru` - Warcraft 3 (Русский)

## After Setting

Play a test sound to confirm:
```bash
python "$CLAUDE_PLUGIN_ROOT/hooks/play_sound.py" complete
```
