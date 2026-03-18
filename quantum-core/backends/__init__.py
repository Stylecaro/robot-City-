"""
Módulo de backends cuánticos para Ciudad Robot.

Proporciona:
    - ``LocalSimulator``: Simulador local usando numpy (sin hardware real).
    - ``IBMQBackend``: Plantilla para integración con IBM Quantum (requiere API key).
"""

from .local_simulator import LocalSimulator
from .ibm_quantum import IBMQBackend

__all__ = ["LocalSimulator", "IBMQBackend"]
