"""Selenium automation of the regional vaccine-booking portal.

The Veneto portal (and most regional ones) worked the same way: log in with your
codice fiscale and health-card number, land on a page that lists the appointment
slots the system currently offers, and confirm one. This class wraps those three
steps behind `login()`, `find_slots()` and `book()`.

The portal is no longer online and each region used slightly different markup, so
the CSS selectors below are grouped in one place (`Selectors`) to be adapted to
whatever portal you point `PORTAL_URL` at.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from .models import Slot

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Selectors:
    """Portal-specific CSS selectors, kept together so they are easy to update."""

    cf_input: str = "input#codiceFiscale"
    card_input: str = "input#tesseraSanitaria"
    login_button: str = "button[type=submit]"
    slot_row: str = ".appointment-slot"
    slot_datetime_attr: str = "data-datetime"  # ISO datetime on each slot row
    slot_hub: str = ".slot-hub"
    slot_book_button: str = "button.book"
    confirm_button: str = "button.confirm"
    confirmation_banner: str = ".booking-confirmed"


class VaccinePortal:
    def __init__(self, url: str, headless: bool = False, selectors: Selectors | None = None) -> None:
        self.url = url
        self.selectors = selectors or Selectors()
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1280,900")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 20)

    # -- lifecycle ------------------------------------------------------------

    def __enter__(self) -> "VaccinePortal":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def close(self) -> None:
        try:
            self.driver.quit()
        except Exception:
            pass

    # -- steps ----------------------------------------------------------------

    def login(self, codice_fiscale: str, health_card: str) -> None:
        s = self.selectors
        self.driver.get(self.url)
        self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, s.cf_input))).send_keys(codice_fiscale)
        self.driver.find_element(By.CSS_SELECTOR, s.card_input).send_keys(health_card)
        self.driver.find_element(By.CSS_SELECTOR, s.login_button).click()
        self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, s.slot_row + ", " + s.confirmation_banner)))
        log.info("Logged in")

    def find_slots(self, location: str | None = None) -> list[Slot]:
        """Read the slots currently offered, optionally filtered by hub/location."""
        s = self.selectors
        slots: list[Slot] = []
        for row in self.driver.find_elements(By.CSS_SELECTOR, s.slot_row):
            hub = row.find_element(By.CSS_SELECTOR, s.slot_hub).text.strip()
            raw = row.get_attribute(s.slot_datetime_attr)
            if not raw:
                continue
            if location and location.lower() not in hub.lower():
                continue
            try:
                when = datetime.fromisoformat(raw)
            except ValueError:
                continue
            slots.append(Slot(hub=hub, when=when))
        slots.sort(key=lambda slot: slot.when)
        return slots

    def book(self, slot: Slot) -> bool:
        """Confirm `slot`. Returns True once the confirmation banner appears."""
        s = self.selectors
        for row in self.driver.find_elements(By.CSS_SELECTOR, s.slot_row):
            raw = row.get_attribute(s.slot_datetime_attr)
            if raw and datetime.fromisoformat(raw) == slot.when:
                row.find_element(By.CSS_SELECTOR, s.slot_book_button).click()
                self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, s.confirm_button))).click()
                self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, s.confirmation_banner)))
                return True
        return False
