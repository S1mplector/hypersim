"""Main renderer implementation for the Pygame backend.

This module provides the PygameRenderer class which is the main entry point
for rendering 3D/4D graphics using Pygame.
"""

from __future__ import annotations

import pygame
import numpy as np
from typing import Any, Optional, List

from ..graphics.color import Color
from ..graphics.scene.scene import Scene, Renderable
from .camera import Camera
from ..input.handlers import InputHandler

__all__ = ["PygameRenderer"]


class PygameRenderer:
    """Main renderer class for 3D/4D graphics using Pygame.
    
    This class manages the rendering window, camera, scene, and input handling.
    It provides a simple interface for creating interactive 3D/4D visualizations.
    """
    
    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        title: str = "4D Renderer",
        background_color: Optional[Color] = None,
        distance: float = 5.0,
    ) -> None:
        """Initialize the Pygame renderer.
        
        Args:
            width: Window width in pixels
            height: Window height in pixels
            title: Window title
            background_color: Background color (default: black)
            distance: Distance to the near clipping plane
        """
        if background_color is None:
            background_color = Color(0, 0, 0)
        
        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
        
        # Set up camera
        self.camera = Camera(width, height, distance=distance)
        
        # Set up input handling
        self.input_handler = InputHandler(self.camera)
        
        # Set up scene
        self.scene = Scene(background_color)
        self.scene.zbuffer = np.ones((width, height), dtype=np.float32) * float("inf")
        
        # Performance metrics
        self.clock = pygame.time.Clock()
        self.fps = 0.0
        self.frame_count = 0
        self.last_fps_update = pygame.time.get_ticks()
    
    def clear(self) -> None:
        """Clear the screen and z-buffer."""
        self.screen.fill(self.scene.background_color.to_tuple())
        if self.scene.zbuffer is not None:
            self.scene.zbuffer.fill(float("inf"))
    
    def add_object(self, obj: Renderable) -> None:
        """Add a renderable object to the scene.
        
        Args:
            obj: Object to add (must implement the Renderable protocol)
        """
        self.scene.add_object(obj)
    
    def remove_object(self, obj: Renderable) -> None:
        """Remove a renderable object from the scene.
        
        Args:
            obj: Object to remove
        """
        self.scene.remove_object(obj)
    
    def clear_scene(self) -> None:
        """Remove all objects from the scene."""
        self.scene.clear()
    
    def update(self, dt: float) -> None:
        """Update the scene and all objects.
        
        Args:
            dt: Time since last update in seconds
        """
        self.scene.update(dt)
        
        # Update FPS counter
        self.frame_count += 1
        now = pygame.time.get_ticks()
        if now - self.last_fps_update > 1000:  # Update FPS every second
            self.fps = self.frame_count * 1000.0 / (now - self.last_fps_update)
            self.frame_count = 0
            self.last_fps_update = now
    
    def render(self) -> None:
        """Render the current scene."""
        self.scene.render(self)
        pygame.display.flip()
    
    def run(self, target_fps: int = 60) -> None:
        """Run the main render loop.
        
        Args:
            target_fps: Target frames per second
        """
        running = True
        last_time = pygame.time.get_ticks() / 1000.0
        
        while running:
            # Calculate delta time
            current_time = pygame.time.get_ticks() / 1000.0
            dt = current_time - last_time
            last_time = current_time
            
            # Handle input
            running = self.input_handler.handle_events()
            
            # Update and render
            self.update(dt)
            self.render()
            
            # Cap the frame rate
            self.clock.tick(target_fps)
        
        # Clean up
        pygame.quit()
    
    # Convenience methods for common operations
    def draw_line_4d(
        self, 
        start: Vector4D, 
        end: Vector4D, 
        color: Color, 
        width: int = 1
    ) -> None:
        """Draw a 4D line.
        
        Args:
            start: Start point in 4D space
            end: End point in 4D space
            color: Line color
            width: Line width in pixels
        """
        from ..graphics.primitives.lines import draw_line_4d as draw_line
        draw_line(
            self.screen, 
            start, 
            end, 
            color, 
            width, 
            camera=self.camera, 
            zbuffer=self.scene.zbuffer
        )
    
    def render_hypercube(
        self, 
        hypercube: Any, 
        color: Color = Color(0, 255, 0), 
        width: int = 1
    ) -> None:
        """Render a hypercube.
        
        Args:
            hypercube: Hypercube object with 'edges' and 'vertices' attributes
            color: Edge color
            width: Line width in pixels
        """
        transform = getattr(hypercube, "transform", np.eye(4, dtype=np.float32))
        for a, b in hypercube.edges:
            start = transform @ hypercube.vertices[a]
            end = transform @ hypercube.vertices[b]
            self.draw_line_4d(start, end, color, width)

    def render_simplex(
        self,
        simplex: Any,
        color: Color = Color(255, 140, 0),
        width: int = 1,
    ) -> None:
        """Render a 4-D simplex (5-cell)."""
        verts = simplex.get_transformed_vertices()
        for a, b in simplex.edges:
            self.draw_line_4d(verts[a], verts[b], color, width)

    def render_4d_object(
        self,
        obj: Any,
        color: Color = Color(0, 255, 255),
        width: int = 1,
    ) -> None:
        """Generic renderer for any polytope with `edges` and `get_transformed_vertices()`."""
        verts = obj.get_transformed_vertices()
        for a, b in obj.edges:
            self.draw_line_4d(verts[a], verts[b], color, width)
