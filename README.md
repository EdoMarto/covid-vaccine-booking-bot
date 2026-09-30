# COVID Vaccine Booking Bot

A Python bot that watched a regional COVID‑19 vaccination portal and booked the earliest available
appointment automatically, instead of refreshing the page by hand for hours.

> **History.** I first wrote this in 2021 to book my own vaccine slot on the Veneto / ULSS 6 Euganea
> (Padova) portal, when appointments for my age group were released in small batches and gone within
> minutes — it got me one of the first slots in my cohort in Padova. The original code was tied to a
> portal that no longer exists. **This is a clean reimplementation I published later** (see the commit
> dates); the portal URL and the page selectors are configurable so the approach can be pointed at
> another portal.

## How it works

```
login (codice fiscale + tessera sanitaria)
      │
      ▼
poll the slots page every POLL_SECONDS ──► any slot in LOCATION? ──no──► wait ──┐
      ▲                                            │yes                          │
      └────────────────────────────────────────────┼─────────────────────────────┘
                                                    ▼
                                    book the earliest slot ──► notify (log + optional Telegram)
```

- **`portal.py`** drives the site with Selenium: `login()`, `find_slots()` and `book()`. All the
  site‑specific CSS selectors live in one `Selectors` dataclass so they are easy to adapt.
- **`app.py`** is the polling loop: it checks the offered slots, books the earliest one in your
  preferred location, and stops once it succeeds.
- **`notifier.py`** logs the result and, if a Telegram bot is configured, sends you a message.

It books only your own appointment, for which you are eligible — it just removes the manual refreshing.

## Setup

Requirements: Python 3.10+, Google Chrome. `webdriver-manager` fetches a matching ChromeDriver
automatically.

```bash
pip install -r requirements.txt
cp .env.example .env      # then fill it in
```

Fill `.env` with your `CODICE_FISCALE` and `HEALTH_CARD`, the `PORTAL_URL`, and your preferred
`LOCATION`. These are read from the environment and never committed (`.env` is git‑ignored).

## Run

```bash
python -m vaccine_bot            # poll until a slot is booked
python -m vaccine_bot --once     # check once and exit
```

## Configuration

| Variable | Default | Description |
|---|---|---|
| `CODICE_FISCALE` | – | Your tax code, used to log in |
| `HEALTH_CARD` | – | Health‑card number (tessera sanitaria) |
| `PORTAL_URL` | Veneto portal | Booking portal to drive |
| `LOCATION` | `Padova` | Preferred hub / city to book in |
| `EARLIEST_ONLY` | `true` | Book the earliest slot within `LOCATION` |
| `POLL_SECONDS` | `60` | Seconds between checks |
| `HEADLESS` | `false` | Run Chrome without a window |
| `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` | – | Optional booking notification |

## Tests

```bash
pytest
```

## Notes

- The original Veneto portal is offline, so the selectors in `portal.py` are illustrative and must be
  adapted to the live markup of whatever portal you target.
- Automating a public booking system may be against its terms; this was personal use to book a slot I
  was entitled to. Use responsibly.

## Tech stack

Python · Selenium · webdriver-manager

## License

[MIT](LICENSE)
