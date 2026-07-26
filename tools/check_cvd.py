"""Colorblindness (CVD) check for the spotviz categorical palette.

Simulates deuteranopia / protanopia / tritanopia using the Machado et al. (2009)
matrices (applied in linear RGB), converts to CIELAB, and reports the minimum
pairwise ΔE (CIE76) among the palette under normal and CVD vision. A small
minimum ΔE means two categories look alike to that viewer.

Also reports WCAG contrast of the text grays against the dark background.

Dev tool only — pure Python + matplotlib (for the optional swatch image); not
part of the shipped package. Run:  python tools/check_cvd.py
"""

import math
from pathlib import Path

import matplotlib.pyplot as plt

import spotviz as sv

# Machado et al. 2009 CVD matrices at severity 1.0 (applied to linear RGB).
CVD = {
    "deuteranopia": [
        [0.367322, 0.860646, -0.227968],
        [0.280085, 0.672501, 0.047413],
        [-0.011820, 0.042940, 0.968881],
    ],
    "protanopia": [
        [0.152286, 1.052583, -0.204868],
        [0.114503, 0.786281, 0.099216],
        [-0.003882, -0.048116, 1.051998],
    ],
    "tritanopia": [
        [1.255528, -0.076749, -0.178779],
        [-0.078411, 0.930809, 0.147602],
        [0.004733, 0.691367, 0.303900],
    ],
}


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def linear_to_srgb(c):
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def apply_matrix(m, v):
    return [sum(m[i][j] * v[j] for j in range(3)) for i in range(3)]


def simulate(hexcolor, kind):
    lin = [srgb_to_linear(c) for c in hex_to_rgb(hexcolor)]
    out = apply_matrix(CVD[kind], lin)
    return tuple(linear_to_srgb(c) for c in out)


def rgb_to_lab(rgb):
    # linear RGB -> XYZ (sRGB, D65) -> LAB
    r, g, b = (srgb_to_linear(c) for c in rgb)
    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505
    xn, yn, zn = 0.95047, 1.0, 1.08883
    def f(t):
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x / xn), f(y / yn), f(z / zn)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def delta_e(lab1, lab2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(lab1, lab2)))


def relative_luminance(hexcolor):
    r, g, b = (srgb_to_linear(c) for c in hex_to_rgb(hexcolor))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg, bg):
    l1, l2 = relative_luminance(fg), relative_luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def min_pairwise(palette, kind=None):
    labs = []
    for h in palette:
        rgb = simulate(h, kind) if kind else hex_to_rgb(h)
        labs.append(rgb_to_lab(rgb))
    worst, pair = math.inf, None
    for i in range(len(labs)):
        for j in range(i + 1, len(labs)):
            d = delta_e(labs[i], labs[j])
            if d < worst:
                worst, pair = d, (i, j)
    return worst, pair


def report(palette):
    print(f"palette: {palette}")
    print(f"{'vision':<14}{'min ΔE':>8}   closest pair")
    for kind in (None, "deuteranopia", "protanopia", "tritanopia"):
        worst, (i, j) = min_pairwise(palette, kind)
        name = kind or "normal"
        flag = "  <-- weak" if worst < 15 else ""
        print(f"{name:<14}{worst:>8.1f}   {palette[i]} / {palette[j]}{flag}")
    print("\nWCAG contrast on dark background (#121212):")
    dark = sv.theme_colors("dark")
    for label, col in [("white text", dark["text"]), ("gray subtext", dark["subtext"]),
                       ("green accent", dark["accent"]), ("muted gray", dark["muted"])]:
        cr = contrast_ratio(col, dark["bg"])
        print(f"  {label:<14} {cr:5.2f}:1")


def swatch_image(palette, path):
    kinds = [None, "deuteranopia", "protanopia", "tritanopia"]
    fig, axes = plt.subplots(len(kinds), 1, figsize=(8, 4.2))
    for ax, kind in zip(axes, kinds):
        for k, h in enumerate(palette):
            rgb = simulate(h, kind) if kind else hex_to_rgb(h)
            ax.add_patch(plt.Rectangle((k, 0), 1, 1, color=rgb))
        ax.set_xlim(0, len(palette)); ax.set_ylim(0, 1)
        ax.set_yticks([]); ax.set_xticks([])
        ax.set_ylabel(kind or "normal", rotation=0, ha="right", va="center")
    fig.suptitle("spotviz categorical palette under CVD simulation")
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    report(sv.CATEGORICAL)
    out = Path(__file__).resolve().parent.parent / "examples" / "palette_cvd.png"
    swatch_image(sv.CATEGORICAL, out)
