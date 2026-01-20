#!/usr/bin/env python3
"""Check if session ended with error and play appropriate sound.

Used as Stop hook for claudecode-sounds plugin.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

# Debug mode - set to True to enable logging
DEBUG = False


def log(msg):
    """Write debug message to stderr if DEBUG is enabled."""
    if DEBUG:
        print(f"[check_stop] {msg}", file=sys.stderr)


def main():
    log("=" * 50)
    log(f"check_stop_error.py started")
    log(f"CWD: {os.getcwd()}")
    log(f"sys.argv: {sys.argv}")

    # Read stdin
    try:
        input_text = sys.stdin.read()
        log(f"stdin length: {len(input_text)}")
        log(f"stdin preview: {input_text[:500] if input_text else 'EMPTY'}")
    except Exception as e:
        log(f"Error reading stdin: {e}")
        input_text = ""

    # Check for error indicators
    error_pattern = r"(error|failed|exception|exit code [1-9]|exit status [1-9]|cannot |fatal:|denied|not found)"
    if re.search(error_pattern, input_text, re.IGNORECASE):
        sound_type = "error"
        log("Detected ERROR in output")
    else:
        sound_type = "complete"
        log("No error detected, using COMPLETE")

    # Get plugin root
    plugin_root_env = os.environ.get("CLAUDE_PLUGIN_ROOT")
    log(f"CLAUDE_PLUGIN_ROOT: {plugin_root_env}")

    if plugin_root_env:
        plugin_root = Path(plugin_root_env)
    else:
        plugin_root = Path(__file__).parent.parent
        log(f"Using fallback plugin root: {plugin_root}")

    # Call play_sound.py
    play_script = plugin_root / "hooks" / "play_sound.py"
    log(f"play_script path: {play_script}, exists: {play_script.exists()}")

    try:
        cmd = [sys.executable, str(play_script), sound_type]
        log(f"Executing: {cmd}")
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        log(f"Started play_sound.py with PID: {proc.pid}")
    except Exception as e:
        log(f"Error starting play_sound.py: {e}")

    log("check_stop_error.py done")


if __name__ == "__main__":
    main()
