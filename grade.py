"""Windward film grade.
Two looks from the brand book:
  colour  - 'Film Colour': muted colour, lifted blacks, warm highlights, cool shadows, grain
  mono    - 'Film Mono': black & white with the same curve and grain
Usage: python3 grade.py src.jpg out.jpg [colour|mono] [width] [exposure]
"""
import sys
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)

def grade(src, out, mode='colour', width=1800, exposure=0.0, seed=7, sat=0.5, crop=None):
    im = Image.open(src).convert('RGB')
    if crop:  # (l, t, r, b) as fractions
        w, h = im.size
        im = im.crop((int(crop[0]*w), int(crop[1]*h), int(crop[2]*w), int(crop[3]*h)))
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255.0
    a = a ** 0.95 * (2 ** exposure)  # exposure in stops
    lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    if mode == 'mono':
        a = np.repeat(lum[..., None], 3, axis=2)
    else:
        a = lum[..., None] + (a - lum[..., None]) * sat  # muted colour
    # film curve: gentle S, lifted blacks, rolled highlights
    a = np.clip(a, 0, 1.2)
    a = a / (1 + 0.18 * a)  # highlight roll-off
    a = a / a.max() if a.max() > 1 else a
    s = smoothstep(0, 1, a)
    a = a * 0.55 + s * 0.45
    a = 0.035 + a * 0.93
    lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    if mode == 'colour':
        sh = (1 - smoothstep(0.0, 0.5, lum))[..., None]
        hi = smoothstep(0.5, 1.0, lum)[..., None]
        a = a + sh * np.array([-0.012, 0.004, 0.016]) + hi * np.array([0.018, 0.008, -0.014])
    # vignette
    h, w = lum.shape
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    a = a * (1 - 0.16 * smoothstep(0.55, 1.45, r))[..., None]
    # grain: luminance noise, slightly clumped, strongest in mid-tones
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 1, (h, w)).astype(np.float32)
    n = gaussian_filter(n, 0.65) * 1.6 + rng.normal(0, 0.35, (h, w)).astype(np.float32)
    mid = 0.45 + 0.55 * (1 - np.abs(lum - 0.5) * 2)
    amt = 0.03 * (width / 1800) ** 0.3
    a = a + (n * mid * amt)[..., None]
    a = np.clip(a, 0, 1)
    Image.fromarray((a * 255 + 0.5).astype(np.uint8)).save(out, quality=84, optimize=True, progressive=True)

if __name__ == '__main__':
    src, out = sys.argv[1], sys.argv[2]
    mode = sys.argv[3] if len(sys.argv) > 3 else 'colour'
    width = int(sys.argv[4]) if len(sys.argv) > 4 else 1800
    exp = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
    grade(src, out, mode, width, exp)

def grain_only(src, out, seed=11, amount=0.026):
    im = Image.open(src).convert('RGB')
    a = np.asarray(im).astype(np.float32) / 255.0
    h, w, _ = a.shape
    lum = a.mean(axis=2)
    rng = np.random.default_rng(seed)
    n = gaussian_filter(rng.normal(0, 1, (h, w)).astype(np.float32), 0.65) * 1.6 + rng.normal(0, 0.35, (h, w)).astype(np.float32)
    mid = 0.45 + 0.55 * (1 - np.abs(lum - 0.5) * 2)
    a = np.clip(a + (n * mid * amount)[..., None], 0, 1)
    Image.fromarray((a * 255 + 0.5).astype(np.uint8)).save(out, quality=84, optimize=True, progressive=True)
