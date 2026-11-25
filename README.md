# The World Today — Tuesday, 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Kkajasd/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Kkajasd/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A one-page newspaper front page summing up the world's news of Tuesday, 24 November 2026: 16 verified stories across world affairs, markets, technology and sport, each with a headline and a one-line summary, under the masthead "The World Today". The v2 layout leads with one hero story across the full width, three leads in a row, then a two-column body (World / Markets, Tech & Sport), and closes with a market-numbers strip. The image is rendered deterministically with Pillow by `tools/draw_frontpage_v2.py` and shipped as `entry.png`; `main.ts` copies it to the output directory. Every story happened, or was first reported, on 24 November 2026 and is sourced in `SOURCES.md`.

## Run

```sh
python3 tools/draw_frontpage_v2.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
