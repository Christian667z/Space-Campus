# PowerShell script to obfuscate and build Python backend using pyarmor and pyinstaller
# Usage: .\obfuscate_backend.ps1 -Entry server.py -Out dist_obf
param(
	[string]$Entry = "server.py",
	[string]$Out = "dist_obf"
)

if (-not (Get-Command pyarmor -ErrorAction SilentlyContinue)){
	Write-Error "pyarmor not found in PATH. Install via 'pip install pyarmor'"
	exit 1
}
if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)){
	Write-Error "pyinstaller not found in PATH. Install via 'pip install pyinstaller'"
	exit 1
}

$work = Split-Path -Path $Entry -Parent
Push-Location $work

# 1) obfuscate with pyarmor
pyarmor obfuscate --recursive --output "_obf" $Entry

# 2) build standalone with pyinstaller from obfuscated sources
pyinstaller --noconfirm --onefile --add-data "frontend/dist;frontend/dist" --add-data "student_notes;student_notes" --distpath $Out "_obf\$Entry"

# compute sha256 of the built exe if present
$exe = Join-Path $Out (Split-Path $Entry -LeafBase) + ".exe"
if (Test-Path $exe) {
	Get-FileHash -Path $exe -Algorithm SHA256 | Select-Object -ExpandProperty Hash | Out-File -FilePath (Join-Path $Out "AstaAcademie.sha256")
}

Pop-Location
Write-Output "Obfuscation + build complete. Output in: $Out"