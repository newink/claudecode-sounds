#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if command -v node >/dev/null 2>&1; then
  exec node "${PLUGIN_ROOT}/hooks/cli.mjs" "$@"
fi

if command -v python3 >/dev/null 2>&1; then
  exec python3 "${PLUGIN_ROOT}/hooks/cli.py" "$@"
fi

if command -v python >/dev/null 2>&1; then
  exec python "${PLUGIN_ROOT}/hooks/cli.py" "$@"
fi

if command -v py >/dev/null 2>&1; then
  exec py -3 "${PLUGIN_ROOT}/hooks/cli.py" "$@"
fi

echo "claudecode-sounds: neither node, python3, python, nor py -3 is available" >&2
exit 127
