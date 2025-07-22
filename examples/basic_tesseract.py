"""
Basic example of visualizing a 4D tesseract using the hypersim package.
"""
from hypersim.objects import Hypercube
from hypersim.visualization.renderers.pygame import PygameRenderer, Color

def main():
    # Create a renderer
    renderer = PygameRenderer(title="Basic Tesseract", background_color=Color(20, 20, 30))
    
    # Create and add a hypercube to the scene
    hypercube = Hypercube(size=1.5)
    renderer.objects.append(hypercube)
    
    renderer.run()

if __name__ == "__main__":
    main()
