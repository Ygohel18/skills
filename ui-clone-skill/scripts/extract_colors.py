#!/usr/bin/env python3
"""
extract_colors.py — Extract dominant colors from a screenshot or image.

Usage:
    python3 scripts/extract_colors.py <image_path> [--top N] [--format hex|hsl|rgb]

Output:
    A color palette report printed to stdout, ready to paste into DESIGN.md.

Dependencies:
    pip install Pillow colorthief

Error handling:
    - Missing file: prints clear message and exits with code 1
    - Missing deps: prints install command and exits with code 2
    - Unsupported format: prints supported formats and exits with code 3
"""

import sys
import os
import argparse


def check_deps():
    missing = []
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        missing.append("Pillow")
    try:
        from colorthief import ColorThief  # noqa: F401
    except ImportError:
        missing.append("colorthief")
    if missing:
        print(f"ERROR: Missing dependencies: {', '.join(missing)}", file=sys.stderr)
        print(f"Install with: pip install {' '.join(missing)}", file=sys.stderr)
        sys.exit(2)


def rgb_to_hex(r, g, b):
    return f"#{r:02X}{g:02X}{b:02X}"


def rgb_to_hsl(r, g, b):
    r_, g_, b_ = r / 255.0, g / 255.0, b / 255.0
    cmax = max(r_, g_, b_)
    cmin = min(r_, g_, b_)
    delta = cmax - cmin
    l = (cmax + cmin) / 2

    if delta == 0:
        h = s = 0.0
    else:
        s = delta / (1 - abs(2 * l - 1))
        if cmax == r_:
            h = 60 * (((g_ - b_) / delta) % 6)
        elif cmax == g_:
            h = 60 * ((b_ - r_) / delta + 2)
        else:
            h = 60 * ((r_ - g_) / delta + 4)

    return f"hsl({h:.0f}, {s*100:.0f}%, {l*100:.0f}%)"


def luminance(r, g, b):
    """Rough luminance for dark/light classification."""
    return 0.299 * r + 0.587 * g + 0.114 * b


def classify_color(r, g, b, index, total):
    """
    Heuristically guess a color's role based on its position in the palette
    and its luminance. Not perfect — review results and adjust manually.
    """
    lum = luminance(r, g, b)
    if index == 0:
        return "primary-background" if lum < 128 else "primary-background-light"
    if index == 1:
        if lum < 60:
            return "surface-dark"
        if lum > 200:
            return "surface-light"
        return "primary-accent"
    if index == 2:
        return "secondary-accent"
    if index == total - 1:
        return "text-color" if lum > 128 else "muted-text"
    return f"color-{index + 1}"


def extract_palette(image_path, top=8, fmt="hex"):
    from colorthief import ColorThief

    if not os.path.isfile(image_path):
        print(f"ERROR: File not found: {image_path}", file=sys.stderr)
        sys.exit(1)

    ext = os.path.splitext(image_path)[1].lower()
    supported = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}
    if ext not in supported:
        print(f"ERROR: Unsupported image format '{ext}'.", file=sys.stderr)
        print(f"Supported: {', '.join(sorted(supported))}", file=sys.stderr)
        sys.exit(3)

    ct = ColorThief(image_path)
    dominant = ct.get_color(quality=1)
    palette  = ct.get_palette(color_count=top + 1, quality=1)

    # Deduplicate (colorthief sometimes returns near-dupes)
    seen = set()
    unique = []
    for c in palette:
        key = (c[0] // 10, c[1] // 10, c[2] // 10)  # bucket to 10-unit granularity
        if key not in seen:
            seen.add(key)
            unique.append(c)
    colors = unique[:top]

    def fmt_color(r, g, b):
        if fmt == "hsl":
            return rgb_to_hsl(r, g, b)
        if fmt == "rgb":
            return f"rgb({r}, {g}, {b})"
        return rgb_to_hex(r, g, b)

    lines = [
        f"# Color Palette — extracted from: {os.path.basename(image_path)}",
        f"# Top {len(colors)} dominant colors (review and adjust roles manually)",
        "",
        "## CSS Variables (copy into globals.css or DESIGN.md)",
        "",
        ":root {",
    ]

    for i, (r, g, b) in enumerate(colors):
        role = classify_color(r, g, b, i, len(colors))
        val  = fmt_color(r, g, b)
        lines.append(f"  --color-{role}: {val};")

    lines += [
        "}",
        "",
        "## Palette Table (for DESIGN.md)",
        "",
        "| Variable | Value | Role (inferred) |",
        "|---|---|---|",
    ]

    for i, (r, g, b) in enumerate(colors):
        role = classify_color(r, g, b, i, len(colors))
        val  = fmt_color(r, g, b)
        lines.append(f"| `--color-{role}` | `{val}` | {role.replace('-', ' ').title()} |")

    lines += [
        "",
        "## Dominant color",
        f"  {fmt_color(*dominant)}",
        "",
        "---",
        "NOTE: These are extracted pixel colors, not semantic design tokens.",
        "Review each color, give it the correct semantic name (primary, surface,",
        "text, border, accent, etc.), and remove near-duplicates.",
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Extract dominant colors from a screenshot and output palette for DESIGN.md."
    )
    parser.add_argument("image", help="Path to the screenshot or image file")
    parser.add_argument("--top", type=int, default=8, help="Number of colors to extract (default: 8)")
    parser.add_argument(
        "--format", choices=["hex", "hsl", "rgb"], default="hex",
        dest="fmt", help="Output color format (default: hex)"
    )
    args = parser.parse_args()

    check_deps()
    output = extract_palette(args.image, top=args.top, fmt=args.fmt)
    print(output)


if __name__ == "__main__":
    main()
