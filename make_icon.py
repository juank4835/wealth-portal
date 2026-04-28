"""Genera apple-touch-icon.png 180x180.

Frame verde saturado (#00ff66) + círculo NEGRO PURO + 4 barras verdes
ascendentes centradas. Sin bleed verde:
  - El borde exterior del círculo se renderiza con LANCZOS (AA suave).
  - El interior se cubre con un overlay negro hard-edge para eliminar
    cualquier rastro de píxeles verdosos del LANCZOS.
  - Las barras se dibujan directamente a 180px (sin supersample) para
    que tengan bordes pixel-perfect sin halo verde.
"""
from PIL import Image, ImageDraw

SIZE = 180
SCALE = 4
S = SIZE * SCALE

BLACK = (0, 0, 0, 255)
GREEN = (29, 185, 84, 255)  # #1DB954 — Spotify green
PAD = 14

# === 1) Frame verde + círculo negro a supersample con LANCZOS ===
# Solo para suavizar el borde EXTERIOR del círculo verde
big = Image.new('RGBA', (S, S), GREEN)
bd = ImageDraw.Draw(big)
bd.ellipse([PAD * SCALE, PAD * SCALE, S - PAD * SCALE, S - PAD * SCALE], fill=BLACK)
final = big.resize((SIZE, SIZE), Image.LANCZOS)

# === 2) Cubrir interior con negro PURO (hard-edge, sin feather) ===
# Esto sobreescribe los píxeles verdosos del bleed dejando el interior limpio
INNER_PAD = PAD + 3
d = ImageDraw.Draw(final)
d.ellipse([INNER_PAD, INNER_PAD, SIZE - INNER_PAD, SIZE - INNER_PAD], fill=BLACK)

# === 3) Bars verdes pixel-perfect (sin supersample = sin halo) ===
BAR_W = 16
Y_BASE = 130
RADIUS = 3
bars = [(54, 110), (78, 96), (102, 78), (126, 60)]
for cx, ytop in bars:
    x1 = cx - BAR_W // 2
    x2 = cx + BAR_W // 2
    d.rounded_rectangle(
        [x1, ytop, x2, Y_BASE],
        radius=RADIUS, fill=GREEN
    )

final.save('/Users/juank4835/Documents/wealth-portal/apple-touch-icon.png')
print(f'Saved {SIZE}x{SIZE} apple-touch-icon.png (pure black interior, sharp bars)')
