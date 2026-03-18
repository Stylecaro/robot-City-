"""
Módulo de circuitos cuánticos para Ciudad Robot.

Proporciona circuitos de ejemplo para semáforos cuánticos y capas
de entrelazamiento entre qubits.
"""

from .traffic_light_circuit import build_traffic_light_circuit
from .entanglement_layer import entanglement_layer

__all__ = ["build_traffic_light_circuit", "entanglement_layer"]
