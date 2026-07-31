#!/usr/bin/env python3
"""Shallow-clone benchmark repos into git-ignored ref_repos/.

Usage:
  python3 fetch_benchmark_repos.py --manifest ../../examples/benchmarks/manifest.json
  python3 fetch_benchmark_repos.py --manifest <path> --repos nanogpt esm --clean
"""
import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def run_git(args, cwd=None):
    return subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--repos", nargs="+", default=None, help="subset of repo ids")
    parser.add_argument(
        "--clean", action="store_true", help="delete existing target dirs first"
    )
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    data = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    out = root / data["clone_root"]
    out.mkdir(parents=True, exist_ok=True)
    wanted = set(args.repos) if args.repos else None
    results = []
    ok = True
    for repo in data["repos"]:
        if wanted and repo["id"] not in wanted:
            continue
        dest = out / repo["id"]
        if args.clean and dest.exists():
            shutil.rmtree(dest)
        cloned = not dest.exists()
        if cloned:
            clone = run_git(
                [
                    "clone",
                    "--depth",
                    "1",
                    "--filter=blob:none",
                    repo["url"],
                    str(dest),
                ]
            )
            if clone.returncode != 0:
                print(
                    f"clone FAILED {repo['id']}: {clone.stderr.strip()}",
                    file=sys.stderr,
                )
                results.append({"id": repo["id"], "ok": False})
                ok = False
                continue
        head = run_git(["rev-parse", "HEAD"], cwd=dest)
        commit = head.stdout.strip()
        print(f"{repo['id']}: {'cloned' if cloned else 'existing'} @ {commit}")
        results.append(
            {"id": repo["id"], "ok": head.returncode == 0, "commit": commit}
        )
        ok = ok and head.returncode == 0
    log = out / "fetch-log.json"
    log.write_text(
        json.dumps(
            {
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "manifest": str(args.manifest),
                "results": results,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"fetch-log: {log}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
