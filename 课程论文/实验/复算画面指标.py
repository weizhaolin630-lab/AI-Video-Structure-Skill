"""Measure tone and saturation in two reference images from the course notes."""

from pathlib import Path

import numpy as np
from PIL import Image


SOURCE = Path(__file__).resolve().parents[2] / "图片和附件"


def measure(path):
    with Image.open(path) as image:
        rgb = np.asarray(image.convert("RGB"), dtype=np.float32) / 255
        width, height = image.size
    luma = rgb @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    p10, p50, p90 = np.percentile(luma, [10, 50, 90])
    peak = rgb.max(axis=2)
    chroma = peak - rgb.min(axis=2)
    saturation = np.divide(chroma, peak, out=np.zeros_like(peak), where=peak > 0)
    return width, height, p10, p50, p90, float(saturation.mean())


def main():
    print("| Image | Pixels | Aspect | P10 | P50 | P90 | P90-P10 | Mean HSV S |")
    print("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for filename in ("image 11.png", "image 34.png"):
        width, height, p10, p50, p90, saturation = measure(SOURCE / filename)
        print(
            f"| {filename} | {width} x {height} | {width / height:.3f} | "
            f"{p10:.3f} | {p50:.3f} | {p90:.3f} | {p90 - p10:.3f} | {saturation:.3f} |"
        )


if __name__ == "__main__":
    main()
