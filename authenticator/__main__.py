"""Command-line entry point to launch the Playwright bridge."""

from __future__ import annotations

import argparse
import asyncio
import logging

from . import Authenticator, AuthenticatorSettings, PlaywrightBridge


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PQ FIDO2 Authenticator Bridge")
    parser.add_argument("--url", required=True, help="Target URL to open in Chromium")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    authenticator = Authenticator(AuthenticatorSettings())
    bridge = PlaywrightBridge(authenticator, args.url, headless=False)
    try:
        asyncio.run(bridge.run())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
