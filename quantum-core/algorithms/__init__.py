"""
Módulo de algoritmos cuánticos para Ciudad Robot.

Contiene implementaciones y plantillas de algoritmos cuánticos principales:
- QAOA (Quantum Approximate Optimization Algorithm)
- Búsqueda de Grover
"""

from .qaoa_maxcut import run_qaoa_maxcut
from .grover_search import grover_search

__all__ = ["run_qaoa_maxcut", "grover_search"]
