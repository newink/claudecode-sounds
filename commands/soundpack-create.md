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

Start each Bash tool call by resolving the bootstrap runner with this exact block:

```bash
semver_gt() {
  local lhs="$1"
  local rhs="$2"
  local lhs_core="${lhs%%-*}"
  local rhs_core="${rhs%%-*}"
  local lhs_pre=""
  local rhs_pre=""
  local i max lhs_part rhs_part
  local -a lhs_parts=()
  local -a rhs_parts=()

  if [ "$lhs_core" != "$lhs" ]; then
    lhs_pre="${lhs#${lhs_core}-}"
  fi
  if [ "$rhs_core" != "$rhs" ]; then
    rhs_pre="${rhs#${rhs_core}-}"
  fi

  IFS=. read -r -a lhs_parts <<< "$lhs_core"
  IFS=. read -r -a rhs_parts <<< "$rhs_core"

  max="${#lhs_parts[@]}"
  if [ "${#rhs_parts[@]}" -gt "$max" ]; then
    max="${#rhs_parts[@]}"
  fi

  for ((i = 0; i < max; i += 1)); do
    lhs_part="${lhs_parts[i]:-0}"
    rhs_part="${rhs_parts[i]:-0}"

    if ((10#"${lhs_part}" > 10#"${rhs_part}")); then
      return 0
    fi
    if ((10#"${lhs_part}" < 10#"${rhs_part}")); then
      return 1
    fi
  done

  if [ -z "$lhs_pre" ] && [ -n "$rhs_pre" ]; then
    return 0
  fi
  if [ -n "$lhs_pre" ] && [ -z "$rhs_pre" ]; then
    return 1
  fi
  if [ "$lhs_pre" != "$rhs_pre" ] && [ "$lhs_pre" \> "$rhs_pre" ]; then
    return 0
  fi

  return 1
}

extract_cached_version() {
  local candidate="$1"

  case "$candidate" in
    */claudecode-sounds/*/scripts/*)
      candidate="${candidate%/scripts/*}"
      printf '%s\n' "${candidate##*/}"
      ;;
    *)
      return 1
      ;;
  esac
}

find_latest_cached_bootstrap() {
  local config_dir="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
  local candidate version best_path="" best_version=""

  for candidate in "$config_dir"/plugins/cache/codingagents/claudecode-sounds/*/scripts/bootstrap-run.sh; do
    [ -f "$candidate" ] || continue
    version="$(extract_cached_version "$candidate" 2>/dev/null || true)"
    if [ -z "$best_path" ] || { [ -n "$version" ] && [ -n "$best_version" ] && semver_gt "$version" "$best_version"; } || { [ -n "$version" ] && [ -z "$best_version" ]; }; then
      best_path="$candidate"
      best_version="$version"
    fi
  done

  if [ -n "$best_path" ]; then
    printf '%s\n' "$best_path"
    return 0
  fi

  while IFS= read -r candidate; do
    [ -f "$candidate" ] || continue
    version="$(extract_cached_version "$candidate" 2>/dev/null || true)"
    if [ -z "$best_path" ] || { [ -n "$version" ] && [ -n "$best_version" ] && semver_gt "$version" "$best_version"; } || { [ -n "$version" ] && [ -z "$best_version" ]; }; then
      best_path="$candidate"
      best_version="$version"
    fi
  done < <(find "$config_dir" -path '*claudecode-sounds*/scripts/bootstrap-run.sh' -print 2>/dev/null)

  if [ -n "$best_path" ]; then
    printf '%s\n' "$best_path"
  fi
}

BOOTSTRAP=""
BOOTSTRAP="$(find_latest_cached_bootstrap)"

if [ -z "$BOOTSTRAP" ]; then
  echo "Could not locate claudecode-sounds bootstrap runner. Ask the user to reinstall the plugin or restart Claude Code." >&2
  exit 1
fi
```

1. Ask for a directory name:
   - lowercase letters, numbers, and hyphens only
   - must not already exist in `soundpacks/`
2. Validate it does not already exist by using one Bash call with the resolution block above followed by `bash "$BOOTSTRAP" soundpack list`.
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
10. If the user wants to activate it immediately, run a Bash tool call with the same resolution block followed by `bash "$BOOTSTRAP" soundpack set "<soundpack-name>"`.

## Notes

- Any skipped sounds fall back to `warcraft3-en`.
- Activation also plays the completion sound.
