"""Genera apple-touch-icon.png 180x180.

Icono: bar chart skyline ascendente — 5 barras subiendo en verde
fluorescente #00ff00 sobre fondo negro puro, con halo glow.
Renderizado a 4x supersample y reducido con LANCZOS.
"""
from PIL import Image, ImageDraw, ImageFilter

SIZE = 180
SCALE = 4
S = SIZE * SCALE

# Fondo negro puro
img = Image.new('RGBA', (S, S), (0, 0, 0, 255))

# Capa del chart (sobre transparente)
chart = Image.new('RGBA', (S, S), (0, 0, 0, 0))
draw = ImageDraw.Draw(chart)

GREEN = (0, 255, 0, 255)
BAR_W = 20  # ancho de cada barra (en coords 180)
Y_BASE = 150  # baseline
RADIUS = 4   # radio esquinas redondeadas

# Skyline ascendente — 5 barras: (centro_x, top_y)
bars = [
    (35, 122),
    (65, 102),
    (95, 76),
    (125, 50),
    (155, 28),
]

for cx, ytop in bars:
    x1 = (cx - BAR_W // 2) * SCALE
    x2 = (cx + BAR_W // 2) * SCALE
    y1 = ytop * SCALE
    y2 = Y_BASE * SCALE
    draw.rounded_rectangle([x1, y1, x2, y2], radius=RADIUS * SCALE, fill=GREEN)

# Glow halo (outer + inner)
outer = chart.filter(ImageFilter.GaussianBlur(radius=14 * SCALE / 4))
inner = chart.filter(ImageFilter.GaussianBlur(radius=4 * SCALE / 4))
img.alpha_composite(outer)
img.alpha_composite(inner)
img.alpha_composite(chart)

# Reducir con LANCZOS para anti-aliasing
img.resize((SIZE, SIZE), Image.LANCZOS).save(
    '/Users/juank4835/Documents/wealth-portal/apple-touch-icon.png'
)
print(f'Saved {SIZE}x{SIZE} apple-touch-icon.png (bar skyline)')
