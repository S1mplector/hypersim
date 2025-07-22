"""Comprehensive test of tesseract rendering to verify the fix."""
import numpy as np
import pygame
from hypersim.objects.hypercube import Hypercube
from hypersim.visualization.renderers.pygame import PygameRenderer, Color

def test_tesseract_rendering():
    print("=== Testing Tesseract Rendering ===")
    
    # Create a hypercube
    hypercube = Hypercube(size=2.0)
    hypercube.set_position([0, 0, 0, 0])
    
    print(f"Created hypercube with {len(hypercube.vertices)} vertices and {len(hypercube.edges)} edges")
    
    # Test different rotation states
    rotation_angles = [
        (0, 0),      # No rotation
        (0.5, 0),    # XY rotation only
        (0, 0.5),    # XW rotation only
        (0.5, 0.5),  # Both rotations
        (1.0, 1.0),  # More rotation
    ]
    
    for i, (angle_xy, angle_xw) in enumerate(rotation_angles):
        print(f"\n--- Test {i+1}: XY={angle_xy}, XW={angle_xw} ---")
        
        # Reset hypercube and apply rotation
        hypercube = Hypercube(size=2.0)
        hypercube.set_position([0, 0, 0, 0])
        hypercube.rotate(angle_xy=angle_xy, angle_xw=angle_xw)
        
        # Get transformed vertices
        transformed = hypercube.get_transformed_vertices()
        
        # Test projection to 2D
        distance = 5.0
        projected_2d = []
        
        for vertex in transformed:
            w = vertex[3]
            perspective = distance / (distance + w)
            projected_3d = vertex[:3] * perspective
            x = int(projected_3d[0] * 100 + 400)
            y = int(-projected_3d[1] * 100 + 300)
            projected_2d.append((x, y))
        
        # Calculate bounding box of projected vertices
        xs = [p[0] for p in projected_2d]
        ys = [p[1] for p in projected_2d]
        
        print(f"  2D Bounding box: X[{min(xs)}, {max(xs)}] Y[{min(ys)}, {max(ys)}]")
        print(f"  2D Size: {max(xs) - min(xs)} x {max(ys) - min(ys)}")
        
        # Count unique projected positions (to see if vertices are collapsing)
        unique_positions = set(projected_2d)
        print(f"  Unique 2D positions: {len(unique_positions)} out of {len(projected_2d)}")
        
        # Test edge lengths in 2D
        edge_lengths = []
        for a, b in hypercube.edges:
            x1, y1 = projected_2d[a]
            x2, y2 = projected_2d[b]
            length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
            edge_lengths.append(length)
        
        non_zero_edges = [l for l in edge_lengths if l > 1.0]  # Edges longer than 1 pixel
        print(f"  Visible edges (>1px): {len(non_zero_edges)} out of {len(edge_lengths)}")
        print(f"  Edge length range: {min(edge_lengths):.1f} to {max(edge_lengths):.1f}")

def test_pygame_rendering():
    """Test the actual pygame rendering."""
    print("\n=== Testing Pygame Rendering ===")
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tesseract Test")
    
    # Create renderer and hypercube
    renderer = PygameRenderer(width=800, height=600)
    hypercube = Hypercube(size=2.0)
    hypercube.set_position([0, 0, 0, 0])
    
    # Test rendering at different rotation states
    for frame in range(5):
        angle = frame * 0.2
        hypercube.rotate(angle_xy=angle, angle_xw=angle * 0.7)
        
        # Clear screen
        renderer.clear()
        
        # Render hypercube
        renderer.render_hypercube(hypercube, Color(0, 255, 0), 2)
        
        # Count non-black pixels to see if anything is being drawn
        surface_array = pygame.surfarray.array3d(renderer.screen)
        non_black_pixels = np.sum(np.any(surface_array > 0, axis=2))
        
        print(f"  Frame {frame}: Non-black pixels: {non_black_pixels}")
    
    pygame.quit()
    print("Pygame test completed")

if __name__ == "__main__":
    test_tesseract_rendering()
    test_pygame_rendering()
