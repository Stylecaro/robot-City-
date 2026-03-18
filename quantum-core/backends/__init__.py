# MIT License - Usar misma licencia que el repositorio
"""
Módulo backends de quantum-core.

Exporta los backends disponibles para ejecución de circuitos cuánticos.
"""

from .local_simulator import LocalSimulator
from .ibm_quantum import IBMQBackend

__all__ = ["LocalSimulator", "IBMQBackend"]
