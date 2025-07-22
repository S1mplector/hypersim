"""Colour utilities for the Pygame renderer."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

__all__ = ["Color"]


@dataclass
class Color:
    """Simple RGBA colour helper compatible with Pygame."""

    r: int
    g: int
    b: int
    a: int = 255

    def to_tuple(self) -> Tuple[int, int, int, int]:
        """Return colour as a tuple recognised by Pygame."""
        return (self.r, self.g, self.b, self.a)
