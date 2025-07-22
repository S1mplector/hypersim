"""Test improved tesseract visualization with better viewing angles."""
import numpy as np
from hypersim.objects.hypercube import Hypercube
from hypersim.core.math_4d import perspective_projection_4d_to_3d

def test_improved_tesseract():
    print("=== Testing Improved Tesseract Visualization ===")
    
    # Create a hypercube with a better initial rotation
    hypercube = Hypercube(size=2.0)
    hypercube.set_position([0, 0, 0, 0])
    
    # Apply rotations that should give us a better view
    # Rotate in multiple planes to avoid symmetrical collapse
    hypercube.rotate(
        angle_xy=0.3,   # Rotate in XY plane
        angle_xz=0.2,   # Rotate in XZ plane  
        angle_xw=0.4,   # Rotate in XW plane (4D rotation)
        angle_yz=0.1,   # Rotate in YZ plane
        angle_yw=0.3,   # Rotate in YW plane (4D rotation)
        angle_zw=0.2    # Rotate in ZW plane (4D rotation)
    )
    
    transformed = hypercube.get_transformed_vertices()
    
    print("Transformed vertices after multi-plane rotation:")
    for i, vertex in enumerate(transformed):
        print(f"  Vertex {i:2d}: [{vertex[0]:6.3f}, {vertex[1]:6.3f}, {vertex[2]:6.3f}, {vertex[3]:6.3f}]")
    
    # Test projection with different distances
    for distance in [3.0, 5.0, 8.0]:
        print(f"\n--- Testing with distance = {distance} ---")
        
        projected_3d = perspective_projection_4d_to_3d(transformed, distance=distance)
        
        # Count unique 3D positions
        unique_3d = []
        for vertex in projected_3d:
            is_duplicate = False
            for existing in unique_3d:
                if np.allclose(vertex, existing, atol=1e-2):
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique_3d.append(vertex)
        
        print(f"  Unique 3D positions: {len(unique_3d)} out of {len(projected_3d)}")
        
        # Project to 2D with better scaling
        projected_2d = []
        scale_factor = 150  # Larger scale for better visibility
        center_x, center_y = 400, 300
        
        for vertex_3d in projected_3d:
            x = int(vertex_3d[0] * scale_factor + center_x)
            y = int(-vertex_3d[1] * scale_factor + center_y)
            projected_2d.append((x, y))
        
        # Count unique 2D positions
        unique_2d = list(set(projected_2d))
        print(f"  Unique 2D positions: {len(unique_2d)} out of {len(projected_2d)}")
        
        # Calculate bounding box
        xs = [p[0] for p in projected_2d]
        ys = [p[1] for p in projected_2d]
        print(f"  2D Bounding box: X[{min(xs)}, {max(xs)}] Y[{min(ys)}, {max(ys)}]")
        print(f"  2D Size: {max(xs) - min(xs)} x {max(ys) - min(ys)}")

def test_alternative_projection():
    """Test an alternative 4D projection method."""
    print("\n=== Testing Alternative 4D Projection ===")
    
    hypercube = Hypercube(size=2.0)
    hypercube.set_position([0, 0, 0, 1.5])  # Move in W dimension
    
    # Apply asymmetric rotations
    hypercube.rotate(angle_xy=0.5, angle_xw=0.7, angle_zw=0.3)
    
    transformed = hypercube.get_transformed_vertices()
    
    # Alternative projection: orthographic projection with W-based scaling
    print("Alternative projection method:")
    projected_2d = []
    
    for i, vertex in enumerate(transformed):
        x, y, z, w = vertex
        
        # Use W coordinate to scale the X,Y coordinates (orthographic + scaling)
        scale = 1.0 / (1.0 + abs(w) * 0.3)  # Scale based on W distance
        
        screen_x = int(x * scale * 100 + 400)
        screen_y = int(-y * scale * 100 + 300)
        
        projected_2d.append((screen_x, screen_y))
        print(f"  Vertex {i:2d}: 4D{vertex} -> 2D({screen_x}, {screen_y})")
    
    unique_2d = list(set(projected_2d))
    print(f"\nAlternative method - Unique 2D positions: {len(unique_2d)} out of {len(projected_2d)}")
    
    # Test edge visibility
    visible_edges = 0
    for a, b in hypercube.edges:
        x1, y1 = projected_2d[a]
        x2, y2 = projected_2d[b]
        distance = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        if distance > 2.0:  # Visible edge
            visible_edges += 1
    
    print(f"Visible edges: {visible_edges} out of {len(hypercube.edges)}")

if __name__ == "__main__":
    test_improved_tesseract()
    test_alternative_projection()
