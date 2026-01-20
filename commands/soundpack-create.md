---
name: claudecode-sounds:soundpack-create
description: Create a custom soundpack from your own WAV files
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - AskUserQuestion
---

# Create Custom Soundpack Wizard

Guide the user through creating a custom soundpack with their own WAV files.

## Wizard Flow

### Step 1: Soundpack Directory Name

Ask user for a directory name using AskUserQuestion:
- Must be lowercase with hyphens only (e.g., `my-sounds`, `zelda-pack`)
- Must not already exist in `$CLAUDE_PLUGIN_ROOT/soundpacks/`
- Validate with: `ls $CLAUDE_PLUGIN_ROOT/soundpacks/` to check existing packs

### Step 2: Display Name

Ask user for a human-readable display name (e.g., "My Custom Sounds", "Legend of Zelda")

### Step 3: Description

Ask user for a brief description of the soundpack.

### Step 4: Sound Files

For each sound type (question, complete, error, permission), ask for the file path:
- Use AskUserQuestion with open text input
- Clearly state that skipping is allowed (empty = skip, will use fallback from warcraft3-en)
- If path provided:
  - Validate file exists using `ls` or `test -f`
  - Validate it ends with `.wav` (case-insensitive)
  - If invalid, ask again with error message

Sound types and their purpose:
- `question` - Plays when Claude asks a question (AskUserQuestion)
- `complete` - Plays when a task completes
- `error` - Plays when an error occurs
- `permission` - Plays when permission is needed

### Step 5: Create Soundpack

1. Create directory:
   ```bash
   mkdir -p "$CLAUDE_PLUGIN_ROOT/soundpacks/{name}"
   ```

2. Copy each provided WAV file:
   ```bash
   cp "{user-provided-path}" "$CLAUDE_PLUGIN_ROOT/soundpacks/{name}/{sound-type}.wav"
   ```

3. Create `soundpack.json` with Write tool - only include sounds that were provided:
   ```json
   {
     "name": "Display Name Here",
     "description": "Description here",
     "sounds": {
       "question": "question.wav",
       "complete": "complete.wav"
     }
   }
   ```
   Note: Only add entries to "sounds" for files that were actually provided.

### Step 6: Confirmation & Activation

1. Show summary of what was created:
   - Soundpack location
   - Which sounds were added
   - Which sounds will fallback to warcraft3-en

2. Ask if user wants to activate the new soundpack now

3. If yes, update `.claude/claudecode-sounds.local.md`:
   ```markdown
   ---
   soundpack: {name}
   ---

   # Claude Code Sounds Settings

   Active soundpack for audio notifications.
   ```

4. Play a test sound to confirm:
   ```bash
   bash $CLAUDE_PLUGIN_ROOT/hooks/play-sound.sh complete
   ```

## Validation Rules

- Directory name: `/^[a-z0-9-]+$/` (lowercase alphanumeric and hyphens)
- File paths: Must exist and end with `.wav` (case-insensitive check)
- At least one sound should be provided (warn if all skipped, but allow it)

## Fallback Behavior

Any skipped sounds will automatically use the warcraft3-en soundpack as fallback.
This is handled by `play-sound.sh` - no additional configuration needed.

## Example Session

```
Claude: "What name for your soundpack directory? (lowercase, hyphens allowed)"
User: "zelda-sounds"

Claude: "What display name? (shown in /sounds)"
User: "Legend of Zelda"

Claude: "Brief description?"
User: "Sounds from Ocarina of Time"

Claude: "Path to question.wav? (skip = use default)"
User: "/Users/me/Downloads/hey-listen.wav"

Claude: "Path to complete.wav? (skip = use default)"
User: "" [skips]

Claude: "Path to error.wav? (skip = use default)"
User: "/Users/me/Downloads/game-over.wav"

Claude: "Path to permission.wav? (skip = use default)"
User: "" [skips]

Claude: "Created soundpack 'zelda-sounds' with 2 custom sounds.
        - question: custom
        - complete: fallback (warcraft3-en)
        - error: custom
        - permission: fallback (warcraft3-en)

        Activate it now?"
User: "Yes"

Claude: [Updates settings, plays test sound]
        "Done! Your new soundpack is active."
```
