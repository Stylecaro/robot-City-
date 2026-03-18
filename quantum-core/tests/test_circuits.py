# MIT License - Usar misma licencia que el repositorio
"""
Tests para los circuitos cuánticos de quantum-core.

Ejecutar con:
    pytest quantum-core/tests/test_circuits.py
"""

import sys
import os

import numpy as np

# Añadir la raíz del módulo al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from circuits.traffic_light_circuit import build_traffic_light_circuit
from circuits.entanglement_layer import entanglement_layer


class TestTrafficLightCircuit:
    """Tests para el circuito de semáforo cuántico."""

    def test_retorna_dict(self):
        """El resultado debe ser un diccionario."""
        circuito = build_traffic_light_circuit()
        assert isinstance(circuito, dict)

    def test_claves_esperadas(self):
        """El resultado debe contener las claves esperadas."""
        circuito = build_traffic_light_circuit()
        assert "name" in circuito
        assert "qubits" in circuito
        assert "gates" in circuito
        assert "measurements" in circuito

    def test_numero_qubits_por_defecto(self):
        """Sin parámetros, debe usar 3 qubits."""
        circuito = build_traffic_light_circuit()
        assert circuito["qubits"] == 3

    def test_numero_qubits_personalizado(self):
        """Debe respetar el número de qubits especificado."""
        circuito = build_traffic_light_circuit(params={"qubits": 4})
        assert circuito["qubits"] == 4

    def test_gates_es_lista(self):
        """El campo gates debe ser una lista."""
        circuito = build_traffic_light_circuit()
        assert isinstance(circuito["gates"], list)

    def test_measurements_es_lista(self):
        """El campo measurements debe ser una lista."""
        circuito = build_traffic_light_circuit()
        assert isinstance(circuito["measurements"], list)

    def test_measurements_por_qubit(self):
        """Debe haber una medición por qubit."""
        for n in [2, 3, 5]:
            circuito = build_traffic_light_circuit(params={"qubits": n})
            assert len(circuito["measurements"]) == n

    def test_params_none(self):
        """Debe funcionar con params=None."""
        circuito = build_traffic_light_circuit(params=None)
        assert circuito["qubits"] == 3


class TestEntanglementLayer:
    """Tests para la capa de entrelazamiento cuántico."""

    def test_retorna_matriz_numpy(self):
        """El resultado debe ser un array numpy."""
        resultado = entanglement_layer(n_qubits=2)
        assert isinstance(resultado, np.ndarray)

    def test_dimension_correcta(self):
        """La dimensión debe ser 2^n x 2^n."""
        for n in [1, 2, 3]:
            mat = entanglement_layer(n_qubits=n)
            assert mat.shape == (2 ** n, 2 ** n)

    def test_es_unitaria(self):
        """La matriz debe ser aproximadamente unitaria (U†U ≈ I)."""
        mat = entanglement_layer(n_qubits=2)
        producto = mat.conj().T @ mat
        identidad = np.eye(mat.shape[0], dtype=complex)
        assert np.allclose(producto, identidad, atol=1e-10)

    def test_un_qubit(self):
        """Debe funcionar con un solo qubit (solo Hadamard)."""
        mat = entanglement_layer(n_qubits=1)
        assert mat.shape == (2, 2)

    def test_error_qubits_invalidos(self):
        """Debe lanzar ValueError con n_qubits < 1."""
        import pytest
        with pytest.raises(ValueError):
            entanglement_layer(n_qubits=0)
