"""Genera apple-touch-icon.png 180x180.

Icono inverso: frame verde saturado (#00ff66) + círculo negro adentro
+ 4 barras verdes saturadas ascendentes centradas.

Técnica para evitar el bleed verde dentro del círculo: el frame se
renderiza a 4x con LANCZOS (borde verde→negro suave por AA), luego se
sobreescribe el interior con negro puro vía máscara con feather. Las
barras se renderizan también a 4x para que tengan bordes AA limpios.
"""
from PIL import Image, ImageDraw, ImageFilter

SIZE = 180
SCALE = 4
S = SIZE * SCALE

BLACK = (0, 0, 0, 255)
GREEN = (0, 255, 102, 255)  # #00ff66 — dashboard saturado
PAD = 14  # padding del frame verde (en coords 180)

# === 1) Frame verde + círculo negro a supersample, luego LANCZOS ===
big = Image.new('RGBA', (S, S), GREEN)
bd = ImageDraw.Draw(big)
bd.ellipse([PAD * SCALE, PAD * SCALE, S - PAD * SCALE, S - PAD * SCALE], fill=BLACK)
frame = big.resize((SIZE, SIZE), Image.LANCZOS)

# === 2) Eliminar bleed verde del interior ===
# Máscara: blanco sólido en el interior del círculo (con inset), feather suave
INNER_PAD = PAD + 3  # 3 px adentro del borde para limpiar la zona de bleed
mask = Image.new('L', (SIZE, SIZE), 0)
md = ImageDraw.Draw(mask)
md.ellipse([INNER_PAD, INNER_PAD, SIZE - INNER_PAD, SIZE - INNER_PAD], fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(radius=0.6))

# Composite: donde mask=255 → negro puro; donde mask=0 → frame original
black_layer = Image.new('RGBA', (SIZE, SIZE), BLACK)
final = Image.composite(black_layer, frame, mask)

# === 3) Barras verdes a supersample con AA, composite encima ===
BAR_W = 16
Y_BASE = 130
RADIUS = 3
bars = [(54, 110), (78, 96), (102, 78), (126, 60)]

bars_big = Image.new('RGBA', (S, S), (0, 0, 0, 0))
ld = ImageDraw.Draw(bars_big)
for cx, ytop in bars:
    x1 = (cx - BAR_W // 2) * SCALE
    x2 = (cx + BAR_W // 2) * SCALE
    ld.rounded_rectangle(
        [x1, ytop * SCALE, x2, Y_BASE * SCALE],
        radius=RADIUS * SCALE, fill=GREEN
    )
bars_180 = bars_big.resize((SIZE, SIZE), Image.LANCZOS)
final.alpha_composite(bars_180)

final.save('/Users/juank4835/Documents/wealth-portal/apple-touch-icon.png')
print(f'Saved {SIZE}x{SIZE} apple-touch-icon.png (4 bars centradas, interior pure black)')
