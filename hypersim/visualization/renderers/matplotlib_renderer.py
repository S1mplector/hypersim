"""Matplotlib-based renderer for 4D objects."""
from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D

from hypersim.core.math_utils import perspective_projection_4d_to_3d


class MatplotlibRenderer:
    """A renderer for 4D objects using Matplotlib's 3D capabilities."""
    
    def __init__(self, figsize=(10, 8), distance: float = 5.0):
        """Initialize the renderer.
        
        Args:
            figsize: Figure size as (width, height) in inches
            distance: Distance for perspective projection
        """
        self.fig = plt.figure(figsize=figsize)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.distance = distance
        self.lines = []
        
        # Set up the plot
        self.ax.set_axis_off()
        self.ax.set_xlim([-1.5, 1.5])
        self.ax.set_ylim([-1.5, 1.5])
        self.ax.set_zlim([-1.5, 1.5])
    
    def add_hypercube(self, hypercube, color='b', alpha=0.6):
        """Add a hypercube to the scene.
        
        Args:
            hypercube: A Hypercube instance
            color: Line color
            alpha: Line alpha (transparency)
        """
        # Project 4D vertices to 3D
        vertices_3d = perspective_projection_4d_to_3d(
            hypercube.vertices, self.distance)
        
        # Create line objects for each edge
        for start_idx, end_idx in hypercube.edges:
            line, = self.ax.plot(
                [vertices_3d[start_idx, 0], vertices_3d[end_idx, 0]],
                [vertices_3d[start_idx, 1], vertices_3d[end_idx, 1]],
                [vertices_3d[start_idx, 2], vertices_3d[end_idx, 2]],
                '-', color=color, alpha=alpha
            )
            self.lines.append((line, (start_idx, end_idx)))
    
    def animate_rotation(self, frames: int = 360, interval: int = 50):
        """Animate rotation of the scene.
        
        Args:
            frames: Number of frames in the animation
            interval: Delay between frames in milliseconds
            
        Returns:
            The animation object
        """
        # Store original vertices for each line
        for line, (start_idx, end_idx) in self.lines:
            # For 3D lines in matplotlib, we can access the data directly
            # The line's data is stored in line._verts3d
            # We'll use the indices to reconstruct the 4D coordinates
            w1 = 1 if start_idx & 8 else -1
            z1 = 1 if start_idx & 4 else -1
            y1 = 1 if start_idx & 2 else -1
            x1 = 1 if start_idx & 1 else -1
            
            w2 = 1 if end_idx & 8 else -1
            z2 = 1 if end_idx & 4 else -1
            y2 = 1 if end_idx & 2 else -1
            x2 = 1 if end_idx & 1 else -1
            
            # Scale by the hypercube size (assuming it's the same for all dimensions)
            scale = 0.5  # Since we're using -1 to 1 range
            line._original_vertices = np.array([
                [x1 * scale, y1 * scale, z1 * scale, w1 * scale],
                [x2 * scale, y2 * scale, z2 * scale, w2 * scale]
            ])
        
        def update(frame):
            # Rotate in XY and ZW planes
            angle_xy = np.radians(frame)
            angle_zw = np.radians(frame * 0.7)  # Different rotation speed for more interesting motion
            
            # Update all lines in the scene
            for line, _ in self.lines:
                # Apply 4D rotation
                from hypersim.core.math_utils import rotation_matrix_4d
                rot_xy = rotation_matrix_4d(0, 1, angle_xy)
                rot_zw = rotation_matrix_4d(2, 3, angle_zw)
                rotation = rot_xy @ rot_zw
                
                # Apply rotation to original vertices and project to 3D
                rotated = np.dot(line._original_vertices, rotation.T)
                projected = perspective_projection_4d_to_3d(rotated, self.distance)
                
                # Update line data
                line.set_data(projected[:, 0], projected[:, 1])
                line.set_3d_properties(projected[:, 2])
            
            # Rotate the view for better visualization
            self.ax.view_init(elev=20, azim=frame/2)
            return [line for line, _ in self.lines]
        
        # Create and return the animation
        ani = FuncAnimation(
            self.fig, update, frames=frames, interval=interval, blit=False)
        
        # Make sure we keep a reference to the animation to prevent it from being garbage collected
        self._animation = ani
        return ani
    
    def show(self):
        """Display the plot."""
        plt.tight_layout()
        plt.show()
