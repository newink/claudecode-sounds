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

Use a single Bash tool call for the full test sequence.

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

Then run the full test sequence in one Bash call:

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

bash "$BOOTSTRAP" soundpack get
bash "$BOOTSTRAP" play question
bash "$BOOTSTRAP" play permission
bash "$BOOTSTRAP" play complete
bash "$BOOTSTRAP" play error
```

Then ask the user which sounds they heard and whether any were missing or incorrect.
