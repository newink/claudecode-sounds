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

Use this Bash command whenever you need the plugin root or to invoke the bundled CLI:

```bash
RUNNER_SH=""; RUNNER_PS1=""; for candidate in "$PWD/.claude-plugin/claudecode-sounds/scripts/run-cli.sh" "$PWD/.claude-plugin/scripts/run-cli.sh"; do if [ -f "$candidate" ]; then RUNNER_SH="$candidate"; break; fi; done; for candidate in "$PWD/.claude-plugin/claudecode-sounds/scripts/run-cli.ps1" "$PWD/.claude-plugin/scripts/run-cli.ps1"; do if [ -f "$candidate" ]; then RUNNER_PS1="$candidate"; break; fi; done; if [ -z "$RUNNER_SH" ]; then RUNNER_SH="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}" -path '*claudecode-sounds/scripts/run-cli.sh' -print -quit 2>/dev/null)"; fi; if [ -z "$RUNNER_PS1" ]; then RUNNER_PS1="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}" -path '*claudecode-sounds/scripts/run-cli.ps1' -print -quit 2>/dev/null)"; fi; if [ -n "$RUNNER_SH" ]; then PLUGIN_ROOT="$(cd "$(dirname "$RUNNER_SH")/.." && pwd)"; bash "$RUNNER_SH" soundpack list; elif [ -n "$RUNNER_PS1" ]; then PLUGIN_ROOT="$(cd "$(dirname "$RUNNER_PS1")/.." && pwd)"; if command -v pwsh >/dev/null 2>&1; then pwsh -NoProfile -ExecutionPolicy Bypass -File "$RUNNER_PS1" soundpack list; elif command -v powershell.exe >/dev/null 2>&1; then powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$RUNNER_PS1" soundpack list; elif command -v powershell >/dev/null 2>&1; then powershell -NoProfile -ExecutionPolicy Bypass -File "$RUNNER_PS1" soundpack list; else echo "Could not execute PowerShell runner." >&2; exit 1; fi; else echo "Could not locate a usable claudecode-sounds runner. Ask the user to reinstall the plugin or restart Claude Code." >&2; exit 1; fi
```

1. Ask for a directory name:
   - lowercase letters, numbers, and hyphens only
   - must not already exist in `soundpacks/`
2. Validate it does not already exist by reading the `soundpack list` output from the command above.
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
10. If the user wants to activate it immediately, run a separate Bash tool call using the same runner-resolution pattern and invoke `soundpack set "<soundpack-name>"`.

## Notes

- Any skipped sounds fall back to `warcraft3-en`.
- Activation also plays the completion sound.
