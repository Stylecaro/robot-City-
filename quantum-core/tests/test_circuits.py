# MIT License - Copyright (c) 2026 Ciudad Robot Team
"""
Tests básicos para los circuitos cuánticos del módulo quantum-core.

Ejecutar con: pytest quantum-core/tests/test_circuits.py -v
"""

import sys
import os

import numpy as np

# Añadir el directorio raíz de quantum-core al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from circuits.traffic_light_circuit import build_traffic_light_circuit
from circuits.entanglement_layer import entanglement_layer, hadamard, cnot
from backends.local_simulator import LocalSimulator
from hybrid.quantum_neural_layer import QuantumNeuralLayer


# ---------------------------------------------------------------------------
# Tests para build_traffic_light_circuit
# ---------------------------------------------------------------------------

class TestBuildTrafficLightCircuit:
    """Tests para la función build_traffic_light_circuit."""

    def test_retorna_dict(self):
        """La función debe devolver un diccionario."""
        resultado = build_traffic_light_circuit()
        assert isinstance(resultado, dict)

    def test_claves_presentes(self):
        """El resultado debe contener las claves esperadas."""
        resultado = build_traffic_light_circuit()
        assert "circuit_name" in resultado
        assert "n_qubits" in resultado
        assert "gates" in resultado
        assert "measurements" in resultado
        assert "params" in resultado

    def test_valores_por_defecto(self):
        """Con params=None, debe usar valores por defecto."""
        resultado = build_traffic_light_circuit(None)
        assert resultado["circuit_name"] == "traffic_light"
        assert resultado["n_qubits"] == 3

    def test_params_personalizados(self):
        """Los parámetros personalizados deben reflejarse en el resultado."""
        params = {"theta": 1.5, "phi": 0.3, "n_qubits": 4, "circuit_name": "test"}
        resultado = build_traffic_light_circuit(params)
        assert resultado["params"]["theta"] == 1.5
        assert resultado["params"]["phi"] == 0.3
        assert resultado["n_qubits"] == 4
        assert resultado["circuit_name"] == "test"

    def test_measurements_cubren_todos_qubits(self):
        """La lista de measurements debe cubrir todos los qubits."""
        for n in [2, 3, 4]:
            resultado = build_traffic_light_circuit({"n_qubits": n})
            assert len(resultado["measurements"]) == n

    def test_gates_es_lista(self):
        """El campo gates debe ser una lista."""
        resultado = build_traffic_light_circuit()
        assert isinstance(resultado["gates"], list)
        assert len(resultado["gates"]) >= 1

    def test_cada_puerta_tiene_nombre(self):
        """Cada puerta debe tener al menos la clave 'gate'."""
        resultado = build_traffic_light_circuit()
        for puerta in resultado["gates"]:
            assert "gate" in puerta


# ---------------------------------------------------------------------------
# Tests para entanglement_layer
# ---------------------------------------------------------------------------

class TestEntanglementLayer:
    """Tests para la función entanglement_layer."""

    def test_retorna_array_numpy(self):
        """Debe devolver un array numpy."""
        estado = entanglement_layer(2)
        assert isinstance(estado, np.ndarray)

    def test_dimension_correcta(self):
        """La dimensión debe ser 2^n_qubits."""
        for n in [1, 2, 3, 4]:
            estado = entanglement_layer(n)
            assert estado.shape == (2**n,)

    def test_norma_unitaria(self):
        """El estado cuántico debe estar normalizado (norma ≈ 1)."""
        for n in [1, 2, 3]:
            estado = entanglement_layer(n)
            norma = np.linalg.norm(estado)
            assert abs(norma - 1.0) < 1e-10

    def test_n_qubits_invalido(self):
        """Con n_qubits < 1 debe lanzar ValueError."""
        import pytest
        with pytest.raises(ValueError):
            entanglement_layer(0)

    def test_hadamard_dimension(self):
        """La matriz Hadamard debe tener dimensión correcta."""
        for n in [1, 2, 3]:
            H = hadamard(n)
            assert H.shape == (2**n, 2**n)

    def test_cnot_dimension(self):
        """La matriz CNOT debe tener dimensión correcta."""
        for n in [2, 3]:
            C = cnot(n)
            assert C.shape == (2**n, 2**n)


