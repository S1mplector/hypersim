"""16-cell (hyperoctahedron) implementation."""
import numpy as np
from typing import List, Tuple, Optional

from ..core.math_4d import create_rotation_matrix_4d

class SixteenCell:
    """A 16-cell (4D hyperoctahedron) implementation.
    
    The 16-cell is the 4D analog of the octahedron, with 8 vertices and 24 edges.
    It's one of the six convex regular 4-polytopes.
    """
    
    def __init__(self, size: float = 1.0):
        """Initialize a 16-cell with the given size.
        
        Args:
            size: The size (edge length) of the 16-cell
        """
        self.size = size
        self.position = np.zeros(4, dtype=np.float32)
        self.transform = np.eye(4, dtype=np.float32)
        
        # Define the 8 vertices of a 16-cell (all permutations of (±1, 0, 0, 0))
        self._base_vertices = np.array([
            [1, 0, 0, 0], [-1, 0, 0, 0],  # ±x
            [0, 1, 0, 0], [0, -1, 0, 0],  # ±y
            [0, 0, 1, 0], [0, 0, -1, 0],  # ±z
            [0, 0, 0, 1], [0, 0, 0, -1]   # ±w
        ], dtype=np.float32) * (size / 2.0)
        
        # Define edges (each vertex connects to all others except its opposite)
        self.edges = [
            (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),  # From +x
            (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),  # From -x
            (2, 4), (2, 5), (2, 6), (2, 7),                  # From +y
            (3, 4), (3, 5), (3, 6), (3, 7),                  # From -y
            (4, 6), (4, 7),                                  # From +z
            (5, 6), (5, 7),                                  # From -z
            # Note: The last edge (6,7) would connect the two W-axis vertices, but they don't connect in a 16-cell
        ]
        
        # Define triangular faces (8 regular octahedra)
        self.faces = [
            # Faces in the 3D subspaces (8 octahedra)
            (0, 2, 4), (0, 2, 5), (0, 3, 4), (0, 3, 5),  # +x octahedron
            (1, 2, 4), (1, 2, 5), (1, 3, 4), (1, 3, 5),  # -x octahedron
            (0, 2, 6), (0, 2, 7), (0, 3, 6), (0, 3, 7),  # +y octahedron
            (1, 2, 6), (1, 2, 7), (1, 3, 6), (1, 3, 7),  # -y octahedron
            (0, 4, 6), (0, 4, 7), (0, 5, 6), (0, 5, 7),  # +z octahedron
            (1, 4, 6), (1, 4, 7), (1, 5, 6), (1, 5, 7),  # -z octahedron
            (2, 4, 6), (2, 4, 7), (2, 5, 6), (2, 5, 7),  # +w octahedron
            (3, 4, 6), (3, 4, 7), (3, 5, 6), (3, 5, 7)   # -w octahedron
        ]
        
        # Define cells (24 octahedra)
        self.cells = [
            # Each cell is an octahedron formed by 6 vertices
            (0, 1, 2, 3, 4, 5),  # XY plane
            (0, 1, 2, 3, 6, 7),  # XW plane
            (0, 1, 4, 5, 6, 7),  # XZ plane
            (2, 3, 4, 5, 6, 7),  # YZW space
            (0, 2, 4, 6, 1, 3),  # XYW space
            (0, 2, 5, 7, 1, 3),  # XYW space (other diagonal)
            (0, 3, 4, 7, 1, 2),  # XZW space
            (0, 3, 5, 6, 1, 2)   # XZW space (other diagonal)
        ]
    
    def set_position(self, position) -> None:
        """Set the position of the 16-cell.
        
        Args:
            position: 4D position as [x, y, z, w] or (x, y, z, w)
        """
        self.position = np.array(position, dtype=np.float32)
    
    def rotate(self, 
              angle_xy: float = 0.0, 
              angle_xz: float = 0.0, 
              angle_yz: float = 0.0,
              angle_xw: float = 0.0,
              angle_yw: float = 0.0,
              angle_zw: float = 0.0) -> None:
        """Rotate the 16-cell in 4D space.
        
        Args:
            angle_xy: Rotation angle in the XY plane (radians)
            angle_xz: Rotation angle in the XZ plane (radians)
            angle_yz: Rotation angle in the YZ plane (radians)
            angle_xw: 4D rotation angle in the XW plane (radians)
            angle_yw: 4D rotation angle in the YW plane (radians)
            angle_zw: 4D rotation angle in the ZW plane (radians)
        """
        if angle_xy != 0:
            rotation = create_rotation_matrix_4d(angle_xy=angle_xy)
            self.transform = rotation @ self.transform
            
        if angle_xz != 0:
            rotation = create_rotation_matrix_4d(angle_xz=angle_xz)
            self.transform = rotation @ self.transform
            
        if angle_yz != 0:
            rotation = create_rotation_matrix_4d(angle_yz=angle_yz)
            self.transform = rotation @ self.transform
            
        if angle_xw != 0:
            rotation = create_rotation_matrix_4d(angle_xw=angle_xw)
            self.transform = rotation @ self.transform
            
        if angle_yw != 0:
            rotation = create_rotation_matrix_4d(angle_yw=angle_yw)
            self.transform = rotation @ self.transform
            
        if angle_zw != 0:
            rotation = create_rotation_matrix_4d(angle_zw=angle_zw)
            self.transform = rotation @ self.transform
    
    def get_transformed_vertices(self) -> np.ndarray:
        """Get the vertices after applying transformations and position offset.
        
        Returns:
            Array of shape (8, 4) containing the transformed vertex coordinates
        """
        # Apply transformation matrix to base vertices
        transformed = (self.transform @ self._base_vertices.T).T
        
        # Add position offset
        transformed += self.position
        
        return transformed
    
    def update(self, dt: float) -> None:
        """Update the 16-cell (can be used for animations).
        
        Args:
            dt: Delta time since last update
        """
        # Apply a gentle rotation for visual interest
        self.rotate(angle_xy=0.3 * dt, angle_zw=0.2 * dt, angle_yw=0.1 * dt)
    
    @property
    def vertices(self) -> np.ndarray:
        """Get the current transformed vertices."""
        return self.get_transformed_vertices()
    
    def get_vertex_count(self) -> int:
        """Get the number of vertices in the 16-cell."""
        return 8
    
    def get_edge_count(self) -> int:
        """Get the number of edges in the 16-cell."""
        return 24
    
    def get_face_count(self) -> int:
        """Get the number of triangular faces in the 16-cell."""
        return 32
    
    def get_cell_count(self) -> int:
        """Get the number of tetrahedral cells in the 16-cell."""
        return 8
