"""Overlay rendering utilities for Pygame visualizations."""
import pygame
from typing import List, Tuple, Optional
from ..graphics.color import Color

class Overlay:
    """A class to handle rendering of UI overlays."""
    
    def __init__(self, 
                 screen: pygame.Surface, 
                 font_size: int = 18, 
                 padding: int = 10,
                 line_height: int = 24):
        """Initialize the overlay renderer.
        
        Args:
            screen: The pygame surface to render on
            font_size: Font size for text
            padding: Padding from screen edges in pixels
            line_height: Height between lines of text
        """
        self.screen = screen
        self.padding = padding
        self.line_height = line_height
        self.font = pygame.font.SysFont('Arial', font_size)
        self.lines: List[Tuple[str, Tuple[int, int, int], Optional[Tuple[int, int, int]]]] = []
    
    def add_line(self, 
                text: str, 
                color: Tuple[int, int, int] = (255, 255, 255),
                bg_color: Optional[Tuple[int, int, int]] = None) -> None:
        """Add a line of text to the overlay.
        
        Args:
            text: The text to display
            color: Text color as RGB tuple
            bg_color: Optional background color for this line
        """
        self.lines.append((text, color, bg_color))
    
    def add_controls(self, controls: List[Tuple[str, str]]) -> None:
        """Add control instructions to the overlay.
        
        Args:
            controls: List of (action, key) tuples
        """
        self.add_line("\nControls:", (200, 200, 200))
        for action, key in controls:
            self.add_line(f"{key: <15}{action}", (200, 200, 200))
    
    def add_position_info(self, position: Tuple[float, float, float, float]) -> None:
        """Add position information to the overlay.
        
        Args:
            position: 4D position as (x, y, z, w)
        """
        x, y, z, w = position
        self.add_line(f"Position: X:{x:6.2f} Y:{y:6.2f} Z:{z:6.2f} W:{w:6.2f}", (200, 255, 200))
    
    def add_shape_info(self, shape_name: str, vertex_count: int, edge_count: int) -> None:
        """Add shape information to the overlay.
        
        Args:
            shape_name: Name of the shape
            vertex_count: Number of vertices
            edge_count: Number of edges
        """
        self.add_line(f"\n{shape_name}:", (255, 255, 200))
        self.add_line(f"Vertices: {vertex_count}", (200, 200, 255))
        self.add_line(f"Edges: {edge_count}", (200, 200, 255))
    
    def draw(self) -> None:
        """Draw all overlay elements on the screen."""
        y = self.padding
        
        for text, color, bg_color in self.lines:
            if text == "":  # Empty line
                y += self.line_height // 2
                continue
                
            text_surface = self.font.render(text, True, color, bg_color)
            text_rect = text_surface.get_rect(topleft=(self.padding, y))
            
            # Draw background if specified
            if bg_color is not None:
                bg_rect = text_rect.inflate(10, 5)
                pygame.draw.rect(self.screen, bg_color, bg_rect, border_radius=3)
            
            self.screen.blit(text_surface, text_rect)
            y += self.line_height
        
        # Clear lines for next frame
        self.lines = []

# Common controls for 4D visualizations
DEFAULT_4D_CONTROLS = [
    ("Move X", "A/D"),
    ("Move Y", "Q/E"),
    ("Move Z", "W/S"),
    ("Move W", "R/F"),
    ("Rotate XY", "Left/Right"),
    ("Rotate XZ", "Up/Down"),
    ("4D Rotate XW", "Z/X"),
    ("4D Rotate YW", "C/V"),
    ("4D Rotate ZW", "B/N"),
    ("Quit", "ESC")
]
