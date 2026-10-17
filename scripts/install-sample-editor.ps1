# Windows x64. Python bootstrap is opt-in, version-pinned and checksum-verified.
param(
    [ValidateSet('auto', 'qt', 'tk')][string]$Ui = 'auto',
    [switch]$InstallPython
)
$ErrorActionPreference = 'Stop'
$projectDir = Split-Path -Parent $PSScriptRoot
$pythonExe = $null
if (Get-Command py -ErrorAction SilentlyContinue) {
    try {
        $candidate = & py -3.12 -c 'import sys; print(sys.executable)' 2>$null
        if ($LASTEXITCODE -eq 0) { $pythonExe = $candidate }
    } catch {
        # A launcher for another Python version may be present. Bootstrap below if requested.
        $pythonExe = $null
    }
}
$localPython = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python312\python.exe'
if (-not $pythonExe -and (Test-Path $localPython)) { $pythonExe = $localPython }
if (-not $pythonExe -and $InstallPython) {
    if (-not [Environment]::Is64BitOperatingSystem) { throw 'The bundled setup targets Windows x64.' }
    $targetDir = Split-Path -Parent $localPython
    $download = Join-Path ([IO.Path]::GetTempPath()) ('case-editor-python-' + [guid]::NewGuid() + '.exe')
    try {
        # Official Python archive. SHA-256 cross-checked against Microsoft's winget manifest:
        # https://github.com/microsoft/winget-pkgs/blob/master/manifests/p/Python/Python/3/12/3.12.10/Python.Python.3.12.installer.yaml
        Invoke-WebRequest -UseBasicParsing -Uri 'https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe' -OutFile $download
        if ((Get-FileHash -Algorithm SHA256 $download).Hash -ne '67B5635E80EA51072B87941312D00EC8927C4DB9BA18938F7AD2D27B328B95FB') {
            throw 'Python installer checksum mismatch.'
        }
        $process = Start-Process -FilePath $download -Wait -PassThru -ArgumentList @(
            '/quiet', 'InstallAllUsers=0', 'Include_launcher=1', 'InstallLauncherAllUsers=0',
            'Include_tcltk=1', 'Include_pip=0', 'Include_test=0', 'PrependPath=0', "TargetDir=`"$targetDir`"")
        if ($process.ExitCode -notin @(0, 3010)) { throw "Python installation failed: $($process.ExitCode)" }
        $pythonExe = $localPython
    } finally {
        if (Test-Path $download) { Remove-Item -LiteralPath $download }
    }
}
if (-not $pythonExe) {
    throw 'Python 3.12 was not found. Rerun with -InstallPython to install verified Python 3.12.10 for this user.'
}
& $pythonExe "$projectDir\scripts\install-sample-editor.py" --ui $Ui
if ($LASTEXITCODE -ne 0) { throw 'Sample editor installation failed.' }
Write-Output 'Start with scripts\run-sample-editor.cmd, optionally followed by samples\ru-v2.'
