---
name: test-sounds
description: Play all notification sounds to test your soundpack
disable-model-invocation: true
allowed-tools:
  - Bash
  - AskUserQuestion
---

# Test All Sounds

Use the plugin wrapper at `${CLAUDE_SKILL_DIR}/../../scripts/run-cli.sh`. It resolves the installed plugin path automatically, so it works after marketplace or manual installation without relying on `CLAUDE_PLUGIN_ROOT`.

## Instructions

1. Run these commands in order with Bash:
   ```bash
   bash "${CLAUDE_SKILL_DIR}/../../scripts/run-cli.sh" soundpack get
   bash "${CLAUDE_SKILL_DIR}/../../scripts/run-cli.sh" play question
   bash "${CLAUDE_SKILL_DIR}/../../scripts/run-cli.sh" play permission
   bash "${CLAUDE_SKILL_DIR}/../../scripts/run-cli.sh" play complete
   bash "${CLAUDE_SKILL_DIR}/../../scripts/run-cli.sh" play error
   ```
2. Summarize the active soundpack and confirm that each of the four sounds was played.
3. Ask the user which sounds they heard and whether any were missing or incorrect.
