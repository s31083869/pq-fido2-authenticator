"""Python 路線的整合測試：authenticator ↔ RP 完整註冊、登入（Day 5 T1–T3）。

Python 路線實際執行時，資料經過「RP → 前端 → bridge → authenticator → bridge → 前端 → RP」。
這裡把「前端 + bridge」換成幾行程式，其餘都是真的：
- RP：create_app() 的 Flask test client，走真的 /register/*、/authenticate/* 路由與 DB；
- authenticator：真的 Authenticator 與 liboqs（CLAUDE.md「真實密碼學」）。

「前端 + bridge」在這裡只做兩件事，和真的程式相同：
1. 重排 pubKeyCredParams：目標演算法移到第一個，其他保持原順序（修正後的前端規則，前端本身由 Day 5 T5 測）；
2. 把 RP 的回應交給 make_credential()／get_assertion()，origin 固定 http://localhost:3000
   （bridge 從頁面真實網址取得的值，見 authenticator/bridge.py 的 _handle_make()），再把結果原樣送回 RP。
bridge 注入腳本與前端的 JavaScript 不在這裡的範圍，由手動端到端 M1–M3 覆蓋。

預期的公鑰長度都寫死為外部數值，不從共用表推算，避免「拿實作驗證實作」。
"""

from __future__ import annotations

import base64

import pytest

from rp_server.database import Database
from rp_server.services import get_user, list_credentials

# 前端頁面的 origin：RP 預設的 origin 也是這個值，bridge 會把它填進 clientDataJSON
ORIGIN = "http://localhost:3000"

# (COSE 編號, 公鑰 bytes)
# ML-DSA：FIPS 204 Table 2（ML-DSA-44／65／87 公鑰 1312／1952／2592 bytes）。
# FN-DSA：Falcon v1.2 第 3.11 節，公鑰 = 1 byte 標頭 + 14·n/8 bytes（n = 512 → 897，n = 1024 → 1793）。
ALL_ALGORITHMS = [
    (-48, 1312),
    (-49, 1952),
    (-50, 2592),
    (-54, 897),
    (-55, 1793),
]
CASE_IDS = [
    "a-ML-DSA-44",
    "b-ML-DSA-65",
    "c-ML-DSA-87",
    "d-FN-DSA-512",
    "e-FN-DSA-1024",
]


def _b64url_decode(value: str) -> bytes:
    """把 RP 存進 DB 的 base64url 字串（不補「=」）還原成 bytes。"""
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def _move_to_front(params: list[dict], alg: int) -> list[dict]:
    """模擬修正後的前端：把 alg 移到清單第一個，其他保持原本的相對順序，不新增也不刪除。

    輸入：RP 的 pubKeyCredParams、要測的 COSE 演算法編號（必須在清單內）。
    輸出：重排後的新清單（不修改原本的 list）。
    """
    chosen = [param for param in params if param["alg"] == alg]
    assert chosen, f"測試前提錯誤：RP 的清單裡沒有 {alg}"
    return chosen + [param for param in params if param["alg"] != alg]


def _register(client, authenticator, username: str, alg: int):
    """走一次完整註冊：/register/options → make_credential() → /register/verify。

    輸入：RP 的 test client、authenticator、使用者名稱、要讓 authenticator 選到的演算法。
    輸出：(/register/verify 的 HTTP 回應, authenticator 回傳的憑證 dict)。
    """
    options_response = client.post(
        "/register/options", json={"username": username, "display_name": username}
    )
    assert options_response.status_code == 200
    options = options_response.get_json()["data"]
    # 前端的工作：只在 RP 的清單裡調整順序，讓 authenticator 選到這次要測的演算法
    options["pubKeyCredParams"] = _move_to_front(options["pubKeyCredParams"], alg)
    # bridge 的工作：把參數交給 authenticator，origin 取自頁面的真實網址
    credential = authenticator.make_credential(options, origin=ORIGIN)
    verify_response = client.post(
        "/register/verify", json={"username": username, "credential": credential}
    )
    return verify_response, credential


def _credentials_of(settings, username: str) -> list:
    """直接查 RP 的 DB，回傳該使用者的所有憑證；使用者不存在時回傳空 list。"""
    with Database(settings).session() as session:
        user = get_user(session, username)
        if user is None:
            return []
        return [
            (cred.id, cred.algorithm, cred.public_key, cred.sign_count)
            for cred in list_credentials(session, user)
        ]


