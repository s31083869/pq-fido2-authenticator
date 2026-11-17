"""讀取並檢查共用演算法表 shared/pq-algorithms.json。

WebAuthn 訊息中只傳 COSE 演算法編號（例如 -54），RP 和 authenticator 必須各自把它翻成同一個
liboqs 演算法名稱（例如 Falcon-512），驗章才會成功。這個模組讓兩端都從同一份表取得翻譯，
不再各自寫死對照表（決策 D3）。

模組載入時就讀取並檢查整份表：缺欄位、型別錯誤、狀態值不認得、COSE 編號或 liboqs 名稱重複，
都會立刻拋出 ValueError，讓程式在啟動時就停下來，而不是帶著錯誤的表等到登入驗章才失敗。
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Tuple

# 共用表與本模組放在同一個資料夾；Extension 之後也會讀同一個檔案
REGISTRY_PATH = Path(__file__).with_name("pq-algorithms.json")

# status 的合法值：standard 表示 COSE 編號已由 IANA 正式分配（ML-DSA，RFC 9964）；
# provisional 表示仍是 IETF 草案申請中的暫定編號（FN-DSA，draft-ietf-cose-falcon-04，決策 D1）
VALID_STATUSES = frozenset({"standard", "provisional"})


@dataclass(frozen=True)
class PQAlgorithm:
    """共用表中的一個後量子簽章演算法。建立後不可修改，避免執行期間被改掉。

    欄位：
    - label：給人看的標準名稱，例如 FN-DSA-512。
    - cose_alg：WebAuthn 中代表這個演算法的 COSE 編號，出現在 pubKeyCredParams 與
      credentialPublicKey 的 3（alg）欄位，例如 -54。
    - oqs_name：liboqs 中的演算法名稱，例如 Falcon-512。
    - public_key_bytes、private_key_bytes：公鑰、私鑰的長度（bytes）。
    - signature_bytes：簽章長度（bytes）。signature_length_fixed 為 False 時這是上限：
      Falcon 不補滿的壓縮格式每次簽章長度都不同（Falcon v1.2 第 3.11.6 節）。
    - signature_length_fixed：簽章長度是否每次都相同。ML-DSA 為 True（FIPS 204），FN-DSA 為 False。
    - status：standard 或 provisional，見 VALID_STATUSES。
    """

    label: str
    cose_alg: int
    oqs_name: str
    public_key_bytes: int
    private_key_bytes: int
    signature_bytes: int
    signature_length_fixed: bool
    status: str


# JSON 欄位名稱（camelCase，和 TypeScript 慣例一致）→ PQAlgorithm 欄位名稱
_FIELDS: Dict[str, str] = {
    "label": "label",
    "coseAlg": "cose_alg",
    "oqsName": "oqs_name",
    "publicKeyBytes": "public_key_bytes",
    "privateKeyBytes": "private_key_bytes",
    "signatureBytes": "signature_bytes",
    "signatureLengthFixed": "signature_length_fixed",
    "status": "status",
}


def _check_field(where: str, key: str, value: Any) -> None:
    """檢查單一欄位的型別與值，不合法就拋出 ValueError。

    輸入：where 是這筆資料的位置（例如 "algorithms[1]"），key 是 JSON 欄位名稱，value 是欄位值。
    錯誤訊息的開頭是「位置.欄位」，讓人一眼看出是哪一筆的哪個欄位寫錯。

    注意 Python 的 bool 是 int 的子類別（True == 1），所以整數欄位用 type(value) is int 判斷，
    避免 true/false 被當成合法的編號或大小（JSON 的 true/false 不是數字，RFC 8259 §3）。
    任何型別的錯誤值都只會拋出 ValueError，不會因為型別本身丟出其他例外。
    """
    if key in ("label", "oqsName"):
        if not isinstance(value, str) or not value:
            raise ValueError(f"{where}.{key} must be a non-empty string")
    elif key == "coseAlg":
        if type(value) is not int:
            raise ValueError(f"{where}.{key} must be an integer, got {value!r}")
    elif key in ("publicKeyBytes", "privateKeyBytes", "signatureBytes"):
        if type(value) is not int or value <= 0:
            raise ValueError(f"{where}.{key} must be a positive integer, got {value!r}")
    elif key == "signatureLengthFixed":
        if not isinstance(value, bool):
            raise ValueError(f"{where}.{key} must be true or false, got {value!r}")
    elif key == "status":
        # 先確認是字串再查集合：清單這類不能雜湊的值直接查 frozenset 會丟 TypeError，
        # 違反「壞掉的表一律拋出 ValueError」
        if not isinstance(value, str) or value not in VALID_STATUSES:
            raise ValueError(
                f"{where}.{key} must be one of {sorted(VALID_STATUSES)}, got {value!r}"
            )


def _parse_entry(index: int, raw: Any) -> PQAlgorithm:
    """把 JSON 中的第 index 筆（從 0 起算）轉成 PQAlgorithm。

    欄位必須剛好是 _FIELDS 列出的那些：缺少欄位代表資料不完整；多出不認得的欄位多半是拼錯
    （例如 oqsname），兩者都拋出 ValueError。
    """
    where = f"algorithms[{index}]"
    if not isinstance(raw, dict):
        raise ValueError(f"{where} must be an object")
    for key in _FIELDS:
        if key not in raw:
            raise ValueError(f"{where}.{key} is missing")
    for key in raw:
        if key not in _FIELDS:
            raise ValueError(f"{where}.{key} is not a known field")
    for key, value in raw.items():
        _check_field(where, key, value)
    return PQAlgorithm(**{_FIELDS[key]: value for key, value in raw.items()})


def load_algorithms(path: Path = REGISTRY_PATH) -> Tuple[PQAlgorithm, ...]:
    """讀取並檢查共用演算法表，依檔案中的順序回傳所有演算法。

    輸入：表的路徑，預設是 shared/pq-algorithms.json；測試會傳入自己組的表。
    輸出：PQAlgorithm 的 tuple（不可修改）。
    任何一筆格式錯誤，或 COSE 編號、liboqs 名稱重複，都拋出 ValueError。
    編號必須唯一，因為協議中只傳編號，一個編號只能對到一個演算法；liboqs 名稱也必須唯一，
    否則同一個演算法會有兩種編號，必定是寫錯。
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("algorithms"), list):
        raise ValueError(f"{path} must contain an 'algorithms' list")

    algorithms = tuple(
        _parse_entry(index, raw) for index, raw in enumerate(data["algorithms"])
    )

    seen_cose: set = set()
    seen_oqs: set = set()
    for algorithm in algorithms:
        if algorithm.cose_alg in seen_cose:
            raise ValueError(f"Duplicate coseAlg {algorithm.cose_alg}")
        if algorithm.oqs_name in seen_oqs:
            raise ValueError(f"Duplicate oqsName {algorithm.oqs_name}")
        seen_cose.add(algorithm.cose_alg)
        seen_oqs.add(algorithm.oqs_name)
    return algorithms


# 模組載入時讀一次：表有錯就在 import 時失敗，RP 或 authenticator 根本不會啟動
ALGORITHMS: Tuple[PQAlgorithm, ...] = load_algorithms()


def cose_to_oqs_names() -> Dict[int, str]:
    """回傳「COSE 編號 → liboqs 名稱」的對照，給 RP 與 authenticator 建立各自的查詢表。

    每次回傳新的 dict，呼叫端修改它不會影響共用表本身。
    """
    return {algorithm.cose_alg: algorithm.oqs_name for algorithm in ALGORITHMS}
