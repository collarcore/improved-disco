```
               \/
  ___  ____   ____ ___ _   _ _____
 / _ \| __ ) / ___|_ _| \ | | ____|
| | | |  _ \| |    | ||  \| |  _|
| |_| | |_) | |___ | || |\  | |___
 \___/|____/ \____|___|_| \_|_____|
```

A text-mode idle clicker about Slovenia's 212 municipalities (občine).
Ring the church bell, build an economy, and unlock every občina from the
smallest (Osilnica, 326 people) to the largest (Ljubljana, ~303,000).
Black and white, one font, one character grid. Slovenian and English.

**Play:** https://collarcore.github.io/improved-disco/

![The game mid-run](docs/screenshot.png)

![The map filling in, občina by občina](docs/map.gif)

## How it plays

- **Zvonik**: click the bell (or press space) for tolarji. Ringing fills the **zvonjenje** meter,
  which multiplies *all* income while you keep ringing: ×1.5 with the handbell, up to ×5 with
  the bells of every parish. It drains when you pause, so active play matters all game.
  Five bell upgrades, each with its own sound, from a small handbell to *pritrkavanje*.
- **Proizvodnja**: 12 producers, from *njiva* to *elektrarna*. New ones open as you unlock more občine.
  `*` marks the best price for the income.
- **Občine**: unlock them in order of population. Every resident adds to your income
  (1 resident = +0.005 %), and finishing a statistical region gives ×1.25.
- **Znamenitosti**: 44 municipalities carry a landmark upgrade, such as Idrija's mercury mine,
  Krško's power plant, Planica in Kranjska Gora or kremšnita in Bled.
- **Kurent**: shows up on the map every 4–8 minutes for 13 seconds. Catch him for ×3 income (30 s),
  a pustni krof worth 3 minutes of income, or clicks ×7 (10 s). A nice bonus, not an engine.
- **Referendum**: prestige. Reset your run for votes (each +5 % income for good) and adopt one of
  12 **constitutional amendments**: cheaper producers, a more frequent Kurent, the first 25 občine free, and so on.
- **Teden**: every weekday has its own bonus from village life: tržni dan (Monday), obrtni dan,
  delavnik, izletniki, petek v gostilni, gasilska veselica and nedeljska maša (Sunday: the meter fills twice as fast).
- **Prazniki**: rarer extras from the real calendar: Pust and Prešernov dan in February,
  Dan državnosti in June, the tourist season, trgatev, Martinovanje in November, Christmas, the ski season.
- **Dosežki**: 55 achievements, each +1 %. One of them is a secret.

The game saves in your browser and earns at half speed while closed (up to 8 h).
Settings → *Prenos igre* copies the save so you can continue on another device.

## How long it takes

From `python3 tools/balance.py` (models producers, landmarks, bells, the ringing meter,
the week and referendums; leaves out the Kurent, achievements, amendments and holidays,
so real players are somewhat faster):

| občine | active player (hours of play) | casual player, 3×10 min a day (days) |
|---|---|---|
| 10 | 0.8 | 0.9 |
| 25 | 2.9 | 1.5 |
| 50 | 6.7 | 2.9 |
| 100 | 9.7 | 4.3 |
| 150 | 15.2 | 7.9 |
| all 212 | ~31 (8 referendums) | ~18.5 (6 referendums) |

Without referendums a run stalls around 150 občin; the *next občina* panel says when one pays off.

## Playtesting

Settings → *kopiraj statistiko* copies a short report: total time with the page open,
calendar days since the first start, and when each milestone (10, 25, 50 … 212 občin,
every referendum) was reached. Testers can paste it into a message. Nothing is sent anywhere by the game.

## Accessibility

The ASCII art, the map and the big counter are hidden from screen readers. Instead there is
a text summary (balance, income, next občina and its cost), panel titles are headings, buttons
carry plain labels, new log entries are announced, and a hidden button lets screen-reader
users catch the Kurent. Animations stop under *prefers-reduced-motion*.

## Files

| path | what |
|---|---|
| `index.html` | the whole game, built (open it directly, no server needed) |
| `src/game.html` | page shell: markup and CSS |
| `src/game.js` | the game; every string is a `tr('slovensko','English')` pair |
| `data/obcine.json` | name, population, area, founding year, region, coordinates |
| `data/maps.json` | the ASCII maps (84 and 44 columns), one cell → one občina |
| `tools/build.py` | fills the shell with the game, data and maps → `index.html` |
| `tools/mapgen.py` | regenerates the maps from coordinates (weighted Voronoi) |
| `tools/econ.py` | game data for the simulator |
| `tools/balance.py` | balance simulator: active and casual players, prices in one place |
| `fonts/` | IBM Plex Mono, self-hosted |
| `docs/` | README images |
| `tests/` | browser tests (see `tests/README.md`) |

Rebuild after editing: `python3 tools/build.py`

Saves carry a version number (`v`). When the save format changes, bump `VERSION` in
`src/game.js` and add a step to `migrate()` so older saves are upgraded instead of broken.

## Hosting

GitHub Pages → *Deploy from a branch* → `main`, folder `/ (root)`.

## Licence

Code: MIT, see `LICENSE`. Data: derived from Wikipedia
([Seznam občin v Sloveniji](https://sl.wikipedia.org/wiki/Seznam_ob%C4%8Din_v_Sloveniji) and the
English articles on each municipality), CC BY-SA 4.0. The map is an approximation built from each
municipality's seat, not real borders. Font: IBM Plex Mono, SIL Open Font License 1.1.
