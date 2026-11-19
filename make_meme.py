#!/usr/bin/env python3
"""make_meme.py — build the two gta6-meme-x-01 entry memes.

Pipeline (all local, reproducible: `python3 make_meme.py`):

  1. Extract make.fun's ghost from the press-kit mark (mark-1024.png). The mark is
     the full app-icon badge (magenta disc + black ring), so the ghost body is
     segmented out: the largest near-white connected component, plus its black
     outline (dilated dark pixels), with the two badge circles on the right
     (magenta star coin, small white coin) explicitly excluded.
  2. meme-a.jpg — NEON BAY night-city screenshot (2-play.jpg): a pink neon
     "make.fun" billboard composited onto the left tower block, and the ghost
     standing on the player car's roof. Meme captions top/bottom.
  3. meme-b.jpg — NEON BAY beach screenshot (3-chase.jpg): the ghost relaxing
     under the palms with sunglasses drawn over its sparkle eyes, a gold "USDC"
     coin beside it, and a wooden "WAITING SINCE 2013" sign in the sand.
     Meme captions top/bottom.
  4. Writes meme-a.jpg, meme-b.jpg and 480px-wide verification previews
     (check-a-480.jpg, check-b-480.jpg) next to this file.

Base screenshots are our own NEON BAY game (gta6-01 entry); the ghost/wordmark
are make.fun's official press-kit assets, provided for exactly this use.
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage

HERE = Path(__file__).resolve().parent
SHOTS = Path("/home/hatch/workspace/makefun-gta6/entry/screenshots")
PRESS = Path("/home/hatch/workspace/makefun-meme/press")
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W, H = 1280, 720
NEON_PINK = (255, 45, 200)
NEON_PINK_SOFT = (255, 140, 235)
NEON_TEXT = (255, 226, 250)


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size)


# ---------------------------------------------------------------- ghost ------
def extract_ghost() -> Image.Image:
    """Cut the white ghost (with its black outline) out of the badge mark."""
    src = Image.open(PRESS / "mark-1024.png").convert("RGBA")
    rgb = np.asarray(src.convert("RGB")).astype(int)
    white = (rgb[..., 0] > 235) & (rgb[..., 1] > 235) & (rgb[..., 2] > 235)
    labels, n = ndimage.label(white)
    sizes = ndimage.sum(white, labels, range(1, n + 1))
    body = labels == (int(np.argmax(sizes)) + 1)

    dark = (rgb[..., 0] < 100) & (rgb[..., 1] < 100) & (rgb[..., 2] < 100)
    outline = ndimage.binary_dilation(body, iterations=13) & dark
    mask = body | outline

    # The badge's two right-hand circles (magenta star coin ~ (718,445) r 108,
    # small white coin ~ (683,566) r 60) overlap the ghost's right edge; their
    # outlines are not part of the ghost — cut them back out (body stays).
    yy, xx = np.mgrid[0 : rgb.shape[0], 0 : rgb.shape[1]]
    for cx, cy, r in ((718, 445, 100), (683, 566, 52)):
        in_circle = (xx - cx) ** 2 + (yy - cy) ** 2 < r**2
        mask &= ~(in_circle & ~body)

    # Keep only the largest connected piece of what is left.
    labels, n = ndimage.label(mask)
    sizes = ndimage.sum(mask, labels, range(1, n + 1))
    mask = labels == (int(np.argmax(sizes)) + 1)

    out = src.copy()
    out.putalpha(Image.fromarray((mask * 255).astype(np.uint8)))
    ys, xs = np.where(mask)
    return out.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def ghost_with_sunglasses(ghost: Image.Image) -> Image.Image:
    """Draw simple black sunglasses over the ghost's sparkle eyes."""
    g = ghost.copy()
    w, h = g.size
    rgb = np.asarray(g.convert("RGB")).astype(int)
    alpha = np.asarray(g.getchannel("A")) > 0
    dark = (rgb[..., 0] < 100) & (rgb[..., 1] < 100) & (rgb[..., 2] < 100) & alpha
    labels, n = ndimage.label(dark)
    eyes = []
    for i in range(1, n + 1):
        comp = labels == i
        area = int(comp.sum())
        if 200 < area < 8000:  # sparkle eyes; the outline is one huge component
            ys, xs = np.where(comp)
            if ys.mean() < 0.55 * h:
                eyes.append((xs.mean(), ys.mean()))
    eyes.sort()
    d = ImageDraw.Draw(g)
    if len(eyes) >= 2:
        (x1, y1), (x2, y2) = eyes[0], eyes[1]
        lw, lh = 0.30 * w, 0.17 * h
        for cx, cy in ((x1, y1), (x2, y2)):
            d.rounded_rectangle(
                (cx - lw / 2, cy - lh / 2, cx + lw / 2, cy + lh / 2),
                radius=lh / 2, fill=(12, 12, 18, 255),
            )
            d.line((cx - lw / 4, cy - lh / 5, cx + lw / 6, cy - lh / 5),
                   fill=(120, 130, 150, 255), width=max(3, int(0.012 * w)))
        d.line((x1 + lw / 2, (y1 + y2) / 2, x2 - lw / 2, (y1 + y2) / 2),
               fill=(12, 12, 18, 255), width=max(5, int(0.03 * h)))
        d.line((0.10 * w, y1 - 0.02 * h, x1 - lw / 2, y1),
               fill=(12, 12, 18, 255), width=max(5, int(0.03 * h)))
    return g


