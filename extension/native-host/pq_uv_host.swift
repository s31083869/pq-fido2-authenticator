import Foundation
import LocalAuthentication

struct UvRequest: Decodable {
    let type: String
    let requestId: String
    let operation: String?
    let rpId: String?
    let origin: String?
    let reason: String?
    let timeoutMs: Int?
}

struct UvResponse: Encodable {
    let type: String
    let requestId: String
    let ok: Bool
    let version: String?
    let platform: String?
    let message: String?
}

let hostVersion = "1.0.0"
let hostPlatform = "macos-touch-id"

enum HostError: Error {
    case invalidFrame
    case invalidJson
}

func readNativeMessage() throws -> Data {
    let stdin = FileHandle.standardInput
    let lengthData = stdin.readData(ofLength: 4)
    guard lengthData.count == 4 else {
        throw HostError.invalidFrame
    }

    let length = lengthData.withUnsafeBytes { bytes in
        UInt32(littleEndian: bytes.load(as: UInt32.self))
    }
    if length == 0 {
        throw HostError.invalidFrame
    }

    let payload = stdin.readData(ofLength: Int(length))
    guard payload.count == Int(length) else {
        throw HostError.invalidFrame
    }

    return payload
}

func writeNativeMessage(_ data: Data) {
    var length = UInt32(data.count).littleEndian
    let stdout = FileHandle.standardOutput
    withUnsafeBytes(of: &length) { bytes in
        stdout.write(Data(bytes))
    }
    stdout.write(data)
    stdout.synchronizeFile()
}

func sendResponse(_ response: UvResponse) {
    let encoder = JSONEncoder()
    guard let payload = try? encoder.encode(response) else {
        return
    }
    writeNativeMessage(payload)
}

func verifyTouchId(reason: String, timeoutMs: Int) -> (Bool, String?) {
    let context = LAContext()
    var evaluateError: NSError?

    guard context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &evaluateError) else {
        return (false, evaluateError?.localizedDescription ?? "Touch ID is unavailable")
    }

    let semaphore = DispatchSemaphore(value: 0)
    var successResult = false
    var errorMessage: String?

    context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, localizedReason: reason) { success, error in
        successResult = success
        if !success {
            errorMessage = error?.localizedDescription ?? "User verification failed"
        }
        semaphore.signal()
    }

    let timeout = DispatchTime.now() + .milliseconds(max(timeoutMs, 1000))
    if semaphore.wait(timeout: timeout) == .timedOut {
        return (false, "Touch ID prompt timed out")
    }

    return (successResult, errorMessage)
}

func run() {
    do {
        let requestData = try readNativeMessage()
        let decoder = JSONDecoder()
        let request = try decoder.decode(UvRequest.self, from: requestData)

        if request.type == "uv-status" {
            sendResponse(
                UvResponse(
                    type: "uv-status-result",
                    requestId: request.requestId,
                    ok: true,
                    version: hostVersion,
                    platform: hostPlatform,
                    message: "ready"
                )
            )
            return
        }

        guard request.type == "uv-request" else {
            sendResponse(
                UvResponse(
                    type: "uv-result",
                    requestId: request.requestId,
                    ok: false,
                    version: hostVersion,
                    platform: hostPlatform,
                    message: "Invalid request type"
                )
            )
            return
        }

        guard let reason = request.reason else {
            sendResponse(
                UvResponse(
                    type: "uv-result",
                    requestId: request.requestId,
                    ok: false,
                    version: hostVersion,
                    platform: hostPlatform,
                    message: "Missing reason"
                )
            )
            return
        }

        let timeoutMs = request.timeoutMs ?? 15_000
        let result = verifyTouchId(reason: reason, timeoutMs: timeoutMs)
        sendResponse(
            UvResponse(
                type: "uv-result",
                requestId: request.requestId,
                ok: result.0,
                version: hostVersion,
                platform: hostPlatform,
                message: result.1
            )
        )
    } catch {
        // Cannot correlate requestId when frame/json parsing fails; emit generic error and exit.
        sendResponse(
            UvResponse(
                type: "uv-result",
                requestId: "unknown",
                ok: false,
                version: hostVersion,
                platform: hostPlatform,
                message: "Malformed request"
            )
        )
    }
}

run()
