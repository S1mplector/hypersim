"""Input event handlers for the Pygame renderer.

This module provides classes and functions for handling user input events
like keyboard and mouse input.
"""

from __future__ import annotations

import pygame
from typing import Callable, Dict, Any, Optional

from ..core.camera import Camera

__all__ = ["InputHandler"]


class InputHandler:
    """Handles user input events and delegates them to appropriate handlers.
    
    This class manages the mapping of input events to their respective
    handler functions and processes events each frame.
    """
    
    def __init__(self, camera: Camera) -> None:
        """Initialize the input handler with a camera to control.
        
        Args:
            camera: The camera instance to control with input
        """
        self.camera = camera
        self.running = True
        self._key_handlers: Dict[int, Callable[[], None]] = {
            pygame.K_ESCAPE: self._handle_quit
        }
        self._mouse_handlers: Dict[int, Callable[[pygame.event.Event], None]] = {
            pygame.MOUSEBUTTONDOWN: self._handle_mouse_down,
            pygame.MOUSEBUTTONUP: self._handle_mouse_up,
            pygame.MOUSEMOTION: self._handle_mouse_motion
        }
    
    def handle_events(self) -> bool:
        """Process all pending events.
        
        Returns:
            bool: True if the application should continue running, False if it should quit
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # Handle keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key in self._key_handlers:
                    self._key_handlers[event.key]()
                else:
                    self.camera.handle_key_press(event.key)
            
            # Handle mouse events
            if event.type in self._mouse_handlers:
                self._mouse_handlers[event.type](event)
        
        return self.running
    
    def _handle_quit(self) -> None:
        """Handle the quit event (e.g., pressing Escape)."""
        self.running = False
    
    def _handle_mouse_down(self, event: pygame.event.Event) -> None:
        """Handle mouse button press events."""
        if event.button == 1:  # Left mouse button
            self.camera.is_rotating = True
            self.camera.last_mouse_pos = event.pos
    
    def _handle_mouse_up(self, event: pygame.event.Event) -> None:
        """Handle mouse button release events."""
        if event.button == 1:  # Left mouse button
            self.camera.is_rotating = False
    
    def _handle_mouse_motion(self, event: pygame.event.Event) -> None:
        """Handle mouse movement events."""
        if not self.camera.is_rotating:
            return
            
        dx = event.pos[0] - self.camera.last_mouse_pos[0]
        dy = event.pos[1] - self.camera.last_mouse_pos[1]
        self.camera.handle_mouse_motion(dx, dy)
        self.camera.last_mouse_pos = event.pos
    
    def register_key_handler(self, key: int, handler: Callable[[], None]) -> None:
        """Register a custom key handler.
        
        Args:
            key: Pygame key constant
            handler: Function to call when the key is pressed
        """
        self._key_handlers[key] = handler
    
    def register_mouse_handler(
        self, 
        event_type: int, 
        handler: Callable[[pygame.event.Event], None]
    ) -> None:
        """Register a custom mouse event handler.
        
        Args:
            event_type: Pygame event type (e.g., pygame.MOUSEBUTTONDOWN)
            handler: Function to call when the event occurs
        """
        self._mouse_handlers[event_type] = handler
