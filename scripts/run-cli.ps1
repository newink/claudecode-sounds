$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pluginRoot = Split-Path -Parent $scriptDir

if (Get-Command node -ErrorAction SilentlyContinue) {
    & node "$pluginRoot/hooks/cli.mjs" @args
    exit $LASTEXITCODE
}

if (Get-Command python3 -ErrorAction SilentlyContinue) {
    & python3 "$pluginRoot/hooks/cli.py" @args
    exit $LASTEXITCODE
}

if (Get-Command python -ErrorAction SilentlyContinue) {
    & python "$pluginRoot/hooks/cli.py" @args
    exit $LASTEXITCODE
}

if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 "$pluginRoot/hooks/cli.py" @args
    exit $LASTEXITCODE
}

Write-Error "claudecode-sounds: neither node, python3, python, nor py -3 is available"
exit 127
