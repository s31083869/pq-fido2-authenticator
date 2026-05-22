$ErrorActionPreference = "Stop"

$RootDir = Resolve-Path (Join-Path $PSScriptRoot "..")
$OutDir = if ($env:NATIVE_HOST_BUILD_DIR) {
    $env:NATIVE_HOST_BUILD_DIR
} else {
    Join-Path $RootDir ".native-host\bin\windows"
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

Copy-Item -Force -Path (Join-Path $RootDir "native-host\pq_uv_host_windows.ps1") -Destination $OutDir
Copy-Item -Force -Path (Join-Path $RootDir "native-host\pq_uv_host_windows.cmd") -Destination $OutDir

Write-Host "[build:native-host:windows] copied host files to:"
Write-Host "  $OutDir"
