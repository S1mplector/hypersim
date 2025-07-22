"""Simple plugin registry for hypersim extensions."""
from __future__ import annotations

from typing import Callable, Dict, Type


class PluginRegistry:
    """Global registry for named plugins.

    Plugins can register initialization callbacks that will receive the engine
    context (e.g., Scene) at runtime.
    """

    _registry: Dict[str, Callable[..., None]] = {}

    # ------------------------------------------------------------------
    # Registration API
    # ------------------------------------------------------------------
    @classmethod
    def register(cls, name: str, callback: Callable[..., None]) -> None:
        if name in cls._registry:
            raise ValueError(f"Plugin '{name}' already registered")
        cls._registry[name] = callback

    @classmethod
    def unregister(cls, name: str) -> None:
        cls._registry.pop(name, None)

    @classmethod
    def invoke(cls, name: str, *args, **kwargs):
        if name not in cls._registry:
            raise KeyError(f"Plugin '{name}' not found")
        return cls._registry[name](*args, **kwargs)

    @classmethod
    def all_plugins(cls):
        return dict(cls._registry)
