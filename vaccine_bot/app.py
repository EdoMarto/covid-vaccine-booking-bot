"""Entry point: poll the portal until a slot is free, then book the earliest one."""

from __future__ import annotations

import argparse
import logging
import time

from .config import Config
from .notifier import Notifier
from .portal import VaccinePortal

log = logging.getLogger("vaccine_bot")


def run(config: Config, once: bool = False) -> bool:
    if not (config.codice_fiscale and config.health_card):
        raise SystemExit("Set CODICE_FISCALE and HEALTH_CARD (see .env.example).")

    notifier = Notifier(config.telegram_token, config.telegram_chat_id)

    with VaccinePortal(config.portal_url, headless=config.headless) as portal:
        portal.login(config.codice_fiscale, config.health_card)

        while True:
            slots = portal.find_slots(config.location if config.earliest_only else None)
            log.info("%d slot(s) available", len(slots))

            if slots:
                slot = slots[0]
                if portal.book(slot):
                    notifier.notify(f"✅ Vaccine slot booked: {slot}")
                    return True
                log.warning("Slot %s disappeared before it could be booked; retrying", slot)

            if once:
                return False
            time.sleep(config.poll_seconds)


def main(argv: list[str] | None = None) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="Auto-book a COVID vaccine appointment.")
    parser.add_argument("--once", action="store_true", help="check once and exit instead of polling")
    args = parser.parse_args(argv)

    booked = run(Config.from_env(), once=args.once)
    if not booked:
        log.info("No slot booked.")


if __name__ == "__main__":
    main()
