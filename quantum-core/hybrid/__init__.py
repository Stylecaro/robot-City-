"""
Módulo híbrido cuántico-clásico para Ciudad Robot.

Proporciona capas neuronales cuánticas simuladas que pueden integrarse
con redes neuronales clásicas (PyTorch, TensorFlow) como capas personalizadas.
"""

from .quantum_neural_layer import QuantumNeuralLayer

__all__ = ["QuantumNeuralLayer"]
