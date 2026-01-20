# Check if session ended with error and play appropriate sound
# Used as Stop hook (Windows PowerShell version)

param()

# Determine plugin root
$PluginRoot = if ($env:CLAUDE_PLUGIN_ROOT) {
    $env:CLAUDE_PLUGIN_ROOT
} else {
    Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
}

# Read stdin
$Input = [Console]::In.ReadToEnd()

# Check for error indicators
$ErrorPatterns = 'error|failed|exception|exit code [1-9]|exit status [1-9]|cannot |fatal:|denied|not found'
if ($Input -match $ErrorPatterns) {
    $SoundType = "error"
} else {
    $SoundType = "complete"
}

# Play sound
$SoundScript = Join-Path $PluginRoot "hooks\play-sound.ps1"
Start-Process -NoNewWindow -FilePath "powershell" -ArgumentList "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $SoundScript, $SoundType

exit 0
