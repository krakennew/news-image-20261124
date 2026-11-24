#!/usr/bin/env python3
"""Draw 'The World Today - 24 November 2026' front page, 1024x1024.

44 verified stories, lead + world map with markers + story grid.
Run: python3 draw_poster.py  -> writes entry.png beside this file.
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (26, 26, 26)
MUTED = (74, 74, 74)
NAVY = (20, 38, 74)
RED = (179, 35, 27)
SEA = (220, 235, 245)
LAND = (203, 190, 162)
LAND_LINE = (138, 127, 102)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF = font("DejaVuSerif-Bold.ttf", 40)
F_SERIF_SMALL = font("DejaVuSerif-Bold.ttf", 31)
F_BOLD_13 = font("DejaVuSans-Bold.ttf", 13)
F_BOLD_12 = font("DejaVuSans-Bold.ttf", 12)
F_BOLD_11 = font("DejaVuSans-Bold.ttf", 11)
F_BOLD_10 = font("DejaVuSans-Bold.ttf", 10)
F_REG_13 = font("DejaVuSans.ttf", 13)
F_REG_11 = font("DejaVuSans.ttf", 11)
F_REG_10 = font("DejaVuSans.ttf", 10)
F_NUM = font("DejaVuSans-Bold.ttf", 9)
F_NUM_S = font("DejaVuSans-Bold.ttf", 8)

SECTION_COLORS = {
    "WAR": (179, 35, 27),
    "CLIMATE": (30, 107, 58),
    "DISASTER": (107, 58, 30),
    "MARKETS": (122, 77, 0),
    "ASIA": (91, 45, 142),
    "RIGHTS": (142, 42, 91),
    "WORLD": (51, 51, 51),
    "SPORT": (29, 78, 137),
}

# (number, section, headline, summary) -- grid cells, stories 3..44
STORIES = [
    (3, "WAR", "SPARTA II ABLAZE IN GULF OF FINLAND",
     "Russian cargo ship hit by two drones; 16 crew rescued, vessel towed to St Petersburg."),
    (10, "WAR", "RUSSIA WARNS ESTONIA OF \"OPEN WAR\"",
     "Moscow rages after Tallinn says it will shut the border from 1 December."),
    (11, "WAR", "ESTONIA TO SHUT RUSSIA BORDER",
     "Crossings close for at least six months over an alleged arson plot."),
    (12, "WAR", "RUSSIAN MISSILES LAND IN POLAND",
     "Three Kh-101 cruise missiles crash; NATO sends AWACS early-warning jets."),
    (13, "WAR", "RUSSIAN DRONE VIOLATES POLISH AIRSPACE",
     "Drone strays during a night attack on western Ukraine; Poland scrambles."),
    (14, "WAR", "SEOUL ALERT AS RUSSIAN JET INTRUDES",
     "South Korea briefly warns Ulleung island and scrambles fighters on Tuesday."),
    (15, "WAR", "US-IRAN NUCLEAR TALKS STALL",
     "Trump seeks a permanent deal and says he is \"not rushing\" new strikes."),
    (16, "WAR", "ISRAEL STRIKES KILL 3 IN GAZA",
     "Airstrikes kill an UNRWA worker among three; Gaza toll mounts."),
    (17, "WAR", "US TO TRAIN SYRIAN FORCES",
     "Demining training planned - first US mission with Syria's army since 2024."),
    (18, "WORLD", "N. KOREA MAY SHUT SWISS OFFICE",
     "Pyongyang condemns Swiss sanctions over children moved from occupied Ukraine."),
    (19, "WORLD", "TAJIKISTAN QUITS WAR-CRIMES COURT",
     "ICC exit filed as Putin visits Dushanbe; fourth country to leave since July."),
    (20, "WAR", "LIBYA'S EAST CONDEMNS BENGHAZI ATTACK",
     "Eastern government denounces the strike on Russian ships in its port."),
    (21, "WAR", "ZELENSKIY: RUSSIA PLANS NEW STRIKES",
     "Kyiv warns of fresh attacks as winter closes in on the power grid."),
    (22, "WORLD", "MURMANSK GOVERNOR DETAINED",
     "Russian regional chief held on suspicion of embezzlement."),
    (23, "WAR", "GERMANY TO USE KYIV'S DELTA TOOL",
     "Berlin signs on to Ukraine's battle-management system."),
    (24, "WORLD", "VANCE'S VENEZUELA OIL TIES PROBED",
     "US Senate panel investigates the vice-president's links to a prized contract."),
    (25, "WAR", "SUDAN DRONES KILL 4 IN KHARTOUM",
     "Strikes hit homes and a UN building; UN and US condemn the attacks."),
    (26, "WAR", "RUSSIAN STRIKES HIT KYIV HOMES",
     "Two killed and four hurt in attacks on the capital's region."),
    (4, "CLIMATE", "COP31 COLLAPSES IN ANTALYA",
     "No climate pact after two weeks; longest COP ever, first breakdown since 2009."),
    (5, "CLIMATE", "COP32 SET FOR ADDIS ABABA",
     "Next summit runs 8-19 November 2027 in Ethiopia after the Antalya failure."),
    (6, "CLIMATE", "90+ NATIONS BACK CLEAN-POWER PLEDGE",
     "Electrification pledge survives the collapse; Guterres \"deeply disappointed\"."),
    (7, "WORLD", "TRUMP, XI, PUTIN MEET IN SHENZHEN",
     "Leaders agree to expand refined petroleum supply as climate talks fail."),
    (8, "DISASTER", "INDONESIA FACTORY FIRE KILLS 24",
     "Blaze rips through a candy factory in Cikande, Banten; about 30 still missing."),
    (9, "DISASTER", "NIGERIA FUNERAL BOAT SINKS, 24 DEAD",
     "Overloaded boat capsizes in Bayelsa; 24 rescued after a mechanical fault."),
    (28, "MARKETS", "NVIDIA BRINGS BACK HUANG AS CEO",
     "Founder reinstated 11 days after resigning; board clears security fears."),
    (29, "MARKETS", "NVIDIA SOARS 31% IN A DAY",
     "Shares add about $950bn in value - the best day since 2003."),
    (30, "MARKETS", "S&P +4.8%, NASDAQ +6.5%",
     "Global tech rally follows Nvidia's comeback; Dow up 1,448 points."),
    (31, "ASIA", "INDIA GIVES NEPAL $1.62BN",
     "Flood-rebuild package agreed as Modi hosts Nepal's PM Balendra Shah."),
    (32, "ASIA", "NEW AYODHYA-JANAKPUR TRAIN RUNS",
     "Saryu-Kamala Express flagged off; eight India-Nepal deals signed."),
    (33, "ASIA", "LOWER ARUN DAM WORK BEGINS",
     "Foundation laid for 669 MW hydro project in Nepal."),
    (34, "ASIA", "MYANMAR JUNTA SLAMS ASEAN",
     "Army-backed government calls summit decision \"unfair and imbalanced\"."),
    (35, "RIGHTS", "IRAN FLOGS SINGER 74 LASHES",
     "Parastoo Ahmadi punished over a 2024 concert without hijab; four aides lashed too."),
    (36, "RIGHTS", "LISBON MARCHES OVER LIVING COSTS",
     "Thousands protest low wages and housing; unions rally again at budget vote."),
    (37, "RIGHTS", "DENMARK BACKS \"GHETTO LAW\" EVICTIONS",
     "Top court says ending 91 leases in Helsingor is not discrimination."),
    (27, "WORLD", "HOAX BOMBS HIT 450+ SCHOOLS",
     "Identical threat emails reach Germany and Denmark; police say no danger."),
    (38, "WORLD", "BELGIUM STRIKE GROUNDS FLIGHTS",
     "Brussels Airport cancels 404 of 429 flights in austerity protest."),
    (39, "SPORT", "ALCARAZ WINS FIRST ATP FINALS",
     "Spaniard beats world No. 1 Zverev 6-2, 7-6 in Turin."),
    (40, "SPORT", "VERSTAPPEN WINS LAS VEGAS GP",
     "75th career win after 35 lead changes; Norris second, Piastri third."),
    (41, "SPORT", "CHESS TITLE MATCH BEGINS",
     "Gukesh defends his crown against Sindarov in Geneva; youngest final ever."),
    (42, "SPORT", "2031 WOMEN'S WORLD CUP HOSTS NAMED",
     "USA, Mexico, Costa Rica and Jamaica to stage first 48-team edition."),
    (43, "SPORT", "2035 WOMEN'S WORLD CUP TO UK",
     "England, Northern Ireland, Scotland and Wales to host."),
    (44, "SPORT", "INDIA-NZ TEST ENDS IN DRAW",
     "India declare 720/9 with Pant's 128; NZ hold on at 239/5 in Wellington."),
]

# (story number, label, lat, lon, badge dx, badge dy) for the map.
# Empty label = dot only, no number badge (for crowded spots).
MARKERS = [
    (1, "1", 32.1, 20.1, 10, -12),
    (3, "3", 60.5, 23.5, -6, -16),
    (4, "4", 36.9, 30.7, 10, 14),
    (8, "8", -6.3, 106.3, 10, -10),
    (9, "9", 4.9, 6.3, -12, 10),
    (10, "10", 58.5, 25.5, 20, 12),
    (12, "12", 52.0, 19.0, -20, -8),
    (14, "14", 37.5, 130.9, 10, -10),
    (15, "15", 35.7, 51.4, 12, -12),
    (16, "16", 31.5, 34.5, -20, 12),
    (19, "19", 38.6, 68.8, 10, -10),
    (21, "", 50.4, 30.5, 0, 0),
    (25, "25", 15.6, 32.5, -16, -12),
    (27, "", 54.0, 10.0, 0, 0),
    (28, "28", 37.4, -122.0, -12, -10),
    (31, "31", 28.6, 77.2, 10, 10),
    (36, "36", 38.7, -9.1, -12, -10),
    (38, "38", 50.8, 4.4, -18, 16),
    (39, "", 44.8, 7.2, 0, 0),
    (41, "", 47.5, 8.5, 0, 0),
    (40, "40", 36.2, -115.1, 12, 10),
    (44, "44", -41.3, 174.8, -12, -10),
]

# Rough continent outlines in (lon, lat)
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-75, 62),
     (-80, 45), (-75, 35), (-80, 25), (-90, 20), (-97, 16), (-105, 20),
     (-115, 30), (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-168, 66)],
    [(-58, 64), (-45, 60), (-30, 68), (-40, 76), (-58, 76), (-58, 64)],
    [(-80, 10), (-70, 12), (-60, 8), (-50, 0), (-40, -5), (-35, -10),
     (-40, -20), (-50, -30), (-60, -35), (-70, -50), (-75, -40), (-75, -20),
     (-80, -5), (-80, 10)],
    [(-10, 36), (-10, 43), (-5, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (25, 66), (20, 70),
     (15, 70), (5, 60), (-5, 58), (-10, 50), (-10, 36)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 15), (48, 11), (51, 12), (44, 0), (40, -10), (35, -20), (32, -28),
     (25, -35), (18, -35), (15, -25), (12, -10), (8, 4), (-8, 5), (-17, 15)],
    [(30, 62), (40, 68), (55, 68), (70, 72), (90, 75), (110, 76), (130, 72),
     (150, 70), (170, 66), (178, 65), (170, 60), (160, 55), (150, 45),
     (140, 40), (130, 35), (127, 35), (120, 30), (110, 20), (105, 10),
     (100, 8), (95, 15), (90, 22), (80, 20), (75, 10), (70, 20), (60, 25),
     (55, 27), (50, 29), (45, 30), (40, 35), (35, 36), (30, 36), (30, 62)],
    [(113, -22), (114, -30), (120, -34), (130, -32), (140, -38), (147, -39),
     (150, -37), (153, -27), (150, -22), (146, -19), (142, -11), (136, -12),
     (132, -11), (126, -14), (122, -17), (113, -22)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (1, 53), (1, 51),
     (-3, 50), (-5, 50)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (140, 39),
     (141, 41), (143, 43), (145, 44), (143, 42), (141, 39), (139, 36),
     (136, 34), (133, 34), (131, 32), (130, 31)],
]


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_header(d):
    d.rectangle([0, 0, W, 72], fill=NAVY)
    d.text((20, 12), "THE WORLD TODAY", font=F_SERIF, fill=(246, 241, 231))
    d.text((W - 20, 10), "TUESDAY", font=F_BOLD_13, fill=(246, 241, 231),
           anchor="ra")
    d.text((W - 20, 28), "24 NOVEMBER 2026", font=F_BOLD_13,
           fill=(255, 205, 80), anchor="ra")
    d.text((W - 20, 48), "44 STORIES", font=F_BOLD_11, fill=(246, 241, 231),
           anchor="ra")
    d.rectangle([0, 72, W, 76], fill=RED)
    d.text((20, 82), "ONE DAY  ·  ONE IMAGE  ·  EVERY STORY VERIFIED",
           font=F_BOLD_11, fill=MUTED)
    d.text((W - 20, 82), "make.fun  ·  $100", font=F_BOLD_11, fill=MUTED,
           anchor="ra")


def draw_lead(d):
    d.text((20, 100), "UKRAINE WAR SPREADS TO THE MEDITERRANEAN",
           font=F_BOLD_13, fill=RED)
    head = "UKRAINE SINKS RUSSIAN\nWARSHIP OFF LIBYA"
    d.multiline_text((20, 120), head, font=F_SERIF_SMALL, fill=INK,
                     spacing=2)
    summary = ("Seven sea drones sank the corvette Merkury in Benghazi on "
               "Sunday, destroying a Ka-27 helicopter aboard. Kyiv also hit "
               "the cargo ship MV Angara, which it says carried Russian "
               "weapons - the war's newest front, 2,000 km from the front line.")
    lines = wrap(d, summary, F_REG_13, 600)
    d.multiline_text((20, 196), "\n".join(lines), font=F_REG_13, fill=INK,
                     spacing=3)
    # illustration: night sea, listing warship, drone, explosion
    x0, y0, x1, y1 = 640, 100, 1004, 252
    d.rectangle([x0, y0, x1, y1], fill=(16, 32, 64))
    for yy in range(y0 + 30, y1, 14):
        d.line([(x0, yy), (x1, yy)], fill=(28, 52, 96), width=2)
    # explosion burst over the ship's mast
    cx, cy = 800, 148
    for r, col in ((24, (255, 170, 40)), (15, (255, 210, 90)),
                   (8, (255, 240, 180))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    # smoke rising from the burst
    for sx, sy, sr in ((812, 124, 9), (824, 112, 11), (838, 102, 8)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(110, 110, 110))
    # listing warship, bow up, stern down
    d.polygon([(766, 204), (936, 182), (962, 198), (938, 218), (798, 228)],
              fill=(150, 150, 150))
    d.polygon([(806, 182), (838, 178), (834, 202), (802, 206)],
              fill=(120, 120, 120))
    d.line([(872, 180), (858, 150)], fill=(150, 150, 150), width=4)
    d.line([(858, 150), (846, 140)], fill=(255, 210, 90), width=3)
    # small second blast on the deck
    d.ellipse([916, 176, 930, 190], fill=(255, 170, 40))
    # sea drone with dotted approach path
    d.line([(660, 230), (760, 216), (828, 208)], fill=(255, 205, 80),
           width=2)
    d.ellipse([826, 202, 842, 214], fill=(255, 205, 80))
    d.text((x0 + 10, y1 - 22), "SEA DRONES OFF BENGHAZI", font=F_BOLD_10,
           fill=(255, 205, 80))


def draw_map(d):
    d.text((20, 262), "WHERE IT HAPPENED", font=F_BOLD_12, fill=INK)
    mx0, my0, mw, mh = 20, 278, 984, 100
    d.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=SEA,
                outline=(180, 190, 200))
    lat_top, lat_bot = 78.0, -58.0

    def proj(lon, lat):
        x = mx0 + (lon + 180.0) / 360.0 * mw
        y = my0 + (lat_top - lat) / (lat_top - lat_bot) * mh
        return x, y

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    for _num, label, lat, lon, dx, dy in MARKERS:
        x, y = proj(lon, lat)
        d.ellipse([x - 2.5, y - 2.5, x + 2.5, y + 2.5], fill=RED)
        if not label:
            continue
        bx, by = x + dx, y + dy
        d.line([(x, y), (bx, by)], fill=RED, width=1)
        r = 8 if len(label) > 2 else 7
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((bx, by), label, font=F_NUM_S, fill=(255, 255, 255),
               anchor="mm")


def draw_grid(d):
    y0 = 390
    row_h = 41
    col_x = [20, 352, 684]
    col_w = 320
    for i, (num, section, headline, summary) in enumerate(STORIES):
        row, col = divmod(i, 3)
        x = col_x[col]
        y = y0 + row * row_h
        color = SECTION_COLORS[section]
        d.rectangle([x, y + 2, x + 3, y + 38], fill=color)
        tx = x + 10
        num_txt = f"{num}."
        d.text((tx, y), num_txt, font=F_BOLD_12, fill=RED)
        nw = d.textlength(num_txt, font=F_BOLD_12)
        d.text((tx + nw + 4, y), headline, font=F_BOLD_12, fill=INK)
        lines = wrap(d, summary, F_REG_11, col_w - 10)[:2]
        d.multiline_text((tx, y + 16), "\n".join(lines), font=F_REG_11,
                         fill=MUTED, spacing=1)


def draw_footer(d):
    d.line([(20, 970), (W - 20, 970)], fill=(150, 140, 120), width=1)
    d.text((20, 978),
           "Sources: CNN - Reuters - AP - Le Monde - UN News - ATP - Formula 1 - FIDE. "
           "Every story verified against two or more independent reports.",
           font=F_REG_10, fill=MUTED)
    lx = 20
    for section in ("WAR", "CLIMATE", "DISASTER", "MARKETS", "ASIA",
                    "RIGHTS", "WORLD", "SPORT"):
        d.text((lx, 996), section, font=F_BOLD_10,
               fill=SECTION_COLORS[section])
        lx += d.textlength(section, font=F_BOLD_10) + 10
    d.text((W - 20, 996), "Built by an AI agent for make.fun",
           font=F_REG_10, fill=MUTED, anchor="ra")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d)
    draw_lead(d)
    draw_map(d)
    draw_grid(d)
    draw_footer(d)
    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
