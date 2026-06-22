param(
  [string]$AppName = "EssayGrader",
  [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Frontend = Join-Path $Root "frontend"
$Backend = Join-Path $Root "backend"
$VenvPython = Join-Path $Backend ".venv\Scripts\python.exe"
$DistDir = Join-Path $Root "release"
$WorkDir = Join-Path $Root "build\pyinstaller"

Write-Host "==> Building frontend"
Push-Location $Frontend
try {
  if (-not $SkipInstall -and -not (Test-Path "node_modules")) {
    npm install
  }
  npm run build
}
finally {
  Pop-Location
}

Write-Host "==> Preparing Python environment"
Push-Location $Backend
try {
  if (-not (Test-Path $VenvPython)) {
    python -m venv .venv
  }
  if (-not $SkipInstall) {
    & $VenvPython -m pip install --upgrade pip
    & $VenvPython -m pip install -r requirements.txt
    & $VenvPython -m pip install pyinstaller
  }

  $StaticData = "$Backend\static;static"
  $TemplatesData = "$Backend\templates;templates"
  $FrontendDistData = "$Frontend\dist;frontend_dist"

  Write-Host "==> Packaging Windows executable"
  if (Test-Path $DistDir) {
    Remove-Item -LiteralPath $DistDir -Recurse -Force
  }

  & $VenvPython -m PyInstaller `
    --noconfirm `
    --clean `
    --onedir `
    --name $AppName `
    --distpath $DistDir `
    --workpath $WorkDir `
    --specpath $WorkDir `
    --add-data $StaticData `
    --add-data $TemplatesData `
    --add-data $FrontendDistData `
    --collect-submodules passlib `
    --collect-submodules jose `
    --collect-submodules uvicorn `
    run_windows.py
}
finally {
  Pop-Location
}

$PackageDir = Join-Path $DistDir $AppName
$Readme = Join-Path $PackageDir "README-Windows.txt"
if (-not (Test-Path $PackageDir)) {
  New-Item -ItemType Directory -Path $PackageDir -Force | Out-Null
}
$ReadmeText = @(
  "Essay Grader - Windows portable package",
  "",
  "How to start:",
  "1. Double-click $AppName.exe",
  "2. Wait a few seconds. The browser opens http://127.0.0.1:8000",
  "3. Default admin account: admin / admin123",
  "",
  "Recommended school-wide usage:",
  "1. Put this folder on one always-on Windows computer or server.",
  "2. Double-click $AppName.exe on that computer.",
  "3. Other teachers on the same LAN open http://SERVER-LAN-IP:8000",
  "   Example: http://192.168.1.25:8000",
  "4. If other computers cannot open it, allow inbound TCP port 8000 in Windows Firewall.",
  "",
  "Important files:",
  "- data\database.db: users and grading records",
  "- data\teacher_config.json: model and API key settings",
  "- logs\app.log: application logs",
  "",
  "Backup suggestion:",
  "Back up the whole data folder regularly."
)
$ReadmeText | Set-Content -LiteralPath $Readme -Encoding UTF8

Write-Host ""
Write-Host "Done."
Write-Host "Portable package: $PackageDir"
