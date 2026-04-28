"""Genera apple-touch-icon.png 180x180.

Icono estilo Spotify: frame negro + círculo verde Spotify (#1DB954)
+ 5 barras negras ascendentes adentro. Sin glow, contraste duro.
Renderizado a 4x supersample y reducido con LANCZOS para AA.
"""
from PIL import Image, ImageDraw

SIZE = 180
SCALE = 4
S = SIZE * SCALE

BLACK = (0, 0, 0, 255)
SPOTIFY_GREEN = (29, 185, 84, 255)  # #1DB954

# Frame negro + círculo verde Spotify
img = Image.new('RGBA', (S, S), BLACK)
d = ImageDraw.Draw(img)
PAD = 14 * SCALE
d.ellipse([PAD, PAD, S - PAD, S - PAD], fill=SPOTIFY_GREEN)

# 5 barras negras ascendentes adentro del círculo
BAR_W = 16
Y_BASE = 130
RADIUS = 3
bars = [
    (46, 110),
    (70, 96),
    (94, 78),
    (118, 60),
    (142, 42),
]
for cx, ytop in bars:
    x1 = (cx - BAR_W // 2) * SCALE
    x2 = (cx + BAR_W // 2) * SCALE
    d.rounded_rectangle(
        [x1, ytop * SCALE, x2, Y_BASE * SCALE],
        radius=RADIUS * SCALE, fill=BLACK
    )

img.resize((SIZE, SIZE), Image.LANCZOS).save(
    '/Users/juank4835/Documents/wealth-portal/apple-touch-icon.png'
)
print(f'Saved {SIZE}x{SIZE} apple-touch-icon.png (Spotify-style)')
