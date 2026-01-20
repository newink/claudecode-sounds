# claudecode-sounds

Play sounds when Claude Code needs your attention.

## Features

- **Question sound**: Plays when Claude asks you a question
- **Complete sound**: Plays when Claude finishes a task
- **Notification sound**: Plays on system notifications
- **Cross-platform**: Works on macOS, Linux, and Windows

## Soundpacks

Included soundpacks:
- `warcraft3-ru` - Warcraft 3 (Русский) - default
- `warcraft3-en` - Warcraft 3 (English)

## Installation

```bash
# Clone or copy to your plugins directory
claude --plugin-dir /path/to/claudecode-sounds
```

Or add to a project:
```bash
cp -r claudecode-sounds /your/project/.claude-plugin/
```

## Commands

- `/sounds` - Show status and test sounds
- `/sounds-set <name>` - Change soundpack (e.g., `/sounds-set warcraft3-en`)

## Configuration

Settings are stored in `.claude/claudecode-sounds.local.md`:

```markdown
---
soundpack: warcraft3-ru
---
```

## Creating Custom Soundpacks

1. Create a folder in `soundpacks/` with your pack name
2. Add these sound files (WAV format):
   - `question.wav` - Played when Claude asks a question
   - `complete.wav` - Played when task completes
   - `error.wav` - Played on errors
   - `permission.wav` - Played when permission needed
3. Create `soundpack.json`:
   ```json
   {
     "name": "My Soundpack",
     "description": "Description of sounds",
     "sounds": {
       "question": "question.wav",
       "complete": "complete.wav",
       "error": "error.wav",
       "permission": "permission.wav"
     }
   }
   ```

## Requirements

### macOS
Built-in `afplay` (no additional software needed)

### Linux
One of: `paplay` (PulseAudio), `aplay` (ALSA), `mpv`, or `ffplay`

### Windows
PowerShell (built-in) or `mpv`

## License

Sound files from Warcraft 3 are property of Blizzard Entertainment.
