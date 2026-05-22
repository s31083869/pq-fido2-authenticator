$ErrorActionPreference = "Stop"

$HostVersion = "1.0.0"
$HostPlatform = "windows-hello"

function Read-NativeMessage {
    $inputStream = [Console]::OpenStandardInput()
    $lengthBytes = New-Object byte[] 4
    $read = $inputStream.Read($lengthBytes, 0, 4)
    if ($read -ne 4) {
        throw "Invalid native messaging frame"
    }

    $length = [BitConverter]::ToUInt32($lengthBytes, 0)
    if ($length -le 0 -or $length -gt 1048576) {
        throw "Invalid native messaging message length"
    }

    $payload = New-Object byte[] $length
    $offset = 0
    while ($offset -lt $length) {
        $chunk = $inputStream.Read($payload, $offset, $length - $offset)
        if ($chunk -le 0) {
            throw "Unexpected end of native messaging frame"
        }
        $offset += $chunk
    }

    $json = [Text.Encoding]::UTF8.GetString($payload)
    return $json | ConvertFrom-Json
}

function Write-NativeMessage {
    param(
        [Parameter(Mandatory = $true)]
        [hashtable] $Response
    )

    $json = $Response | ConvertTo-Json -Compress -Depth 8
    $payload = [Text.Encoding]::UTF8.GetBytes($json)
    $lengthBytes = [BitConverter]::GetBytes([UInt32]$payload.Length)
    $outputStream = [Console]::OpenStandardOutput()
    $outputStream.Write($lengthBytes, 0, $lengthBytes.Length)
    $outputStream.Write($payload, 0, $payload.Length)
    $outputStream.Flush()
}

function Await-WinRtOperation {
    param(
        [Parameter(Mandatory = $true)]
        $Operation,
        [Parameter(Mandatory = $true)]
        [Type] $ResultType
    )

    Add-Type -AssemblyName System.Runtime.WindowsRuntime
    $asTask = [System.WindowsRuntimeSystemExtensions].GetMethods() |
        Where-Object {
            $_.Name -eq "AsTask" -and
            $_.IsGenericMethodDefinition -and
            $_.GetParameters().Count -eq 1
        } |
        Select-Object -First 1

    $task = $asTask.MakeGenericMethod($ResultType).Invoke($null, @($Operation))
    $task.Wait()
    return $task.Result
}

function Get-WindowsHelloAvailability {
    $verifier = [Windows.Security.Credentials.UI.UserConsentVerifier, Windows.Security.Credentials.UI, ContentType = WindowsRuntime]
    $availabilityType = [Windows.Security.Credentials.UI.UserConsentVerifierAvailability, Windows.Security.Credentials.UI, ContentType = WindowsRuntime]
    return Await-WinRtOperation -Operation ($verifier::CheckAvailabilityAsync()) -ResultType $availabilityType
}

function Test-WindowsHelloReady {
    $availability = Get-WindowsHelloAvailability
    if ($availability.ToString() -eq "Available") {
        return @{ ok = $true; message = "ready" }
    }

    return @{
        ok = $false
        message = "Windows Hello is not available: $availability"
    }
}

function Invoke-WindowsHelloVerification {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Reason
    )

    $ready = Test-WindowsHelloReady
    if (-not $ready.ok) {
        return $ready
    }

    $verifier = [Windows.Security.Credentials.UI.UserConsentVerifier, Windows.Security.Credentials.UI, ContentType = WindowsRuntime]
    $resultType = [Windows.Security.Credentials.UI.UserConsentVerificationResult, Windows.Security.Credentials.UI, ContentType = WindowsRuntime]
    $result = Await-WinRtOperation -Operation ($verifier::RequestVerificationAsync($Reason)) -ResultType $resultType

    if ($result.ToString() -eq "Verified") {
        return @{ ok = $true; message = "verified" }
    }

    return @{
        ok = $false
        message = "Windows Hello verification failed: $result"
    }
}

try {
    $request = Read-NativeMessage
    $requestId = if ($request.requestId) { [string]$request.requestId } else { "unknown" }

    if ($request.type -eq "uv-status") {
        $status = Test-WindowsHelloReady
        Write-NativeMessage @{
            type = "uv-status-result"
            requestId = $requestId
            ok = $status.ok
            version = $HostVersion
            platform = $HostPlatform
            message = $status.message
        }
        exit 0
    }

    if ($request.type -ne "uv-request") {
        Write-NativeMessage @{
            type = "uv-result"
            requestId = $requestId
            ok = $false
            version = $HostVersion
            platform = $HostPlatform
            message = "Invalid request type"
        }
        exit 0
    }

    $reason = if ($request.reason) { [string]$request.reason } else { "Verify with Windows Hello" }
    $result = Invoke-WindowsHelloVerification -Reason $reason
    Write-NativeMessage @{
        type = "uv-result"
        requestId = $requestId
        ok = $result.ok
        version = $HostVersion
        platform = $HostPlatform
        message = $result.message
    }
} catch {
    Write-NativeMessage @{
        type = "uv-result"
        requestId = "unknown"
        ok = $false
        version = $HostVersion
        platform = $HostPlatform
        message = $_.Exception.Message
    }
    exit 1
}
