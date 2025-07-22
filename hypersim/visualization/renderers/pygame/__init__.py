"""Pygame renderer package for 3D/4D visualization.

This package provides a Pygame-based renderer for 3D and 4D graphics. The main
entry point is the :class:`PygameRenderer` class, which manages the rendering
window, camera, and scene graph.

Basic usage::

    from hypersim.visualization.renderers.pygame import PygameRenderer, Color
    from hypersim.core.math_4d import create_vector_4d

    # Create a renderer
    renderer = PygameRenderer(800, 600, "4D Scene")
    
    # Add objects to the scene
    class MyObject:
        def render(self, renderer):
            start = create_vector_4d(0, 0, 0, 0)
            end = create_vector_4d(1, 1, 1, 1)
            renderer.draw_line_4d(start, end, Color(255, 0, 0))
    
    renderer.add_object(MyObject())
    
    # Run the render loop
    renderer.run()

The implementation is organized into several submodules:

- :mod:`.core`: Core rendering components (renderer, camera, shaders)
- :mod:`.graphics`: Graphics-related components (colors, primitives, scene)
- :mod:`.input`: Input handling
- :mod:`.ui`: User interface components
- :mod:`.utils`: Utility functions
"""

from __future__ import annotations

from .graphics.color import Color
from .core.renderer import PygameRenderer

__all__: list[str] = [
    "Color",
    "PygameRenderer",
]
