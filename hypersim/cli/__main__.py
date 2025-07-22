"""Entry-point so that ``python -m hypersim.cli`` works.

This thin wrapper simply calls :pyfunc:`hypersim.cli.main`.
"""
from . import main as _main

if __name__ == "__main__":
    _main()
