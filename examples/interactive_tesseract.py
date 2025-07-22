"""Interactive 4D hypercube visualization using Pygame renderer.

Controls:
- WASD: Move camera in XZ plane
- QE: Move camera up/down (Y axis)
- ZX: Move in the 4th dimension (W axis)
- Left mouse button + drag: Rotate camera around target
- ESC: Quit
"""
import sys
import math
import numpy as np
import pygame

# Add the project root to the path
sys.path.append("..")
from hypersim.visualization.renderers.pygame import PygameRenderer, Color
from hypersim.objects.hypercube import Hypercube

def main():
    # Create a renderer with a larger window
    renderer = PygameRenderer(
        width=1200,
        height=800,
        title="4D Hypercube Interactive Demo",
        background_color=Color(15, 15, 25),
        distance=5.0
    )
    
    # Create multiple hypercubes with different properties
    hypercubes = [
        {"object": Hypercube(size=1.0, position=[0, 0, 0, 0]), "color": Color(0, 200, 255), "rotation_speed": 0.01},
        {"object": Hypercube(size=0.5, position=[2, 0, 0, 0]), "color": Color(255, 100, 0), "rotation_speed": 0.02},
        {"object": Hypercube(size=0.3, position=[0, 0, 2, 0]), "color": Color(100, 255, 50), "rotation_speed": -0.015},
    ]
    
    # Add all hypercubes to the scene
    for cube in hypercubes:
        renderer.objects.append(cube["object"])
    
    # Main game loop
    clock = pygame.time.Clock()
    running = True
    
    # Store the original camera position for reset
    original_camera_pos = renderer.camera_pos.copy()
    
    # Help text
    font = pygame.font.Font(None, 24)
    help_texts = [
        "WASD: Move in XZ plane",
        "QE: Move up/down (Y)",
        "ZX: Move in 4D (W)",
        "Left click + drag: Rotate",
        "R: Reset camera",
        "ESC: Quit"
    ]
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:  # Reset camera
                    renderer.camera_pos = original_camera_pos.copy()
                    renderer._update_view_matrix()
        
        # Handle continuous key presses for movement
        keys = pygame.key.get_pressed()
        move_speed = 0.1
        
        # XZ movement (WASD)
        if keys[pygame.K_w]:
            renderer.camera_pos[2] += move_speed
        if keys[pygame.K_s]:
            renderer.camera_pos[2] -= move_speed
        if keys[pygame.K_a]:
            renderer.camera_pos[0] -= move_speed
        if keys[pygame.K_d]:
            renderer.camera_pos[0] += move_speed
            
        # Y movement (QE)
        if keys[pygame.K_q]:
            renderer.camera_pos[1] += move_speed
        if keys[pygame.K_e]:
            renderer.camera_pos[1] -= move_speed
            
        # W movement (ZX for 4th dimension)
        if keys[pygame.K_z]:
            renderer.camera_pos[3] += move_speed
        if keys[pygame.K_x]:
            renderer.camera_pos[3] -= move_speed
        
        # Update view matrix if camera moved
        if any(keys):
            renderer._update_view_matrix()
        
        # Update hypercube rotations
        time = pygame.time.get_ticks() / 1000.0  # Convert to seconds
        for cube in hypercubes:
            # Apply continuous rotation
            cube["object"].rotate(
                angle_xy=time * cube["rotation_speed"],
                angle_xz=time * cube["rotation_speed"] * 0.5,
                angle_zw=time * cube["rotation_speed"] * 0.3
            )
        
        # Clear the screen
        renderer.clear()
        
        # Render all objects
        for obj in renderer.objects:
            if hasattr(obj, 'render'):
                obj.render(renderer)
        
        # Draw help text
        for i, text in enumerate(help_texts):
            text_surface = font.render(text, True, (200, 200, 255))
            renderer.screen.blit(text_surface, (10, 10 + i * 25))
        
        # Draw FPS and camera position
        fps_text = font.render(f"FPS: {renderer.clock.get_fps():.1f}", True, (255, 255, 255))
        cam_text = font.render(
            f"Camera: [{renderer.camera_pos[0]:.1f}, {renderer.camera_pos[1]:.1f}, {renderer.camera_pos[2]:.1f}, {renderer.camera_pos[3]:.1f}]", 
            True, (255, 255, 255)
        )
        renderer.screen.blit(fps_text, (renderer.width - 150, 10))
        renderer.screen.blit(cam_text, (10, renderer.height - 30))
        
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        renderer.clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
