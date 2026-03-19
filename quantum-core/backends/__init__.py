# MIT License - Copyright (c) 2026 Ciudad Robot Team
"""
Paquete de Backends Cuánticos - quantum-core
=============================================
Exporta las clases de backends disponibles para ejecución de circuitos.
"""

from .local_simulator import LocalSimulator
from .ibm_quantum import IBMQBackend

__all__ = ["LocalSimulator", "IBMQBackend"]
