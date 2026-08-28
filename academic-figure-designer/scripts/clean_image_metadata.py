#!/usr/bin/env python3
"""Sanitize image metadata and strip C2PA, EXIF, XMP, and invisible provenance markers.

This module provides standalone CLI and importable utilities to strip all
generative AI provenance metadata (C2PA, JUMBF, EXIF, XMP, IPTC, Adobe markers,
and trailing payloads) from rendered academic figures, ensuring pristine,
publication-ready deliverables.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image


def strip_image_metadata(
    input_path: str | Path,
    output_path: Optional[str | Path] = None,
    output_format: Optional[str] = None,
    quality: int = 95,
) -> Tuple[bool, int, int]:
    """Strip all metadata (C2PA, EXIF, XMP, IPTC) from an image file.

    Args:
        input_path: Path to the source image.
        output_path: Destination path. If None, overwrites input_path atomically.
        output_format: Desired format ('PNG', 'JPEG', etc.). Defaults to source format.
        quality: JPEG compression quality (1-100) if saving as JPEG. Default 95.

    Returns:
        Tuple of (success: bool, original_bytes: int, cleaned_bytes: int)
    """
    src = Path(input_path).resolve()
    if not src.is_file():
        raise FileNotFoundError(f"Image not found: {src}")

    dst = Path(output_path).resolve() if output_path else src

    original_size = src.stat().st_size

    with Image.open(src) as img:
        img_format = output_format.upper() if output_format else (img.format or "PNG").upper()
        
        # Normalize modes
        if img_format in ("JPEG", "JPG"):
            if img.mode in ("RGBA", "LA", "P"):
                # Composite onto opaque white background
                bg = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "RGBA":
                    bg.paste(img, mask=img.split()[3])
                else:
                    bg.paste(img.convert("RGBA"), mask=img.convert("RGBA").split()[3])
                clean_img = bg
            elif img.mode != "RGB":
                clean_img = img.convert("RGB")
            else:
                clean_img = Image.new("RGB", img.size)
                clean_img.paste(img)
        else:
            # PNG or other lossless formats
            target_mode = "RGBA" if img.mode in ("RGBA", "LA", "P") else "RGB"
            clean_img = Image.new(target_mode, img.size)
            clean_img.paste(img)

        # Write to temporary file first for atomic overwrite
        dst.parent.mkdir(parents=True, exist_ok=True)
        tmp_dst = dst.with_name(f".tmp_clean_{dst.name}")
        
        try:
            if img_format in ("JPEG", "JPG"):
                clean_img.save(
                    tmp_dst,
                    format="JPEG",
                    quality=quality,
                    subsampling=0,
                    optimize=True,
                )
            elif img_format == "PNG":
                clean_img.save(
                    tmp_dst,
                    format="PNG",
                    optimize=True,
                )
            elif img_format == "WEBP":
                clean_img.save(
                    tmp_dst,
                    format="WEBP",
                    lossless=True,
                    quality=100,
                )
            else:
                clean_img.save(tmp_dst, format=img_format)

            tmp_dst.replace(dst)
        finally:
            if tmp_dst.exists():
                tmp_dst.unlink()

    cleaned_size = dst.stat().st_size
    return True, original_size, cleaned_size


def batch_clean_directory(
    directory_path: str | Path,
    recursive: bool = True,
    extensions: Tuple[str, ...] = (".png", ".jpg", ".jpeg", ".webp"),
) -> int:
    """Batch clean metadata for all supported images in a directory.

    Returns the count of processed images.
    """
    root = Path(directory_path).resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Directory not found: {root}")

    files = root.rglob("*") if recursive else root.glob("*")
    count = 0
    for file_path in files:
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
    parser.add_argument("target", help="Path to image file or directory")
    parser.add_argument(
        "-o", "--output", help="Output path (for single image; defaults to in-place replacement)"
    )
    parser.add_argument(
        "--format", choices=["PNG", "JPEG", "WEBP"], help="Convert to specific format"
    )
    parser.add_argument(
        "-q", "--quality", type=int, default=95, help="JPEG quality (default: 95)"
    )
    parser.add_argument(
        "-r", "--recursive", action="store_true", default=True, help="Recurse into subdirectories"
    )

    args = parser.parse_args()
    target_path = Path(args.target).resolve()

    if target_path.is_file():
        success, orig, clean = strip_image_metadata(
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
        count = batch_clean_directory(target_path, recursive=args.recursive)
        print(f"✅ Batch cleaned {count} images in {target_path}")
    else:
        print(f"❌ Target path not found: {target_path}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
