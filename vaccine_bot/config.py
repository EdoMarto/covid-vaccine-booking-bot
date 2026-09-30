"""Configuration, read from environment variables (and a local .env file)."""

from __future__ import annotations

import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # python-dotenv is optional
    pass


@dataclass
class Config:
    # Personal identifiers required by the booking portal.
    codice_fiscale: str | None
    health_card: str | None  # numero tessera sanitaria

    # Portal + search preferences.
    portal_url: str
    location: str  # preferred vaccination hub / city
    earliest_only: bool  # book the earliest slot found, anywhere in `location`

    # Polling.
    poll_seconds: int
    headless: bool

    # Optional Telegram notification when a slot is booked.
    telegram_token: str | None
    telegram_chat_id: str | None

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            codice_fiscale=os.environ.get("CODICE_FISCALE"),
            health_card=os.environ.get("HEALTH_CARD"),
            portal_url=os.environ.get("PORTAL_URL", "https://vaccinicovid.regione.veneto.it/"),
            location=os.environ.get("LOCATION", "Padova"),
            earliest_only=os.environ.get("EARLIEST_ONLY", "true").lower() == "true",
            poll_seconds=int(os.environ.get("POLL_SECONDS", "60")),
            headless=os.environ.get("HEADLESS", "false").lower() == "true",
            telegram_token=os.environ.get("TELEGRAM_BOT_TOKEN"),
            telegram_chat_id=os.environ.get("TELEGRAM_CHAT_ID"),
        )
