"""Line drawing primitives for the Pygame renderer.

This module provides functions for drawing various types of lines and curves.
"""

from __future__ import annotations

from typing import Tuple

import numpy as np
import pygame

from hypersim.core.math_4d import Vector4D
from ...graphics.color import Color

__all__ = ["draw_line_4d"]


def draw_line_4d(
    surface: pygame.Surface,
    start: Vector4D,
    end: Vector4D,
    color: Color,
    width: int = 1,
    camera: Any = None,
    zbuffer: Optional[np.ndarray] = None
) -> None:
    """Draw a 4D line on the given surface.
    
    Args:
        surface: The surface to draw on
        start: Start point in 4D space
        end: End point in 4D space
        color: Color of the line
        width: Width of the line in pixels
        camera: Camera instance for projection (must have project_4d_to_2d method)
        zbuffer: Z-buffer for depth testing (optional)
    """
    if camera is None:
        raise ValueError("Camera instance is required for 4D projection")
    
    # Project 4D points to 2D screen space
    x1, y1, z1 = camera.project_4d_to_2d(start)
    x2, y2, z2 = camera.project_4d_to_2d(end)
    
    # Skip drawing if both points are behind the camera
    if z1 > 5 and z2 > 5:
        return
    
    # Clip line if it crosses the near plane
    if z1 > 0 and z2 < 0:
        # Line crosses from behind to in front of camera
        t = -z1 / (z2 - z1) if (z2 - z1) != 0 else 0.0
        x1 = x1 + t * (x2 - x1)
        y1 = y1 + t * (y2 - y1)
        z1 = 0
    elif z1 < 0 and z2 > 0:
        # Line crosses from in front to behind camera
        t = -z2 / (z1 - z2) if (z1 - z2) != 0 else 0.0
        x2 = x2 + t * (x1 - x2)
        y2 = y2 + t * (y1 - y2)
        z2 = 0
    
    # Skip if line is completely outside the viewport
    if ((x1 < 0 and x2 < 0) or (x1 > surface.get_width() and x2 > surface.get_width()) or
        (y1 < 0 and y2 < 0) or (y1 > surface.get_height() and y2 > surface.get_height())):
        return
    
    # Simple z-buffering (if provided)
    if zbuffer is not None:
        # For simplicity, we'll just use the midpoint depth
        z = (z1 + z2) / 2
        # Cast midpoint coordinates to integers for safe NumPy indexing
        x = int((x1 + x2) // 2)
        y = int((y1 + y2) // 2)
        
        # Skip if there's a closer pixel in the z-buffer
        if (0 <= x < zbuffer.shape[0] and 0 <= y < zbuffer.shape[1] and 
            z > zbuffer[x, y]):
            return
        
        # Update z-buffer (simplified)
        if 0 <= x < zbuffer.shape[0] and 0 <= y < zbuffer.shape[1]:
            zbuffer[x, y] = z
    
    # Draw the line
    pygame.draw.line(
        surface, 
        color.to_tuple(), 
        (int(x1), int(y1)), 
        (int(x2), int(y2)), 
        width
    )
