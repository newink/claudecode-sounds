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

1. If no argument is provided, use one Bash tool call to run `bash "$BOOTSTRAP" soundpack list`, then ask the user to choose a soundpack name.
2. Validate that the requested name exists in the `soundpack list` output.
3. Set the soundpack with one Bash tool call:

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

bash "$BOOTSTRAP" soundpack set "<soundpack-name>"
```

4. Report the active soundpack name. Mention that setting it also plays the completion sound as confirmation.
