"""Detailed analysis of tesseract vertex generation and projection."""
import numpy as np
from hypersim.objects.hypercube import Hypercube
from hypersim.core.math_4d import perspective_projection_4d_to_3d

def analyze_tesseract_vertices():
    print("=== Detailed Tesseract Vertex Analysis ===")
    
    # Create a hypercube
    hypercube = Hypercube(size=2.0)
    hypercube.set_position([0, 0, 0, 0])
    
    print("Original vertices:")
    for i, vertex in enumerate(hypercube.vertices):
        print(f"  Vertex {i:2d}: {vertex}")
    
    print(f"\nVertex analysis:")
    print(f"  X values: {set(hypercube.vertices[:, 0])}")
    print(f"  Y values: {set(hypercube.vertices[:, 1])}")
    print(f"  Z values: {set(hypercube.vertices[:, 2])}")
    print(f"  W values: {set(hypercube.vertices[:, 3])}")
    
    # Apply a small rotation to see what happens
    hypercube.rotate(angle_xy=0.1, angle_xw=0.1)
    transformed = hypercube.get_transformed_vertices()
    
    print(f"\nAfter small rotation:")
    for i, vertex in enumerate(transformed):
        print(f"  Vertex {i:2d}: {vertex}")
    
    # Test 4D to 3D projection
    print(f"\n4D to 3D projection (distance=5.0):")
    projected_3d = perspective_projection_4d_to_3d(transformed, distance=5.0)
    for i, vertex in enumerate(projected_3d):
        print(f"  Vertex {i:2d}: {vertex}")
    
    # Check for duplicates in 3D projection
    unique_3d = []
    for vertex in projected_3d:
        is_duplicate = False
        for existing in unique_3d:
            if np.allclose(vertex, existing, atol=1e-3):
                is_duplicate = True
                break
        if not is_duplicate:
            unique_3d.append(vertex)
    
    print(f"\nUnique 3D positions: {len(unique_3d)} out of {len(projected_3d)}")
    for i, vertex in enumerate(unique_3d):
        print(f"  Unique {i:2d}: {vertex}")
    
    # Manual 2D projection
    print(f"\n2D projection:")
    projected_2d = []
    for i, vertex_3d in enumerate(projected_3d):
        x = int(vertex_3d[0] * 100 + 400)
        y = int(-vertex_3d[1] * 100 + 300)
        projected_2d.append((x, y))
        print(f"  Vertex {i:2d}: 3D{vertex_3d} -> 2D({x}, {y})")
    
    # Check for duplicates in 2D projection
    unique_2d = list(set(projected_2d))
    print(f"\nUnique 2D positions: {len(unique_2d)} out of {len(projected_2d)}")
    for i, pos in enumerate(unique_2d):
        print(f"  Unique {i:2d}: {pos}")
    
    # Test with different projection distances
    print(f"\n=== Testing Different Projection Distances ===")
    for distance in [1.0, 2.0, 5.0, 10.0, 20.0]:
        proj_3d = perspective_projection_4d_to_3d(transformed, distance=distance)
        
        # Count unique 3D positions
        unique_count = 0
        seen = []
        for vertex in proj_3d:
            is_new = True
            for existing in seen:
                if np.allclose(vertex, existing, atol=1e-3):
                    is_new = False
                    break
            if is_new:
                seen.append(vertex)
                unique_count += 1
        
        print(f"  Distance {distance:4.1f}: {unique_count} unique 3D positions")

if __name__ == "__main__":
    analyze_tesseract_vertices()
