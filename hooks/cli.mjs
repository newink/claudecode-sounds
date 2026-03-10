/**
 * Unified CLI for claudecode-sounds plugin.
 *
 * Usage:
 *   node cli.mjs play <type>           - play a sound (question/complete/error/permission)
 *   node cli.mjs check-stop            - read Stop hook JSON, play error on failed turns
 *   node cli.mjs soundpack list        - list available soundpacks as JSON
 *   node cli.mjs soundpack get         - print current active soundpack name
 *   node cli.mjs soundpack set <name>  - set soundpack, play test sound
 */

import { spawn } from 'child_process';
import { existsSync, readFileSync, readdirSync, writeFileSync, mkdirSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import { homedir, platform } from 'os';

const DEBUG = false;
const STOP_ERROR_PATTERN = /\b(error|failed|failure|exception|cannot|can't|unable to|fatal|denied|not found)\b|exit code [1-9]|exit status [1-9]/i;

function log(msg) {
  if (DEBUG) {
    process.stderr.write(`[cli] ${msg}\n`);
  }
}

async function readStdinText() {
  try {
    const chunks = [];
    for await (const chunk of process.stdin) {
      chunks.push(chunk);
    }
    return Buffer.concat(chunks).toString('utf-8');
  } catch (e) {
    log(`Error reading stdin: ${e}`);
    return '';
  }
}

function getLastAssistantMessage(inputText) {
  if (!inputText) return '';

  try {
    const payload = JSON.parse(inputText);
    const message = payload && typeof payload.last_assistant_message === 'string'
      ? payload.last_assistant_message
      : '';
    log(`Parsed Stop payload with last_assistant_message length: ${message.length}`);
    return message;
  } catch (e) {
    log(`Error parsing hook payload JSON: ${e}`);
    return '';
  }
}

// --- Shared utilities ---

export function getPluginRoot() {
  const envRoot = process.env.CLAUDE_PLUGIN_ROOT;
  log(`CLAUDE_PLUGIN_ROOT env: ${envRoot || 'NOT SET'}`);
  if (envRoot) return envRoot;
  const fallback = join(dirname(fileURLToPath(import.meta.url)), '..');
  log(`Using fallback plugin root: ${fallback}`);
  return fallback;
}

export function getSoundpack() {
  const configDir = process.env.CLAUDE_CONFIG_DIR || join(homedir(), '.claude');
  log(`CLAUDE_CONFIG_DIR: ${configDir}`);

  // Try JSON format first
  const jsonFile = join(configDir, 'claudecode-sounds.json');
  log(`JSON settings: ${jsonFile}, exists: ${existsSync(jsonFile)}`);
  if (existsSync(jsonFile)) {
    try {
      const data = JSON.parse(readFileSync(jsonFile, 'utf-8'));
      if (data.soundpack) {
        log(`Using soundpack from JSON: ${data.soundpack}`);
        return data.soundpack;
      }
    } catch (e) {
      log(`Error reading JSON settings: ${e}`);
    }
  }

  // Fall back to old markdown format
  const mdFile = join(configDir, 'claudecode-sounds.local.md');
  log(`Fallback MD settings: ${mdFile}, exists: ${existsSync(mdFile)}`);
  if (existsSync(mdFile)) {
    try {
      const content = readFileSync(mdFile, 'utf-8');
      if (content.startsWith('---')) {
        const end = content.indexOf('---', 3);
        if (end !== -1) {
          const frontmatter = content.slice(3, end);
          for (const line of frontmatter.split('\n')) {
            if (line.trim().startsWith('soundpack:')) {
              const value = line.split(':', 2)[1].trim().replace(/^["']|["']$/g, '');
              if (value) {
                log(`Using soundpack from MD fallback: ${value}`);
                return value;
              }
            }
          }
        }
      }
    } catch (e) {
      log(`Error reading MD settings: ${e}`);
    }
  }

  log(`Using default soundpack: warcraft3-en`);
  return 'warcraft3-en';
}

export function getSoundFile(packDir, soundType) {
  log(`Looking for sound '${soundType}' in ${packDir}`);
  const jsonFile = join(packDir, 'soundpack.json');

  if (!existsSync(jsonFile)) {
    const direct = join(packDir, `${soundType}.wav`);
    log(`No soundpack.json, trying direct: ${direct}, exists: ${existsSync(direct)}`);
    if (existsSync(direct)) return direct;
    return null;
  }

  try {
    const data = JSON.parse(readFileSync(jsonFile, 'utf-8'));
    const soundValue = (data.sounds || {})[soundType];
    log(`Sound value from JSON: ${soundValue}`);
    if (!soundValue) return null;

    let filename;
    if (Array.isArray(soundValue)) {
      filename = soundValue[Math.floor(Math.random() * soundValue.length)];
    } else {
      filename = soundValue;
    }

    const resolved = join(packDir, filename);
    log(`Resolved sound file: ${resolved}, exists: ${existsSync(resolved)}`);
    if (existsSync(resolved)) return resolved;
  } catch (e) {
    log(`Error reading soundpack.json: ${e}`);
    const direct = join(packDir, `${soundType}.wav`);
    if (existsSync(direct)) return direct;
  }

  return null;
}

function startProcess(command, args, options = {}) {
  return new Promise((resolve, reject) => {
    const {
      waitForExit = false,
      detached = true,
      ...spawnOptions
    } = options;

    let proc;
    try {
      proc = spawn(command, args, {
        detached,
        stdio: 'ignore',
        ...spawnOptions,
      });
    } catch (e) {
      if (e.code === 'ENOENT') {
        resolve(false);
        return;
      }
      reject(e);
      return;
    }

    let settled = false;
    const settle = (fn, value) => {
      if (settled) return;
      settled = true;
      fn(value);
    };

    proc.once('spawn', () => {
      log(`${command} started with PID: ${proc.pid}`);

      if (!waitForExit) {
        if (detached) {
          proc.unref();
        }
        settle(resolve, true);
      }
    });

    proc.once('error', (e) => {
      if (e.code === 'ENOENT') {
        log(`${command} not found`);
        settle(resolve, false);
        return;
      }
      settle(reject, e);
    });

    if (waitForExit) {
      proc.once('exit', (code, signal) => {
        log(`${command} exited with code=${code} signal=${signal || 'none'}`);
        settle(resolve, code === 0);
      });
    }
  });
}

export async function playSoundAsync(soundFile) {
  const os = platform();
  log(`Playing sound on ${os}: ${soundFile}`);

  try {
    if (os === 'win32') {
      const escaped = soundFile.replace(/'/g, "''");
      const commands = [
        ['powershell.exe', '-NoProfile', '-Command', `(New-Object Media.SoundPlayer '${escaped}').PlaySync()`],
        ['pwsh', '-NoProfile', '-Command', `(New-Object Media.SoundPlayer '${escaped}').PlaySync()`],
        ['powershell', '-NoProfile', '-Command', `(New-Object Media.SoundPlayer '${escaped}').PlaySync()`],
      ];
      let started = false;
      for (const command of commands) {
        started = await startProcess(command[0], command.slice(1), {
          detached: false,
          waitForExit: true,
          windowsHide: true,
        });
        if (started) {
          break;
        }
      }
      if (!started) {
        log('No usable PowerShell runtime found');
      }
    } else if (os === 'darwin') {
      log('Using afplay');
      const started = await startProcess('afplay', [soundFile]);
      if (!started) {
        log('afplay not found');
      }
    } else {
      // Linux
      const players = [
        ['paplay', soundFile],
        ['aplay', '-q', soundFile],
        ['mpv', '--no-video', '--really-quiet', soundFile],
        ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', soundFile],
      ];
      let found = false;
      for (const cmd of players) {
        try {
          log(`Trying: ${cmd[0]}`);
          found = await startProcess(cmd[0], cmd.slice(1));
          if (found) {
            break;
          }
        } catch (e) {
          throw e;
        }
      }
      if (!found) {
        console.log(JSON.stringify({
          systemMessage: "claudecode-sounds: No audio player found. Install one of: pulseaudio-utils, alsa-utils, mpv, or ffmpeg."
        }));
      }
    }
  } catch (e) {
    log(`Error playing sound: ${e}`);
  }
}

export async function playByType(soundType) {
  if (!soundType) return;

  const pluginRoot = getPluginRoot();
  const soundpack = getSoundpack();

  let soundFile = getSoundFile(join(pluginRoot, 'soundpacks', soundpack), soundType);

  if (!soundFile && soundpack !== 'warcraft3-en') {
    log('Trying fallback soundpack warcraft3-en');
    soundFile = getSoundFile(join(pluginRoot, 'soundpacks', 'warcraft3-en'), soundType);
  }

  if (!soundFile) {
    log('No sound file found, exiting');
    return;
  }

  log(`Final sound file: ${soundFile}`);
  await playSoundAsync(soundFile);
}

// --- Subcommand: play ---

async function cmdPlay(args) {
  const soundType = args[0];
  if (!soundType) {
    console.error('Usage: cli.mjs play <type>');
    process.exit(1);
  }
  log(`play: type=${soundType}`);
  await playByType(soundType);
}

// --- Subcommand: check-stop ---

async function cmdCheckStop() {
  log('check-stop started');

  const inputText = await readStdinText();
  log(`stdin length: ${inputText.length}`);
  log(`stdin preview: ${inputText.slice(0, 500) || 'EMPTY'}`);

  const lastAssistantMessage = getLastAssistantMessage(inputText);
  if (lastAssistantMessage) {
    log(`last_assistant_message preview: ${lastAssistantMessage.slice(0, 500)}`);
  }

  if (!lastAssistantMessage) {
    log('No last_assistant_message found; skipping error sound');
    return;
  }

  if (!STOP_ERROR_PATTERN.test(lastAssistantMessage)) {
    log('Stop payload did not look like an error; skipping');
    return;
  }

  log('Detected error in last_assistant_message');
  await playByType('error');
  log('check-stop done');
}

// --- Subcommand: soundpack ---

function cmdSoundpackList() {
  const pluginRoot = getPluginRoot();
  const packsDir = join(pluginRoot, 'soundpacks');

  if (!existsSync(packsDir)) {
    console.log('[]');
    return;
  }

  const entries = readdirSync(packsDir, { withFileTypes: true })
    .filter(e => e.isDirectory())
    .map(e => {
      const packDir = join(packsDir, e.name);
      const jsonFile = join(packDir, 'soundpack.json');
      let displayName = e.name;
      let description = '';

      if (existsSync(jsonFile)) {
        try {
          const data = JSON.parse(readFileSync(jsonFile, 'utf-8'));
          if (data.name) displayName = data.name;
          if (data.description) description = data.description;
        } catch (_) {}
      }

      return { name: e.name, displayName, description };
    });

  console.log(JSON.stringify(entries, null, 2));
}

function cmdSoundpackGet() {
  console.log(getSoundpack());
}

async function cmdSoundpackSet(args) {
  const name = args[0];
  if (!name) {
    console.error('Usage: cli.mjs soundpack set <name>');
    process.exit(1);
  }

  const pluginRoot = getPluginRoot();
  const packDir = join(pluginRoot, 'soundpacks', name);

  if (!existsSync(packDir)) {
    console.error(`Soundpack '${name}' not found in ${join(pluginRoot, 'soundpacks')}`);
    process.exit(1);
  }

  const configDir = process.env.CLAUDE_CONFIG_DIR || join(homedir(), '.claude');
  if (!existsSync(configDir)) {
    mkdirSync(configDir, { recursive: true });
  }

  const settingsFile = join(configDir, 'claudecode-sounds.json');
  let data = {};
  if (existsSync(settingsFile)) {
    try {
      data = JSON.parse(readFileSync(settingsFile, 'utf-8'));
    } catch (e) {
      log(`Error reading existing settings: ${e}`);
    }
  }
  data.soundpack = name;
  writeFileSync(settingsFile, JSON.stringify(data, null, 2) + '\n', 'utf-8');

  log(`Soundpack set to: ${name}`);
  await playByType('complete');
}

async function cmdSoundpack(args) {
  const sub = args[0];
  switch (sub) {
    case 'list':
      cmdSoundpackList();
      break;
    case 'get':
      cmdSoundpackGet();
      break;
    case 'set':
      await cmdSoundpackSet(args.slice(1));
      break;
    default:
      console.error('Usage: cli.mjs soundpack <list|get|set>');
      process.exit(1);
  }
}

// --- CLI Router ---

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'play':
      await cmdPlay(args.slice(1));
      break;
    case 'check-stop':
      await cmdCheckStop();
      break;
    case 'soundpack':
      await cmdSoundpack(args.slice(1));
      break;
    default:
      console.error('Usage: cli.mjs <play|check-stop|soundpack> [args...]');
      process.exit(1);
  }
}

main().catch((e) => {
  log(`Unhandled error: ${e && e.stack ? e.stack : e}`);
  process.exit(1);
});
