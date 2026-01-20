---
name: claudecode-sounds:sounds
description: Show sound notification status and test sounds
allowed-tools:
  - Read
  - Bash
---

# Sound Notifications Status

Show the current soundpack configuration and available soundpacks.

## Instructions

1. Read the settings file at `.claude/claudecode-sounds.local.md` if it exists
2. List available soundpacks from `$CLAUDE_PLUGIN_ROOT/soundpacks/`
3. Show current configuration:
   - Active soundpack (default: warcraft3-en)
   - Available soundpacks with descriptions
4. Offer to test sounds by playing each one

## Testing Sounds

To test a sound, run:
```bash
bash $CLAUDE_PLUGIN_ROOT/hooks/play-sound.sh <sound_type>
```

Where `<sound_type>` is one of: question, complete, error, permission

## Example Output

```
Sound Notifications Status
==========================
Active soundpack: warcraft3-en (Warcraft 3 English)

Available soundpacks:
- warcraft3-ru: Озвучка Warcraft 3 на русском языке
- warcraft3-en: Classic Warcraft 3 interface sounds

Sounds:
- question: Plays when Claude asks a question
- complete: Plays when task finishes
- error: Plays on errors
- permission: Plays when permission needed
```
