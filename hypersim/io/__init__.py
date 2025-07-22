"""I/O adapters for hypersim.

This subpackage handles loading/saving scenes, objects, and configuration
files in various formats (JSON, YAML, custom binary, etc.).

The public API intentionally remains minimal at this stage; concrete loaders
and writers can be registered via the `register_loader`/`register_writer`
helpers for plugin-like extensibility.
"""
from __future__ import annotations

from typing import Callable, Dict

_loaders: Dict[str, Callable[[str], object]] = {}
_writers: Dict[str, Callable[[object, str], None]] = {}


def register_loader(ext: str, fn: Callable[[str], object]) -> None:
    """Register a loader for a given file extension (e.g. 'json')."""
    _loaders[ext.lower()] = fn


def register_writer(ext: str, fn: Callable[[object, str], None]) -> None:
    """Register a writer for a given file extension (e.g. 'yaml')."""
    _writers[ext.lower()] = fn


def load(path: str):  # noqa: D401  # simple utility
    """Load an object from *path* using the registered loader."""
    ext = path.rsplit('.', 1)[-1].lower()
    if ext not in _loaders:
        raise ValueError(f"No loader registered for *.{ext}* files")
    return _loaders[ext](path)


def save(obj: object, path: str) -> None:
    """Save *obj* to *path* using the registered writer."""
    ext = path.rsplit('.', 1)[-1].lower()
    if ext not in _writers:
        raise ValueError(f"No writer registered for *.{ext}* files")
    _writers[ext](obj, path)

__all__ = [
    "register_loader",
    "register_writer",
    "load",
    "save",
]
