#!/usr/bin/env python3
"""Add numbered SVG markers over a local reference image."""

import argparse
import base64
from io import BytesIO
import json
from pathlib import Path

from PIL import Image, ImageOps


def load_points(path):
    points = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(points, list) or not 1 <= len(points) <= 8:
        raise ValueError("Provide 1–8 annotation points as a JSON array.")
    for point in points:
        if not isinstance(point, list) or len(point) != 2:
            raise ValueError("Each point must be an array with x and y.")
        if any(type(value) not in (int, float) or not 0 <= value <= 1 for value in point):
            raise ValueError("Each coordinate must be a number between 0 and 1.")
    return points


def build_svg(path, points):
    with Image.open(path, formats=["PNG", "JPEG", "WEBP"]) as source:
        if getattr(source, "n_frames", 1) != 1:
            raise ValueError("Provide a single-frame PNG, JPEG or WebP image.")
        image = ImageOps.exif_transpose(source)
        width, height = image.size
        if min(width, height) < 24:
            raise ValueError("The image must be at least 24 pixels on each side.")
        png = BytesIO()
        if image.mode == "CMYK":
            image = image.convert("RGB")
            image.info.pop("icc_profile", None)
        image.save(png, format="PNG", exif=b"")
    payload = base64.b64encode(png.getvalue()).decode("ascii")
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<image width="{width}" height="{height}" xlink:href="data:image/png;base64,{payload}"/>',
    ]
    radius = max(6, min(width, height) / 38)
    margin = radius + 2
    for number, (x, y) in enumerate(points, start=1):
        target_x, target_y = x * width, y * height
        mark_x = min(width - margin, max(margin, target_x))
        mark_y = min(height - margin, max(margin, target_y))
        if (mark_x, mark_y) != (target_x, target_y):
            parts.append(
                f'<line x1="{target_x:.2f}" y1="{target_y:.2f}" '
                f'x2="{mark_x:.2f}" y2="{mark_y:.2f}" stroke="#fff" stroke-width="2"/>'
            )
        parts.extend([
            f'<circle cx="{mark_x:.2f}" cy="{mark_y:.2f}" r="{radius:.2f}" '
            f'fill="#111827" stroke="#fff" stroke-width="2"/>',
            f'<text x="{mark_x:.2f}" y="{mark_y + radius * 0.40:.2f}" fill="#fff" '
            f'text-anchor="middle" font-family="sans-serif" font-size="{radius * 1.12:.2f}" '
            f'font-weight="bold">{number}</text>',
        ])
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("points", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.output.suffix.lower() != ".svg":
        parser.error("The output path must end in .svg.")
    try:
        svg = build_svg(args.image, load_points(args.points))
        with args.output.open("x", encoding="utf-8") as output:
            output.write(svg)
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
