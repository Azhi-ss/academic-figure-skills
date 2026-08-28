from __future__ import annotations

import sys
from pathlib import Path
from PIL import Image
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "academic-figure-designer" / "scripts"))

from clean_image_metadata import strip_image_metadata, batch_clean_directory  # noqa: E402


def test_strip_image_metadata_jpeg(tmp_path: Path):
    # Create an image with dummy extra data/segments
    test_file = tmp_path / "test_image.jpg"
    img = Image.new("RGB", (100, 100), color=(200, 100, 50))
    img.save(test_file, format="JPEG")
    
    # Append trailing dummy bytes (simulating trailing watermark payload)
    with open(test_file, "ab") as f:
        f.write(b"c2pa_fake_watermark_data_payload_12345")
    
    initial_size = test_file.stat().st_size
    with open(test_file, "rb") as f:
        assert b"c2pa_fake" in f.read()
    
    success, orig, clean = strip_image_metadata(test_file)
    assert success is True
    assert orig == initial_size
    
    # Check that metadata and trailing bytes are gone
    with open(test_file, "rb") as f:
        cleaned_bytes = f.read()
        assert b"c2pa_fake" not in cleaned_bytes
        # Ends exactly with JPEG EOI \xff\xd9
        assert cleaned_bytes.endswith(b"\xff\xd9")
    
    # Check image is readable and dimensions are preserved
    with Image.open(test_file) as result:
        assert result.size == (100, 100)


def test_strip_image_metadata_png_transparency(tmp_path: Path):
    test_file = tmp_path / "test_image.png"
    img = Image.new("RGBA", (50, 50), color=(100, 150, 200, 128))
    img.save(test_file, format="PNG")
    
    output_file = tmp_path / "cleaned.png"
    success, orig, clean = strip_image_metadata(test_file, output_path=output_file)
    assert success is True
    assert output_file.exists()
    
    with Image.open(output_file) as result:
        assert result.mode == "RGBA"
        assert result.size == (50, 50)


def test_batch_clean_directory(tmp_path: Path):
    sub = tmp_path / "subdir"
    sub.mkdir()
    
    f1 = tmp_path / "img1.png"
    f2 = sub / "img2.jpg"
    Image.new("RGB", (20, 20)).save(f1, "PNG")
    Image.new("RGB", (30, 30)).save(f2, "JPEG")
    
    count = batch_clean_directory(tmp_path, recursive=True)
    assert count == 2