@pytest.mark.parametrize(("alg", "pk_len"), ALL_ALGORITHMS, ids=CASE_IDS)
def test_registration_with_each_algorithm_is_stored_by_rp(
    make_rp, authenticator, alg, pk_len
) -> None:
    """T1：五個演算法各自完整註冊一次，RP 接受並把正確的演算法與公鑰存進 DB。

    依據：workflow.md F14（註冊後保存 algorithm=-54/-55）、F17；WebAuthn §7.1（RP 註冊驗證）；
    FIPS 204 Table 2、Falcon v1.2 第 3.11 節（公鑰長度）。
    """
    client, settings = make_rp()
    username = f"user{abs(alg)}"

    response, credential = _register(client, authenticator, username, alg)

    assert response.status_code == 200
    assert response.get_json()["success"] is True
    stored = _credentials_of(settings, username)
    # 剛好一張憑證；credential ID 就是 authenticator 回傳的那一張
    assert len(stored) == 1
    credential_id, algorithm, public_key, _ = stored[0]
    assert credential_id == credential["id"]
    # DB 的 algorithm 欄位就是 authenticator 選的演算法（credentialPublicKey 的 3 欄位）
    assert algorithm == alg
    # DB 的 public_key 欄位是原始公鑰 bytes 的 base64url（rp_server/services.py 的 verify_registration_payload）
    assert len(_b64url_decode(public_key)) == pk_len


@pytest.mark.parametrize(("alg", "pk_len"), ALL_ALGORITHMS, ids=CASE_IDS)
def test_login_after_registration_is_verified_by_rp(
    make_rp, authenticator, alg, pk_len
) -> None:
    """T2：接著 T1 的註冊，同一個使用者登入一次，RP 用 DB 裡的公鑰驗章成功，signCount 從 0 變成 1。

    每個測試各自註冊，彼此不共用狀態。

    依據：workflow.md F15、F17；WebAuthn §7.2（RP 登入驗證與驗章）、§6.1.1（signCount 每次使用遞增）。
    """
    client, settings = make_rp()
    username = f"user{abs(alg)}"
    register_response, _ = _register(client, authenticator, username, alg)
    assert register_response.status_code == 200
    # 註冊後、登入前：RP 存的 signCount 為 0（rp_server/services.py 的 store_credential）
    assert _credentials_of(settings, username)[0][3] == 0

    options_response = client.post("/authenticate/options", json={"username": username})
    assert options_response.status_code == 200
    request_options = options_response.get_json()["data"]
    # bridge 的工作：把登入參數交給 authenticator 簽章，結果原樣送回 RP
    assertion = authenticator.get_assertion(request_options, origin=ORIGIN)
    verify_response = client.post(
        "/authenticate/verify", json={"username": username, "credential": assertion}
    )

    assert verify_response.status_code == 200
    assert verify_response.get_json()["success"] is True
    # RP 驗章成功後，把 authenticatorData 裡的 signCount（第一次登入為 1）寫回 DB
    assert _credentials_of(settings, username)[0][3] == 1


def test_rp_rejects_fn_dsa_inserted_by_buggy_frontend(make_rp, authenticator) -> None:
    """T3：RP 沒宣告 FN-DSA，舊前端卻把 -54 塞到清單最前面；authenticator 照清單選 -54，RP 回 400 且不存任何憑證。

    authenticator 只看得到收到的清單，所以選 -54 不算錯；保證要靠 RP 用自己的 hosted_algorithms 再檢查一次。

    依據：workflow.md F16；WebAuthn §7.1（alg 必須是 RP 在 pubKeyCredParams 宣告過的）；
    Day 4 對齊紀錄「保證要靠兩端」、Day 5 對齊紀錄（前端的檢查可被繞過，RP 的檢查才是規則本身）。
    """
    client, settings = make_rp(hosted_algorithms=[-49, -48, -50])
    username = "buggy"
    options = client.post(
        "/register/options", json={"username": username, "display_name": username}
    ).get_json()["data"]
    # 前提：RP 發出的清單確實沒有 FN-DSA
    assert [param["alg"] for param in options["pubKeyCredParams"]] == [-49, -48, -50]
    # 模擬修正前的前端（frontend/src/pages/index.tsx 原本的寫法）：不管 RP 有沒有宣告，一律塞到最前面
    options["pubKeyCredParams"] = [{"type": "public-key", "alg": -54}] + options[
        "pubKeyCredParams"
    ]

    credential = authenticator.make_credential(options, origin=ORIGIN)
    # authenticator 依 WebAuthn §6.3.2 選收到的清單中第一個自己支援的：-54
    assert credential["response"]["publicKeyAlgorithm"] == -54
    response = client.post(
        "/register/verify", json={"username": username, "credential": credential}
    )

    assert response.status_code == 400
    assert response.get_json()["success"] is False
    # 400 的原因必須是演算法檢查（rp_server/services.py 的 hosted_algorithms 比對），
    # 不是 origin、challenge 等其他檢查；破壞檢查發現只看 400 時，origin 錯誤也會讓這個測試通過
    assert response.get_json()["message"] == "Unsupported algorithm"
    assert _credentials_of(settings, username) == []
