"""Test the updated pygame renderer to verify tesseract fix is working."""
import numpy as np
from hypersim.objects.hypercube import Hypercube
from hypersim.visualization.renderers.pygame import PygameRenderer, Color

def test_updated_renderer():
    print("=== Testing Updated Pygame Renderer ===")
    
    # Create renderer and hypercube
    renderer = PygameRenderer(width=800, height=600)
    hypercube = Hypercube(size=2.0)
    hypercube.set_position([0, 0, 0, 1.0])  # Offset in W dimension
    
    # Apply multi-plane rotation for better 4D visualization
    hypercube.rotate(
        angle_xy=0.3,
        angle_xw=0.4,
        angle_zw=0.2
    )
    
    # Get transformed vertices
    transformed_vertices = hypercube.get_transformed_vertices()
    
    print("Testing renderer projection method:")
    projected_2d = []
    
    for i, vertex in enumerate(transformed_vertices):
        x, y, depth = renderer._project_4d_to_2d(vertex)
        projected_2d.append((x, y))
        print(f"  Vertex {i:2d}: 4D{vertex} -> 2D({x}, {y}) depth={depth:.3f}")
    
    # Count unique 2D positions
    unique_2d = list(set(projected_2d))
    print(f"\nRenderer projection results:")
    print(f"  Unique 2D positions: {len(unique_2d)} out of {len(projected_2d)}")
    print(f"  Improvement: {len(unique_2d) > 4}")
    
    # Calculate bounding box
    xs = [p[0] for p in projected_2d]
    ys = [p[1] for p in projected_2d]
    print(f"  2D Bounding box: X[{min(xs)}, {max(xs)}] Y[{min(ys)}, {max(ys)}]")
    print(f"  2D Size: {max(xs) - min(xs)} x {max(ys) - min(ys)}")
    
    # Test edge visibility with renderer projection
    visible_edges = 0
    edge_lengths = []
    
    for a, b in hypercube.edges:
        x1, y1 = projected_2d[a]
        x2, y2 = projected_2d[b]
        length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        edge_lengths.append(length)
        if length > 2.0:  # Visible edge
            visible_edges += 1
    
    print(f"  Visible edges (>2px): {visible_edges} out of {len(hypercube.edges)}")
    print(f"  Edge length range: {min(edge_lengths):.1f} to {max(edge_lengths):.1f}")
    
    # Test animation frames
    print(f"\n=== Testing Animation Frames ===")
    for frame in range(5):
        angle = frame * 0.2
        
        # Reset and apply new rotation
        hypercube = Hypercube(size=2.0)
        hypercube.set_position([0, 0, 0, 1.0])
        hypercube.rotate(
            angle_xy=angle,
            angle_xw=angle * 0.7,
            angle_zw=angle * 0.5
        )
        
        # Project vertices
        transformed = hypercube.get_transformed_vertices()
        frame_projected = []
        
        for vertex in transformed:
            x, y, depth = renderer._project_4d_to_2d(vertex)
            frame_projected.append((x, y))
        
        unique_count = len(set(frame_projected))
        
        # Calculate spread (how distributed the vertices are)
        xs = [p[0] for p in frame_projected]
        ys = [p[1] for p in frame_projected]
        spread = (max(xs) - min(xs)) + (max(ys) - min(ys))
        
        print(f"  Frame {frame}: {unique_count} unique positions, spread: {spread:.0f}px")

if __name__ == "__main__":
    test_updated_renderer()
