---
name: soundpack-set
description: Change the active soundpack
disable-model-invocation: true
allowed-tools:
  - Bash
  - AskUserQuestion
---

# Set Active Soundpack

Use the plugin wrapper at `${CLAUDE_SKILL_DIR}/../../scripts/run-cli.sh`. It resolves the installed plugin path automatically, so it works after marketplace or manual installation without relying on `CLAUDE_PLUGIN_ROOT`.

## Instructions

1. If no argument was provided, list available soundpacks with:
   ```bash
   bash "${CLAUDE_SKILL_DIR}/../../scripts/run-cli.sh" soundpack list
   ```
   Then ask the user to choose one of the returned pack names.
2. Validate the requested soundpack exists by checking the output of the same `soundpack list` command.
3. Set the soundpack with:
   ```bash
   bash "${CLAUDE_SKILL_DIR}/../../scripts/run-cli.sh" soundpack set "<soundpack-name>"
   ```
4. Report which soundpack is now active. Mention that the command also plays the completion sound as a confirmation.
