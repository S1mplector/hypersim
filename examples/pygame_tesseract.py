"""Example of rendering a 4D hypercube using the Pygame renderer."""
import numpy as np
from hypersim.visualization.renderers.pygame import PygameRenderer, Color
from hypersim.objects.hypercube import Hypercube

def main():
    # Create a renderer
    renderer = PygameRenderer(
        width=1024,
        height=768,
        title="4D Hypercube Renderer",
        background_color=Color(10, 10, 20),
        distance=5.0
    )
    
    # Create a 4D hypercube
    hypercube = Hypercube()
    
    # Add the hypercube to the scene
    renderer.objects.append(hypercube)
    
    # Run the renderer
    renderer.run(target_fps=60)

if __name__ == "__main__":
    main()
