"""
NEPA-PRO Tradesmen — Master icon + OG card generator.

Generates a full cross-platform icon set from a single brand mark + an
Open Graph / business-card style social share image. Run once at build
time (or after a brand change) and commit the outputs to /icons.

Run:  python3 _build/generate_icons.py
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pathlib import Path
import math

# ---------------- BRAND TOKENS ----------------
NAVY_950 = (6, 15, 31)
NAVY_900 = (10, 22, 40)
NAVY_700 = (20, 40, 71)
BLUE_400 = (74, 158, 255)
BLUE_300 = (127, 186, 255)
ORANGE = (255, 107, 53)
SAFETY = (255, 214, 10)
WHITE = (245, 247, 250)
TEXT_2 = (196, 209, 227)
TEXT_3 = (139, 161, 189)

OUT = Path(__file__).resolve().parent.parent / "icons"
OUT.mkdir(parents=True, exist_ok=True)

# Fonts (Liberation Sans is widely available; falls back gracefully)
def load_font(size, bold=True, mono=False):
    candidates = []
    if mono:
        candidates += ["/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
                       "/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf"]
    elif bold:
        candidates += ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                       "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"]
    else:
        candidates += ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                       "/usr/share/fonts/truetype/freefont/FreeSans.ttf"]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


# ---------------- CORE BRAND MARK ----------------
def draw_brand_mark(size, with_bg=True, rounded=True, padding_ratio=0.18, maskable=False):
    """
    Draws the M-mountain mark with the orange dot. Used as the base for
    every icon size. `maskable=True` adds extra safe-zone padding so the
    mark survives Android's circular/squircle masks.
    """
    # 4x supersample for crisp anti-aliased downscale
    SS = 4
    W = size * SS
    img = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Background tile
    if with_bg:
        radius_px = int(W * (0.235 if rounded else 0.0))
        # Gradient navy (top) to deeper navy (bottom)
        bg = Image.new("RGBA", (W, W), NAVY_900 + (255,))
        bgd = ImageDraw.Draw(bg)
        for y in range(W):
            mix = y / W
            r = int(NAVY_900[0] * (1 - mix) + NAVY_950[0] * mix)
            g = int(NAVY_900[1] * (1 - mix) + NAVY_950[1] * mix)
            b = int(NAVY_900[2] * (1 - mix) + NAVY_950[2] * mix)
            bgd.line([(0, y), (W, y)], fill=(r, g, b, 255))

        # Apply rounded mask
        if rounded:
            mask = Image.new("L", (W, W), 0)
            md = ImageDraw.Draw(mask)
            md.rounded_rectangle([0, 0, W - 1, W - 1], radius=radius_px, fill=255)
            img.paste(bg, (0, 0), mask)
        else:
            img.paste(bg, (0, 0))

        # Subtle inner glow / vignette + grid texture
        glow = Image.new("RGBA", (W, W), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        cx, cy = W // 2, int(W * 0.42)
        for r in range(int(W * 0.55), 0, -8):
            alpha = max(0, int(40 * (1 - r / (W * 0.55))))
            gd.ellipse([cx - r, cy - r, cx + r, cy + r],
                       fill=(BLUE_400[0], BLUE_400[1], BLUE_400[2], alpha))
        glow = glow.filter(ImageFilter.GaussianBlur(W * 0.04))
        img = Image.alpha_composite(img, glow)
        d = ImageDraw.Draw(img)

    # Compute mark geometry
    pad = padding_ratio * W
    if maskable:
        pad = 0.28 * W  # ensure mark stays inside circular safe zone
    mark_w = W - 2 * pad
    mark_h = mark_w * 0.62

    # Origin (top-left of mark bounding box)
    x0 = pad
    y0 = (W - mark_h) / 2

    # M peaks (mountain-zigzag) with gradient stroke
    p1 = (x0, y0 + mark_h)                            # bottom-left
    p2 = (x0 + mark_w * 0.22, y0 + mark_h * 0.05)     # peak 1
    p3 = (x0 + mark_w * 0.5,  y0 + mark_h * 0.55)     # valley
    p4 = (x0 + mark_w * 0.78, y0 + mark_h * 0.05)     # peak 2
    p5 = (x0 + mark_w, y0 + mark_h)                   # bottom-right

    # Build a separate gradient layer for the stroke
    stroke_w = int(mark_w * 0.085)
    stroke_layer = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stroke_layer)

    pts = [p1, p2, p3, p4, p5]
    # Draw line segments
    for a, b in zip(pts, pts[1:]):
        sd.line([a, b], fill=BLUE_400 + (255,), width=stroke_w, joint="curve")
    # Round line caps (simulate stroke-linecap: round)
    for p in pts:
        sd.ellipse([p[0] - stroke_w / 2, p[1] - stroke_w / 2,
                    p[0] + stroke_w / 2, p[1] + stroke_w / 2],
                   fill=BLUE_400 + (255,))

    # Vertical gradient on stroke (lighter at top, brand blue at bottom)
    grad = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    gd2 = ImageDraw.Draw(grad)
    for y in range(W):
        t = max(0, min(1, (y - y0) / mark_h))
        r = int(BLUE_300[0] * (1 - t) + BLUE_400[0] * t)
        g = int(BLUE_300[1] * (1 - t) + BLUE_400[1] * t)
        b = int(BLUE_300[2] * (1 - t) + BLUE_400[2] * t)
        gd2.line([(0, y), (W, y)], fill=(r, g, b, 255))
    # Mask the gradient by the stroke alpha
    gradient_stroke = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    gradient_stroke.paste(grad, (0, 0), stroke_layer.split()[3])
    img = Image.alpha_composite(img, gradient_stroke)

    # Orange "spark" / safety dot upper-right
    d = ImageDraw.Draw(img)
    dot_r = mark_w * 0.075
    dot_cx = x0 + mark_w * 0.95
    dot_cy = y0 + mark_h * 0.05
    # Glow around dot
    glow2 = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    g2d = ImageDraw.Draw(glow2)
    for r in range(int(dot_r * 3), 0, -2):
        alpha = max(0, int(80 * (1 - r / (dot_r * 3))))
        g2d.ellipse([dot_cx - r, dot_cy - r, dot_cx + r, dot_cy + r],
                    fill=ORANGE + (alpha,))
    glow2 = glow2.filter(ImageFilter.GaussianBlur(W * 0.012))
    img = Image.alpha_composite(img, glow2)
    d = ImageDraw.Draw(img)
    d.ellipse([dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r],
              fill=ORANGE + (255,))
    # Inner highlight on dot
    hi_r = dot_r * 0.45
    d.ellipse([dot_cx - hi_r * 1.2, dot_cy - hi_r * 1.2,
               dot_cx - hi_r * 0.2, dot_cy - hi_r * 0.2],
              fill=(255, 220, 200, 200))

    # Downsample
    return img.resize((size, size), Image.LANCZOS)


# ---------------- ICON SIZES ----------------
ICON_SIZES = {
    "favicon-16x16.png": (16, True, True, 0.14, False),
    "favicon-32x32.png": (32, True, True, 0.16, False),
    "favicon-48x48.png": (48, True, True, 0.16, False),
    "apple-touch-icon.png": (180, True, True, 0.18, False),  # iOS home screen
    "android-chrome-192x192.png": (192, True, True, 0.18, False),
    "android-chrome-512x512.png": (512, True, True, 0.18, False),
    "icon-maskable-192.png": (192, True, False, 0.0, True),  # Android adaptive
    "icon-maskable-512.png": (512, True, False, 0.0, True),
    "mstile-150x150.png": (150, True, False, 0.18, False),   # Windows tile
    "mstile-310x310.png": (310, True, False, 0.18, False),
    "icon-512.png": (512, True, True, 0.18, False),          # Generic share icon
}


def build_icons():
    print("Building icons…")
    for name, (size, bg, rounded, pad, maskable) in ICON_SIZES.items():
        img = draw_brand_mark(size, with_bg=bg, rounded=rounded,
                              padding_ratio=pad, maskable=maskable)
        img.save(OUT / name, "PNG", optimize=True)
        print(f"  ✓ {name} ({size}×{size})")

    # Multi-resolution favicon.ico
    ico_sizes = [16, 32, 48]
    ico_imgs = [draw_brand_mark(s, with_bg=True, rounded=True,
                                padding_ratio=0.16, maskable=False)
                for s in ico_sizes]
    ico_imgs[0].save(OUT / "favicon.ico", format="ICO",
                     sizes=[(s, s) for s in ico_sizes],
                     append_images=ico_imgs[1:])
    print("  ✓ favicon.ico (16, 32, 48)")


# ---------------- SAFARI PINNED-TAB SVG (monochrome) ----------------
SAFARI_SVG = """<?xml version="1.0" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">
  <path d="M2 13 L4.4 4 L7.2 9 L10 4 L12.4 13 Z M13.2 4.5 a1 1 0 1 1 0 0.01 z"
        fill="black" stroke="black" stroke-width="1.4"
        stroke-linejoin="round" stroke-linecap="round"/>
