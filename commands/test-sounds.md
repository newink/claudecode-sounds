---
name: claudecode-sounds:test-sounds
description: Play all notification sounds to test your soundpack
prefix-required: true
allowed-tools:
  - Bash
  - AskUserQuestion
---

# Test All Sounds

Test sounds by running the plugin playback commands directly.

## Instructions

First locate the bundled wrapper script. Check these paths in order:

1. `$PWD/.claude-plugin/claudecode-sounds/scripts/run-cli.sh`
2. `$PWD/.claude-plugin/scripts/run-cli.sh`
3. `$PWD/.claude-plugin/claudecode-sounds/scripts/run-cli.ps1`
4. `$PWD/.claude-plugin/scripts/run-cli.ps1`
5. Search under `${CLAUDE_CONFIG_DIR:-$HOME/.claude}` for `*/claudecode-sounds/scripts/run-cli.sh`
6. Search under `${CLAUDE_CONFIG_DIR:-$HOME/.claude}` for `*/claudecode-sounds/scripts/run-cli.ps1`

Use this Bash snippet to resolve it and define a portable `run_cli` helper:

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

Run the sound test commands through that wrapper so each sound can be verified deterministically without depending on hook timing.

1. Run these commands in order:
   ```bash
   run_cli soundpack get
   run_cli play question
   run_cli play permission
   run_cli play complete
   run_cli play error
   ```
2. Then ask the user which sounds they heard and whether any were missing or incorrect.
