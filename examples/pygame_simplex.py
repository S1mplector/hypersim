"""Example of rendering a 4D simplex (5-cell) using the Pygame renderer."""
import numpy as np
import pygame
from hypersim.visualization.renderers.pygame import PygameRenderer, Color
from hypersim.visualization.renderers.pygame.ui.shape_info_overlay import ShapeInfoOverlay
from hypersim.objects.simplex_4d import Simplex4D
from hypersim.core.math_4d import create_vector_4d
from hypersim.core.math_utils import rotation_matrix_4d

def main():
    # Create a renderer with adjusted settings for better 4D visualization
    renderer = PygameRenderer(
        width=1024,
        height=768,
        title="4D Simplex (5-cell) Renderer - Use WASD/QE to move, Arrow keys to rotate",
        background_color=Color(10, 10, 30),
        distance=5.0  # Closer for better perspective
    )
    
    # Create a 4D simplex with better initial positioning
    simplex = Simplex4D(size=1.5)
    simplex.set_position([0, 0, 0, 1.0])  # Offset in W dimension for better projection
    
    # Apply initial rotation for better viewing angle
    simplex.rotate(
        angle_xy=0.4,   # Initial XY rotation
        angle_xw=0.3,   # Initial 4D rotation
        angle_zw=0.2    # Initial 4D rotation
    )
    
    # Camera/movement variables
    camera_pos = [0.0, 0.0, 0.0, 0.0]  # 4D camera position
    rotation_speed = 2.0  # radians per second
    movement_speed = 3.0  # units per second

    # Create the shape info overlay
    overlay = ShapeInfoOverlay(
        screen=renderer.screen,
        shape_name="4D Simplex (5-cell)",
        shape=simplex,
        font_size=18,
        padding=10
    )
    
    # Add a custom description
    overlay.add_additional_info("Description", "The simplest 4D polytope")
    
    # Save the original render method
    original_render = renderer.render
    
    # Create a closure to capture the simplex and overlay
    def custom_render():
        # Call the original render method to clear the screen
        if hasattr(renderer, 'clear'):
            renderer.clear()
        
        # Render the simplex with orange color
        renderer.render_simplex(simplex, Color(255, 140, 0), 2)
        
        # Update and draw the overlay
        overlay.update()
        overlay.draw()
        
        # Update the display
        pygame.display.flip()
    
    # Replace the render method with our custom one
    renderer.render = custom_render
    
    # Run the renderer
    running = True
    clock = pygame.time.Clock()
    target_fps = 60
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Handle continuous key presses for movement and rotation
        keys = pygame.key.get_pressed()
        dt = clock.get_time() / 1000.0  # seconds
        
        # Movement controls (WASD + QE for 4D movement)
        if keys[pygame.K_w]:  # Move forward in Z
            camera_pos[2] += movement_speed * dt
        if keys[pygame.K_s]:  # Move backward in Z
            camera_pos[2] -= movement_speed * dt
        if keys[pygame.K_a]:  # Move left in X
            camera_pos[0] -= movement_speed * dt
        if keys[pygame.K_d]:  # Move right in X
            camera_pos[0] += movement_speed * dt
        if keys[pygame.K_q]:  # Move up in Y
            camera_pos[1] += movement_speed * dt
        if keys[pygame.K_e]:  # Move down in Y
            camera_pos[1] -= movement_speed * dt
        if keys[pygame.K_r]:  # Move forward in W (4th dimension)
            camera_pos[3] += movement_speed * dt
        if keys[pygame.K_f]:  # Move backward in W (4th dimension)
            camera_pos[3] -= movement_speed * dt
        
        # Rotation controls (Arrow keys + additional keys for 4D rotations)
        if keys[pygame.K_LEFT]:  # Rotate around Y axis
            simplex.rotate(angle_xy=-rotation_speed * dt)
        if keys[pygame.K_RIGHT]:  # Rotate around Y axis
            simplex.rotate(angle_xy=rotation_speed * dt)
        if keys[pygame.K_UP]:  # Rotate around X axis
            simplex.rotate(angle_xz=rotation_speed * dt)
        if keys[pygame.K_DOWN]:  # Rotate around X axis
            simplex.rotate(angle_xz=-rotation_speed * dt)
        if keys[pygame.K_z]:  # 4D rotation XW plane
            simplex.rotate(angle_xw=rotation_speed * dt)
        if keys[pygame.K_x]:  # 4D rotation XW plane
            simplex.rotate(angle_xw=-rotation_speed * dt)
        if keys[pygame.K_c]:  # 4D rotation YW plane
            simplex.rotate(angle_yw=rotation_speed * dt)
        if keys[pygame.K_v]:  # 4D rotation YW plane
            simplex.rotate(angle_yw=-rotation_speed * dt)
        if keys[pygame.K_b]:  # 4D rotation ZW plane
            simplex.rotate(angle_zw=rotation_speed * dt)
        if keys[pygame.K_n]:  # 4D rotation ZW plane
            simplex.rotate(angle_zw=-rotation_speed * dt)
        
        # Apply camera position to simplex (move simplex relative to camera)
        simplex.set_position([-camera_pos[0], -camera_pos[1], -camera_pos[2], 1.0 - camera_pos[3]])
        
        # Update simplex rotation (gentle auto-rotation)
        simplex.update(dt)
        
        # Update
        renderer.update(1.0 / target_fps)
        
        # Render
        renderer.render()
        
        # Cap the frame rate
        clock.tick(target_fps)
    
    pygame.quit()

if __name__ == "__main__":
    main()
