#!/usr/bin/env python3
"""Sanitize image metadata and strip C2PA, EXIF, XMP, and invisible provenance markers.

Pixels are re-encoded into a fresh image, so generative AI provenance metadata
(C2PA, JUMBF, EXIF, XMP, IPTC, Adobe markers, and trailing payloads) is dropped
from rendered academic figures, leaving publication-ready deliverables.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image


def strip_image_metadata(
    input_path: str | Path,
    output_path: str | Path | None = None,
    output_format: str | None = None,
    quality: int = 95,
) -> tuple[int, int]:
    """Strip all metadata from an image and return ``(original_bytes, cleaned_bytes)``.

    Writes *output_path*, or atomically replaces *input_path* when it is omitted.
    *output_format* defaults to the source format; *quality* applies to JPEG only.
    """
    src = Path(input_path).resolve()
    if not src.is_file():
        raise FileNotFoundError(f"Image not found: {src}")
    dst = Path(output_path).resolve() if output_path else src
    original_size = src.stat().st_size

    with Image.open(src) as img:
        img_format = (output_format or img.format or "PNG").upper()
        img_format = "JPEG" if img_format == "JPG" else img_format
        if img_format == "JPEG":
            # JPEG has no alpha: composite onto an opaque white background.
            rgba = img.convert("RGBA")
            clean_img = Image.new("RGB", img.size, (255, 255, 255))
            clean_img.paste(rgba, mask=rgba)
        else:
            clean_img = Image.new("RGBA" if img.mode in ("RGBA", "LA", "P") else "RGB", img.size)
            clean_img.paste(img)

    options = {
        "JPEG": {"quality": quality, "subsampling": 0, "optimize": True},
        "PNG": {"optimize": True},
        "WEBP": {"lossless": True, "quality": 100},
    }.get(img_format, {})
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp_dst = dst.with_name(f".tmp_clean_{dst.name}")
    try:
        clean_img.save(tmp_dst, format=img_format, **options)
        tmp_dst.replace(dst)
    finally:
        tmp_dst.unlink(missing_ok=True)
    return original_size, dst.stat().st_size


def batch_clean_directory(
    directory_path: str | Path,
    recursive: bool = True,
    extensions: tuple[str, ...] = (".png", ".jpg", ".jpeg", ".webp"),
) -> int:
    """Batch clean metadata for all supported images in a directory.

    Returns the count of processed images.
    """
    root = Path(directory_path).resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Directory not found: {root}")

    count = 0
    for file_path in root.rglob("*") if recursive else root.glob("*"):
        if file_path.is_file() and file_path.suffix.lower() in extensions:
            try:
                strip_image_metadata(file_path)
                count += 1
            except Exception as err:
                print(f"[Warning] Failed to clean {file_path}: {err}", file=sys.stderr)
    return count


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sanitize image metadata, stripping C2PA, EXIF, and AI provenance markers."
    )
    parser.add_argument("target", help="Path to image file or directory (directories are cleaned recursively)")
    parser.add_argument(
        "-o", "--output", help="Output path (for single image; defaults to in-place replacement)"
    )
    parser.add_argument(
        "--format", choices=["PNG", "JPEG", "WEBP"], help="Convert to specific format"
    )
    parser.add_argument(
        "-q", "--quality", type=int, default=95, help="JPEG quality (default: 95)"
    )

    args = parser.parse_args()
    target_path = Path(args.target).resolve()

    if target_path.is_file():
        orig, clean = strip_image_metadata(
            target_path,
            output_path=args.output,
            output_format=args.format,
            quality=args.quality,
        )
        print(
            f"✅ Cleaned {target_path.name}: {orig:,} bytes -> {clean:,} bytes "
            f"(stripped {max(0, orig - clean):,} bytes metadata)"
        )
    elif target_path.is_dir():
        count = batch_clean_directory(target_path)
        print(f"✅ Batch cleaned {count} images in {target_path}")
    else:
        print(f"❌ Target path not found: {target_path}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
