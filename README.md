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
Black and white, one font, one character grid.

## How it plays

- **Zvonik**: click the bell (or press space) for tolarji.
- **Proizvodnja**: 12 producers, from *njiva* to *elektrarna*. New ones open as you unlock more občine.
- **Občine**: unlock them in order of population. Every resident adds to your income
  (1 resident = +0.005 %), and finishing a statistical region gives ×1.25.
- **Znamenitosti**: 44 municipalities carry a landmark upgrade, such as Idrija's mercury mine,
  Krško's power plant, Planica in Kranjska Gora or kremšnita in Bled.
- **Kurent**: shows up on the map now and then. Catch him for a ×7 boost, a pustni krof or a click frenzy.
- **Referendum**: prestige. Reset your run for votes; each vote gives +2 % income for good.
- **Dosežki**: 50 achievements, each +1 %. One of them is a secret.

A perfect bot clicking 5×/s needs about 1 h for 50 občine, 2 h for 100 and 10 h for all 212;
real players take longer, and referendums speed up later runs. The game saves to your browser and earns at half speed while you're away (up to 8 h).

## Files

| path | what |
|---|---|
| `index.html` | the whole game, built (open it directly, no server needed) |
| `src/game.html` | source template with `/*DATA*/` and `/*MAPS*/` placeholders |
| `data/obcine.json` | name, population, area, founding year, region, coordinates |
| `data/maps.json` | the ASCII maps (84 and 44 columns), one cell → one občina |
| `tools/build.py` | fills the template → `index.html` |
| `tools/mapgen.py` | regenerates the maps from coordinates (weighted Voronoi) |
| `tools/econ.py`, `tools/sim.py` | balance simulation with a greedy bot |
| `fonts/` | IBM Plex Mono, self-hosted (SIL Open Font License, see `fonts/OFL.txt`) |

Rebuild after editing: `python3 tools/build.py`

## Hosting

GitHub Pages → *Deploy from a branch* → `main`, folder `/ (root)`.

## Data

Population and area from the list of municipalities on Slovenian Wikipedia
([Seznam občin v Sloveniji](https://sl.wikipedia.org/wiki/Seznam_ob%C4%8Din_v_Sloveniji)),
coordinates from the English Wikipedia articles, both CC BY-SA 4.0.
The map is an approximation built from each municipality's seat, not real borders.
