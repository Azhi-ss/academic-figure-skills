#!/usr/bin/env python3
"""Extract embedded images from academic PDFs for architecture analysis.

Backends (first available wins for embedded images):
  1. pdfimages (poppler)
  2. PyMuPDF (fitz)
Optional page rasterization: pdftoppm when --pages is set.

This is a helper for academic-figure-architecture-extractor — not a trained
classifier. Filtering is size-based only; structure analysis stays with the agent.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def which(name: str) -> str | None:
    return shutil.which(name)


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=False, capture_output=True, text=True)


def list_pdfimages(pdf: Path) -> list[dict]:
    bin_ = which("pdfimages")
    if not bin_:
        return []
    proc = run([bin_, "-list", str(pdf)])
    if proc.returncode != 0:
        return []
    rows: list[dict] = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("page") or line.startswith("-"):
            continue
        parts = line.split()
        if len(parts) < 5:
            continue
        try:
            page = int(parts[0])
            num = int(parts[1])
            width = int(parts[2]) if parts[2].isdigit() else int(parts[3])
            # pdfimages -list columns: page num type width height ...
            # When type is present, width/height are at 3/4
            if parts[2] in {"image", "smask", "stencil"}:
                width, height = int(parts[3]), int(parts[4])
            else:
                width, height = int(parts[2]), int(parts[3])
        except (ValueError, IndexError):
            continue
        rows.append({"page": page, "index": num, "width": width, "height": height})
    return rows


def extract_pdfimages(pdf: Path, out_dir: Path) -> list[dict]:
    bin_ = which("pdfimages")
    if not bin_:
        return []
    prefix = out_dir / "img"
    proc = run([bin_, "-all", str(pdf), str(prefix)])
    if proc.returncode != 0:
        # fallback png/jpeg only
        proc = run([bin_, "-png", str(pdf), str(prefix)])
        if proc.returncode != 0:
            return []
    listed = list_pdfimages(pdf)
    files = sorted(out_dir.glob("img-*")) + sorted(out_dir.glob("img.*"))
    # pdfimages names: img-000.png or img-000.jpg
    extracted = sorted(
        p for p in out_dir.iterdir() if p.is_file() and p.name.startswith("img")
    )
    results: list[dict] = []
    for i, path in enumerate(extracted):
        meta = listed[i] if i < len(listed) else {}
        w = meta.get("width")
        h = meta.get("height")
        if w is None or h is None:
            try:
                from PIL import Image  # type: ignore

                with Image.open(path) as im:
                    w, h = im.size
            except Exception:
                w, h = None, None
        results.append(
            {
                "path": str(path.resolve()),
                "page": meta.get("page"),
                "index": meta.get("index", i),
                "width": w,
                "height": h,
                "backend": "pdfimages",
            }
        )
    return results


def extract_pymupdf(pdf: Path, out_dir: Path) -> list[dict]:
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return []
    doc = fitz.open(pdf)
    results: list[dict] = []
    n = 0
    for page_i, page in enumerate(doc, start=1):
        for img_i, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            try:
                pix = fitz.Pixmap(doc, xref)
                if pix.n - pix.alpha > 3:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                out = out_dir / f"pymupdf-p{page_i:03d}-{img_i:03d}.png"
                pix.save(str(out))
                results.append(
                    {
                        "path": str(out.resolve()),
                        "page": page_i,
                        "index": img_i,
                        "width": pix.width,
                        "height": pix.height,
                        "backend": "pymupdf",
                    }
                )
                n += 1
            except Exception as exc:
                results.append(
                    {
                        "path": None,
                        "page": page_i,
                        "index": img_i,
                        "error": str(exc),
                        "backend": "pymupdf",
                    }
                )
    return results


def rasterize_pages(pdf: Path, out_dir: Path, pages: str, dpi: int) -> list[dict]:
    bin_ = which("pdftoppm")
    if not bin_:
        return []
    prefix = out_dir / "page"
    cmd = [bin_, "-png", "-r", str(dpi)]
    # pages like "1-3,5" or "all"
    if pages and pages != "all":
        # pdftoppm supports -f -l for a range only; for complex, do all then filter
        if "-" in pages and "," not in pages:
            a, b = pages.split("-", 1)
            cmd.extend(["-f", a, "-l", b])
        elif pages.isdigit():
            cmd.extend(["-f", pages, "-l", pages])
    cmd.extend([str(pdf), str(prefix)])
    proc = run(cmd)
    if proc.returncode != 0:
        return []
    results: list[dict] = []
    for path in sorted(out_dir.glob("page-*.png")):
        # page-1.png
        try:
            page_num = int(path.stem.split("-")[-1])
        except ValueError:
            page_num = None
        results.append(
            {
                "path": str(path.resolve()),
                "page": page_num,
                "index": 0,
                "width": None,
                "height": None,
                "backend": "pdftoppm",
            }
        )
    return results


def size_filter(
    items: list[dict], min_side: int, min_pixels: int
) -> tuple[list[dict], list[dict]]:
    kept, dropped = [], []
    for it in items:
        if it.get("path") is None:
            dropped.append({**it, "filter": "extract_failed"})
            continue
        w, h = it.get("width"), it.get("height")
        if w is None or h is None:
            # keep unknowns for agent review
            kept.append({**it, "filter": "unknown_size_kept"})
            continue
        pixels = w * h
        if w < min_side or h < min_side or pixels < min_pixels:
            dropped.append(
                {
                    **it,
                    "filter": f"too_small ({w}x{h}, {pixels}px)",
                }
            )
        else:
            kept.append({**it, "filter": "size_ok"})
    return kept, dropped


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pdf", type=Path, help="Path to PDF")
    ap.add_argument(
        "-o",
        "--out",
        type=Path,
        default=None,
        help="Output directory (default: ./arch-extract/<pdf-stem>)",
    )
    ap.add_argument(
        "--min-side",
        type=int,
        default=300,
        help="Min width and height in pixels (default 300)",
    )
    ap.add_argument(
        "--min-pixels",
        type=int,
        default=90_000,
        help="Min total pixels (default 90000)",
    )
    ap.add_argument(
        "--pages",
        default="",
        help="Also rasterize pages with pdftoppm: N, N-M, or all",
    )
    ap.add_argument("--dpi", type=int, default=150, help="pdftoppm DPI (default 150)")
    ap.add_argument(
        "--backend",
        choices=["auto", "pdfimages", "pymupdf"],
        default="auto",
        help="Embedded-image backend",
    )
    args = ap.parse_args()

    pdf = args.pdf.expanduser().resolve()
    if not pdf.is_file():
        print(json.dumps({"ok": False, "error": f"PDF not found: {pdf}"}), file=sys.stderr)
        return 2

    out_dir = (
        args.out.expanduser().resolve()
        if args.out
        else (Path.cwd() / "arch-extract" / pdf.stem).resolve()
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    tools = {
        "pdfimages": bool(which("pdfimages")),
        "pdftoppm": bool(which("pdftoppm")),
        "pymupdf": False,
    }
    try:
        import fitz  # noqa: F401

        tools["pymupdf"] = True
    except ImportError:
        pass

    embedded: list[dict] = []
    backend_used = None
    if args.backend in {"auto", "pdfimages"} and tools["pdfimages"]:
        embedded = extract_pdfimages(pdf, out_dir)
        backend_used = "pdfimages"
    if not embedded and args.backend in {"auto", "pymupdf"} and tools["pymupdf"]:
        embedded = extract_pymupdf(pdf, out_dir)
        backend_used = "pymupdf"

    pages: list[dict] = []
    if args.pages:
        pages = rasterize_pages(pdf, out_dir, args.pages, args.dpi)

    all_imgs = [x for x in embedded if x.get("path")] + pages
    kept, dropped = size_filter(all_imgs, args.min_side, args.min_pixels)

    report = {
        "ok": True,
        "pdf": str(pdf),
        "out_dir": str(out_dir),
        "tools": tools,
        "backend_used": backend_used,
        "counts": {
            "embedded_extracted": len([x for x in embedded if x.get("path")]),
            "pages_rasterized": len(pages),
            "kept_after_size_filter": len(kept),
            "dropped": len(dropped),
        },
        "kept": kept,
        "dropped": dropped,
        "next": [
            "Agent: review kept images for architecture-like structure",
            "Agent: emit 架构图分析结果 + redraw params",
            "Load docs/palettes.md for palette names only",
        ],
    }

    report_path = out_dir / "extract-report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if (backend_used or pages) else 1


if __name__ == "__main__":
    raise SystemExit(main())
