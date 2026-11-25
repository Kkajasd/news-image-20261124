#!/usr/bin/env python3
"""Draw 'The World Today' front page, v2 layout, Tuesday 24 November 2026.

Rebuild: 14 verified stories from 24 November 2026, none of them the
original front page's 40. Layout differs from v1: one hero lead across the
full width, three leads in a row, then a two-column body, plus a market
numbers strip. Fully deterministic: fixed layout, fixed fonts, no
timestamps, no randomness. Writes entry.png to the repository root.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
PAPER = (250, 246, 236)
INK = (20, 20, 20)
RED = (143, 29, 29)
GREY = (90, 86, 76)
RULE = (60, 58, 50)
FAINT = (200, 196, 184)

# Fonts are vendored in tools/fonts: the grading sandbox has no system
# fonts. Fall back to the system path when running locally.
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
if not os.path.isdir(FONT_DIR):
    FONT_DIR = "/usr/share/fonts/truetype/liberation"
SERIF_B = os.path.join(FONT_DIR, "LiberationSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "LiberationSerif-Regular.ttf")
SERIF_I = os.path.join(FONT_DIR, "LiberationSerif-Italic.ttf")
SANS_B = os.path.join(FONT_DIR, "LiberationSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "LiberationSans-Regular.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- stories
# (kicker, headline, summary) -- every story happened, or was first
# reported, on Tuesday, 24 November 2026. See SOURCES.md for outlets.
HERO = (
    "UKRAINE \u00b7 LIBYA",
    "Ukraine sinks Russian warship off Libya",
    "Kyiv confirms drone strikes sank the corvette Merkury off Benghazi and "
    "hit a cargo ship in the Gulf of Finland; Tripoli protests as the war "
    "reaches its waters.",
)

LEADS = [
    ("WORLD",
     "Three tankers hit by mines in Hormuz",
     "Iran's Revolutionary Guard says three oil tankers caught fire after "
     "striking naval mines; crude climbs as shipping risks return."),
    ("TRADE",
     "US readies tariff probe on 16 partners",
     "The Trump administration prepares Section 301 findings on excess "
     "industrial capacity in China, the EU, Japan and others; new duties "
     "expected."),
    ("TECH",
     "GPT-6.2 Sol becomes ChatGPT default",
     "OpenAI rolls out the chat-tuned model worldwide; image understanding "
     "jumps to 71.7% from 47.4%."),
]

COLUMNS = [
    ("WORLD", [
        ("Zelenskyy: Ukraine needs $125bn in 2027",
         "Kyiv will need \u20ac115bn in external support next year as the "
         "war enters its fifth year, the president says."),
        ("Lukashenko offers to fly with Zelenskyy to Moscow",
         "Belarus leader proposes a joint trip for Kremlin talks and says "
         "Russian forces are winning."),
        ("UK warns of Russian sabotage threat",
         "MI5 alerts companies supplying Ukraine's military to a heightened "
         "sabotage risk from Moscow."),
        ("Norway\u2013Ukraine expand anti-drone pact",
         "Allies deepen work on the DESNA air-defence system as Kyiv faces "
         "near-daily air attacks."),
        ("Moscow accuses Estonia of hostile acts",
         "Russia warns Tallinn's actions are on the verge of triggering "
         "open war, state media report."),
        ("Hungary's Magyar to meet Zelenskyy",
         "The Hungarian premier meets Ukraine's president in Zakarpattia, "
         "but says Budapest will send no arms."),
    ]),
    ("MARKETS, TECH & SPORT", [
        ("Canada's Macklem hints at rate rises",
         "Bank of Canada governor says rates may need to rise if inflation "
         "stays too high; the loonie jumps."),
        ("Germany's Ifo beats forecasts",
         "Business climate rises to 90.6 in November, above the 90.5 "
         "forecast, in a further sign of recovery."),
        ("China suspends export curbs to US",
         "Beijing extends the suspension on some critical-material export "
         "curbs until January after the Shenzhen summit."),
        ("Australia inflation jumps to 4.9%",
         "October CPI surge keeps the Reserve Bank on alert for further "
         "rate rises as the economy slows."),
        ("Google Search adds Personal Intelligence",
         "Search can now draw on Gmail, Drive, Photos and Calendar for "
         "tailored answers."),
        ("English clubs held in Europe",
         "Arsenal draw 1\u20131 with Dortmund and Manchester City 2\u20132 "
         "with Napoli as Galatasaray and Como win again."),
    ]),
]

NUMBERS = ("S&P 500  7,206  \u22120.7%      Gold  $3,553  \u22122.3%      "
           "WTI crude  $82.53  +1.4%      USD/CAD  1.4269  \u22120.7%")


def draw_masthead(d):
    title = font(SERIF_B, 60)
    d.text((W // 2, 22), "THE WORLD TODAY", font=title, fill=INK,
           anchor="ma")
    date_f = font(SERIF_I, 20)
    d.text((W // 2, 92), "Tuesday, 24 November 2026", font=date_f,
           fill=INK, anchor="ma")
    sub_f = font(SANS_B, 11)
    d.text((W // 2, 118), "THE DAY'S NEWS IN ONE PAGE  \u00b7  16 STORIES",
           font=sub_f, fill=GREY, anchor="ma")
    d.line([(MARGIN, 140), (W - MARGIN, 140)], fill=RULE, width=2)


def draw_hero(d):
    y0 = 152
    kicker, head, summ = HERO
    d.text((MARGIN, y0), kicker, font=font(SANS_B, 13), fill=RED)
    head_f = font(SERIF_B, 30)
    hl = wrap(d, head, head_f, W - 2 * MARGIN)
    y = y0 + 22
    for line in hl[:2]:
        d.text((MARGIN, y), line, font=head_f, fill=INK)
        y += 35
    sum_f = font(SANS, 14)
    sl = wrap(d, summ, sum_f, W - 2 * MARGIN)
    y += 2
    for line in sl[:2]:
        d.text((MARGIN, y), line, font=sum_f, fill=INK)
        y += 18
    d.line([(MARGIN, 288), (W - MARGIN, 288)], fill=RULE, width=2)
    return 300


def draw_leads(d, y0):
    col_w = 312
    gap = 12
    xs = [MARGIN + i * (col_w + gap) for i in range(3)]
    kick_f = font(SANS_B, 12)
    head_f = font(SERIF_B, 19)
    sum_f = font(SANS, 13)
    for x, (kicker, head, summ) in zip(xs, LEADS):
        d.text((x, y0), kicker, font=kick_f, fill=RED)
        hl = wrap(d, head, head_f, col_w)
        y = y0 + 20
        for line in hl[:2]:
            d.text((x, y), line, font=head_f, fill=INK)
            y += 22
        sl = wrap(d, summ, sum_f, col_w)
        y += 2
        for line in sl[:3]:
            d.text((x, y), line, font=sum_f, fill=INK)
            y += 16
    d.line([(MARGIN, 428), (W - MARGIN, 428)], fill=RULE, width=2)
    return 440


def draw_columns(d, y0):
    col_w = 472
    gap = 24
    xs = [MARGIN, MARGIN + col_w + gap]
    sec_f = font(SANS_B, 14)
    head_f = font(SERIF_B, 16)
    sum_f = font(SANS, 12)
    bottom = 892
    for x, (section, stories) in zip(xs, COLUMNS):
        d.text((x, y0), section, font=sec_f, fill=INK)
        d.line([(x, y0 + 21), (x + col_w, y0 + 21)], fill=RULE, width=1)
        y = y0 + 30
        for head, summ in stories:
            hl = wrap(d, head, head_f, col_w)
            sl = wrap(d, summ, sum_f, col_w)
            block = len(hl[:2]) * 19 + len(sl[:2]) * 15 + 8
            if y + block > bottom:
                raise SystemExit(
                    "OVERFLOW in %s at story %r (y=%d, block=%d)"
                    % (section, head, y, block))
            for line in hl[:2]:
                d.text((x, y), line, font=head_f, fill=INK)
                y += 19
            for line in sl[:2]:
                d.text((x, y), line, font=sum_f, fill=INK)
                y += 15
            y += 8
        if x > MARGIN:
            d.line([(x - gap // 2 - 1, y0), (x - gap // 2 - 1, bottom)],
                   fill=FAINT, width=1)


def draw_numbers(d):
    d.line([(MARGIN, 908), (W - MARGIN, 908)], fill=RULE, width=1)
    lab_f = font(SANS_B, 11)
    d.text((W // 2, 918), "THE DAY IN NUMBERS", font=lab_f, fill=GREY,
           anchor="ma")
    num_f = font(SANS, 13)
    d.text((W // 2, 938), NUMBERS, font=num_f, fill=INK, anchor="ma")


def draw_footer(d):
    foot_f = font(SANS, 11)
    d.line([(MARGIN, 992), (W - MARGIN, 992)], fill=RULE, width=1)
    d.text((W // 2, 1000),
           "All stories happened, or were first reported, on Tuesday, "
           "24 November 2026.",
           font=foot_f, fill=GREY, anchor="ma")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    y0 = draw_hero(d)
    y0 = draw_leads(d, y0)
    draw_columns(d, y0)
    draw_numbers(d)
    draw_footer(d)
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "entry.png")
    img.save(out, format="PNG")
    print("wrote %s (%dx%d)" % (out, W, H))


if __name__ == "__main__":
    main()
