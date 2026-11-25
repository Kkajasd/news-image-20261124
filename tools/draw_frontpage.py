#!/usr/bin/env python3
"""Draw 'The World Today' front page for Tuesday, 24 November 2026.

Renders a 1024x1024 newspaper front page with 40 verified stories from
24 November 2026. Fully deterministic: fixed layout, fixed fonts, no
timestamps, no randomness. Writes entry.png next to this script's parent
directory (the repository root) and, when run directly, to ./entry.png.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 26
PAPER = (248, 244, 233)
INK = (20, 20, 20)
RED = (143, 29, 29)
GREY = (90, 86, 76)
RULE = (60, 58, 50)

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
LEADS = [
    ("MARKETS",
     "Dow tops 50,000 as Wall St splits",
     "Dow +0.85% to 50,018.70; S&P 500 -0.50%, Nasdaq -1.48% as Nvidia "
     "gives back Monday's 31% surge."),
    ("BUSINESS",
     "Sanofi to buy Insmed for $41bn",
     "Drugmaker agrees $175 a share in cash, its biggest bet yet on "
     "respiratory medicine."),
    ("GAZA",
     "Strikes kill Hamas security chief",
     "Israeli airstrikes kill Naeem Abu Nahel and six others, including "
     "two police officers, medics and police say."),
]

COLUMNS = [
    ("WORLD", [
        ("Zaporizhzhia flats hit overnight",
         "Russian attack kills two and wounds 40, four of them children, "
         "the regional governor says."),
        ("Russian jets enter Seoul air zone",
         "Several aircraft flew into South Korea's air defence zone, its "
         "Joint Chiefs of Staff say."),
        ("NATO vows to defend space",
         "Rutte warns the alliance will answer threats in orbit after "
         "reports of a Russian nuclear satellite."),
        ("Germany first into Ukraine's Delta",
         "Berlin gains access to Kyiv's battlefield system; talks on more "
         "interceptor missiles."),
        ("Vance and Rubio meet Qatar PM",
         "Separate White House talks with Sheikh Mohammed focus on Iran, "
         "AP reports."),
        ("Baghdad orders Kurdish oilfields run",
         "PM tells the ministry to manage fields in Diyala, Kirkuk and "
         "Nineveh after a smuggling probe."),
        ("Fighting traps Ebola teams in DRC",
         "Clashes near a hospital in Ituri force responders to take cover "
         "for more than 24 hours."),
        ("UN seeks Libya port attack probe",
         "Mission urges an independent inquiry into strikes at Benghazi "
         "port and offshore."),
        ("Quake shakes Nepal and Kathmandu",
         "Magnitude 5.6 tremor strikes near the Tibet border at 7:17 a.m.; "
         "no damage reported."),
        ("Car bomb rocks Villavicencio",
         "Blast destroys buildings in the Colombian city; no victims "
         "confirmed, the president says."),
        ("Pakistan astronaut bound for Tiangong",
         "China opens its space station to a first foreign astronaut, "
         "Zeeshan Ali, on Shenzhou-24."),
        ("Fourteen back Rohingya ruling",
         "UK, Spain, Canada, Australia and ten others affirm the ICJ "
         "genocide finding on Myanmar."),
    ]),
    ("MARKETS & AMERICAS", [
        ("Dell reports record AI backlog",
         "AI server backlog hits $132.3bn as Dell posts results after the "
         "closing bell."),
        ("CrowdStrike in $44bn Zscaler deal",
         "Cybersecurity pair at the centre of a reported $44bn "
         "acquisition as AI fuels attacks."),
        ("Nvidia board backs Huang return",
         "Board re-nominates Jensen Huang as chief executive and says "
         "there is no national-security risk."),
        ("US confidence at 21-month high",
         "Consumer confidence rises to 103.3, its highest since January "
         "2025."),
        ("Singapore grows 6.1% in Q3",
         "AI boom lifts exports; the government raises its 2026 forecast "
         "to around 6%."),
        ("Bitcoin slides below $60,000",
         "Bitcoin falls 2.7% to $59,655 as crypto joins the tech "
         "sell-off."),
        ("Dollar General suit spans 30 states",
         "Ten more states join the FTC case over alleged till "
         "overcharges."),
        ("UK retail sales beat forecasts",
         "October sales top every forecast as shoppers stock up on "
         "long-life food."),
        ("Trump orders death-penalty push",
         "President to direct the DOJ to speed federal death sentences, "
         "including for child murders."),
        ("Pentagon faults Canada on defence",
         "US says Ottawa falls short as a credible partner in defending "
         "North America."),
        ("Measles claims ninth in Pennsylvania",
         "State reports a ninth death in an outbreak now touching 46 "
         "counties."),
        ("Mexico to try 'El Chapo Isidro'",
         "Mexico will prosecute the cartel figure despite a US "
         "extradition request."),
    ]),
    ("TECHNOLOGY, SPORT & LIFE", [
        ("Claude 'proves' VP \u2260 VNP",
         "Anthropic posts a 70-page paper credited solely to Claude; no "
         "human has yet reviewed it."),
        ("Gemini agents cut quantum costs 290\u00d7",
         "DeepMind teams find cheaper quantum algorithms, each verified "
         "in the Lean prover."),
        ("Anthropic launches Claude Ship",
         "New tool lets Claude review pull requests and approve merges by "
         "team policy."),
        ("Claude misuse scan goes to beta",
         "Enterprise Frontier Safeguards open in public beta, data kept in "
         "customer clouds."),
        ("AI brings few layoffs, study finds",
         "Anthropic interviews 58 firms: only two cut a role because of "
         "AI; hiring slows."),
        ("Meta's Muse reaches the UK",
         "Personal AI agent launches for UK adults, with approval needed "
         "on every purchase."),
        ("Amazon buys Decart chip software",
         "Amazon acquires the AI optimisation stack and hires Decart's "
         "founders and engineers."),
        ("OpenAI and Cisco launch Shirudo",
         "Open-source Linux runtime shields systems while security "
         "patches roll out."),
        ("DeepMind sets 'Humanity's First Exam'",
         "New Kaggle benchmark tests whether models answer everyday "
         "questions reliably."),
        ("States sue SpaceX over Grok images",
         "Oregon and Virginia sue over Grok-generated child abuse images, "
         "CNBC reports."),
        ("Madrid rout PSV 5\u20131 in Europe",
         "Mbapp\u00e9 scores twice; Arsenal draw 1\u20131 with Dortmund, "
         "Man City 2\u20132 with Napoli."),
        ("Cyclone Akvan drives 80,000 to safety",
         "India moves people from Odisha and Andhra Pradesh as the severe "
         "storm closes in."),
        ("Pilgrims mark Guru Nanak's 557th",
         "Thousands of Sikhs gather at Nankana Sahib in Pakistan for the "
         "birth anniversary."),
    ]),
]


def draw_masthead(d):
    title = font(SERIF_B, 62)
    d.text((W // 2, 24), "THE WORLD TODAY", font=title, fill=INK,
           anchor="ma")
    date_f = font(SERIF_I, 21)
    d.text((W // 2, 96), "Tuesday, 24 November 2026", font=date_f,
           fill=INK, anchor="ma")
    sub_f = font(SANS_B, 11)
    d.text((W // 2, 122), "THE DAY'S NEWS IN ONE PAGE  \u00b7  40 STORIES",
           font=sub_f, fill=GREY, anchor="ma")
    d.line([(MARGIN, 142), (W - MARGIN, 142)], fill=RULE, width=2)


def draw_leads(d):
    y0 = 152
    col_w = 318
    gap = 9
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
    d.line([(MARGIN, 284), (W - MARGIN, 284)], fill=RULE, width=2)
    return 296


def draw_columns(d, y0):
    col_w = 318
    gap = 9
    xs = [MARGIN + i * (col_w + gap) for i in range(3)]
    sec_f = font(SANS_B, 13)
    head_f = font(SERIF_B, 15)
    sum_f = font(SANS, 12)
    bottom = 986
    for x, (section, stories) in zip(xs, COLUMNS):
        d.text((x, y0), section, font=sec_f, fill=INK)
        d.line([(x, y0 + 20), (x + col_w, y0 + 20)], fill=RULE, width=1)
        y = y0 + 28
        for head, summ in stories:
            hl = wrap(d, head, head_f, col_w)
            sl = wrap(d, summ, sum_f, col_w)
            block = len(hl[:2]) * 17 + len(sl[:2]) * 14 + 4
            if y + block > bottom:
                raise SystemExit(
                    "OVERFLOW in %s at story %r (y=%d, block=%d)"
                    % (section, head, y, block))
            for line in hl[:2]:
                d.text((x, y), line, font=head_f, fill=INK)
                y += 17
            for line in sl[:2]:
                d.text((x, y), line, font=sum_f, fill=INK)
                y += 14
            y += 4
        # vertical divider between columns
        if x > MARGIN:
            d.line([(x - gap // 2 - 1, y0), (x - gap // 2 - 1, bottom)],
                   fill=(200, 196, 184), width=1)


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
    y0 = draw_leads(d)
    draw_columns(d, y0)
    draw_footer(d)
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "entry.png")
    img.save(out, format="PNG")
    print("wrote %s (%dx%d)" % (out, W, H))


if __name__ == "__main__":
    main()
