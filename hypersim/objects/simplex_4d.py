"""4D Simplex (5-cell) implementation.

The 4D simplex is the simplest 4D polytope, analogous to how a triangle is the simplest 2D polygon
and a tetrahedron is the simplest 3D polyhedron. It has 5 vertices, 10 edges, 10 triangular faces,
and 5 tetrahedral cells.
"""
from __future__ import annotations

import numpy as np
from typing import List, Tuple
from hypersim.core.math_4d import Vector4D, create_vector_4d, create_rotation_matrix_4d


class Simplex4D:
    """A 4D simplex (5-cell) - the simplest 4D polytope."""
    
    def __init__(self, size: float = 1.0):
        """Initialize a 4D simplex.
        
        Args:
            size: The scale of the simplex
        """
        self.size = size
        self.position = create_vector_4d(0, 0, 0, 0)
        self.transform = np.eye(4)
        
        # Create the 5 vertices of a regular 4D simplex
        # Using coordinates that form a regular simplex in 4D space
        sqrt5 = np.sqrt(5)
        sqrt10 = np.sqrt(10)
        
        # These coordinates create a regular 4D simplex centered at origin
        self._base_vertices = np.array([
            [1, 1, 1, -1/sqrt5],
            [1, -1, -1, -1/sqrt5], 
            [-1, 1, -1, -1/sqrt5],
            [-1, -1, 1, -1/sqrt5],
            [0, 0, 0, 4/sqrt5]
        ]) * size
        
        # Define the edges (connections between vertices)
        # In a 4D simplex, every vertex connects to every other vertex
        self.edges = []
        for i in range(5):
            for j in range(i + 1, 5):
                self.edges.append((i, j))
        
        # Define the triangular faces (3 vertices each)
        # Each face is formed by 3 vertices
        self.faces = []
        for i in range(5):
            for j in range(i + 1, 5):
                for k in range(j + 1, 5):
                    self.faces.append((i, j, k))
        
        # Define the tetrahedral cells (4 vertices each)
        # Each cell is formed by 4 vertices
        self.cells = []
        for i in range(5):
            for j in range(i + 1, 5):
                for k in range(j + 1, 5):
                    for l in range(k + 1, 5):
                        self.cells.append((i, j, k, l))
    
    def set_position(self, position: List[float]) -> None:
        """Set the position of the simplex in 4D space."""
        self.position = create_vector_4d(*position)
    
    def rotate(self, angle_xy: float = 0, angle_xz: float = 0, angle_xw: float = 0,
               angle_yz: float = 0, angle_yw: float = 0, angle_zw: float = 0) -> None:
        """Apply rotations in various 4D planes.
        
        Args:
            angle_xy: Rotation angle in XY plane (radians)
            angle_xz: Rotation angle in XZ plane (radians)  
            angle_xw: Rotation angle in XW plane (radians)
            angle_yz: Rotation angle in YZ plane (radians)
            angle_yw: Rotation angle in YW plane (radians)
            angle_zw: Rotation angle in ZW plane (radians)
        """
        if angle_xy != 0:
            rotation = create_rotation_matrix_4d(angle_xy=angle_xy)
            self.transform = rotation @ self.transform
            
        if angle_xz != 0:
            rotation = create_rotation_matrix_4d(angle_xz=angle_xz)
            self.transform = rotation @ self.transform
            
        if angle_xw != 0:
            rotation = create_rotation_matrix_4d(angle_xw=angle_xw)
            self.transform = rotation @ self.transform
            
        if angle_yz != 0:
            rotation = create_rotation_matrix_4d(angle_yz=angle_yz)
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
            Array of shape (5, 4) containing the transformed vertex coordinates
        """
        # Apply transformation matrix to base vertices
        transformed = (self.transform @ self._base_vertices.T).T
        
        # Add position offset
        transformed += self.position  # position is already a numpy array
        
        return transformed
    
    def update(self, dt: float) -> None:
        """Update the simplex (can be used for animations).
        
        Args:
            dt: Delta time since last update
        """
        # Apply a gentle rotation for visual interest
        self.rotate(angle_xy=0.5 * dt, angle_xw=0.3 * dt, angle_zw=0.2 * dt)
    
    @property
    def vertices(self) -> np.ndarray:
        """Get the current transformed vertices."""
        return self.get_transformed_vertices()
    
    def get_vertex_count(self) -> int:
        """Get the number of vertices in the simplex."""
        return 5
    
    def get_edge_count(self) -> int:
        """Get the number of edges in the simplex."""
        return len(self.edges)
    
    def get_face_count(self) -> int:
        """Get the number of triangular faces in the simplex."""
        return len(self.faces)
    
    def get_cell_count(self) -> int:
        """Get the number of tetrahedral cells in the simplex."""
        return len(self.cells)
