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
2. Locate the bundled wrapper script before running any plugin command:
   - Check `$PWD/.claude-plugin/claudecode-sounds/scripts/run-cli.sh`
   - Then `$PWD/.claude-plugin/scripts/run-cli.sh`
   - Then `$PWD/.claude-plugin/claudecode-sounds/scripts/run-cli.ps1`
   - Then `$PWD/.claude-plugin/scripts/run-cli.ps1`
   - Then search `${CLAUDE_CONFIG_DIR:-$HOME/.claude}` for `*/claudecode-sounds/scripts/run-cli.sh`
   - Then search `${CLAUDE_CONFIG_DIR:-$HOME/.claude}` for `*/claudecode-sounds/scripts/run-cli.ps1`
3. Validate the soundpack exists in the wrapper's `soundpack list` output
4. Use `run_cli soundpack set "<soundpack-name>"` to update the global settings file at `$CLAUDE_CONFIG_DIR/claudecode-sounds.json` (fallback to `~/.claude/` if not set)

Use this Bash snippet to resolve the runner and define `run_cli`:

```bash
PLUGIN_RUNNER_SH=""
PLUGIN_RUNNER_PS1=""
for candidate in \
  "$PWD/.claude-plugin/claudecode-sounds/scripts/run-cli.sh" \
  "$PWD/.claude-plugin/scripts/run-cli.sh"
do
  if [ -f "$candidate" ]; then
    PLUGIN_RUNNER_SH="$candidate"
    break
  fi
done

for candidate in \
  "$PWD/.claude-plugin/claudecode-sounds/scripts/run-cli.ps1" \
  "$PWD/.claude-plugin/scripts/run-cli.ps1"
do
  if [ -f "$candidate" ]; then
    PLUGIN_RUNNER_PS1="$candidate"
    break
  fi
done

if [ -z "$PLUGIN_RUNNER_SH" ]; then
  PLUGIN_RUNNER_SH="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}" -path '*claudecode-sounds/scripts/run-cli.sh' -print -quit 2>/dev/null)"
fi

if [ -z "$PLUGIN_RUNNER_PS1" ]; then
  PLUGIN_RUNNER_PS1="$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}" -path '*claudecode-sounds/scripts/run-cli.ps1' -print -quit 2>/dev/null)"
fi

run_cli() {
  if [ -n "$PLUGIN_RUNNER_SH" ]; then
    bash "$PLUGIN_RUNNER_SH" "$@"
    return
  fi

  if [ -n "$PLUGIN_RUNNER_PS1" ]; then
    if command -v pwsh >/dev/null 2>&1; then
      pwsh -NoProfile -ExecutionPolicy Bypass -File "$PLUGIN_RUNNER_PS1" "$@"
      return
    fi
    if command -v powershell.exe >/dev/null 2>&1; then
      powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$PLUGIN_RUNNER_PS1" "$@"
      return
    fi
    if command -v powershell >/dev/null 2>&1; then
      powershell -NoProfile -ExecutionPolicy Bypass -File "$PLUGIN_RUNNER_PS1" "$@"
      return
    fi
  fi

  echo "Could not locate a usable claudecode-sounds runner. Ask the user to reinstall the plugin or restart Claude Code." >&2
  exit 1
}
```

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
run_cli soundpack list
```

## After Setting

Play a test sound to confirm:
```bash
run_cli soundpack set "<soundpack-name>"
```
