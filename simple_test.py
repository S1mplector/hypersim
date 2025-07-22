"""Simple test to verify the tesseract fix."""
import numpy as np
from hypersim.objects.hypercube import Hypercube

def test_simple():
    print("=== Simple Tesseract Test ===")
    
    # Create and transform hypercube
    hypercube = Hypercube(size=2.0)
    hypercube.set_position([0, 0, 0, 1.0])
    hypercube.rotate(angle_xy=0.3, angle_xw=0.4, angle_zw=0.2)
    
    # Get transformed vertices
    transformed = hypercube.get_transformed_vertices()
    print(f"Successfully created tesseract with {len(transformed)} vertices")
    
    # Test manual projection with improved method
    projected_2d = []
    for vertex in transformed:
        x, y, z, w = vertex
        scale = 1.0 / (1.0 + abs(w) * 0.3)
        screen_x = int(x * scale * 120 + 400)
        screen_y = int(-y * scale * 120 + 300)
        projected_2d.append((screen_x, screen_y))
    
    unique_2d = list(set(projected_2d))
    print(f"Unique 2D positions: {len(unique_2d)} out of {len(projected_2d)}")
    print(f"Fix successful: {len(unique_2d) > 4}")
    
    # Test edges
    visible_edges = 0
    for a, b in hypercube.edges:
        x1, y1 = projected_2d[a]
        x2, y2 = projected_2d[b]
        distance = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        if distance > 2.0:
            visible_edges += 1
    
    print(f"Visible edges: {visible_edges} out of {len(hypercube.edges)}")

if __name__ == "__main__":
    test_simple()
