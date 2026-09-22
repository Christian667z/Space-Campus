<#
  scripts/build_asta.ps1
  - Pack and prepare AstaAcademie distribution into dist\build_asta
  - Steps: run frontend build, run pyinstaller on main_qt.py (or use existing exe), copy files, compute SHA256
#>

param(
	[string]$RepoRoot = "$(Split-Path -Parent $PSScriptRoot)",
	[string]$OutDir = "$(Split-Path -Parent $PSScriptRoot)\dist\build_asta"
)

Set-StrictMode -Version Latest
Write-Host "[build_asta] RepoRoot = $RepoRoot"

Push-Location $RepoRoot

# 1) Build frontend
if (Test-Path "frontend") {
	Write-Host "Building frontend..."
	Push-Location frontend
	npm ci
	npm run build
	Pop-Location
}

# 2) Ensure out dir
if (-Not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir | Out-Null }

# 3) Build python exe with pyinstaller (if available)
if (Get-Command pyinstaller -ErrorAction SilentlyContinue) {
	Write-Host "Running pyinstaller on main_qt.py..."
	pyinstaller --onefile --noconsole --add-data "frontend/dist;frontend/dist" --name AstaAcademie main_qt.py
	$exe = Join-Path $RepoRoot "dist\AstaAcademie.exe"
	if (Test-Path $exe) { Copy-Item $exe $OutDir -Force }
}

# 4) Copy additional artifacts (data, student_notes)
$extras = @('data','student_notes','native\build\Release\native.dll')
foreach ($e in $extras) {
	$src = Join-Path $RepoRoot $e
	if (Test-Path $src) {
		Write-Host "Copying $e"
		Copy-Item $src $OutDir -Recurse -Force -ErrorAction SilentlyContinue
	}
}

# 5) Compute SHA256
if (Get-Command Get-FileHash -ErrorAction SilentlyContinue) {
	$exePath = Join-Path $OutDir "AstaAcademie.exe"
	if (Test-Path $exePath) {
		$hash = Get-FileHash -Path $exePath -Algorithm SHA256
		$hash.Hash | Out-File -FilePath (Join-Path $OutDir "AstaAcademie.sha256") -Encoding ASCII
		Write-Host "SHA256: $($hash.Hash)"
	}
}

Pop-Location
Write-Host "build_asta complete -> $OutDir"
