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
4. **Display sound details for active soundpack**:
   - Read the active soundpack's `soundpack.json`
   - For each sound type, show the count:
     - Single sound (string in JSON): show as "1 sound"
     - Multiple sounds (array in JSON): show as "N sounds (random)"
     - Not configured: show as "fallback (warcraft3-en)"
5. Offer to test sounds by playing each one

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

Sound Events:
- question: 1 sound - Plays when Claude asks a question
- complete: 3 sounds (random) - Plays when task finishes
- error: 1 sound - Plays on errors
- permission: fallback (warcraft3-en) - Plays when permission needed
```

Note: When a soundpack has multiple sounds configured for an event (array format in soundpack.json),
one is randomly selected each time the event occurs.
