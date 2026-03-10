---
name: soundpack-create
description: Create a custom soundpack from your own WAV files
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - AskUserQuestion
---

# Create Custom Soundpack Wizard

Use the plugin wrapper at `${CLAUDE_SKILL_DIR}/../../scripts/run-cli.sh` and the plugin root `${CLAUDE_SKILL_DIR}/../..`. These paths resolve correctly after installation.

## Wizard Flow

### Step 1: Soundpack Directory Name

Ask the user for a directory name:
- Must be lowercase with hyphens only, for example `my-sounds` or `zelda-pack`
- Must not already exist in `${CLAUDE_SKILL_DIR}/../../soundpacks/`
- Validate existing packs with:
  ```bash
  bash "${CLAUDE_SKILL_DIR}/../../scripts/run-cli.sh" soundpack list
  ```

### Step 2: Display Name

Ask for a human-readable display name.

### Step 3: Description

Ask for a brief description.

### Step 4: Sound Files

For each sound type `question`, `complete`, `error`, and `permission`, ask for one or more WAV file paths:
- Empty input means skip and fall back to `warcraft3-en`
- Multiple files may be provided as a comma-separated list for random playback
- Validate each provided path exists
- Validate each provided path ends with `.wav`, case-insensitive

### Step 5: Create Soundpack

1. Create the directory `${CLAUDE_SKILL_DIR}/../../soundpacks/<name>`.
2. Copy the user-provided WAV files into that directory:
   - Single file: `<sound-type>.wav`
   - Multiple files: `<sound-type>-1.wav`, `<sound-type>-2.wav`, and so on
3. Write `${CLAUDE_SKILL_DIR}/../../soundpacks/<name>/soundpack.json` with:
   - `name`
   - `description`
   - `sounds`
4. Only include sound entries for files the user actually provided.
5. Use a string value for a single file and an array for multiple files.

### Step 6: Confirmation & Activation

1. Summarize:
   - The created soundpack path
   - Which sounds were added
   - Which sounds will fall back to `warcraft3-en`
2. Ask whether the user wants to activate the new soundpack now.
3. If yes, run:
   ```bash
   bash "${CLAUDE_SKILL_DIR}/../../scripts/run-cli.sh" soundpack set "<soundpack-name>"
   ```
4. Tell the user that activation also plays the completion sound.
