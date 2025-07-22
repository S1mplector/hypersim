"""Third-party integrations (optional back-ends).

Place integration modules here. Each integration should declare its extra
runtime dependencies in `pyproject.toml` via an optional dependency group, e.g.

[project.optional-dependencies.opengl]
PyOpenGL = "*"

Then, guard imports so the core library never hard-requires them unless the
user installs the extra.
"""

__all__: list[str] = []
