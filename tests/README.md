# Tests

Browser tests with Playwright (`pip install playwright && playwright install chromium`).
Serve the repo first: `python3 -m http.server 8765`, then run from the repo root:

| script | checks |
|---|---|
| `suite.py` | clicks register (slow, fast, touch), nothing moves while buying or unlocking, pop-up stays still, Kurent bells, voice cap, catching the Kurent, save copy/load |
| `layout.py` | every line of every panel is the same width, no sideways overflow, at 10 widths and 5 game stages |
| `truncation.py` | no text is cut off anywhere (pages through the register and achievements, hovers every municipality) |
| `flicker.py` | spamming the bell keeps the button steady |
| `taps.py` | phone: 30 quick taps ring 30 times, drumming pays at most 10 a second, 5 fast [KUPI] taps buy 5, no zoom, the page stays put |
| `popups.py` | every pop-up kind with the longest texts, 10 sizes × 3 scroll positions × 2 languages: on screen, on its column, box intact |
| `secrets.py` | every secret can be found and none of them breaks anything (spoilers!) |
| `hover.py` | sweeping the mouse across the map never flashes the legend |
| `extra.py` | two-column layouts, keyboard play, performance, offline income, meter drain, English UI, light theme, map highlighting, referendum |

`LANGX=en python3 tests/layout.py` runs the layout and truncation checks in English.
Set `CHROME=/path/to/chrome` to use a specific browser.

The tests use the game's `window.__dbg` hooks, which exist only on `localhost`/`127.0.0.1` or with `?debug`
in the address, so the live site has no cheat menu in the console.
