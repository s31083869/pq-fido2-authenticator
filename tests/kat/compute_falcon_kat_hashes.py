"""從官方 Falcon 第三輪提交包算出 KAT 雜湊表（Day 7 T6 的預期值）。

為什麼需要：官方 KAT 檔（falcon512-KAT.rsp 1.25 MB、falcon1024-KAT.rsp 1.76 MB）太大，不放進 git
（計畫書 Day 10 的原則）。這個腳本直接從官方 zip 讀出兩個 .rsp，算出整份檔案與每一筆的 SHA-256，
寫成 tests/kat/falcon-round3-kat.json；wasm-falcon-kat.test.ts 再用 WASM 重現同樣的內容並比對雜湊。
預期值因此全部來自官方檔案，不是被測程式的輸出（CLAUDE.md「避免球員兼裁判」第 2 條）。

任何人都能重算核對：
    1. 下載 SOURCE_URL 的 Falcon-Round3.zip（4,067,127 bytes）
    2. uv run python tests/kat/compute_falcon_kat_hashes.py <zip 路徑> tests/kat/falcon-round3-kat.json
    3. 確認輸出的 JSON 與 git 裡的相同

輸入：zip 路徑、輸出 JSON 路徑。腳本只讀 zip 裡的兩個 .rsp（純文字），不解壓、不執行其他檔案。
"""

from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path

# NIST CSRC 的 PQC 第三輪提交包（2026-11-25 下載，伺服器標示最後修改 2024-09-29）
SOURCE_URL = (
    "https://csrc.nist.gov/CSRC/media/Projects/post-quantum-cryptography/"
    "documents/round-3/submissions/Falcon-Round3.zip"
)

# 演算法標題（.rsp 第一行 "# <標題>"）→ zip 內的檔案路徑
RSP_FILES = {
    "Falcon-512": "Falcon/falcon-round3/KAT/falcon512-KAT.rsp",
    "Falcon-1024": "Falcon/falcon-round3/KAT/falcon1024-KAT.rsp",
}

# 官方 .rsp 每一筆依序有這 8 行（NIST PQCgenKAT_sign.c 的輸出格式）
ENTRY_FIELDS = ["count", "seed", "mlen", "msg", "pk", "sk", "smlen", "sm"]


def sha256_hex(data: bytes) -> str:
    """回傳 data 的 SHA-256（小寫 16 進位）。"""
    return hashlib.sha256(data).hexdigest()


def parse_rsp(title: str, data: bytes) -> list[str]:
    """把官方 .rsp 拆成每一筆的文字，並確認能原封不動組回原檔。

    格式（2026-11-25 核對官方檔案）：第一行 "# <title>"、一個空行；之後每筆 8 行，
    每筆後面接一個空行（包含最後一筆）；只有 LF 換行。

    輸入：演算法標題、整份檔案的 bytes。
    輸出：每一筆的文字（8 行，每行以 LF 結尾，不含後面的空行），依 count 排序。
    任何一處不符預期格式就丟出 ValueError，避免算出錯的雜湊。
    """
    text = data.decode("ascii")
    header = f"# {title}\n\n"
    if not text.startswith(header):
        raise ValueError(f"{title}: unexpected header")
    blocks = text[len(header) :].split("\n\n")
    if blocks[-1] != "":
        raise ValueError(f"{title}: file must end with a blank line")
    entries = [block + "\n" for block in blocks[:-1]]

    for count, entry in enumerate(entries):
        names = [line.split(" = ", 1)[0] for line in entry.splitlines()]
        if names != ENTRY_FIELDS or not entry.startswith(f"count = {count}\n"):
            raise ValueError(f"{title}: entry {count} has unexpected fields {names}")

    # 組回去必須和原檔逐 byte 相同，證明拆法沒有遺漏任何字元
    if (header + "".join(entry + "\n" for entry in entries)).encode("ascii") != data:
        raise ValueError(f"{title}: entries do not reassemble into the original file")
    return entries


def seed_msg_text(entry: str) -> str:
    """取出一筆中的 seed、mlen、msg 三行：這部分只由 NIST DRBG 決定，與簽章演算法無關。"""
    lines = entry.splitlines(keepends=True)
    return "".join(lines[1:4])


def main(zip_path: Path, out_path: Path) -> None:
    """讀官方 zip、算雜湊、寫出 JSON。"""
    zip_bytes = zip_path.read_bytes()
    result: dict = {
        "description": (
            "Falcon 第三輪官方 KAT 的雜湊表，由 tests/kat/compute_falcon_kat_hashes.py 從官方 zip 算出。"
            "entries[i].seedMsgSha256 是第 i 筆 seed、mlen、msg 三行的 SHA-256；"
            "entries[i].entrySha256 是第 i 筆 8 行（含結尾 LF、不含後面的空行）的 SHA-256；"
            "sha256 是整份 .rsp 的 SHA-256。"
        ),
        "source": {
            "url": SOURCE_URL,
            "file": zip_path.name,
            "bytes": len(zip_bytes),
            "sha256": sha256_hex(zip_bytes),
            "retrieved": "2026-11-25",
        },
        "algorithms": {},
    }

    with zipfile.ZipFile(zip_path) as archive:
        for title, member in RSP_FILES.items():
            data = archive.read(member)
            entries = parse_rsp(title, data)
            result["algorithms"][title] = {
                "file": member,
                "bytes": len(data),
                "sha256": sha256_hex(data),
                "header": f"# {title}",
                "entries": [
                    {
                        "count": count,
                        "seedMsgSha256": sha256_hex(
                            seed_msg_text(entry).encode("ascii")
                        ),
                        "entrySha256": sha256_hex(entry.encode("ascii")),
                    }
                    for count, entry in enumerate(entries)
                ],
            }

    out_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(
            "usage: compute_falcon_kat_hashes.py <Falcon-Round3.zip> <output.json>"
        )
    main(Path(sys.argv[1]), Path(sys.argv[2]))
