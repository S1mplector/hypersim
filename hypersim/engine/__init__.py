"""
Application / engine layer.

Provides high-level orchestration of scenes, simulation loops, and plugin
management. Depends only on `hypersim.core` and `hypersim.objects` but not on
any concrete visualization or IO back-ends so that it can be reused across
interfaces.
"""

from .scene import Scene  # noqa: F401
from .simulation import Simulation  # noqa: F401
from .plugins import PluginRegistry  # noqa: F401

__all__ = [
    "Scene",
    "Simulation",
    "PluginRegistry",
]