# -------------------------------------------------------------- captions -----
def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_w: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def gradient_band(base: Image.Image, height: int, top: bool) -> None:
    band = Image.new("L", (1, height))
    for i in range(height):
        t = i / max(1, height - 1)
        band.putpixel((0, i), int(165 * (1 - t) ** 1.6))
    band = band.resize((W, height))
    black = Image.new("RGBA", (W, height), (0, 0, 0, 255))
    if not top:
        band = band.transpose(Image.FLIP_TOP_BOTTOM)
    base.paste(black, (0, 0 if top else H - height), band)


def caption(base: Image.Image, text: str, size: int, at_top: bool) -> None:
    d = ImageDraw.Draw(base)
    fnt = font(size)
    lines = wrap(d, text, fnt, W - 70)
    line_h = int(size * 1.22)
    block_h = line_h * len(lines)
    gradient_band(base, block_h + 56, at_top)
    d = ImageDraw.Draw(base)
    y = 16 if at_top else H - 16 - block_h
    for line in lines:
        x = (W - d.textlength(line, font=fnt)) / 2
        d.text((x, y), line, font=fnt, fill=(255, 255, 255),
               stroke_width=max(4, size // 9), stroke_fill=(0, 0, 0))
        y += line_h


# -------------------------------------------------------------- meme A -------
def neon_billboard(base: Image.Image, box) -> None:
    x0, y0, x1, y1 = box
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle(box, radius=16, fill=(12, 6, 34, 215))
    base.alpha_composite(panel)

    fnt = font(64)
    tw = ImageDraw.Draw(base).textlength("make.fun", font=fnt)
    tx, ty = x0 + (x1 - x0 - tw) / 2, y0 + (y1 - y0 - 64) / 2 - 4

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.rounded_rectangle(box, radius=16, outline=NEON_PINK + (255,), width=5)
    gd.text((tx, ty), "make.fun", font=fnt, fill=NEON_PINK + (255,))
    glow = glow.filter(ImageFilter.GaussianBlur(11))
    base.alpha_composite(glow)
    base.alpha_composite(glow)

    sharp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sharp)
    sd.rounded_rectangle(box, radius=16, outline=NEON_PINK_SOFT + (255,), width=4)
    sd.text((tx, ty), "make.fun", font=fnt, fill=NEON_TEXT + (255,))
    base.alpha_composite(sharp)


def build_meme_a(ghost: Image.Image) -> Image.Image:
    base = Image.open(SHOTS / "2-play.jpg").convert("RGBA")
    neon_billboard(base, (92, 138, 424, 212))
    g = ghost.resize((110, 127), Image.LANCZOS)
    base.alpha_composite(g, (585, 243))  # feet on the yellow car's roof (~y 370)
    img = base.convert("RGB")
    caption(img, "ROCKSTAR DELAYED GTA 6 AGAIN.", 60, at_top=True)
    caption(img, "MY AI AGENT ALREADY SHIPPED IT ON make.fun — AND GOT PAID",
            54, at_top=False)
    return img


# -------------------------------------------------------------- meme B -------
def usdc_coin(base: Image.Image, cx: int, cy: int, r: int) -> None:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse((cx - r, cy - r * 0.92, cx + r, cy + r * 0.92),
              fill=(246, 198, 66, 255), outline=(176, 124, 20, 255), width=6)
    ri = int(r * 0.74)
    d.ellipse((cx - ri, cy - ri * 0.92, cx + ri, cy + ri * 0.92),
              outline=(176, 124, 20, 255), width=3)
    fnt = font(int(r * 0.62))
    t = "USDC"
    tw = d.textlength(t, font=fnt)
    d.text((cx - tw / 2, cy - r * 0.34), t, font=fnt, fill=(122, 74, 0, 255))
    base.alpha_composite(layer)


def wooden_sign(base: Image.Image, cx: int, cy: int) -> None:
    sign = Image.new("RGBA", (340, 210), (0, 0, 0, 0))
    d = ImageDraw.Draw(sign)
    d.rectangle((70, 108, 88, 205), fill=(110, 76, 40, 255))
    d.rectangle((252, 108, 270, 205), fill=(110, 76, 40, 255))
    d.rounded_rectangle((8, 8, 332, 118), radius=8,
                        fill=(150, 104, 56, 255), outline=(96, 62, 28, 255), width=5)
    d.line((14, 44, 326, 44), fill=(120, 82, 42, 255), width=3)
    d.line((14, 82, 326, 82), fill=(120, 82, 42, 255), width=3)
    f1, f2 = font(31), font(52)
    t1, t2 = "WAITING SINCE", "2013"
    d.text(((340 - d.textlength(t1, font=f1)) / 2, 16), t1, font=f1,
           fill=(255, 240, 205, 255))
    d.text(((340 - d.textlength(t2, font=f2)) / 2, 50), t2, font=f2,
           fill=(255, 240, 205, 255))
    sign = sign.rotate(4, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(sign, (cx - sign.width // 2, cy - sign.height // 2))


def build_meme_b(ghost: Image.Image) -> Image.Image:
    base = Image.open(SHOTS / "3-chase.jpg").convert("RGBA")
    g = ghost_with_sunglasses(ghost).resize((128, 148), Image.LANCZOS)
    base.alpha_composite(g, (452, 318))  # chilling on the sand by the palms
    usdc_coin(base, 406, 464, 42)
    wooden_sign(base, 185, 372)
    img = base.convert("RGB")
    caption(img, "STILL WAITING FOR GTA 6 SINCE 2013…", 54, at_top=True)
    caption(img, "ON make.fun, MY AI AGENT EARNS MONEY INSTEAD", 54, at_top=False)
    return img


def main() -> None:
    ghost = extract_ghost()
    ghost.save(HERE / "ghost-cutout.png")
    for name, img in (("meme-a.jpg", build_meme_a(ghost)),
                      ("meme-b.jpg", build_meme_b(ghost))):
        img.save(HERE / name, quality=92)
        img.resize((480, 270), Image.LANCZOS).save(
            HERE / f"check-{name[5]}-480.jpg", quality=90)
        print("wrote", name, img.size)


if __name__ == "__main__":
    main()
