# MIT License - Usar misma licencia que el repositorio
"""
Módulo algorithms de quantum-core.

Exporta los stubs de algoritmos cuánticos disponibles.
"""

from .qaoa_maxcut import run_qaoa_maxcut
from .grover_search import grover_search

__all__ = ["run_qaoa_maxcut", "grover_search"]
