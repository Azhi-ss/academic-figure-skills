"""Checks for the fig-pptx script fixes."""

import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "fig-pptx" / "scripts"


def load(name):
    path = SCRIPTS / name
    spec = importlib.util.spec_from_file_location(name.replace(".py", ""), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Fig2PptxFixes(unittest.TestCase):
    def test_comic_font_does_not_fall_back(self):
        fonts = load("pick_font.py")
        self.assertEqual(fonts.choose("comic", ["Liberation Sans", "Comic Neue"]), "Comic Neue")
        with self.assertRaises(SystemExit) as caught:
            fonts.choose("comic", ["Liberation Sans"])
        self.assertIn("Comic Neue", str(caught.exception))

    def test_probe_reports_original_size(self):
        probe = load("probe_palette.py")
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "slide.png"
            Image.new("RGB", (800, 400), (255, 255, 255)).save(image)
            result = probe.analyze(image)
        self.assertEqual(result["size"], [800, 400])
        self.assertLess(result["sample_size"][0], 800)

    def test_padded_text_box_is_not_a_half_resolution_error(self):
        guard = load("layout_guard.py")
        slide = {"texts": [{
            "text": "Title",
            "source_bbox": [10, 10, 200, 32],
            "size_px": 18,
            "x": 10 / 400, "y": 10 / 200, "w": 200 / 400, "h": 32 / 200,
        }]}
        warnings = guard._check_text_styles(1, slide, 200, 200 / 96 * 72, 6, 0.85, False)
        self.assertFalse(any("twice" in item for item in warnings))

        slide["texts"][0]["size_px"] = 16
        slide["texts"][0]["source_bbox"] = [10, 10, 200, 32]
        warnings = guard._check_text_styles(1, slide, 200, 200 / 96 * 72, 6, 0.85, False)
        self.assertTrue(any("twice" in item for item in warnings))

    def test_slide_size_follows_source_pixels(self):
        compose = load("compose_pptx.py")
        with tempfile.TemporaryDirectory() as tmp:
            layout = Path(tmp) / "layout.json"
            layout.write_text(
                '{"ref_width": 960, "ref_height": 480, "units": "fraction", "texts": []}'
            )
            deck = compose._load_deck(layout)
        self.assertEqual(deck["slide_width_in"], 10)
        self.assertEqual(deck["slide_height_in"], 5)

    def test_text_box_has_no_theme_shadow(self):
        compose = load("compose_pptx.py")
        families = compose._installed_families()
        if not families:
            self.skipTest("fc-list returned no fonts")
        font = "liberation sans" if "liberation sans" in families else sorted(families)[0]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            layout = root / "layout.json"
            layout.write_text(json.dumps({
                "ref_width": 96, "ref_height": 96, "units": "fraction",
                "texts": [{
                    "text": "Hi", "x": 0.1, "y": 0.2, "w": 0.5, "h": 0.3,
                    "source_bbox": [10, 20, 48, 28], "size_px": 18,
                    "font": font, "color": "#111111",
                }],
            }))
            out = root / "out.pptx"
            compose.build_pptx(compose._load_deck(layout), out)
            with zipfile.ZipFile(out) as zf:
                slide = zf.read("ppt/slides/slide1.xml").decode("utf-8")
        self.assertNotIn("effectRef", slide)
        self.assertNotIn("outerShdw", slide)
        self.assertIn("Hi", slide)


if __name__ == "__main__":
    unittest.main()
