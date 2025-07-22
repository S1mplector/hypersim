"""4D Simplex (5-cell) implementation.

The 4D simplex is the simplest 4D polytope, analogous to how a triangle is the simplest 2D polygon
and a tetrahedron is the simplest 3D polyhedron. It has 5 vertices, 10 edges, 10 triangular faces,
and 5 tetrahedral cells.
"""
from __future__ import annotations

import numpy as np
from typing import List, Tuple, Dict, Any
from dataclasses import field
from hypersim.core.math_4d import Vector4D, Matrix4D, create_vector_4d
from hypersim.core.shape_4d import Shape4D

class Simplex4D(Shape4D):
    """A 4D simplex (5-cell) - the simplest 4D polytope."""
    
    def __init__(self, size: float = 1.0, **kwargs):
        """Initialize a 4D simplex.
        
        Args:
            size: The scale of the simplex
            **kwargs: Additional arguments to pass to Shape4D
        """
        super().__init__(**kwargs)
        self.size = size
        
        # Create the 5 vertices of a regular 4D simplex
        # Using coordinates that form a regular simplex in 4D space
        sqrt5 = np.sqrt(5)
        
        # These coordinates create a regular 4D simplex centered at origin
        self._base_vertices = [
            np.array([1, 1, 1, -1/sqrt5], dtype=np.float32),
            np.array([1, -1, -1, -1/sqrt5], dtype=np.float32), 
            np.array([-1, 1, -1, -1/sqrt5], dtype=np.float32),
            np.array([-1, -1, 1, -1/sqrt5], dtype=np.float32),
            np.array([0, 0, 0, 4/sqrt5], dtype=np.float32)
        ]
        
        # Scale the vertices
        self._base_vertices = [v * size for v in self._base_vertices]
        
        # Define the edges (connections between vertices)
        # In a 4D simplex, every vertex connects to every other vertex
        self._edges = []
        for i in range(5):
            for j in range(i + 1, 5):
                self._edges.append((i, j))
        
        # Define the triangular faces (3 vertices each)
        # Each face is formed by 3 vertices
        self._faces = []
        for i in range(5):
            for j in range(i + 1, 5):
                for k in range(j + 1, 5):
                    self._faces.append((i, j, k))
        
        # Define the tetrahedral cells (4 vertices each)
        # Each cell is formed by 4 vertices
        self._cells = []
        for i in range(5):
            for j in range(i + 1, 5):
                for k in range(j + 1, 5):
                    for l in range(k + 1, 5):
                        self._cells.append((i, j, k, l))
    
    @property
    def vertices(self) -> List[Vector4D]:
        """Get the vertices of the simplex in local space."""
        return self._base_vertices
    
    @property
    def edges(self) -> List[Tuple[int, int]]:
        """Get the edges of the simplex as vertex index pairs."""
        return self._edges
    
    @property
    def faces(self) -> List[Tuple[int, ...]]:
        """Get the faces of the simplex as tuples of vertex indices."""
        return self._faces
    
    @property
    def cells(self) -> List[Tuple[int, int, int, int]]:
        """Get the tetrahedral cells of the simplex as tuples of 4 vertex indices."""
        return self._cells
        
    def get_transformed_vertices(self) -> np.ndarray:
        """Get the vertices after applying transformations and position offset.
        
        Returns:
            Array of shape (5, 4) containing the transformed vertex coordinates
        """
        # Get transformed vertices from parent class and convert to numpy array
        transformed_verts = super().get_transformed_vertices()
        return np.array(transformed_verts, dtype=np.float32)
    
    def update(self, dt: float) -> None:
        """Update the simplex (can be used for animations).
        
        Args:
            dt: Delta time since last update
        """
        # Apply a gentle rotation for visual interest
        self.rotate(xy=0.5 * dt, xw=0.3 * dt, zw=0.2 * dt)
