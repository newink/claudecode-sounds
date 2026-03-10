---
name: claudecode-sounds:soundpack-create
description: Create a custom soundpack from your own WAV files
prefix-required: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - AskUserQuestion
---

# Create Custom Soundpack Wizard

Guide the user through creating a custom soundpack with their own WAV files.

## Instructions

Use a single Bash invocation per action. Do not rely on shell variables or functions carrying across separate Bash tool calls.

First resolve the bootstrap runner:

```bash
BOOTSTRAP=""
for candidate in \
  "$PWD/scripts/bootstrap-run.sh" \
  "$PWD/.claude-plugin/claudecode-sounds/scripts/bootstrap-run.sh" \
  "$PWD/.claude-plugin/scripts/bootstrap-run.sh"
do
  if [ -f "$candidate" ]; then
    BOOTSTRAP="$candidate"
    break
  fi
done

if [ -z "$BOOTSTRAP" ]; then
  BOOTSTRAP="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}" -path '*claudecode-sounds*/scripts/bootstrap-run.sh' -print -quit 2>/dev/null)"
fi

if [ -z "$BOOTSTRAP" ]; then
  echo "Could not locate claudecode-sounds bootstrap runner. Ask the user to reinstall the plugin or restart Claude Code." >&2
  exit 1
fi
```

1. Ask for a directory name:
   - lowercase letters, numbers, and hyphens only
   - must not already exist in `soundpacks/`
2. Validate it does not already exist by using one Bash call to run `bash "$BOOTSTRAP" soundpack list`.
3. Ask for:
   - display name
   - description
   - WAV paths for `question`, `complete`, `error`, and `permission`
4. Empty input means fallback to `warcraft3-en`.
5. Multiple WAV files may be provided as a comma-separated list for random playback.
6. Validate each provided path exists and ends with `.wav`.
7. Create the soundpack directory under the resolved plugin root.
8. Copy files into `soundpacks/<name>/`:
   - single file: `<type>.wav`
   - multiple files: `<type>-1.wav`, `<type>-2.wav`, and so on
9. Write `soundpack.json` with `name`, `description`, and `sounds`.
10. If the user wants to activate it immediately, run a Bash tool call that resolves `BOOTSTRAP` and then executes `bash "$BOOTSTRAP" soundpack set "<soundpack-name>"`.

## Notes

- Any skipped sounds fall back to `warcraft3-en`.
- Activation also plays the completion sound.
