"""Pygame renderer package – public surface only.

Re-exports the public classes so external code can simply do::

    from hypersim.visualization.renderers.pygame import PygameRenderer, Color

The full implementation lives in ``renderer.py`` and ``color.py`` modules.
"""

from __future__ import annotations

from .color import Color
from .renderer import PygameRenderer

__all__: list[str] = [
    "Color",
    "PygameRenderer",
]
