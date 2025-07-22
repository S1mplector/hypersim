"""Mathematical utilities for 4D operations."""
import numpy as np

def rotation_matrix_4d(plane1: int, plane2: int, angle: float) -> np.ndarray:
    """Create a 4D rotation matrix for rotation in the specified plane.
    
    Args:
        plane1: First axis of rotation plane (0-3)
        plane2: Second axis of rotation plane (0-3)
        angle: Rotation angle in radians
        
    Returns:
        4x4 rotation matrix
    """
    rotation = np.eye(4)
    c, s = np.cos(angle), np.sin(angle)
    rotation[plane1, plane1] = c
    rotation[plane1, plane2] = -s
    rotation[plane2, plane1] = s
    rotation[plane2, plane2] = c
    return rotation

def perspective_projection_4d_to_3d(points_4d: np.ndarray, distance: float = 5.0) -> np.ndarray:
    """Project 4D points to 3D using perspective projection.
    
    Args:
        points_4d: Array of shape (n, 4) containing 4D points
        distance: Distance from 4D camera to 3D hyperplane
        
    Returns:
        Array of shape (n, 3) containing projected 3D points
    """
    w = points_4d[:, 3]
    scale = 1 / (distance - w)
    points_3d = points_4d[:, :3] * scale.reshape(-1, 1)
    return points_3d
