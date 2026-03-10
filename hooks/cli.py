#!/usr/bin/env python3
"""Unified CLI for claudecode-sounds plugin.

Usage:
    python cli.py play <type>           - play a sound (question/complete/error/permission)
    python cli.py check-stop            - read Stop hook JSON, play error on failed turns
    python cli.py soundpack list        - list available soundpacks as JSON
    python cli.py soundpack get         - print current active soundpack name
    python cli.py soundpack set <name>  - set soundpack, play test sound
"""

import json
import os
import platform
import random
import re
import subprocess
import sys
from pathlib import Path

# Debug mode - set to True to enable logging
DEBUG = False
STOP_ERROR_PATTERN = re.compile(
    r"\b(error|failed|failure|exception|cannot|can't|unable to|fatal|denied|not found)\b|exit code [1-9]|exit status [1-9]",
    re.IGNORECASE,
)


def log(msg):
    """Write debug message to stderr if DEBUG is enabled."""
    if DEBUG:
        print(f"[cli] {msg}", file=sys.stderr)


def get_last_assistant_message(input_text: str) -> str:
    """Parse hook JSON and return last_assistant_message when present."""
    if not input_text:
        return ""

    try:
        payload = json.loads(input_text)
    except Exception as e:
        log(f"Error parsing hook payload JSON: {e}")
        return ""

    message = payload.get("last_assistant_message")
    if isinstance(message, str):
        log(f"Parsed Stop payload with last_assistant_message length: {len(message)}")
        return message
    return ""


# --- Shared utilities ---


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

    # Try JSON format first
    json_file = Path(config_dir) / "claudecode-sounds.json"
    log(f"JSON settings: {json_file}, exists: {json_file.exists()}")
    if json_file.exists():
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
            if data.get("soundpack"):
                log(f"Using soundpack from JSON: {data['soundpack']}")
                return data["soundpack"]
        except Exception as e:
            log(f"Error reading JSON settings: {e}")

    # Fall back to old markdown format
    md_file = Path(config_dir) / "claudecode-sounds.local.md"
    log(f"Fallback MD settings: {md_file}, exists: {md_file.exists()}")
    if md_file.exists():
        try:
            content = md_file.read_text(encoding="utf-8")
            if content.startswith("---"):
                end = content.find("---", 3)
                if end != -1:
                    frontmatter = content[3:end]
                    for line in frontmatter.split("\n"):
                        if line.strip().startswith("soundpack:"):
                            value = line.split(":", 1)[1].strip().strip("\"'")
                            if value:
                                log(f"Using soundpack from MD fallback: {value}")
                                return value
        except Exception as e:
            log(f"Error reading MD settings: {e}")

    log("Using default soundpack: warcraft3-en")
    return "warcraft3-en"


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
            played = False
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
                    played = True
                    break
                except FileNotFoundError:
                    log(f"{cmd[0]} not found")
                    continue
            if not played:
                print(json.dumps({
                    "systemMessage": "claudecode-sounds: No audio player found. Install one of: pulseaudio-utils, alsa-utils, mpv, or ffmpeg."
                }))
    except Exception as e:
        log(f"Error playing sound: {e}")


def play_by_type(sound_type):
    """Play a sound by type, with soundpack resolution and fallback."""
    if not sound_type:
        return

    plugin_root = get_plugin_root()
    soundpack = get_soundpack()

    sound_file = get_sound_file(plugin_root / "soundpacks" / soundpack, sound_type)

    if not sound_file and soundpack != "warcraft3-en":
        log("Trying fallback soundpack warcraft3-en")
        sound_file = get_sound_file(plugin_root / "soundpacks" / "warcraft3-en", sound_type)

    if not sound_file:
        log("No sound file found, exiting")
        return

    log(f"Final sound file: {sound_file}")
    play_sound_async(sound_file)


# --- Subcommand: play ---


def cmd_play(args):
    if not args:
        print("Usage: cli.py play <type>", file=sys.stderr)
        sys.exit(1)
    sound_type = args[0]
    log(f"play: type={sound_type}")
    play_by_type(sound_type)


# --- Subcommand: check-stop ---


def cmd_check_stop():
    log("check-stop started")

    # Read stdin
    try:
        input_text = sys.stdin.read()
        log(f"stdin length: {len(input_text)}")
        log(f"stdin preview: {input_text[:500] if input_text else 'EMPTY'}")
    except Exception as e:
        log(f"Error reading stdin: {e}")
        input_text = ""

    last_assistant_message = get_last_assistant_message(input_text)
    if last_assistant_message:
        log(f"last_assistant_message preview: {last_assistant_message[:500]}")

    if not last_assistant_message:
        log("No last_assistant_message found; skipping error sound")
        return

    if not STOP_ERROR_PATTERN.search(last_assistant_message):
        log("Stop payload did not look like an error; skipping")
        return

    log("Detected error in last_assistant_message")
    play_by_type("error")
    log("check-stop done")


# --- Subcommand: soundpack ---


def cmd_soundpack_list():
    plugin_root = get_plugin_root()
    packs_dir = plugin_root / "soundpacks"

    if not packs_dir.exists():
        print("[]")
        return

    entries = []
    for entry in sorted(packs_dir.iterdir()):
        if not entry.is_dir():
            continue
        display_name = entry.name
        description = ""
        json_file = entry / "soundpack.json"
        if json_file.exists():
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("name"):
                    display_name = data["name"]
                if data.get("description"):
                    description = data["description"]
            except Exception:
                pass
        entries.append({
            "name": entry.name,
            "displayName": display_name,
            "description": description,
        })

    print(json.dumps(entries, indent=2))


def cmd_soundpack_get():
    print(get_soundpack())


def cmd_soundpack_set(args):
    if not args:
        print("Usage: cli.py soundpack set <name>", file=sys.stderr)
        sys.exit(1)

    name = args[0]
    plugin_root = get_plugin_root()
    pack_dir = plugin_root / "soundpacks" / name

    if not pack_dir.exists():
        print(f"Soundpack '{name}' not found in {plugin_root / 'soundpacks'}", file=sys.stderr)
        sys.exit(1)

    config_dir = os.environ.get("CLAUDE_CONFIG_DIR") or str(Path.home() / ".claude")
    config_path = Path(config_dir)
    config_path.mkdir(parents=True, exist_ok=True)

    settings_file = config_path / "claudecode-sounds.json"
    data = {}
    if settings_file.exists():
        try:
            data = json.loads(settings_file.read_text(encoding="utf-8"))
        except Exception as e:
            log(f"Error reading existing settings: {e}")
    data["soundpack"] = name
    settings_file.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    log(f"Soundpack set to: {name}")
    play_by_type("complete")


def cmd_soundpack(args):
    if not args:
        print("Usage: cli.py soundpack <list|get|set>", file=sys.stderr)
        sys.exit(1)

    sub = args[0]
    if sub == "list":
        cmd_soundpack_list()
    elif sub == "get":
        cmd_soundpack_get()
    elif sub == "set":
        cmd_soundpack_set(args[1:])
    else:
        print("Usage: cli.py soundpack <list|get|set>", file=sys.stderr)
        sys.exit(1)


# --- CLI Router ---


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: cli.py <play|check-stop|soundpack> [args...]", file=sys.stderr)
        sys.exit(1)

    command = args[0]
    if command == "play":
        cmd_play(args[1:])
    elif command == "check-stop":
        cmd_check_stop()
    elif command == "soundpack":
        cmd_soundpack(args[1:])
    else:
        print("Usage: cli.py <play|check-stop|soundpack> [args...]", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
