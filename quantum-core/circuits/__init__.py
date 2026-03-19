# MIT License - Copyright (c) 2026 Ciudad Robot Team
"""
Paquete de Circuitos Cuánticos - quantum-core
==============================================
Exporta las funciones principales de construcción de circuitos cuánticos.
"""

from .traffic_light_circuit import build_traffic_light_circuit
from .entanglement_layer import entanglement_layer, hadamard, cnot

__all__ = [
    "build_traffic_light_circuit",
    "entanglement_layer",
    "hadamard",
    "cnot",
]
