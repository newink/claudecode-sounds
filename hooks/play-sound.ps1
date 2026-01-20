# Cross-platform sound player for claudecode-sounds plugin (Windows PowerShell)
# Usage: powershell -File play-sound.ps1 <sound_type>
# Sound types: question, complete, error, permission
# Supports multiple sounds per event with random selection

param(
    [Parameter(Position=0)]
    [string]$SoundType
)

# Exit silently if no sound type
if (-not $SoundType) {
    exit 0
}

# Determine plugin root
$PluginRoot = if ($env:CLAUDE_PLUGIN_ROOT) {
    $env:CLAUDE_PLUGIN_ROOT
} else {
    Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
}

# Settings file location
$ProjectDir = if ($env:CLAUDE_PROJECT_DIR) { $env:CLAUDE_PROJECT_DIR } else { "." }
$SettingsFile = Join-Path $ProjectDir ".claude\claudecode-sounds.local.md"

# Default soundpack
$Soundpack = "warcraft3-en"

# Read soundpack from settings if exists
if (Test-Path $SettingsFile) {
    $content = Get-Content $SettingsFile -Raw -ErrorAction SilentlyContinue
    if ($content -match '(?s)^---.*?soundpack:\s*[''"]?([^''"}\r\n]+)[''"]?.*?---') {
        $Soundpack = $Matches[1].Trim()
    }
}

function Get-SoundFile {
    param(
        [string]$PackDir,
        [string]$Type
    )

    $JsonFile = Join-Path $PackDir "soundpack.json"

    # If no soundpack.json, try direct file
    if (-not (Test-Path $JsonFile)) {
        $DirectFile = Join-Path $PackDir "$Type.wav"
        if (Test-Path $DirectFile) {
            return $DirectFile
        }
        return $null
    }

    try {
        $json = Get-Content $JsonFile -Raw | ConvertFrom-Json
        $soundValue = $json.sounds.$Type

        if (-not $soundValue) {
            return $null
        }

        # Check if it's an array
        if ($soundValue -is [array]) {
            # Random selection from array
            $index = Get-Random -Minimum 0 -Maximum $soundValue.Count
            $filename = $soundValue[$index]
        } else {
            # Single string value
            $filename = $soundValue
        }

        $resolved = Join-Path $PackDir $filename
        if (Test-Path $resolved) {
            return $resolved
        }
    } catch {
        # JSON parsing failed, try direct file
        $DirectFile = Join-Path $PackDir "$Type.wav"
        if (Test-Path $DirectFile) {
            return $DirectFile
        }
    }

    return $null
}

# Try to get sound file from configured soundpack
$SoundFile = Get-SoundFile -PackDir (Join-Path $PluginRoot "soundpacks\$Soundpack") -Type $SoundType

# Fallback to warcraft3-en if not found
if (-not $SoundFile -and $Soundpack -ne "warcraft3-en") {
    $SoundFile = Get-SoundFile -PackDir (Join-Path $PluginRoot "soundpacks\warcraft3-en") -Type $SoundType
}

# Exit if no sound file found
if (-not $SoundFile) {
    exit 0
}

# Play sound asynchronously using a job (don't block Claude)
Start-Job -ScriptBlock {
    param($file)
    Add-Type -AssemblyName PresentationCore
    $player = New-Object System.Windows.Media.MediaPlayer
    $player.Open([Uri]$file)
    $player.Play()
    # Wait for playback to complete (max 10 seconds)
    Start-Sleep -Seconds 10
} -ArgumentList $SoundFile | Out-Null

exit 0
