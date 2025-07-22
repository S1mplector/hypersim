"""Basic simulation loop utilities."""
from __future__ import annotations

import time
from typing import Callable, Optional

from hypersim.engine.scene import Scene


class Simulation:
    """Run a simple real-time simulation loop on a `Scene`."""

    def __init__(self, scene: Scene, tick: float = 1 / 60.0) -> None:
        self.scene = scene
        self.tick = tick  # seconds per frame
        self._running = False
        self._on_step: Optional[Callable[[float], None]] = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def set_step_callback(self, fn: Callable[[float], None]) -> None:
        """Register a callback executed each tick after scene update."""
        self._on_step = fn

    def run(self, duration: float | None = None) -> None:
        """Run the simulation. If duration is None, run indefinitely."""
        self._running = True
        start = time.perf_counter()
        last = start
        while self._running:
            now = time.perf_counter()
            dt = now - last
            if dt < self.tick:
                time.sleep(self.tick - dt)
                continue
            last = now
            self.scene.update(dt)
            if self._on_step is not None:
                self._on_step(dt)
            if duration is not None and now - start >= duration:
                break

    def stop(self) -> None:
        """Stop the simulation loop."""
        self._running = False
