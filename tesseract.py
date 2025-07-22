import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

class Tesseract:
    def __init__(self):
        # Define the 16 vertices of a tesseract
        self.vertices = np.array([
            [-1, -1, -1, -1],
            [-1, -1, -1, 1],
            [-1, -1, 1, -1],
            [-1, -1, 1, 1],
            [-1, 1, -1, -1],
            [-1, 1, -1, 1],
            [-1, 1, 1, -1],
            [-1, 1, 1, 1],
            [1, -1, -1, -1],
            [1, -1, -1, 1],
            [1, -1, 1, -1],
            [1, -1, 1, 1],
            [1, 1, -1, -1],
            [1, 1, -1, 1],
            [1, 1, 1, -1],
            [1, 1, 1, 1]
        ])
        
        # Define edges (pairs of vertex indices)
        self.edges = [
            # Cube 1 (w = -1)
            (0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3), (2, 6), 
            (3, 7), (4, 5), (4, 6), (5, 7), (6, 7),
            # Cube 2 (w = 1)
            (8, 9), (8, 10), (8, 12), (9, 11), (9, 13), (10, 11), 
            (10, 14), (11, 15), (12, 13), (12, 14), (13, 15), (14, 15),
            # Connections between cubes
            (0, 8), (1, 9), (2, 10), (3, 11), (4, 12), (5, 13), (6, 14), (7, 15)
        ]
        
        # Rotation matrices
        self.rotation_xy = lambda a: np.array([
            [np.cos(a), -np.sin(a), 0, 0],
            [np.sin(a), np.cos(a), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        self.rotation_zw = lambda a: np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, np.cos(a), -np.sin(a)],
            [0, 0, np.sin(a), np.cos(a)]
        ])
        
    def project_4d_to_3d(self, points_4d, distance=5):
        """Project 4D points to 3D using perspective projection"""
        w = points_4d[:, 3]
        scale = 1 / (distance - w)
        
        # Apply perspective projection
        points_3d = points_4d[:, :3] * scale.reshape(-1, 1)
        return points_3d
    
    def rotate_4d(self, points, angle_xy, angle_zw):
        """Rotate 4D points in XY and ZW planes"""
        rot_xy = self.rotation_xy(angle_xy)
        rot_zw = self.rotation_zw(angle_zw)
        rotation = rot_xy @ rot_zw
        return np.dot(points, rotation.T)

# Create the figure and 3D axis
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_axis_off()
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])

# Create tesseract instance
tesseract = Tesseract()

# Initialize plot elements
lines = [ax.plot([], [], [], 'b-', alpha=0.6)[0] for _ in tesseract.edges]

# Animation update function
def update(frame):
    angle_xy = frame * 0.02
    angle_zw = frame * 0.015
    
    # Rotate and project vertices
    rotated = tesseract.rotate_4d(tesseract.vertices, angle_xy, angle_zw)
    projected = tesseract.project_4d_to_3d(rotated)
    
    # Update edges
    for i, (start_idx, end_idx) in enumerate(tesseract.edges):
        lines[i].set_data(
            [projected[start_idx, 0], projected[end_idx, 0]],
            [projected[start_idx, 1], projected[end_idx, 1]]
        )
        lines[i].set_3d_properties(
            [projected[start_idx, 2], projected[end_idx, 2]]
        )
    
    # Rotate the view for better visualization
    ax.view_init(elev=20, azim=frame/2)
    
    return lines

# Create animation
ani = FuncAnimation(fig, update, frames=360, interval=50, blit=False)

plt.title('4D Tesseract Projection')
plt.tight_layout()
plt.show()
