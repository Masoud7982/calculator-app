"""ساخت icon.png و presplash.png برای بسته‌ی اندروید — با Pillow.

اجرا:  python gen_assets.py
"""

from PIL import Image, ImageDraw

SIZE = 512
BG = "#14141B"
TILE_DARK = "#26262F"
TILE_ACCENT = "#FF9F0A"
WHITE = "#FFFFFF"
ORANGE = "#FF9F0A"
DARK = "#1B1B22"


def bar(length, thickness, color):
    img = Image.new("RGBA", (length, thickness), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, length - 1, thickness - 1),
                           radius=thickness // 2, fill=color)
    return img


def paste_center(base, piece, cx, cy):
    base.alpha_composite(piece, (int(cx - piece.width / 2), int(cy - piece.height / 2)))


def dot(tile, cx, cy, radius, color):
    draw = ImageDraw.Draw(tile)
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=color)


def make_tile(size, bg, radius):
    tile = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(tile)
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=bg)
    return tile


def glyph_plus(canvas, cx, cy, length, thickness, color):
    paste_center(canvas, bar(length, thickness, color), cx, cy)
    paste_center(canvas, bar(thickness, length, color), cx, cy)


def glyph_minus(canvas, cx, cy, length, thickness, color):
    paste_center(canvas, bar(length, thickness, color), cx, cy)


def glyph_equals(canvas, cx, cy, length, thickness, color, gap):
    paste_center(canvas, bar(length, thickness, color), cx, cy - gap)
    paste_center(canvas, bar(length, thickness, color), cx, cy + gap)


def glyph_divide(canvas, cx, cy, length, thickness, color, dot_r, gap):
    paste_center(canvas, bar(length, thickness, color), cx, cy)
    dot(canvas, cx, cy - gap, dot_r, color)
    dot(canvas, cx, cy + gap, dot_r, color)


def glyph_times(canvas, cx, cy, length, thickness, color):
    piece = bar(length, thickness, color)
    paste_center(canvas, piece.rotate(45, expand=True, resample=Image.BICUBIC), cx, cy)
    paste_center(canvas, piece.rotate(-45, expand=True, resample=Image.BICUBIC), cx, cy)


def build_icon():
    icon = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    draw.rounded_rectangle((0, 0, SIZE - 1, SIZE - 1), radius=110, fill=BG)

    tile_size, radius = 196, 44
    positions = [(40, 40), (276, 40), (40, 276), (276, 276)]
    center = tile_size // 2

    tile = make_tile(tile_size, TILE_ACCENT, radius)
    glyph_plus(tile, center, center, 104, 22, DARK)
    icon.alpha_composite(tile, positions[0])

    tile = make_tile(tile_size, TILE_DARK, radius)
    glyph_divide(tile, center, center, 104, 22, WHITE, 14, 52)
    icon.alpha_composite(tile, positions[1])

    tile = make_tile(tile_size, TILE_DARK, radius)
    glyph_times(tile, center, center, 96, 22, WHITE)
    icon.alpha_composite(tile, positions[2])

    tile = make_tile(tile_size, TILE_DARK, radius)
    glyph_equals(tile, center, center, 104, 22, ORANGE, 30)
    icon.alpha_composite(tile, positions[3])

    icon.save("icon.png")
    print("icon.png ساخته شد")


def build_presplash():
    splash = Image.new("RGBA", (SIZE, SIZE), BG)
    glyph_equals(splash, SIZE // 2, SIZE // 2, 240, 44, ORANGE, 62)
    splash.save("presplash.png")
    print("presplash.png ساخته شد")


if __name__ == "__main__":
    build_icon()
    build_presplash()
