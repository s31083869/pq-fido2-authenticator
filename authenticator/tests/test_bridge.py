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
        self.origins: list = []

    def make_credential(self, options, origin):
        self.origins.append(origin)
        return {"handled": "make_credential"}

    def get_assertion(self, options, origin):
        self.origins.append(origin)
        return {"handled": "get_assertion"}


def _call_handler(handler_name: str, page_url: str, payload: dict) -> list:
    """模擬 Playwright 呼叫 binding，回傳 bridge 交給 authenticator 的 origin。

    Playwright 會在 source 中附上呼叫者所在的 frame。frame.url 由瀏覽器提供，頁面最多只能用
    history.pushState 改同一個 origin 內的路徑，改不了 origin；payload 則是頁面 JavaScript
    自己組出來的資料，內容完全由頁面決定。
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
    """
    payload = {"origin": "http://localhost:3000", "publicKey": {"challenge": "abc"}}

    origins = _call_handler(handler_name, "https://evil.example/login", payload)

    assert origins == ["https://evil.example"]


@pytest.mark.parametrize("handler_name", ["_handle_make", "_handle_get"])
def test_bridge_derives_origin_from_scheme_host_and_port(handler_name):
    """T11：payload 中沒有 origin，頁面網址帶有路徑與查詢字串時，origin 只取協定、網域、埠。"""
    payload = {"publicKey": {"challenge": "abc"}}

    origins = _call_handler(
        handler_name, "http://localhost:3000/register?step=2", payload
    )

    assert origins == ["http://localhost:3000"]
