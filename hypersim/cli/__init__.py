"""Command-line interface for hypersim."""

import argparse
from typing import Any

from hypersim.engine.scene import Scene
from hypersim.engine.simulation import Simulation
from hypersim.objects import Hypercube
from hypersim.visualization import MatplotlibRenderer


def main(argv: list[str] | None = None) -> None:
    """Entry point for `python -m hypersim.cli` or `hypersim` console script."""
    parser = argparse.ArgumentParser(description="Run hypersim demos")
    parser.add_argument(
        "--demo",
        choices=["tesseract"],
        default="tesseract",
        help="Which built-in demo to run",
    )
    args = parser.parse_args(argv)

    if args.demo == "tesseract":
        _run_tesseract_demo()
    else:
        parser.error(f"Unknown demo: {args.demo}")


def _run_tesseract_demo() -> None:
    """Run the basic tesseract visualization using the internal architecture."""
    scene = Scene()
    cube = Hypercube(size=1.5)
    scene.add(cube)

    renderer = MatplotlibRenderer()
    renderer.add_hypercube(cube)
    renderer.animate_rotation()

    sim = Simulation(scene, tick=1 / 60)
    sim.set_step_callback(lambda dt: None)  # no-op for now
    # Run simulation for demo purposes in a blocking manner via matplotlib show
    renderer.show()

__all__ = ["main"]