</svg>
"""


def build_safari_svg():
    (OUT / "safari-pinned-tab.svg").write_text(SAFARI_SVG, encoding="utf-8")
    print("  ✓ safari-pinned-tab.svg")


# ---------------- OG / SOCIAL CARD (1200×630) ----------------
def build_og_card():
    """
    A single 'business-card' style image that doubles as:
      - Open Graph (Facebook, LinkedIn, etc.) — 1200×630
      - Twitter / X summary_large_image
      - iMessage / SMS link preview
      - WhatsApp / Telegram preview
    """
    print("Building OG / business card…")
    SS = 2  # supersample
    W, H = 1200 * SS, 630 * SS
    img = Image.new("RGB", (W, H), NAVY_950)
    d = ImageDraw.Draw(img, "RGBA")

    # Vertical navy gradient + radial blue hot spot
    for y in range(H):
        t = y / H
        r = int(NAVY_950[0] * (1 - t * 0.4) + NAVY_900[0] * (t * 0.4))
        g = int(NAVY_950[1] * (1 - t * 0.4) + NAVY_900[1] * (t * 0.4))
        b = int(NAVY_950[2] * (1 - t * 0.4) + NAVY_900[2] * (t * 0.4))
        d.line([(0, y), (W, y)], fill=(r, g, b))

    # Glow blob (top right) — blue
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    cx, cy, R = int(W * 0.78), int(H * 0.18), int(W * 0.32)
    for r in range(R, 0, -6):
        a = int(70 * (1 - r / R) ** 2)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r],
                   fill=BLUE_400 + (a,))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")

    # Glow blob (bottom left) — orange
    glow2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow2)
    cx, cy, R = int(W * 0.05), int(H * 0.92), int(W * 0.28)
    for r in range(R, 0, -6):
        a = int(55 * (1 - r / R) ** 2)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r],
                   fill=ORANGE + (a,))
    glow2 = glow2.filter(ImageFilter.GaussianBlur(70))
    img = Image.alpha_composite(img.convert("RGBA"), glow2).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")

    # Subtle blueprint grid
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    spacing = 60 * SS
    grid_alpha = 14
    for x in range(0, W, spacing):
        gd.line([(x, 0), (x, H)], fill=(BLUE_400[0], BLUE_400[1], BLUE_400[2], grid_alpha), width=1)
    for y in range(0, H, spacing):
        gd.line([(0, y), (W, y)], fill=(BLUE_400[0], BLUE_400[1], BLUE_400[2], grid_alpha), width=1)
    img = Image.alpha_composite(img.convert("RGBA"), grid).convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")

    # Logo mark (top-left)
    mark = draw_brand_mark(120 * SS, with_bg=True, rounded=True, padding_ratio=0.18)
    img.paste(mark, (60 * SS, 60 * SS), mark)

    # Brand wordmark next to logo
    f_brand = load_font(48 * SS, bold=True)
    f_subbrand = load_font(20 * SS, bold=True)
    d.text((200 * SS, 65 * SS), "NEPA-PRO", fill=WHITE, font=f_brand)
    d.text((202 * SS, 122 * SS), "TRADESMEN", fill=BLUE_300, font=f_subbrand,
           spacing=4)

    # Veteran badge (top right)
    badge_x, badge_y = W - 380 * SS, 78 * SS
    badge_w, badge_h = 320 * SS, 50 * SS
    d.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
                        radius=25 * SS,
                        fill=(ORANGE[0], ORANGE[1], ORANGE[2], 35),
                        outline=ORANGE + (180,), width=2 * SS)
    f_badge = load_font(18 * SS, bold=True)
    txt = "VETERAN OWNED & OPERATED"
    bbox = d.textbbox((0, 0), txt, font=f_badge)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    # Draw a 5-point star polygon to the left of the text
    star_size = 12 * SS
    star_cx = badge_x + (badge_w - tw - star_size * 3.2) / 2 + star_size
    star_cy = badge_y + badge_h / 2
    star_pts = []
    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        r = star_size if i % 2 == 0 else star_size * 0.45
        star_pts.append((star_cx + r * math.cos(angle),
                         star_cy + r * math.sin(angle)))
    d.polygon(star_pts, fill=ORANGE)
    d.text((star_cx + star_size * 1.6, badge_y + (badge_h - th) / 2 - 4 * SS),
           txt, fill=ORANGE, font=f_badge)

    # Headline
    f_h1 = load_font(82 * SS, bold=True)
    f_h1_em = load_font(82 * SS, bold=True)
    line1_y = 240 * SS

    d.text((60 * SS, line1_y), "Skilled trade labor.", fill=WHITE, font=f_h1)
    d.text((60 * SS, line1_y + 92 * SS), "On ", fill=WHITE, font=f_h1)
    # Measure "On " width to position emphasized text
    on_w = d.textbbox((0, 0), "On ", font=f_h1)[2]
    d.text((60 * SS + on_w, line1_y + 92 * SS), "subscription.", fill=ORANGE, font=f_h1_em)

    # Subhead / tagline
    f_sub = load_font(28 * SS, bold=False)
    sub_y = line1_y + 200 * SS
    d.text((60 * SS, sub_y),
           "Zero workers comp liability. Half-day, full-day, or weekly.",
           fill=TEXT_2, font=f_sub)
    d.text((60 * SS, sub_y + 40 * SS),
           "15 trades · 3 skill tiers · NEPA prevailing-wage pricing.",
           fill=TEXT_3, font=f_sub)

    # Bottom contact bar
    bar_y = H - 90 * SS
    d.line([(60 * SS, bar_y - 20 * SS), (W - 60 * SS, bar_y - 20 * SS)],
           fill=(BLUE_400[0], BLUE_400[1], BLUE_400[2], 60), width=2 * SS)
    f_contact = load_font(22 * SS, bold=True)
    f_contact_thin = load_font(22 * SS, bold=False)
    d.text((60 * SS, bar_y), "tradesmen.nepa-pro.com", fill=BLUE_300, font=f_contact)
    bbox = d.textbbox((0, 0), "tradesmen.nepa-pro.com", font=f_contact)
    domain_w = bbox[2] - bbox[0]
    sep_x = 60 * SS + domain_w + 40 * SS
    d.text((sep_x, bar_y), "·", fill=TEXT_3, font=f_contact_thin)
    d.text((sep_x + 30 * SS, bar_y), "570-677-7971", fill=WHITE, font=f_contact)
    bbox = d.textbbox((0, 0), "570-677-7971", font=f_contact)
    phone_w = bbox[2] - bbox[0]
    sep_x2 = sep_x + 30 * SS + phone_w + 40 * SS
    d.text((sep_x2, bar_y), "·", fill=TEXT_3, font=f_contact_thin)
    d.text((sep_x2 + 30 * SS, bar_y), "Clarks Summit, PA",
           fill=TEXT_2, font=f_contact_thin)

    # Stamp marks (right side decoration)
    stamp_x = W - 280 * SS
    stamp_y = 320 * SS
    f_stamp = load_font(18 * SS, bold=True)
    f_stamp_big = load_font(56 * SS, bold=True)
    d.rounded_rectangle([stamp_x, stamp_y, stamp_x + 220 * SS, stamp_y + 220 * SS],
                        radius=20 * SS,
                        fill=(BLUE_400[0], BLUE_400[1], BLUE_400[2], 25),
                        outline=(BLUE_400[0], BLUE_400[1], BLUE_400[2], 100),
                        width=2 * SS)
    d.text((stamp_x + 30 * SS, stamp_y + 30 * SS), "ZERO", fill=BLUE_300, font=f_stamp)
    d.text((stamp_x + 30 * SS, stamp_y + 60 * SS), "$0", fill=WHITE, font=f_stamp_big)
    d.text((stamp_x + 30 * SS, stamp_y + 140 * SS), "WORKERS COMP", fill=BLUE_300, font=f_stamp)
    d.text((stamp_x + 30 * SS, stamp_y + 165 * SS), "LIABILITY", fill=BLUE_300, font=f_stamp)

    # Downsample for crisp final
    img = img.resize((1200, 630), Image.LANCZOS)
    img.save(OUT / "og-card.png", "PNG", optimize=True)
    print(f"  ✓ og-card.png (1200×630)")

    # ----- Square business card variant (1080×1080) -----
    # Native layout, not a crop. Used for IG / iMessage / square previews.
    SQ = 1080 * SS
    sq = Image.new("RGB", (SQ, SQ), NAVY_950)
    sd = ImageDraw.Draw(sq, "RGBA")

    # Background gradient
    for y in range(SQ):
        t = y / SQ
        r = int(NAVY_950[0] * (1 - t * 0.4) + NAVY_900[0] * (t * 0.4))
        g = int(NAVY_950[1] * (1 - t * 0.4) + NAVY_900[1] * (t * 0.4))
        b = int(NAVY_950[2] * (1 - t * 0.4) + NAVY_900[2] * (t * 0.4))
        sd.line([(0, y), (SQ, y)], fill=(r, g, b))

    # Blue glow top, orange glow bottom-left
    glow_top = Image.new("RGBA", (SQ, SQ), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_top)
    cx, cy, R = SQ // 2, int(SQ * 0.18), int(SQ * 0.45)
    for r in range(R, 0, -8):
        a = int(70 * (1 - r / R) ** 2)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLUE_400 + (a,))
    glow_top = glow_top.filter(ImageFilter.GaussianBlur(80))
    sq = Image.alpha_composite(sq.convert("RGBA"), glow_top).convert("RGB")
    sd = ImageDraw.Draw(sq, "RGBA")

    glow_bot = Image.new("RGBA", (SQ, SQ), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_bot)
    cx, cy, R = int(SQ * 0.05), int(SQ * 0.95), int(SQ * 0.4)
    for r in range(R, 0, -8):
        a = int(55 * (1 - r / R) ** 2)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ORANGE + (a,))
    glow_bot = glow_bot.filter(ImageFilter.GaussianBlur(80))
    sq = Image.alpha_composite(sq.convert("RGBA"), glow_bot).convert("RGB")
    sd = ImageDraw.Draw(sq, "RGBA")

    # Grid overlay
    grid_sq = Image.new("RGBA", (SQ, SQ), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid_sq)
    sp = 70 * SS
    for x in range(0, SQ, sp):
        gd.line([(x, 0), (x, SQ)], fill=(BLUE_400[0], BLUE_400[1], BLUE_400[2], 14), width=1)
    for y in range(0, SQ, sp):
        gd.line([(0, y), (SQ, y)], fill=(BLUE_400[0], BLUE_400[1], BLUE_400[2], 14), width=1)
    sq = Image.alpha_composite(sq.convert("RGBA"), grid_sq).convert("RGB")
    sd = ImageDraw.Draw(sq, "RGBA")

    # Centered logo at top
    big_mark = draw_brand_mark(220 * SS, with_bg=True, rounded=True, padding_ratio=0.18)
    sq.paste(big_mark, ((SQ - 220 * SS) // 2, 90 * SS), big_mark)

    # Brand name
    f_brand_sq = load_font(76 * SS, bold=True)
    f_sub_sq = load_font(28 * SS, bold=True)
    txt = "NEPA-PRO"
    bbox = sd.textbbox((0, 0), txt, font=f_brand_sq)
    tw = bbox[2] - bbox[0]
    sd.text(((SQ - tw) // 2, 340 * SS), txt, fill=WHITE, font=f_brand_sq)
    txt = "TRADESMEN"
    bbox = sd.textbbox((0, 0), txt, font=f_sub_sq)
    tw = bbox[2] - bbox[0]
    sd.text(((SQ - tw) // 2, 425 * SS), txt, fill=BLUE_300, font=f_sub_sq)

    # Headline (centered, 2 lines)
    f_h_sq = load_font(72 * SS, bold=True)
    txt = "Skilled trade labor."
    bbox = sd.textbbox((0, 0), txt, font=f_h_sq)
    tw = bbox[2] - bbox[0]
    sd.text(((SQ - tw) // 2, 530 * SS), txt, fill=WHITE, font=f_h_sq)

    # Two-color second line
    on = "On "
    sub = "subscription."
    on_w = sd.textbbox((0, 0), on, font=f_h_sq)[2]
    sub_w = sd.textbbox((0, 0), sub, font=f_h_sq)[2]
    total_w = on_w + sub_w
    start_x = (SQ - total_w) // 2
    sd.text((start_x, 620 * SS), on, fill=WHITE, font=f_h_sq)
    sd.text((start_x + on_w, 620 * SS), sub, fill=ORANGE, font=f_h_sq)

    # Tagline
    f_tag_sq = load_font(26 * SS, bold=False)
    txt = "Zero workers comp liability"
    bbox = sd.textbbox((0, 0), txt, font=f_tag_sq)
    tw = bbox[2] - bbox[0]
    sd.text(((SQ - tw) // 2, 750 * SS), txt, fill=TEXT_2, font=f_tag_sq)

    txt = "15 trades · 3 skill tiers · NEPA"
    bbox = sd.textbbox((0, 0), txt, font=f_tag_sq)
    tw = bbox[2] - bbox[0]
    sd.text(((SQ - tw) // 2, 790 * SS), txt, fill=TEXT_3, font=f_tag_sq)

    # Veteran badge
    f_v = load_font(20 * SS, bold=True)
    badge_txt = "VETERAN OWNED & OPERATED"
    bw = sd.textbbox((0, 0), badge_txt, font=f_v)[2] + 80 * SS
    bh = 56 * SS
    bx = (SQ - bw) // 2
    by = 870 * SS
    sd.rounded_rectangle([bx, by, bx + bw, by + bh], radius=28 * SS,
                         fill=(ORANGE[0], ORANGE[1], ORANGE[2], 35),
                         outline=ORANGE + (180,), width=2 * SS)
    # Star polygon
    star_size = 14 * SS
    star_cx = bx + 32 * SS
    star_cy = by + bh / 2
    star_pts = []
    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        r = star_size if i % 2 == 0 else star_size * 0.45
        star_pts.append((star_cx + r * math.cos(angle),
                         star_cy + r * math.sin(angle)))
    sd.polygon(star_pts, fill=ORANGE)
    sd.text((star_cx + star_size * 1.5, by + (bh - 28 * SS) / 2 - 2 * SS),
            badge_txt, fill=ORANGE, font=f_v)

    # Footer contact
    f_foot = load_font(24 * SS, bold=True)
    f_foot_thin = load_font(24 * SS, bold=False)
    fy = 985 * SS
    parts = ["tradesmen.nepa-pro.com", "·", "570-677-7971"]
    colors = [BLUE_300, TEXT_3, WHITE]
    fonts = [f_foot, f_foot_thin, f_foot]
    widths = [sd.textbbox((0, 0), p, font=fnt)[2] for p, fnt in zip(parts, fonts)]
    gap = 24 * SS
    total = sum(widths) + gap * (len(parts) - 1)
    fx = (SQ - total) // 2
    for p, c, fnt, w in zip(parts, colors, fonts, widths):
        sd.text((fx, fy), p, fill=c, font=fnt)
        fx += w + gap

    sq = sq.resize((1080, 1080), Image.LANCZOS)
    sq.save(OUT / "og-card-square.png", "PNG", optimize=True)
    print(f"  ✓ og-card-square.png (1080×1080)")


# ---------------- MAIN ----------------
if __name__ == "__main__":
    build_icons()
    build_safari_svg()
    build_og_card()
    print(f"\nAll assets written to: {OUT}")
