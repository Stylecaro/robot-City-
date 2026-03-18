# MIT License - Copyright (c) 2026 Ciudad Robot Team
"""
Capa Neuronal Cuántica (Híbrida)
==================================
Implementación stub de una capa neuronal cuántica para redes híbridas
clásico-cuánticas. Diseñada para integrarse con el módulo ai-engine.

Esta capa puede reemplazar una capa densa clásica en una red neuronal,
aprovechando la capacidad de los circuitos cuánticos parametrizados (PQC)
para representar funciones de mayor complejidad con menos parámetros.
"""

import numpy as np


class QuantumNeuralLayer:
    """
    Capa neuronal cuántica simulada con numpy.

    Implementa una capa tipo Variational Quantum Circuit (VQC) que puede
    usarse como bloque en una red neuronal híbrida clásico-cuántica.
    Los pesos de la capa son ángulos de rotación para puertas cuánticas RY y RZ.

    Atributos
    ---------
    n_qubits : int
        Número de qubits de la capa cuántica.
    n_layers : int
        Número de capas de puertas parametrizadas (profundidad del ansatz).
    weights : numpy.ndarray
        Pesos (ángulos) entrenables de forma (n_layers, n_qubits, 2).
    """

    def __init__(self, n_qubits=4, n_layers=2, seed=None):
        """
        Inicializa la capa neuronal cuántica.

        Parámetros
        ----------
        n_qubits : int
            Número de qubits. Por defecto 4.
        n_layers : int
            Profundidad del circuito ansatz. Por defecto 2.
        seed : int o None
            Semilla para inicialización de pesos. Por defecto None.
        """
        self.n_qubits = n_qubits
        self.n_layers = n_layers
        rng = np.random.default_rng(seed=seed)
        # Inicialización aleatoria de ángulos en [-π, π]
        self.weights = rng.uniform(-np.pi, np.pi, size=(n_layers, n_qubits, 2))

    def forward(self, inputs):
        """
        Pasa las entradas a través de la capa cuántica simulada.

        El proceso simula:
        1. Codificación de las entradas como ángulos de rotación (encoding layer).
        2. Capas de puertas parametrizadas RY y RZ con entrelazamiento CNOT.
        3. Medición de expectativas en la base Z (valores en [-1, 1]).

        Parámetros
        ----------
        inputs : array-like
            Vector de entrada de longitud n_qubits (valores normalizados en [-π, π]).

        Retorna
        -------
        numpy.ndarray
            Vector de salida de longitud n_qubits con valores de expectación
            simulados en el intervalo [-1, 1].

        Ejemplo
        -------
        >>> capa = QuantumNeuralLayer(n_qubits=4, n_layers=2, seed=0)
        >>> entrada = np.array([0.5, -0.3, 1.2, 0.0])
        >>> salida = capa.forward(entrada)
        >>> print(salida.shape)
        (4,)
        >>> print(all(-1 <= v <= 1 for v in salida))
        True

        Notas
        -----
        Esta implementación usa transformaciones matriciales numpy como placeholder.
        Para integración con TensorFlow/PyTorch + Qiskit, usar PennyLane o
        qiskit-machine-learning con QuantumKernel o SamplerQNN.
        """
        inputs = np.asarray(inputs, dtype=float)
        if inputs.shape != (self.n_qubits,):
            raise ValueError(
                f"Se esperan {self.n_qubits} entradas, se recibieron {inputs.shape}"
            )

        # Estado inicial: amplitudes codificadas desde las entradas
        estado = np.sin(inputs) + np.cos(inputs) * 0.5

        # Aplicar capas parametrizadas simuladas
        for layer in range(self.n_layers):
            # Rotaciones RY y RZ con los pesos de esta capa
            ry_angles = self.weights[layer, :, 0]
            rz_angles = self.weights[layer, :, 1]

            estado = estado * np.cos(ry_angles) + np.sin(ry_angles) * 0.5
            estado = estado * np.cos(rz_angles)

            # Entrelazamiento simulado: mezcla entre qubits vecinos
            estado = np.roll(estado, 1) * 0.3 + estado * 0.7

        # Proyectar salida al intervalo [-1, 1] (valores de expectación Z)
        salida = np.tanh(estado)
        return salida

    def get_weights(self):
        """Devuelve los pesos actuales de la capa."""
        return self.weights.copy()

    def set_weights(self, new_weights):
        """
        Actualiza los pesos de la capa.

        Parámetros
        ----------
        new_weights : numpy.ndarray
            Nuevos pesos de forma (n_layers, n_qubits, 2).
        """
        expected = (self.n_layers, self.n_qubits, 2)
        if np.asarray(new_weights).shape != expected:
            raise ValueError(f"Los pesos deben tener forma {expected}")
        self.weights = np.asarray(new_weights, dtype=float)

    def __repr__(self):
        return (
            f"QuantumNeuralLayer(n_qubits={self.n_qubits}, "
            f"n_layers={self.n_layers})"
        )


if __name__ == "__main__":
    print("=== Capa Neuronal Cuántica - Demo ===")
    capa = QuantumNeuralLayer(n_qubits=4, n_layers=2, seed=0)
    entrada = np.array([0.5, -0.3, 1.2, 0.0])
    salida = capa.forward(entrada)
    print(f"Entrada:  {entrada}")
    print(f"Salida:   {salida}")
    print(f"Forma:    {salida.shape}")
    print(f"Rango:    [{salida.min():.4f}, {salida.max():.4f}]")
