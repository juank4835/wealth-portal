"""Genera apple-touch-icon.png 180x180.

Fondo negro puro + 4 barras verdes ascendentes centradas.
Sin frame, sin círculo — bars son el héroe del icono.
Pixel-perfect a 180px (sin supersample = sin halo verde).
"""
from PIL import Image, ImageDraw

SIZE = 180

BLACK = (0, 0, 0, 255)
GREEN = (29, 185, 84, 255)  # #1DB954 — Spotify green

img = Image.new('RGBA', (SIZE, SIZE), BLACK)
d = ImageDraw.Draw(img)

# 4 barras ascendentes centradas
# spacing 28, ancho 20, baseline 140
BAR_W = 20
Y_BASE = 138
RADIUS = 4
bars = [
    (48, 108),    # más baja  (height 30)
    (76, 86),     #           (height 52)
    (104, 64),    #           (height 74)
    (132, 38),    # más alta  (height 100)
]
for cx, ytop in bars:
    x1 = cx - BAR_W // 2
    x2 = cx + BAR_W // 2
    d.rounded_rectangle(
        [x1, ytop, x2, Y_BASE],
        radius=RADIUS, fill=GREEN
    )

img.save('/Users/juank4835/Documents/wealth-portal/apple-touch-icon.png')
print(f'Saved {SIZE}x{SIZE} apple-touch-icon.png (bars sobre negro puro)')
