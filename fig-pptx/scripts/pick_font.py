#!/usr/bin/env python3
"""Pick an installed font that matches the figure's lettering.

Does not fall back to another style. A comic figure stays on a comic family.
"""

from __future__ import annotations

import argparse
import subprocess
import sys

# First installed name wins. Order is the preference for that lettering.
COMIC_PACKAGE = "fonts-comic-neue"
STYLES = {
    "comic": ["Comic Neue"],
    "hand": ["Patrick Hand", "Caveat", "Comic Neue"],
    "technical": ["Liberation Sans", "DejaVu Sans", "Noto Sans CJK SC"],
    "serif": ["Liberation Serif", "DejaVu Serif"],
}


def installed_families():
    try:
        raw = subprocess.check_output(["fc-list", ":", "family"], text=True, errors="replace")
    except FileNotFoundError:
        sys.exit("需要 fontconfig 的 fc-list 才能核对字体。")
    fams = []
    seen = set()
    for line in raw.splitlines():
        for part in line.split(","):
            part = part.strip()
            key = part.lower()
            if part and key not in seen:
                seen.add(key)
                fams.append(part)
    return fams


def choose(style: str, families: list[str]) -> str:
    names = STYLES.get(style)
    if names is None:
        sys.exit(f"未知风格 {style}。可用: {', '.join(STYLES)}")
    have = {name.lower(): name for name in families}
    for name in names:
        if name.lower() in have:
            return have[name.lower()]
    wanted = "、".join(names)
    installed = "\n".join(families)
    sys.exit(f"风格 {style} 需要这些字体之一: {wanted}\n已安装字体:\n{installed}")


def install_comic():
    subprocess.check_call(["sudo", "apt-get", "install", "-y", COMIC_PACKAGE])


def self_check():
    assert choose("comic", ["Liberation Sans", "Comic Neue"]) == "Comic Neue"
    assert choose("technical", ["DejaVu Sans"]) == "DejaVu Sans"
    try:
        choose("comic", ["Liberation Sans"])
    except SystemExit as exc:
        assert "Comic Neue" in str(exc)
    else:
        raise AssertionError("comic must not fall back to a sans")
    print("self-check ok")


def main(argv):
    parser = argparse.ArgumentParser(description="按画面字选已安装字体")
    parser.add_argument("--style", choices=sorted(STYLES))
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args(argv)
    if args.self_check:
        self_check()
        return
    if not args.style:
        sys.exit("用法: pick_font.py --style comic|hand|technical|serif")
    families = installed_families()
    if args.style == "comic" and "comic neue" not in {name.lower() for name in families}:
        install_comic()
        families = installed_families()
    print(choose(args.style, families))


if __name__ == "__main__":
    main(sys.argv[1:])
