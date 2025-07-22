"""Implementation of a 4D hypercube (tesseract)."""
import numpy as np
from typing import List, Tuple


class Hypercube:
    """A 4D hypercube (tesseract) implementation.
    
    This class represents a 4D hypercube with methods for generating its vertices,
    edges, and performing 4D transformations.
    """
    
    def __init__(self, size: float = 1.0):
        """Initialize a hypercube with the given size.
        
        Args:
            size: The length of each edge of the hypercube.
        """
        self.size = size
        self._vertices = self._generate_vertices()
        self._edges = self._generate_edges()
    
    def _generate_vertices(self) -> np.ndarray:
        """Generate the 16 vertices of the hypercube."""
        vertices = []
        for w in [-1, 1]:
            for z in [-1, 1]:
                for y in [-1, 1]:
                    for x in [-1, 1]:
                        vertices.append([x, y, z, w])
        return (self.size / 2) * np.array(vertices)
    
    def _generate_edges(self) -> List[Tuple[int, int]]:
        """Generate the 32 edges of the hypercube."""
        edges = []
        # Connect vertices that differ in exactly one coordinate
        for i in range(16):
            for dim in range(4):
                j = i ^ (1 << dim)  # Flip one bit
                if i < j:  # Avoid duplicate edges
                    edges.append((i, j))
        return edges
    
    @property
    def vertices(self) -> np.ndarray:
        """Get the vertices of the hypercube."""
        return self._vertices.copy()
    
    @property
    def edges(self) -> List[Tuple[int, int]]:
        """Get the edges of the hypercube as vertex index pairs."""
        return self._edges.copy()
    
    def transform(self, transformation: np.ndarray) -> 'Hypercube':
        """Apply a 4x4 transformation matrix to the hypercube.
        
        Args:
            transformation: A 4x4 transformation matrix.
            
        Returns:
            A new Hypercube instance with transformed vertices.
        """
        new_hypercube = Hypercube(self.size)
        new_hypercube._vertices = np.dot(self._vertices, transformation.T)
        return new_hypercube
