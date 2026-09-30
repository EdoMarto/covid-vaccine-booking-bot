"""Notify the user when a slot is booked: always to the log, optionally to Telegram."""

from __future__ import annotations

import logging

log = logging.getLogger(__name__)


class Notifier:
    def __init__(self, token: str | None = None, chat_id: str | None = None) -> None:
        self._token = token
        self._chat_id = chat_id

    def notify(self, text: str) -> None:
        log.info(text)
        if not (self._token and self._chat_id):
            return
        try:
            import requests

            requests.post(
                f"https://api.telegram.org/bot{self._token}/sendMessage",
                json={"chat_id": self._chat_id, "text": text},
                timeout=30,
            ).raise_for_status()
        except Exception as exc:  # a failed notification must not crash the bot
            log.warning("Telegram notification failed: %s", exc)
