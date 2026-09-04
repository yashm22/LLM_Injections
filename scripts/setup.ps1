$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

$python = Get-Command python -ErrorAction SilentlyContinue
if ($python -and $python.Source -notlike '*WindowsApps*') {
    & $python.Source -m venv .venv
} else {
    $launcher = Get-Command py -ErrorAction SilentlyContinue
    $defaultPython = Join-Path $env:LocalAppData 'Programs\Python\Python312\python.exe'
    if ($launcher) {
        & $launcher.Source -3.12 -m venv .venv
    } elseif (Test-Path -LiteralPath $defaultPython) {
        & $defaultPython -m venv .venv
    } else {
        throw 'A usable Python installation was not found. Close and reopen PowerShell, then rerun this script.'
    }
}
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
Write-Host 'Setup complete. Activate with: .\.venv\Scripts\Activate.ps1'
