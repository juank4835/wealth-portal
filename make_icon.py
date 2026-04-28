"""Genera apple-touch-icon.png 180x180 con W neón sobre fondo gradiente.

Renderiza a 4x (720x720) y reduce con LANCZOS para anti-aliasing limpio.
"""
from PIL import Image, ImageDraw
import math

SIZE = 180
SCALE = 4
S = SIZE * SCALE

# 1) Fondo: gradiente radial desde verde-oscuro arriba a negro
img = Image.new('RGBA', (S, S), (0, 0, 0, 255))
cx, cy = S * 0.5, S * 0.30
max_r = S * 0.75
px = img.load()
for y in range(S):
    for x in range(S):
        r = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        t = min(1.0, r / max_r)
        if t < 0.6:
            f = t / 0.6
            R = int(13 * (1 - f) + 5 * f)
            G = int(40 * (1 - f) + 10 * f)
            B = int(24 * (1 - f) + 7 * f)
        else:
            f = (t - 0.6) / 0.4
            R = int(5 * (1 - f))
            G = int(10 * (1 - f))
            B = int(7 * (1 - f))
        px[x, y] = (R, G, B, 255)

# 2) Forma de la W (blanca, sobre transparente) — usada como máscara
mask = Image.new('L', (S, S), 0)
md = ImageDraw.Draw(mask)
points = [(42, 50), (72, 132), (90, 90), (108, 132), (138, 50)]
points = [(p[0] * SCALE, p[1] * SCALE) for p in points]
WIDTH = 18 * SCALE
for i in range(len(points) - 1):
    md.line([points[i], points[i + 1]], fill=255, width=WIDTH)
for p in points:
    md.ellipse([p[0] - WIDTH // 2, p[1] - WIDTH // 2,
                p[0] + WIDTH // 2, p[1] + WIDTH // 2], fill=255)

# 3) Gradiente vertical neón verde (00ff8a -> 00cc55)
grad = Image.new('RGBA', (S, S))
gpx = grad.load()
for y in range(S):
    f = y / S
    R = 0
    G = int(0xff * (1 - f) + 0xcc * f)
    B = int(0x8a * (1 - f) + 0x55 * f)
    for x in range(S):
        gpx[x, y] = (R, G, B, 255)

# 4) Componer: poner el gradiente sobre el fondo usando la W como máscara
img.paste(grad, (0, 0), mask)

# 5) Reducir con LANCZOS para AA
img.resize((SIZE, SIZE), Image.LANCZOS).save(
    '/Users/juank4835/Documents/wealth-portal/apple-touch-icon.png'
)
print(f'Saved {SIZE}x{SIZE} apple-touch-icon.png')
