"""Python bridge（Playwright 攔截層）的測試：origin 必須取自呼叫者頁面的真實網址。

依據：WebAuthn §5.8.1，clientDataJSON 的 origin 由瀏覽器依呼叫者的真實來源填入，網頁無法指定。
bridge 扮演瀏覽器的角色，所以不能採用頁面在 payload 裡自稱的 origin。
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from authenticator.bridge import PlaywrightBridge


class RecordingAuthenticator:
    """假的 authenticator：只記錄 bridge 交給它的 origin，不做任何密碼學運算。"""

    def __init__(self) -> None:
        # 依呼叫順序記下 bridge 交來的 origin
        self.origins: list = []

    def make_credential(self, options, origin):
        """代替 Authenticator.make_credential()：記下 origin，回傳標示呼叫來源的假結果。

        參數：
            options：bridge 轉交的 publicKey 選項，這裡用不到。
            origin：bridge 算出的 origin，也就是測試要檢查的值。

        回傳：
            {"handled": "make_credential"}，表示註冊入口被呼叫。
        """
        self.origins.append(origin)
        return {"handled": "make_credential"}

    def get_assertion(self, options, origin):
        """代替 Authenticator.get_assertion()：記下 origin，回傳標示呼叫來源的假結果。

        參數的意義同 make_credential()。

        回傳：
            {"handled": "get_assertion"}，表示登入入口被呼叫。
        """
        self.origins.append(origin)
        return {"handled": "get_assertion"}


def _call_handler(handler_name: str, page_url: str, payload: dict) -> list:
    """模擬 Playwright 呼叫 binding，回傳 bridge 交給 authenticator 的 origin。

    Playwright 會在 source 中附上呼叫者所在的 frame。frame.url 由瀏覽器提供，頁面最多只能用
    history.pushState 改同一個 origin 內的路徑，改不了 origin；payload 則是頁面 JavaScript
    自己組出來的資料，內容完全由頁面決定。

    參數：
        handler_name：要測試的 bridge 方法，"_handle_make"（註冊）或 "_handle_get"（登入）。
        page_url：呼叫者 frame 的真實網址，也就是 Playwright 會放進 source["frame"].url 的值。
        payload：頁面傳給 binding 的資料。

    回傳：
        authenticator 收到的 origin，每被呼叫一次記一筆。
    """
    authenticator = RecordingAuthenticator()
    bridge = PlaywrightBridge(authenticator, target_url="http://localhost:3000")
    source = {"context": None, "page": None, "frame": SimpleNamespace(url=page_url)}
    asyncio.run(getattr(bridge, handler_name)(source, payload))
    return authenticator.origins


@pytest.mark.parametrize("handler_name", ["_handle_make", "_handle_get"])
def test_bridge_uses_real_page_origin_instead_of_claimed_origin(handler_name):
    """T10：頁面在 payload 中自稱 origin 是 localhost:3000，但實際網址是 evil.example 時，
    bridge 交給 authenticator 的 origin 必須是頁面的真實來源 https://evil.example。

    依據：WebAuthn §5.8.1，origin 由瀏覽器依呼叫者的真實來源填入，網頁無法指定（見模組說明）。
    """
    payload = {"origin": "http://localhost:3000", "publicKey": {"challenge": "abc"}}

    origins = _call_handler(handler_name, "https://evil.example/login", payload)

    assert origins == ["https://evil.example"]


@pytest.mark.parametrize("handler_name", ["_handle_make", "_handle_get"])
def test_bridge_derives_origin_from_scheme_host_and_port(handler_name):
    """T11：payload 中沒有 origin，頁面網址帶有路徑與查詢字串時，origin 只取協定、網域、埠。

    依據：RFC 6454 對 origin 的定義：origin 只由協定、網域、埠三者組成，路徑與查詢字串不屬於 origin。
    """
    payload = {"publicKey": {"challenge": "abc"}}

    origins = _call_handler(
        handler_name, "http://localhost:3000/register?step=2", payload
    )

    assert origins == ["http://localhost:3000"]
