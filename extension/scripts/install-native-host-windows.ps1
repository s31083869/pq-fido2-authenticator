param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string] $ExtensionId,
    [Parameter(Mandatory = $false, Position = 1)]
    [string] $HostCommandPath
)

$ErrorActionPreference = "Stop"

$RootDir = Resolve-Path (Join-Path $PSScriptRoot "..")
$HostName = "com.scalebear.pqwebauthn_uv"

if (-not $HostCommandPath) {
    $HostCommandPath = Join-Path $RootDir ".native-host\bin\windows\pq_uv_host_windows.cmd"
}

if (-not (Test-Path $HostCommandPath)) {
    throw "[install:native-host:windows] host command not found. Run: bun run build:native-host:windows"
}

$ManifestDir = Join-Path $RootDir ".native-host\manifest\windows"
New-Item -ItemType Directory -Force -Path $ManifestDir | Out-Null
$ManifestPath = Join-Path $ManifestDir "$HostName.json"

$manifest = [ordered]@{
    name = $HostName
    description = "PQ WebAuthn native UV host (Windows Hello)"
    path = (Resolve-Path $HostCommandPath).Path
    type = "stdio"
    allowed_origins = @("chrome-extension://$ExtensionId/")
}

$manifest | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 -Path $ManifestPath

$RegistryPath = "HKCU\Software\Google\Chrome\NativeMessagingHosts\$HostName"
& reg.exe ADD $RegistryPath /ve /t REG_SZ /d (Resolve-Path $ManifestPath).Path /f | Out-Null

Write-Host "[install:native-host:windows] installed manifest:"
Write-Host "  $ManifestPath"
Write-Host "[install:native-host:windows] registered:"
Write-Host "  HKEY_CURRENT_USER\Software\Google\Chrome\NativeMessagingHosts\$HostName"
Write-Host "[install:native-host:windows] extension id:"
Write-Host "  $ExtensionId"
