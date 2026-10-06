from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image
from PIL.PngImagePlugin import PngInfo


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "fig1-draw" / "scripts"))

from clean_image_metadata import batch_clean_directory, strip_image_metadata  # noqa: E402


class CleanImageMetadataTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.tmp = Path(temporary.name)

    def test_jpeg_trailing_payload_is_removed_in_place(self) -> None:
        test_file = self.tmp / "test_image.jpg"
        Image.new("RGB", (100, 100), color=(200, 100, 50)).save(test_file, format="JPEG")
        with test_file.open("ab") as handle:
            handle.write(b"c2pa_fake_watermark_data_payload_12345")
        initial_size = test_file.stat().st_size

        original_size, _ = strip_image_metadata(test_file)

        self.assertEqual(initial_size, original_size)
        cleaned = test_file.read_bytes()
        self.assertNotIn(b"c2pa_fake", cleaned)
        self.assertTrue(cleaned.endswith(b"\xff\xd9"))
        with Image.open(test_file) as result:
            self.assertEqual((100, 100), result.size)

    def test_png_text_metadata_is_removed_and_transparency_kept(self) -> None:
        test_file = self.tmp / "test_image.png"
        info = PngInfo()
        info.add_text("parameters", "c2pa provenance manifest")
        Image.new("RGBA", (50, 50), color=(100, 150, 200, 128)).save(test_file, pnginfo=info)
        output_file = self.tmp / "cleaned.png"

        strip_image_metadata(test_file, output_path=output_file)

        with Image.open(output_file) as result:
            self.assertEqual("RGBA", result.mode)
            self.assertEqual((50, 50), result.size)
            self.assertNotIn("parameters", result.info)

    def test_batch_clean_directory_recurses(self) -> None:
        sub = self.tmp / "subdir"
        sub.mkdir()
        Image.new("RGB", (20, 20)).save(self.tmp / "img1.png", "PNG")
        Image.new("RGB", (30, 30)).save(sub / "img2.jpg", "JPEG")

        self.assertEqual(2, batch_clean_directory(self.tmp))


if __name__ == "__main__":
    unittest.main()
