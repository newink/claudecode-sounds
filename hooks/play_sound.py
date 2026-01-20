#!/usr/bin/env python3
"""Cross-platform sound player for claudecode-sounds plugin.

Usage: python play_sound.py <sound_type>
Sound types: question, complete, error, permission
"""

import json
import os
import platform
import random
import subprocess
import sys
from pathlib import Path

# Debug mode - set to True to enable logging
DEBUG = False


def log(msg):
    """Write debug message to stderr if DEBUG is enabled."""
    if DEBUG:
        print(f"[play_sound] {msg}", file=sys.stderr)


def get_plugin_root():
    """Get the plugin root directory."""
    log(f"CLAUDE_PLUGIN_ROOT env: {os.environ.get('CLAUDE_PLUGIN_ROOT', 'NOT SET')}")
    if os.environ.get("CLAUDE_PLUGIN_ROOT"):
        return Path(os.environ["CLAUDE_PLUGIN_ROOT"])
    fallback = Path(__file__).parent.parent
    log(f"Using fallback plugin root: {fallback}")
    return fallback


def get_soundpack():
    """Read soundpack from global settings file."""
    config_dir = os.environ.get("CLAUDE_CONFIG_DIR") or str(Path.home() / ".claude")
    log(f"CLAUDE_CONFIG_DIR: {config_dir}")
    settings_file = Path(config_dir) / "claudecode-sounds.local.md"
    log(f"Settings file: {settings_file}, exists: {settings_file.exists()}")

    soundpack = "warcraft3-en"  # default

    if settings_file.exists():
        try:
            content = settings_file.read_text(encoding="utf-8")
            if content.startswith("---"):
                end = content.find("---", 3)
                if end != -1:
                    frontmatter = content[3:end]
                    for line in frontmatter.split("\n"):
                        if line.strip().startswith("soundpack:"):
                            value = line.split(":", 1)[1].strip().strip("\"'")
                            if value:
                                soundpack = value
                            break
        except Exception as e:
            log(f"Error reading settings: {e}")

    log(f"Using soundpack: {soundpack}")
    return soundpack


def get_sound_file(pack_dir: Path, sound_type: str):
    """Get sound file from soundpack, handling both string and array formats."""
    log(f"Looking for sound '{sound_type}' in {pack_dir}")
    json_file = pack_dir / "soundpack.json"

    if not json_file.exists():
        direct = pack_dir / f"{sound_type}.wav"
        log(f"No soundpack.json, trying direct: {direct}, exists: {direct.exists()}")
        if direct.exists():
            return direct
        return None

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        sound_value = data.get("sounds", {}).get(sound_type)
        log(f"Sound value from JSON: {sound_value}")
        if not sound_value:
            return None

        if isinstance(sound_value, list):
            filename = random.choice(sound_value)
        else:
            filename = sound_value

        resolved = pack_dir / filename
        log(f"Resolved sound file: {resolved}, exists: {resolved.exists()}")
        if resolved.exists():
            return resolved
    except Exception as e:
        log(f"Error reading soundpack.json: {e}")
        direct = pack_dir / f"{sound_type}.wav"
        if direct.exists():
            return direct

    return None


def play_sound_async(sound_file: Path):
    """Play sound without blocking, based on OS."""
    system = platform.system()
    log(f"Playing sound on {system}: {sound_file}")

    try:
        if system == "Windows":
            import winsound
            log("Using winsound")
            winsound.PlaySound(str(sound_file), winsound.SND_FILENAME | winsound.SND_ASYNC)
            log("winsound.PlaySound called")
        elif system == "Darwin":
            log("Using afplay")
            proc = subprocess.Popen(
                ["afplay", str(sound_file)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            log(f"afplay started with PID: {proc.pid}")
        elif system == "Linux":
            players = [
                ["paplay", str(sound_file)],
                ["aplay", "-q", str(sound_file)],
                ["mpv", "--no-video", "--really-quiet", str(sound_file)],
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", str(sound_file)],
            ]
            for cmd in players:
                try:
                    log(f"Trying: {cmd[0]}")
                    proc = subprocess.Popen(
                        cmd,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        start_new_session=True
                    )
                    log(f"{cmd[0]} started with PID: {proc.pid}")
                    break
                except FileNotFoundError:
                    log(f"{cmd[0]} not found")
                    continue
    except Exception as e:
        log(f"Error playing sound: {e}")


def main():
    log("=" * 50)
    log(f"Script started with args: {sys.argv}")
    log(f"CWD: {os.getcwd()}")
    log(f"All env vars: {dict(os.environ)}")

    if len(sys.argv) < 2:
        log("No sound type provided, exiting")
        sys.exit(0)

    sound_type = sys.argv[1]
    if not sound_type:
        log("Empty sound type, exiting")
        sys.exit(0)

    log(f"Sound type: {sound_type}")

    plugin_root = get_plugin_root()
    log(f"Plugin root: {plugin_root}, exists: {plugin_root.exists()}")

    soundpack = get_soundpack()

    sound_file = get_sound_file(plugin_root / "soundpacks" / soundpack, sound_type)

    if not sound_file and soundpack != "warcraft3-en":
        log("Trying fallback soundpack warcraft3-en")
        sound_file = get_sound_file(plugin_root / "soundpacks" / "warcraft3-en", sound_type)

    if not sound_file:
        log("No sound file found, exiting")
        sys.exit(0)

    log(f"Final sound file: {sound_file}")
    play_sound_async(sound_file)
    log("Done")


if __name__ == "__main__":
    main()
