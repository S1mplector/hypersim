"""Shape information overlay for Pygame visualizations."""
from typing import List, Tuple, Optional, Dict, Any
import pygame
from .overlay import Overlay

class ShapeInfoOverlay(Overlay):
    """A specialized overlay for displaying information about 4D shapes.
    
    This class extends the base Overlay to provide common functionality
    for displaying information about 4D shapes like simplex, hypercube, etc.
    """
    
    # Common controls for 4D visualizations
    DEFAULT_CONTROLS = [
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
    
    def __init__(self, 
                screen: pygame.Surface,
                shape_name: str,
                shape: Any,
                font_size: int = 18,
                padding: int = 10,
                line_height: int = 24):
        """Initialize the shape info overlay.
        
        Args:
            screen: The pygame surface to render on
            shape_name: Display name of the shape (e.g., "4D Simplex")
            shape: The shape object (must have get_vertex_count, get_edge_count, etc.)
            font_size: Font size for text
            padding: Padding from screen edges in pixels
            line_height: Height between lines of text
        """
        super().__init__(screen, font_size, padding, line_height)
        self.shape_name = shape_name
        self.shape = shape
        self.additional_info = {}
    
    def add_additional_info(self, key: str, value: Any) -> None:
        """Add additional information to display in the overlay.
        
        Args:
            key: The label for the information
            value: The value to display
        """
        self.additional_info[key] = value
    
    def update(self) -> None:
        """Update the overlay with current shape information.
        
        This should be called each frame to update the displayed information.
        """
        # Clear previous lines
        self.lines = []
        
        # Add shape title and basic info
        self.add_line(f"{self.shape_name} - {self.shape.__class__.__name__}", 
                     (255, 200, 100), (40, 40, 60))
        
        # Add shape statistics if available
        if hasattr(self.shape, 'get_vertex_count'):
            stats = [
                ("Vertices", self.shape.get_vertex_count()),
                ("Edges", self.shape.get_edge_count()),
            ]
            
            # Add faces and cells if available
            if hasattr(self.shape, 'get_face_count'):
                stats.append(("Faces", self.shape.get_face_count()))
            if hasattr(self.shape, 'get_cell_count'):
                stats.append(("Cells", self.shape.get_cell_count()))
            
            # Add position if available
            if hasattr(self.shape, 'get_position'):
                pos = self.shape.get_position()
                if len(pos) >= 4:
                    stats.append(("Position", f"X:{pos[0]:.2f}, Y:{pos[1]:.2f}, Z:{pos[2]:.2f}, W:{pos[3]:.2f}"))
            
            # Add any additional info
            for key, value in self.additional_info.items():
                if callable(value):
                    value = value()
                stats.append((key, str(value)))
            
            # Add all stats to the overlay
            for label, value in stats:
                self.add_line(f"{label}: {value}", (200, 220, 255))
        
        # Add controls section
        self.add_line("\nControls:", (200, 200, 200))
        for action, key in self.DEFAULT_CONTROLS:
            self.add_line(f"{key: <15}{action}", (180, 180, 180))
