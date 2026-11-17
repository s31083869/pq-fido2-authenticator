"""共用演算法表 shared/pq-algorithms.json 與其 Python 讀取模組的測試（Day 2 的 T1–T4）。

共用演算法表是「COSE 演算法編號 → liboqs 名稱、金鑰與簽章大小」的唯一資料來源（決策 D3），
RP、authenticator，以及之後的 Extension、WASM bridge 都從這份表讀。
這裡的預期值全部來自外部依據，而不是從程式輸出抄來：
- ML-DSA：COSE 編號依 RFC 9964；大小依 FIPS 204 Table 2。
- FN-DSA：COSE 編號依 draft-ietf-cose-falcon-04（暫定，D1）；公鑰、私鑰大小依 Falcon 第三輪規格 v1.2
  第 3.11 節；不補滿格式（D2）的簽章上限依 liboqs 演算法資料表 docs/algorithms/sig/falcon.yml。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import oqs
import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.pq_algorithms import ALGORITHMS, load_algorithms  # noqa: E402

# 依外部依據寫下的預期內容，順序也是共用表的順序（D6：ML-DSA 在前、FN-DSA 在後）。
# 欄位依序：label、coseAlg、oqsName、公鑰 bytes、私鑰 bytes、簽章 bytes、簽章長度是否固定、status。
# FN-DSA 的簽章 bytes 是上限：不補滿的壓縮格式每次簽章長度都不同（Falcon v1.2 第 3.11.6 節）。
EXPECTED = [
    ("ML-DSA-44", -48, "ML-DSA-44", 1312, 2560, 2420, True, "standard"),
    ("ML-DSA-65", -49, "ML-DSA-65", 1952, 4032, 3309, True, "standard"),
    ("ML-DSA-87", -50, "ML-DSA-87", 2592, 4896, 4627, True, "standard"),
    ("FN-DSA-512", -54, "Falcon-512", 897, 1281, 752, False, "provisional"),
    ("FN-DSA-1024", -55, "Falcon-1024", 1793, 2305, 1462, False, "provisional"),
]


def _entry(label: str, cose_alg: int, oqs_name: str) -> dict:
    """產生一筆格式正確的演算法資料（JSON 物件），供 T3、T4 組出測試用的表。

    大小沿用 ML-DSA-44 的數值；這兩個測試只關心重複與欄位檢查，不關心大小本身。
    """
    return {
        "label": label,
        "coseAlg": cose_alg,
        "oqsName": oqs_name,
        "publicKeyBytes": 1312,
        "privateKeyBytes": 2560,
        "signatureBytes": 2420,
        "signatureLengthFixed": True,
        "status": "standard",
    }


def _write_table(tmp_path: Path, entries: list) -> Path:
    """把演算法清單寫成和共用表相同結構的 JSON 檔，回傳檔案路徑。"""
    path = tmp_path / "pq-algorithms.json"
    path.write_text(json.dumps({"algorithms": entries}), encoding="utf-8")
    return path


def test_registry_matches_published_specifications() -> None:
    """T1：共用表剛好五筆，每一筆的編號、名稱、大小、長度是否固定與狀態都符合外部依據。

    依據：RFC 9964、FIPS 204 Table 2、Falcon v1.2 第 3.11 節、draft-ietf-cose-falcon-04、
    liboqs 演算法資料表，以及決策 D1（-54/-55 暫定）、D2（使用不補滿的 Falcon-512/1024）。
    """
    actual = [
        (
            a.label,
            a.cose_alg,
            a.oqs_name,
            a.public_key_bytes,
            a.private_key_bytes,
            a.signature_bytes,
            a.signature_length_fixed,
            a.status,
        )
        for a in ALGORITHMS
    ]
    assert actual == EXPECTED


@pytest.mark.parametrize("algorithm", ALGORITHMS, ids=lambda a: a.label)
def test_registry_sizes_match_liboqs(algorithm) -> None:
    """T2：表內的公鑰、私鑰、簽章大小，等於 liboqs 對該演算法實際回報的大小。

    依據：FN-DSA-PLAN.md Day 2「表內大小等於 liboqs 實際大小」，以及交接文件 5.1 節
    「byte 長度應以實際 liboqs 版本為準」。這個測試確保共用表和真正在用的函式庫沒有脫節；
    liboqs 升級後若大小改變，這裡會先變紅。
    """
    with oqs.Signature(algorithm.oqs_name) as signer:
        details = signer.details
    assert details["length_public_key"] == algorithm.public_key_bytes
    assert details["length_secret_key"] == algorithm.private_key_bytes
    assert details["length_signature"] == algorithm.signature_bytes


@pytest.mark.parametrize(
    ("entries", "message"),
    [
        # (a) 兩筆都宣稱自己是 COSE -48：RP 和 authenticator 無法確定 -48 指的是哪個演算法
        (
            [_entry("ML-DSA-44", -48, "ML-DSA-44"), _entry("Other", -48, "ML-DSA-65")],
            "Duplicate coseAlg -48",
        ),
        # (b) 兩個 COSE 編號對到同一個 liboqs 演算法：同一把金鑰會有兩種編號，必定是寫錯
        (
            [_entry("ML-DSA-44", -48, "ML-DSA-44"), _entry("Other", -49, "ML-DSA-44")],
            "Duplicate oqsName ML-DSA-44",
        ),
    ],
    ids=["duplicate-cose-alg", "duplicate-oqs-name"],
)
def test_loader_rejects_duplicates(tmp_path: Path, entries: list, message: str) -> None:
    """T3：表中有重複的 COSE 編號或 liboqs 名稱時，讀取模組拋出 ValueError 並指出重複的值。

    依據：COSE 演算法編號必須唯一對應一個演算法（IANA COSE Algorithms registry）；
    FN-DSA-PLAN.md Day 2「COSE 編號不重複」。
    """
    with pytest.raises(ValueError, match=message):
        load_algorithms(_write_table(tmp_path, entries))


def _without_oqs_name() -> dict:
    """產生一筆缺少 oqsName 的資料，模擬漏寫欄位。"""
    entry = _entry("ML-DSA-65", -49, "ML-DSA-65")
    del entry["oqsName"]
    return entry


@pytest.mark.parametrize(
    ("bad_entry", "field"),
    [
        # (a) 缺少 oqsName：不知道要叫 liboqs 的哪個演算法
        (_without_oqs_name(), "oqsName"),
        # (b) coseAlg 寫成字串：協議中的編號是整數，字串 "-49" 永遠比對不到 RP 送來的 -49
        ({**_entry("ML-DSA-65", -49, "ML-DSA-65"), "coseAlg": "-49"}, "coseAlg"),
        # (c) status 不是 standard 或 provisional：無法判斷編號是否已正式分配
        ({**_entry("ML-DSA-65", -49, "ML-DSA-65"), "status": "planned"}, "status"),
    ],
    ids=["missing-oqs-name", "string-cose-alg", "unknown-status"],
)
def test_loader_rejects_malformed_entry(
    tmp_path: Path, bad_entry: dict, field: str
) -> None:
    """T4：有一筆缺欄位、型別錯誤或狀態值不認得時，讀取模組拋出 ValueError，
    訊息指出是第幾筆（從 0 起算）的哪個欄位。

    依據：workflow.md F02 規定的欄位；壞掉的表必須在程式啟動時就被擋下，不能等到驗章時才出錯。
    壞的那一筆放在索引 1（第二筆），確認訊息指的是正確的位置。
    """
    entries = [_entry("ML-DSA-44", -48, "ML-DSA-44"), bad_entry]
    with pytest.raises(ValueError, match=rf"algorithms\[1\]\.{field}"):
        load_algorithms(_write_table(tmp_path, entries))


def _with(**changes) -> dict:
    """以一筆格式正確的 ML-DSA-65 資料為基礎，套用 changes 後回傳，用來組出 T9 的壞資料。"""
    return {**_entry("ML-DSA-65", -49, "ML-DSA-65"), **changes}


@pytest.mark.parametrize(
    ("bad_entry", "field"),
    [
        # (a)(b) JSON 的 true／false 不是數字（RFC 8259 §3），但 Python 的 bool 是 int 的子類別，
        # 若只用 isinstance(value, int) 檢查，true 會被當成編號 1 或大小 1 接受
        (_with(coseAlg=True), "coseAlg"),
        (_with(publicKeyBytes=True), "publicKeyBytes"),
        # (c) 拼錯的欄位若被默默忽略，Python 與之後讀同一份表的 TypeScript 可能看到不同的資料
        (_with(oqsname="ML-DSA-65"), "oqsname"),
        # (d) 長度為 0 的金鑰不可能存在
        (_with(publicKeyBytes=0), "publicKeyBytes"),
        # (e) 字串 "false" 在 JavaScript 與 Python 中都會被當成「真」，必須是 JSON 的 true／false
        (_with(signatureLengthFixed="false"), "signatureLengthFixed"),
        # (f)(g) 空字串的名稱：給人看的名稱是空的，或叫不到任何 liboqs 演算法
        (_with(label=""), "label"),
        (_with(oqsName=""), "oqsName"),
        # (h) 不能雜湊的值（清單）：檢查本身不能因為型別而丟出 ValueError 以外的例外
        (_with(status=["standard"]), "status"),
    ],
    ids=[
        "bool-cose-alg",
        "bool-public-key-bytes",
        "unknown-field",
        "zero-public-key-bytes",
        "string-signature-length-fixed",
        "empty-label",
        "empty-oqs-name",
        "list-status",
    ],
)
def test_loader_rejects_wrongly_typed_or_unknown_field(
    tmp_path: Path, bad_entry: dict, field: str
) -> None:
    """T9 (a)–(h)：欄位型別錯誤、值不合理或欄位名稱不認得時，讀取模組拋出 ValueError，
    訊息開頭指出 algorithms[1].<欄位>（索引 1，也就是第二筆）。

    依據：RFC 8259 §3（true／false 是獨立的字面值，不是數字）；workflow.md F02 規定的欄位；
    D3「唯一的資料來源」；模組說明承諾壞掉的表一律拋出 ValueError。
    """
    entries = [_entry("ML-DSA-44", -48, "ML-DSA-44"), bad_entry]
    with pytest.raises(ValueError, match=rf"^algorithms\[1\]\.{field}\b"):
        load_algorithms(_write_table(tmp_path, entries))


def test_loader_rejects_table_without_algorithm_list(tmp_path: Path) -> None:
    """T9 (i)：整份表沒有 algorithms 清單時，讀取模組拋出 ValueError，訊息提到 algorithms。

    依據：共用表的結構是 {"algorithms": [...]}；少了清單代表檔案寫錯，不能當成「沒有任何演算法」。
    錯誤訊息以檔案路徑開頭，而暫存檔名 pq-algorithms.json 本身就含有 "algorithms"，
    所以斷言比對訊息中的「'algorithms' list」，確認是讀取模組指出少了清單，而不是碰巧比對到檔名。
    """
    path = tmp_path / "pq-algorithms.json"
    path.write_text(json.dumps({"items": []}), encoding="utf-8")
    with pytest.raises(ValueError, match=r"'algorithms' list"):
        load_algorithms(path)
