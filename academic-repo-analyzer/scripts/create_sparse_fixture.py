#!/usr/bin/env python3
"""Create ref_repos/fixture-sparse: a minimal non-ML scientific repo (no model files, no train entry)."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "ref_repos" / "fixture-sparse"

README = "# Sparse Scientific Simulator\n\nToy N-body simulator used as a sparse-input fixture.\nNo neural networks, no training scripts.\n"
SIMULATE = '"""Entry point: python simulate.py --steps 100"""\nimport argparse\n\ndef main():\n    p = argparse.ArgumentParser()\n    p.add_argument("--steps", type=int, default=100)\n    a = p.parse_args()\n    print(f"simulated {a.steps} steps")\n\nif __name__ == "__main__":\n    main()\n'
LJ = '"""Lennard-Jones potential."""\n\ndef potential(r: float) -> float:\n    return 4 * (r ** -12 - r ** -6)\n'
INTEGRATOR = '"""Velocity-Verlet integrator."""\n\ndef step(positions, velocities, dt: float):\n    return [p + v * dt for p, v in zip(positions, velocities)], velocities\n'

def main() -> None:
    if ROOT.exists():
        shutil.rmtree(ROOT)
    (ROOT / "src").mkdir(parents=True)
    (ROOT / "README.md").write_text(README, encoding="utf-8")
    (ROOT / "simulate.py").write_text(SIMULATE, encoding="utf-8")
    (ROOT / "src" / "lennard_jones.py").write_text(LJ, encoding="utf-8")
    (ROOT / "src" / "integrator.py").write_text(INTEGRATOR, encoding="utf-8")
    print(f"fixture created: {ROOT}")

if __name__ == "__main__":
    main()
