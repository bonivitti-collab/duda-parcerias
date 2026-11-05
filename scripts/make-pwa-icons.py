#!/usr/bin/env python3
"""Build PWA icons from Eduarda Vitti's public profile photo.

Source: public TikTok avatar for @eduarda.vitti (display name Duda Vitti),
saved as icons/source-eduarda-vitti.jpg. The same person as the public
Instagram profile @eduarda.vitti. Crop is a face-centered square so the
portrait stays recognizable at home-screen size and the face sits inside
the maskable safe circle (center 80%).
"""

from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "icons" / "source-eduarda-vitti.jpg"
ICONS = ROOT / "icons"


def face_crop(src: Image.Image) -> Image.Image:
    w, h = src.size
    side = int(round(w * 0.66))
    cx, cy = int(w * 0.50), int(h * 0.32)
    x0 = max(0, min(w - side, cx - side // 2))
    y0 = max(0, min(h - side, cy - side // 2))
    return src.crop((x0, y0, x0 + side, y0 + side))


def render(crop: Image.Image, size: int) -> Image.Image:
    img = crop.resize((size, size), Image.Resampling.LANCZOS)
    if size <= 192:
        img = img.filter(ImageFilter.UnsharpMask(radius=0.7, percent=60, threshold=2))
    return img


def main() -> None:
    src = Image.open(SOURCE).convert("RGB")
    crop = face_crop(src)
    ICONS.mkdir(exist_ok=True)

    outputs = {
        ICONS / "icon-512.png": 512,
        ICONS / "icon-192.png": 192,
        ICONS / "icon-maskable-512.png": 512,
        ICONS / "icon-maskable-192.png": 192,
        ICONS / "apple-touch-icon.png": 180,
        ICONS / "favicon-32.png": 32,
        ICONS / "favicon-16.png": 16,
    }
    # Full-bleed portrait works as both "any" and "maskable": the face is
    # inside the center 80% safe circle, and the hair fills the mask edges.
    rendered = {}
    for path, size in outputs.items():
        img = render(crop, size)
        img.save(path, format="PNG", optimize=True)
        rendered[size] = img

    apple = rendered[180]
    apple.save(ROOT / "apple-touch-icon.png", format="PNG", optimize=True)

    # Build the ico from the largest frame so 32 and 48 are not upscaled from 16.
    render(crop, 48).save(
        ROOT / "favicon.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
    )
    print("wrote icons from", SOURCE.name, "crop", crop.size)


if __name__ == "__main__":
    main()
