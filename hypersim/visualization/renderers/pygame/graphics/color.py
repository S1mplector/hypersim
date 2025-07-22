"""Color utilities for the Pygame renderer.

This module provides the Color class which is used throughout the renderer
for consistent color handling and conversion to Pygame-compatible formats.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

__all__ = ["Color"]


@dataclass
class Color:
    """Simple RGBA color helper compatible with Pygame.
    
    This class provides a convenient way to work with colors in the renderer,
    with easy conversion to Pygame's native color format.
    
    Attributes:
        r: Red component (0-255)
        g: Green component (0-255)
        b: Blue component (0-255)
        a: Alpha component (0-255, default: 255)
    """
    r: int
    g: int
    b: int
    a: int = 255

    def to_tuple(self) -> Tuple[int, int, int, int]:
        """Convert the color to a tuple recognized by Pygame.
        
        Returns:
            A 4-tuple of (r, g, b, a) with values in the range 0-255.
        """
        return (self.r, self.g, self.b, self.a)
    
    @classmethod
    def from_hex(cls, hex_color: str, alpha: int = 255) -> 'Color':
        """Create a Color instance from a hex color string.
        
        Args:
            hex_color: A hex color string (e.g., "#RRGGBB" or "#RRGGBBAA")
            alpha: Alpha value (0-255) if not specified in the hex string
            
        Returns:
            A new Color instance.
            
        Raises:
            ValueError: If the hex string is invalid.
        """
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return cls(r, g, b, alpha)
        elif len(hex_color) == 8:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            a = int(hex_color[6:8], 16)
            return cls(r, g, b, a)
        else:
            raise ValueError(f"Invalid hex color string: {hex_color}")
