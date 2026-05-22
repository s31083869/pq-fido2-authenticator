param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string] $ExtensionId
)

$ErrorActionPreference = "Stop"

& (Join-Path $PSScriptRoot "build-native-host-windows.ps1")
& (Join-Path $PSScriptRoot "install-native-host-windows.ps1") $ExtensionId

Write-Host "[setup:windows-hello] done"
Write-Host "[setup:windows-hello] next:"
Write-Host "  1) reload extension in chrome://extensions"
Write-Host "  2) open extension options"
Write-Host "  3) set UV mode = native-windows-hello"
