#!/usr/bin/env bash

set -euo pipefail

find_runner_sh() {
  local candidate
  for candidate in \
    "$PWD/scripts/run-cli.sh" \
    "$PWD/.claude-plugin/claudecode-sounds/scripts/run-cli.sh" \
    "$PWD/.claude-plugin/scripts/run-cli.sh"
  do
    if [ -f "$candidate" ]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done

  find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}" -path '*claudecode-sounds*/scripts/run-cli.sh' -print -quit 2>/dev/null || true
}

find_runner_ps1() {
  local candidate
  for candidate in \
    "$PWD/scripts/run-cli.ps1" \
    "$PWD/.claude-plugin/claudecode-sounds/scripts/run-cli.ps1" \
    "$PWD/.claude-plugin/scripts/run-cli.ps1"
  do
    if [ -f "$candidate" ]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done

  find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}" -path '*claudecode-sounds*/scripts/run-cli.ps1' -print -quit 2>/dev/null || true
}

RUNNER_SH="$(find_runner_sh)"
if [ -n "$RUNNER_SH" ]; then
  exec bash "$RUNNER_SH" "$@"
fi

RUNNER_PS1="$(find_runner_ps1)"
if [ -n "$RUNNER_PS1" ]; then
  if command -v pwsh >/dev/null 2>&1; then
    exec pwsh -NoProfile -ExecutionPolicy Bypass -File "$RUNNER_PS1" "$@"
  fi
  if command -v powershell.exe >/dev/null 2>&1; then
    exec powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$RUNNER_PS1" "$@"
  fi
  if command -v powershell >/dev/null 2>&1; then
    exec powershell -NoProfile -ExecutionPolicy Bypass -File "$RUNNER_PS1" "$@"
  fi
fi

echo "Could not locate a usable claudecode-sounds runner. Ask the user to reinstall the plugin or restart Claude Code." >&2
exit 1
