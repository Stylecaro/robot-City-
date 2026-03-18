"""
Tests unitarios para los circuitos cuánticos de quantum-core.

Ejecutar con::

    cd quantum-core
    pytest tests/test_circuits.py -v
"""

# MIT License — Copyright (c) 2026 Ciudad Robot Team

import sys
import os

import numpy as np
import pytest

# Añadir la carpeta raíz de quantum-core al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from circuits.traffic_light_circuit import build_traffic_light_circuit
from circuits.entanglement_layer import entanglement_layer
from backends.local_simulator import LocalSimulator


class TestTrafficLightCircuit:
    """Tests para build_traffic_light_circuit."""

    def test_devuelve_dict(self):
        """El resultado debe ser un diccionario."""
        circuito = build_traffic_light_circuit()
        assert isinstance(circuito, dict)

    def test_nombre_circuito(self):
        """El nombre debe ser 'SemaforoQuantico'."""
        circuito = build_traffic_light_circuit()
        assert circuito["nombre"] == "SemaforoQuantico"

    def test_numero_qubits(self):
        """Debe usar 2 qubits."""
        circuito = build_traffic_light_circuit()
        assert circuito["qubits"] == 2

    def test_amplitudes_longitud(self):
        """Debe haber 4 amplitudes (2^2)."""
        circuito = build_traffic_light_circuit()
        assert len(circuito["amplitudes"]) == 4

    def test_amplitudes_normalizadas(self):
        """Las amplitudes deben estar normalizadas (suma de cuadrados ≈ 1)."""
        circuito = build_traffic_light_circuit()
        suma = sum(a ** 2 for a in circuito["amplitudes"])
        assert abs(suma - 1.0) < 1e-9

    def test_matriz_4x4(self):
        """La matriz debe ser 4×4."""
        circuito = build_traffic_light_circuit()
        assert len(circuito["matriz"]) == 4
        assert all(len(fila) == 4 for fila in circuito["matriz"])

    def test_estados_lista(self):
        """El campo 'estados' debe ser una lista."""
        circuito = build_traffic_light_circuit()
        assert isinstance(circuito["estados"], list)
        assert len(circuito["estados"]) > 0


class TestEntanglementLayer:
    """Tests para entanglement_layer."""

    def test_forma_matriz_2_qubits(self):
        """Para 2 qubits la matriz debe ser 4×4."""
        M = entanglement_layer(2)
        assert M.shape == (4, 4)

    def test_forma_matriz_3_qubits(self):
        """Para 3 qubits la matriz debe ser 8×8."""
        M = entanglement_layer(3)
        assert M.shape == (8, 8)

    def test_unitaria_2_qubits(self):
        """La matriz debe ser unitaria: M @ M†  ≈ I."""
        M = entanglement_layer(2)
        producto = M @ M.conj().T
        assert np.allclose(producto, np.eye(4), atol=1e-10)

    def test_unitaria_3_qubits(self):
        """La matriz de 3 qubits debe ser unitaria."""
        M = entanglement_layer(3)
        producto = M @ M.conj().T
        assert np.allclose(producto, np.eye(8), atol=1e-10)

    def test_error_menos_de_2_qubits(self):
        """Debe lanzar ValueError si n_qubits < 2."""
        with pytest.raises(ValueError):
            entanglement_layer(1)


class TestLocalSimulator:
    """Tests para LocalSimulator."""

    def test_devuelve_dict(self):
        """El resultado debe ser un diccionario."""
        sim = LocalSimulator(shots=10)
        circuito = build_traffic_light_circuit()
        resultado = sim.run(circuito)
        assert isinstance(resultado, dict)

    def test_backend_nombre(self):
        """El campo 'backend' debe ser 'LocalSimulator'."""
        sim = LocalSimulator(shots=10)
        resultado = sim.run({"amplitudes": [1.0, 0.0], "matriz": None})
        assert resultado["backend"] == "LocalSimulator"

    def test_shots_correctos(self):
        """El número de shots debe coincidir con el configurado."""
        sim = LocalSimulator(shots=50)
        resultado = sim.run({"amplitudes": [1.0, 0.0], "matriz": None})
        assert resultado["shots"] == 50
        assert sum(resultado["conteos"].values()) == 50

    def test_probabilidades_normalizadas(self):
        """Las probabilidades deben sumar ≈ 1."""
        sim = LocalSimulator(shots=100)
        circuito = build_traffic_light_circuit()
        resultado = sim.run(circuito)
        suma = sum(resultado["probabilidades"])
        assert abs(suma - 1.0) < 1e-9

    def test_estado_clasico(self):
        """Estado |0⟩ puro debe tener conteos concentrados en el primer estado."""
        sim = LocalSimulator(shots=1000)
        resultado = sim.run({"amplitudes": [1.0, 0.0], "matriz": None})
        # El primer estado debe tener todos los shots
        assert resultado["conteos"]["0"] == 1000