# ---------------------------------------------------------------------------
# Tests para LocalSimulator
# ---------------------------------------------------------------------------

class TestLocalSimulator:
    """Tests para la clase LocalSimulator."""

    def test_instancia_correcta(self):
        """Debe poder instanciar LocalSimulator."""
        sim = LocalSimulator(shots=512, seed=0)
        assert sim.shots == 512
        assert sim.seed == 0

    def test_run_retorna_dict(self):
        """run() debe devolver un diccionario."""
        sim = LocalSimulator(shots=100, seed=0)
        circuito = {"n_qubits": 2, "gates": [], "measurements": [0, 1]}
        resultado = sim.run(circuito)
        assert isinstance(resultado, dict)

    def test_conteos_suman_shots(self):
        """Los conteos deben sumar el número de shots."""
        shots = 256
        sim = LocalSimulator(shots=shots, seed=1)
        circuito = {"n_qubits": 2, "gates": [{"gate": "H", "qubits": [0]}], "measurements": [0, 1]}
        resultado = sim.run(circuito)
        assert sum(resultado["conteos"].values()) == shots

    def test_backend_es_local_simulator(self):
        """El campo backend debe indicar 'local_simulator'."""
        sim = LocalSimulator()
        circuito = {"n_qubits": 1, "gates": [], "measurements": [0]}
        resultado = sim.run(circuito)
        assert resultado["backend"] == "local_simulator"

    def test_run_requiere_dict(self):
        """run() debe lanzar TypeError si el circuito no es dict."""
        import pytest
        sim = LocalSimulator()
        with pytest.raises(TypeError):
            sim.run("no_es_dict")


# ---------------------------------------------------------------------------
# Tests para QuantumNeuralLayer
# ---------------------------------------------------------------------------

class TestQuantumNeuralLayer:
    """Tests para la clase QuantumNeuralLayer."""

    def test_instancia_correcta(self):
        """Debe poder instanciar QuantumNeuralLayer."""
        capa = QuantumNeuralLayer(n_qubits=4, n_layers=2, seed=0)
        assert capa.n_qubits == 4
        assert capa.n_layers == 2

    def test_forward_retorna_array(self):
        """forward() debe devolver un array numpy."""
        capa = QuantumNeuralLayer(n_qubits=4, n_layers=2, seed=0)
        entrada = np.array([0.5, -0.3, 1.2, 0.0])
        salida = capa.forward(entrada)
        assert isinstance(salida, np.ndarray)

    def test_forward_dimension_correcta(self):
        """La salida debe tener la misma dimensión que la entrada."""
        n = 4
        capa = QuantumNeuralLayer(n_qubits=n, n_layers=2, seed=0)
        entrada = np.zeros(n)
        salida = capa.forward(entrada)
        assert salida.shape == (n,)

    def test_forward_valores_en_rango(self):
        """Los valores de salida deben estar en [-1, 1]."""
        capa = QuantumNeuralLayer(n_qubits=4, n_layers=2, seed=0)
        entrada = np.array([1.0, -1.0, 0.5, -0.5])
        salida = capa.forward(entrada)
        assert all(-1.0 <= v <= 1.0 for v in salida)

    def test_forward_entrada_incorrecta(self):
        """forward() debe lanzar ValueError con entrada de tamaño incorrecto."""
        import pytest
        capa = QuantumNeuralLayer(n_qubits=4, n_layers=2, seed=0)
        with pytest.raises(ValueError):
            capa.forward(np.array([1.0, 2.0]))  # Solo 2 elementos para 4 qubits
