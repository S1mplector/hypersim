# HyperSim

A Python framework for 4D visualization and simulation. This project provides tools for working with 4D geometry, including 4D objects, transformations, and visualizations.

## Features

- 4D geometric primitives (currently supports hypercube/tesseract)
- 4D to 3D perspective projection
- Interactive visualization using Matplotlib
- Extensible architecture for adding new 4D objects and renderers

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/hypersim.git
   cd hypersim
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Unix/macOS
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

## Quick Start

```python
from hypersim.objects import Hypercube
from hypersim.visualization import MatplotlibRenderer
import matplotlib.pyplot as plt

# Create a renderer
renderer = MatplotlibRenderer()

# Create and add a hypercube to the scene
hypercube = Hypercube(size=1.5)
renderer.add_hypercube(hypercube, color='blue', alpha=0.6)

# Animate the rotation
_ = renderer.animate_rotation(frames=360, interval=50)

# Display the plot
plt.title('4D Tesseract Projection')
renderer.show()
```

## Project Structure

```
hypersim/
├── hypersim/               # Main package
│   ├── core/              # Core simulation and math
│   ├── objects/           # 4D object definitions
│   └── visualization/     # Visualization components
├── examples/              # Example scripts
├── tests/                 # Unit and integration tests
└── docs/                  # Documentation
```

## Running Examples

Check the `examples/` directory for example scripts. To run the basic tesseract example:

```bash
python examples/basic_tesseract.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
