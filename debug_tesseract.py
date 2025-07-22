"""Debug script to understand tesseract rendering issues."""
import numpy as np
from hypersim.objects.hypercube import Hypercube
from hypersim.core.math_4d import perspective_projection_4d_to_3d

def debug_tesseract():
    print("=== Tesseract Debug ===")
    
    # Create a hypercube
    hypercube = Hypercube(size=2.0)
    hypercube.set_position([0, 0, 0, 0])
    
    print(f"Initial vertices shape: {hypercube.vertices.shape}")
    print(f"Number of edges: {len(hypercube.edges)}")
    print(f"First few vertices:\n{hypercube.vertices[:4]}")
    
    # Apply some rotation
    hypercube.rotate(angle_xy=0.5, angle_xw=0.3)
    
    # Get transformed vertices
    transformed = hypercube.get_transformed_vertices()
    print(f"\nTransformed vertices shape: {transformed.shape}")
    print(f"First few transformed vertices:\n{transformed[:4]}")
    
    # Check if vertices are actually different after transformation
    print(f"\nVertices changed after rotation: {not np.allclose(hypercube.vertices, transformed)}")
    
    # Test 4D to 3D projection
    projected_3d = perspective_projection_4d_to_3d(transformed, distance=5.0)
    print(f"\nProjected 3D vertices shape: {projected_3d.shape}")
    print(f"First few projected vertices:\n{projected_3d[:4]}")
    
    # Check if projection creates variety in 3D space
    print(f"\n3D projection has variety:")
    print(f"  X range: {projected_3d[:, 0].min():.3f} to {projected_3d[:, 0].max():.3f}")
    print(f"  Y range: {projected_3d[:, 1].min():.3f} to {projected_3d[:, 1].max():.3f}")
    print(f"  Z range: {projected_3d[:, 2].min():.3f} to {projected_3d[:, 2].max():.3f}")
    
    # Test manual 2D projection
    print(f"\n=== Testing Manual 2D Projection ===")
    distance = 5.0
    for i, vertex in enumerate(transformed[:8]):  # Test first 8 vertices
        # Manual 4D to 3D projection
        w = vertex[3]
        perspective = distance / (distance + w)
        projected_3d = vertex[:3] * perspective
        
        # Simple 3D to 2D projection
        x = int(projected_3d[0] * 100 + 400)  # center at 400
        y = int(-projected_3d[1] * 100 + 300)  # center at 300
        print(f"Vertex {i}: 4D{vertex} -> 3D{projected_3d} -> 2D({x}, {y})")
    
    print(f"\n=== Edge Analysis ===")
    # Check a few edges to see if they create lines or just points
    for i, (a, b) in enumerate(hypercube.edges[:5]):
        v1 = transformed[a]
        v2 = transformed[b]
        
        # Project both vertices
        w1, w2 = v1[3], v2[3]
        p1 = distance / (distance + w1)
        p2 = distance / (distance + w2)
        proj1 = v1[:3] * p1
        proj2 = v2[:3] * p2
        
        x1 = int(proj1[0] * 100 + 400)
        y1 = int(-proj1[1] * 100 + 300)
        x2 = int(proj2[0] * 100 + 400)
        y2 = int(-proj2[1] * 100 + 300)
        
        distance_2d = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        print(f"Edge {i}: ({x1},{y1}) -> ({x2},{y2}), 2D distance: {distance_2d:.1f}")

if __name__ == "__main__":
    debug_tesseract()
