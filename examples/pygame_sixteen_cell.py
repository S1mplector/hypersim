"""Example of rendering a 4D 16-cell using the Pygame renderer with overlay."""
import numpy as np
import pygame
from hypersim.visualization.renderers.pygame import PygameRenderer, Color
from hypersim.visualization.renderers.pygame.ui.shape_info_overlay import ShapeInfoOverlay
from hypersim.objects.sixteen_cell import SixteenCell

def main():
    # Create a renderer with adjusted settings for better 4D visualization
    renderer = PygameRenderer(
        width=1024,
        height=768,
        title="4D 16-Cell Renderer",
        background_color=Color(10, 10, 20),
        distance=5.0  # Closer for better perspective
    )
    
    # Create a 16-cell with better initial positioning
    sixteen_cell = SixteenCell(size=1.5)
    sixteen_cell.set_position([0, 0, 0, 1.0])  # Offset in W dimension for better projection
    
    # Apply initial rotation for better viewing angle
    sixteen_cell.rotate(
        xy=0.3,   # Initial XY rotation
        xw=0.2,   # Initial 4D rotation
        zw=0.1    # Initial 4D rotation
    )
    
    # Camera/movement variables
    camera_pos = [0.0, 0.0, 0.0, 0.0]  # 4D camera position
    rotation_speed = 2.0  # radians per second
    movement_speed = 3.0  # units per second

    # Create the shape info overlay
    overlay = ShapeInfoOverlay(
        screen=renderer.screen,
        shape_name="16-Cell (Hyperoctahedron)",
        shape=sixteen_cell,
        font_size=16,
        padding=10,
        line_height=20
    )
    
    # Add a custom description
    overlay.add_additional_info("Description", "One of the six convex regular 4-polytopes")
    
    # Save the original render method
    original_render = renderer.render
    
    # Create a closure to capture the sixteen_cell and overlay
    def custom_render():
        # Call the original render method to clear the screen
        if hasattr(renderer, 'clear'):
            renderer.clear()
        
        # Render the 16-cell in a nice blue color
        renderer.render_4d_object(sixteen_cell, Color(100, 150, 255), 2)
        
        # Update the position in the overlay
        overlay.add_additional_info("Position", lambda: f"X:{camera_pos[0]:.2f}, Y:{camera_pos[1]:.2f}, Z:{camera_pos[2]:.2f}, W:{camera_pos[3]:.2f}")
        
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
        if keys[pygame.K_LEFT]:  # Rotate around Y axis (XY plane)
            sixteen_cell.rotate(xy=-rotation_speed * dt)
        if keys[pygame.K_RIGHT]:  # Rotate around Y axis (XY plane)
            sixteen_cell.rotate(xy=rotation_speed * dt)
        if keys[pygame.K_UP]:  # Rotate around X axis (XZ plane)
            sixteen_cell.rotate(xz=rotation_speed * dt)
        if keys[pygame.K_DOWN]:  # Rotate around X axis (XZ plane)
            sixteen_cell.rotate(xz=-rotation_speed * dt)
        if keys[pygame.K_z]:  # 4D rotation XW plane
            sixteen_cell.rotate(xw=rotation_speed * dt)
        if keys[pygame.K_x]:  # 4D rotation XW plane
            sixteen_cell.rotate(xw=-rotation_speed * dt)
        if keys[pygame.K_c]:  # 4D rotation YW plane
            sixteen_cell.rotate(yw=rotation_speed * dt)
        if keys[pygame.K_v]:  # 4D rotation YW plane
            sixteen_cell.rotate(yw=-rotation_speed * dt)
        if keys[pygame.K_b]:  # 4D rotation ZW plane
            sixteen_cell.rotate(zw=rotation_speed * dt)
        if keys[pygame.K_n]:  # 4D rotation ZW plane
            sixteen_cell.rotate(zw=-rotation_speed * dt)
        
        # Apply camera position to 16-cell (move 16-cell relative to camera)
        sixteen_cell.set_position([-camera_pos[0], -camera_pos[1], -camera_pos[2], 1.0 - camera_pos[3]])
        
        # Update 16-cell rotation
        sixteen_cell.update(dt)
        
        # Update and render
        renderer.update(1.0 / target_fps)
        renderer.render()
        
        # Cap the frame rate
        clock.tick(target_fps)
    
    pygame.quit()

if __name__ == "__main__":
    main()
