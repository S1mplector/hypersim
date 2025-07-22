"""
Basic example of visualizing a 4D tesseract using the hypersim package.
"""
import matplotlib.pyplot as plt
from hypersim.objects import Hypercube
from hypersim.visualization import MatplotlibRenderer

def main():
    # Create a renderer
    renderer = MatplotlibRenderer()
    
    # Create and add a hypercube to the scene
    hypercube = Hypercube(size=1.5)
    renderer.add_hypercube(hypercube, color='blue', alpha=0.6)
    
    # Set the title
    plt.title('4D Tesseract Projection')
    
    # Start the animation
    _ = renderer.animate_rotation(frames=360, interval=50)
    
    # Display the plot
    renderer.show()

if __name__ == "__main__":
    main()
