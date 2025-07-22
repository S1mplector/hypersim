"""Implementation of a 4D hypercube (tesseract)."""
import numpy as np
from typing import List, Tuple, Optional, Union

from hypersim.core.math_4d import create_vector_4d, create_rotation_matrix_4d


class Hypercube:
    """A 4D hypercube (tesseract) implementation.
    
    This class represents a 4D hypercube with methods for generating its vertices,
    edges, and performing 4D transformations.
    """
    
    def __init__(self, size: float = 1.0, position: Optional[Union[list, np.ndarray]] = None):
        """Initialize a hypercube with the given size and position.
        
        Args:
            size: The length of each edge of the hypercube.
            position: Optional 4D position of the hypercube's center.
        """
        self.size = size
        self._vertices = self._generate_vertices()
        self._edges = self._generate_edges()
        
        # Initialize transform matrix
        self.transform = np.eye(4, dtype=np.float32)
        
        # Set initial position if provided
        if position is not None:
            self.set_position(position)
    
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
    
    def set_position(self, position: Union[list, np.ndarray]) -> None:
        """Set the position of the hypercube.
        
        Args:
            position: 4D position as a list or numpy array [x, y, z, w]
        """
        if len(position) != 4:
            raise ValueError("Position must be a 4D vector")
        self.transform[:4, 3] = position
    
    def rotate(self, angle_xy: float = 0.0, angle_xz: float = 0.0, 
              angle_xw: float = 0.0, angle_yz: float = 0.0,
              angle_yw: float = 0.0, angle_zw: float = 0.0) -> None:
        """Rotate the hypercube in 4D space.
        
        Args:
            angle_xy: Rotation angle in the XY plane (radians)
            angle_xz: Rotation angle in the XZ plane (radians)
            angle_xw: Rotation angle in the XW plane (radians)
            angle_yz: Rotation angle in the YZ plane (radians)
            angle_yw: Rotation angle in the YW plane (radians)
            angle_zw: Rotation angle in the ZW plane (radians)
        """
        rot_matrix = create_rotation_matrix_4d(
            angle_xy=angle_xy, angle_xz=angle_xz, angle_xw=angle_xw,
            angle_yz=angle_yz, angle_yw=angle_yw, angle_zw=angle_zw
        )
        self.transform = np.dot(rot_matrix, self.transform)
    
    def scale(self, factor: float) -> None:
        """Scale the hypercube by a uniform factor.
        
        Args:
            factor: Scaling factor
        """
        scale_matrix = np.eye(4, dtype=np.float32) * factor
        scale_matrix[3, 3] = 1.0  # Preserve W component
        self.transform = np.dot(scale_matrix, self.transform)
    
    def get_transformed_vertices(self) -> np.ndarray:
        """Get the vertices after applying the current transform."""
        # Convert to homogeneous coordinates
        homogeneous = np.column_stack([
            self._vertices,
            np.ones(len(self._vertices))
        ])
        
        # Apply transform
        transformed = np.dot(homogeneous, self.transform.T)
        
        # Convert back from homogeneous coordinates
        return transformed[:, :4]
    
    def render(self, renderer) -> None:
        """Render the hypercube using the specified renderer.
        
        Args:
            renderer: Renderer instance with a render_hypercube method
        """
        if hasattr(renderer, 'render_hypercube'):
            renderer.render_hypercube(self)
    
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
