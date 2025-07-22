"""Command-line interface for hypersim."""

import argparse
from typing import Any

# No simulation engine needed for simple demo
from hypersim.objects import Hypercube
from hypersim.visualization.renderers.pygame import PygameRenderer, Color


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
    cube = Hypercube(size=1.5)

    renderer = PygameRenderer(title="Tesseract Demo", background_color=Color(10, 10, 20))
    renderer.objects.append(cube)
    

    renderer.run()

__all__ = ["main"]
