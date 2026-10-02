# COVID Vaccine Booking Bot

A Python bot that watched a regional COVID-19 vaccination portal and booked the first available
appointment on its own, instead of sitting there refreshing the page for hours.

A bit of history: I first wrote this in 2021 to book my own vaccine slot on the Veneto / ULSS 6 Euganea
(Padova) portal, back when slots for my age group dropped in small batches and vanished within minutes.
It got me one of the first slots in my cohort in Padova. The original code was tied to a portal that
doesn't exist anymore, so this is a clean rewrite I published later (you can see that from the commit
dates). The portal URL and the page selectors are configurable, so the same approach can point at a
different portal.

## How it works

It logs in with your codice fiscale and health card number, then polls the slots page every
`POLL_SECONDS`. As soon as a slot shows up in your chosen location it books the earliest one and lets you
know, in the log and optionally over Telegram.

The code is in three small pieces. `portal.py` drives the site with Selenium (`login()`, `find_slots()`
and `book()`), with all the site-specific CSS selectors kept together in one `Selectors` dataclass so
they're easy to change. `app.py` is the polling loop. `notifier.py` logs the result and, if you've set up
a Telegram bot, sends you a message.

It only books your own appointment, the one you're entitled to. All it really does is take the manual
refreshing off your hands.

## Setup

You need Python 3.10+ and Google Chrome. `webdriver-manager` grabs a matching ChromeDriver for you.

```bash
pip install -r requirements.txt
cp .env.example .env      # then fill it in
```

Put your `CODICE_FISCALE` and `HEALTH_CARD` in `.env`, along with the `PORTAL_URL` and your preferred
`LOCATION`. These are read from the environment and never committed (`.env` is git-ignored).

## Run

```bash
python -m vaccine_bot            # poll until a slot is booked
python -m vaccine_bot --once     # check once and exit
```

## Configuration

| Variable | Default | What it is |
|---|---|---|
| `CODICE_FISCALE` | (none) | Your tax code, used to log in |
| `HEALTH_CARD` | (none) | Health card number (tessera sanitaria) |
| `PORTAL_URL` | Veneto portal | The booking portal to drive |
| `LOCATION` | `Padova` | Preferred hub or city to book in |
| `EARLIEST_ONLY` | `true` | Book the earliest slot within `LOCATION` |
| `POLL_SECONDS` | `60` | Seconds between checks |
| `HEADLESS` | `false` | Run Chrome without a window |
| `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` | (none) | Optional booking notification |

## Tests

```bash
pytest
```

## Notes

The original Veneto portal is gone, so the selectors in `portal.py` are just illustrative and you'd need
to adapt them to whatever portal you point it at. Automating a public booking system can also be against
its terms; this was personal use, to book a slot I was entitled to, so use it responsibly.

## Built with

Python, Selenium and webdriver-manager.

## License

[MIT](LICENSE)
