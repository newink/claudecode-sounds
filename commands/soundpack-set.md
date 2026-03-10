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

Change which soundpack is used for notifications globally.

## Instructions

Use a single Bash invocation per action. Do not rely on shell variables or functions carrying across separate Bash tool calls.

Use this self-contained invocation pattern, replacing only the final CLI arguments:

```bash
RUNNER_SH=""; RUNNER_PS1=""; for candidate in "$PWD/.claude-plugin/claudecode-sounds/scripts/run-cli.sh" "$PWD/.claude-plugin/scripts/run-cli.sh"; do if [ -f "$candidate" ]; then RUNNER_SH="$candidate"; break; fi; done; for candidate in "$PWD/.claude-plugin/claudecode-sounds/scripts/run-cli.ps1" "$PWD/.claude-plugin/scripts/run-cli.ps1"; do if [ -f "$candidate" ]; then RUNNER_PS1="$candidate"; break; fi; done; if [ -z "$RUNNER_SH" ]; then RUNNER_SH="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}" -path '*claudecode-sounds/scripts/run-cli.sh' -print -quit 2>/dev/null)"; fi; if [ -z "$RUNNER_PS1" ]; then RUNNER_PS1="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}" -path '*claudecode-sounds/scripts/run-cli.ps1' -print -quit 2>/dev/null)"; fi; if [ -n "$RUNNER_SH" ]; then bash "$RUNNER_SH" soundpack list; elif [ -n "$RUNNER_PS1" ] && command -v pwsh >/dev/null 2>&1; then pwsh -NoProfile -ExecutionPolicy Bypass -File "$RUNNER_PS1" soundpack list; elif [ -n "$RUNNER_PS1" ] && command -v powershell.exe >/dev/null 2>&1; then powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$RUNNER_PS1" soundpack list; elif [ -n "$RUNNER_PS1" ] && command -v powershell >/dev/null 2>&1; then powershell -NoProfile -ExecutionPolicy Bypass -File "$RUNNER_PS1" soundpack list; else echo "Could not locate a usable claudecode-sounds runner. Ask the user to reinstall the plugin or restart Claude Code." >&2; exit 1; fi
```

1. If no argument is provided, run the list command above and ask the user to choose a soundpack name.
2. Validate that the requested name exists in the `soundpack list` output.
3. Set the soundpack with a separate Bash tool call:

```bash
RUNNER_SH=""; RUNNER_PS1=""; for candidate in "$PWD/.claude-plugin/claudecode-sounds/scripts/run-cli.sh" "$PWD/.claude-plugin/scripts/run-cli.sh"; do if [ -f "$candidate" ]; then RUNNER_SH="$candidate"; break; fi; done; for candidate in "$PWD/.claude-plugin/claudecode-sounds/scripts/run-cli.ps1" "$PWD/.claude-plugin/scripts/run-cli.ps1"; do if [ -f "$candidate" ]; then RUNNER_PS1="$candidate"; break; fi; done; if [ -z "$RUNNER_SH" ]; then RUNNER_SH="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}" -path '*claudecode-sounds/scripts/run-cli.sh' -print -quit 2>/dev/null)"; fi; if [ -z "$RUNNER_PS1" ]; then RUNNER_PS1="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}" -path '*claudecode-sounds/scripts/run-cli.ps1' -print -quit 2>/dev/null)"; fi; if [ -n "$RUNNER_SH" ]; then bash "$RUNNER_SH" soundpack set "<soundpack-name>"; elif [ -n "$RUNNER_PS1" ] && command -v pwsh >/dev/null 2>&1; then pwsh -NoProfile -ExecutionPolicy Bypass -File "$RUNNER_PS1" soundpack set "<soundpack-name>"; elif [ -n "$RUNNER_PS1" ] && command -v powershell.exe >/dev/null 2>&1; then powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$RUNNER_PS1" soundpack set "<soundpack-name>"; elif [ -n "$RUNNER_PS1" ] && command -v powershell >/dev/null 2>&1; then powershell -NoProfile -ExecutionPolicy Bypass -File "$RUNNER_PS1" soundpack set "<soundpack-name>"; else echo "Could not locate a usable claudecode-sounds runner. Ask the user to reinstall the plugin or restart Claude Code." >&2; exit 1; fi
```

4. Report the active soundpack name. Mention that setting it also plays the completion sound as confirmation.
