"""跨實作驗章：Extension 的 WASM 版 liboqs 簽章，交給 RP 的 Python liboqs 驗章（Day 7 T5）。

背景：Extension 用 Emscripten 編譯的 liboqs（commit 33815beb，決策 D4），RP 用原生 liboqs 0.14.0
（liboqs-python）。兩份是分別編譯的實作；這個測試證明 WASM 簽出來的簽章，RP 真的驗得過，
也就是 CLAUDE.md「真實密碼學」要求的「產生金鑰 → 簽章 → RP 驗章」在 Extension 這一側真的跑起來。

做法：執行 extension/scripts/wasm-sign-vectors.ts（需要 bun；CI 的 Python 工作已安裝），
它用進 git 的 extension/public/wasm/pq_bridge.wasm 對每個演算法產生金鑰並簽一則固定訊息；
這裡用 RP 自己的演算法對照 _cose_to_oqs() 取得 liboqs 名稱，再以 Python liboqs 驗章。
依據：workflow.md F11、F15、F17；WebAuthn §7.2（RP 以公鑰驗證簽章）。
"""

from __future__ import annotations

import base64
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict

import oqs
import pytest

from rp_server.services import _cose_to_oqs

ROOT = Path(__file__).resolve().parents[2]
VECTOR_SCRIPT = ROOT / "extension" / "scripts" / "wasm-sign-vectors.ts"

# 五個演算法的 COSE 編號（決策 D1；RFC 9964 與 draft-ietf-cose-falcon）
ALGORITHMS = [
    pytest.param(-48, id="ML-DSA-44"),
    pytest.param(-49, id="ML-DSA-65"),
    pytest.param(-50, id="ML-DSA-87"),
    pytest.param(-54, id="FN-DSA-512"),
    pytest.param(-55, id="FN-DSA-1024"),
]


@pytest.fixture(scope="module")
def wasm_vectors() -> Dict[int, dict]:
    """執行一次 bun 腳本，取得 WASM 對每個演算法產生的公鑰、訊息與簽章。

    輸出：COSE 編號 → 該演算法的結果（成功時有 publicKey／message／signature，失敗時有 error）。
    找不到 bun 時直接失敗而不是跳過：使用者決定這個測試要在 CI 上真的執行（Day 7「待你決定」第 3 點）。
    """
    bun = shutil.which("bun")
    assert bun is not None, (
        "bun is required to run the WASM signer (see CI setup-bun step)"
    )
    completed = subprocess.run(
        [bun, str(VECTOR_SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=300,
        check=True,
    )
    return {entry["alg"]: entry for entry in json.loads(completed.stdout)}


def _decode(entry: dict, field: str) -> bytes:
    """把腳本輸出的 base64 欄位解回 bytes。"""
    return base64.b64decode(entry[field])


@pytest.mark.parametrize("alg", ALGORITHMS)
def test_rp_verifies_signature_made_by_wasm(
    wasm_vectors: Dict[int, dict], alg: int
) -> None:
    """T5：WASM 產生的簽章，RP 端的 Python liboqs 驗章成功；簽章最後一個 byte 翻轉後驗章失敗。

    翻轉的那一組同時是破壞檢查：驗章若不論輸入都回傳成功，這裡會失敗。
    """
    entry = wasm_vectors[alg]
    assert "error" not in entry, f"WASM failed for COSE alg {alg}: {entry.get('error')}"

    public_key = _decode(entry, "publicKey")
    message = _decode(entry, "message")
    signature = _decode(entry, "signature")
    tampered = signature[:-1] + bytes([signature[-1] ^ 0x01])

    # 和 RP 登入驗章完全相同的路徑：COSE 編號 → 共用演算法表的 liboqs 名稱 → oqs.Signature.verify
    with oqs.Signature(_cose_to_oqs(alg)) as verifier:
        assert verifier.verify(message, signature, public_key) is True
        assert verifier.verify(message, tampered, public_key) is False
