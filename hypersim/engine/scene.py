"""Scene graph for 4D simulations.

The `Scene` class aggregates objects and handles hierarchical transformations
as well as update dispatching to objects each simulation tick.
"""
from __future__ import annotations

from typing import List

from hypersim.objects import Hypercube  # Future: generic `Object4D` base class


class Scene:
    """A collection of 4D objects and their relationships."""

    def __init__(self) -> None:
        self._objects: List[object] = []

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def add(self, obj: object) -> None:
        """Add an object (e.g., `Hypercube`) to the scene."""
        self._objects.append(obj)

    def objects(self) -> List[object]:
        """Return objects currently in the scene (read-only)."""
        return list(self._objects)

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------
    def update(self, dt: float) -> None:
        """Update all objects in the scene.

        Args:
            dt: Delta-time (seconds) since last update.
        """
        # Placeholder: Objects may implement an `update(dt)` method.
        for obj in self._objects:
            update_fn = getattr(obj, "update", None)
            if callable(update_fn):
                update_fn(dt)
