# PowerShell helper to run ConfuserEx on a built .NET exe
# Requires ConfuserEx installed and confuser.CLI available
param(
	[string]$ExePath = "./bin/Release/net7.0/AstaAcademie.exe",
	[string]$ProjectDir = "."
)

if (-not (Test-Path $ExePath)){
	Write-Error "Exe not found: $ExePath -- build your project in Release first"
	exit 1
}

if (-not (Get-Command Confuser.CLI -ErrorAction SilentlyContinue)){
	Write-Error "Confuser.CLI not found. Install ConfuserEx and add to PATH."
	exit 1
}

# Simple confuser project file creation
$proj = @"
<?xml version="1.0"?>
<project outputDir="confused_output" baseDir=".">
  <module path="$ExePath">
	<rule pattern="true" preset="maximum" />
  </module>
</project>
"@
$cfg = Join-Path $ProjectDir "confuser_project.crproj"
$proj | Out-File -Encoding utf8 $cfg

Confuser.CLI -n $cfg
Write-Output "Confuser run completed. See confused_output folder."