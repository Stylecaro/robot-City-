# MIT License - Copyright (c) 2026 Ciudad Robot Team
"""
Tests básicos para los algoritmos cuánticos del módulo quantum-core.

Ejecutar con: pytest quantum-core/tests/test_algorithms.py -v
"""

import sys
import os

# Añadir el directorio raíz de quantum-core al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from algorithms.qaoa_maxcut import run_qaoa_maxcut
from algorithms.grover_search import grover_search


# ---------------------------------------------------------------------------
# Tests para run_qaoa_maxcut
# ---------------------------------------------------------------------------

class TestRunQaoaMaxcut:
    """Tests para la función run_qaoa_maxcut."""

    def test_retorna_dict(self):
        """La función debe devolver un diccionario."""
        grafo = {"nodos": [0, 1], "aristas": [(0, 1)]}
        resultado = run_qaoa_maxcut(grafo)
        assert isinstance(resultado, dict)

    def test_claves_presentes(self):
        """El resultado debe contener las claves esperadas."""
        grafo = {"nodos": [0, 1, 2], "aristas": [(0, 1), (1, 2)]}
        resultado = run_qaoa_maxcut(grafo, p=1)
        assert "corte_maximo" in resultado
        assert "particion" in resultado
        assert "probabilidades" in resultado
        assert "capas_p" in resultado

    def test_corte_es_entero(self):
        """El valor del corte máximo debe ser un entero no negativo."""
        grafo = {"nodos": [0, 1, 2, 3], "aristas": [(0, 1), (1, 2), (2, 3), (3, 0)]}
        resultado = run_qaoa_maxcut(grafo, p=2)
        assert isinstance(resultado["corte_maximo"], int)
        assert resultado["corte_maximo"] >= 0

    def test_capas_p_correctas(self):
        """El campo capas_p debe coincidir con el parámetro p."""
        grafo = {"nodos": [0, 1], "aristas": [(0, 1)]}
        for p in [1, 2, 3]:
            resultado = run_qaoa_maxcut(grafo, p=p)
            assert resultado["capas_p"] == p

    def test_particion_cubre_todos_los_nodos(self):
        """La partición debe cubrir todos los nodos del grafo."""
        nodos = [0, 1, 2, 3]
        grafo = {"nodos": nodos, "aristas": [(0, 1), (2, 3)]}
        resultado = run_qaoa_maxcut(grafo)
        nodos_en_particion = set(resultado["particion"][0]) | set(resultado["particion"][1])
        assert nodos_en_particion == set(nodos)

    def test_grafo_vacio(self):
        """Con un grafo vacío, el corte debe ser 0."""
        grafo = {"nodos": [], "aristas": []}
        resultado = run_qaoa_maxcut(grafo)
        assert resultado["corte_maximo"] == 0
        assert resultado["particion"] == [[], []]

    def test_probabilidades_suman_aproximadamente_uno(self):
        """Las probabilidades deben sumar aproximadamente 1."""
        grafo = {"nodos": [0, 1, 2], "aristas": [(0, 1), (1, 2)]}
        resultado = run_qaoa_maxcut(grafo)
        total = sum(resultado["probabilidades"].values())
        assert abs(total - 1.0) < 0.05


# ---------------------------------------------------------------------------
# Tests para grover_search
# ---------------------------------------------------------------------------

class TestGroverSearch:
    """Tests para la función grover_search."""

    def test_retorna_dict(self):
        """La función debe devolver un diccionario."""
        oraculo = [lambda s: s == "10"]
        resultado = grover_search(oraculo)
        assert isinstance(resultado, dict)

    def test_claves_presentes(self):
        """El resultado debe contener las claves esperadas."""
        oraculo = [lambda s: s == "01"]
        resultado = grover_search(oraculo, n_iters=1)
        assert "estado_encontrado" in resultado
        assert "probabilidad" in resultado
        assert "iteraciones" in resultado
        assert "conteos" in resultado

    def test_iteraciones_correctas(self):
        """El campo iteraciones debe coincidir con n_iters."""
        oraculo = [lambda s: s == "11"]
        for n in [1, 2, 3]:
            resultado = grover_search(oraculo, n_iters=n)
            assert resultado["iteraciones"] == n

    def test_probabilidad_en_rango(self):
        """La probabilidad del estado encontrado debe estar en [0, 1]."""
        oraculo = [lambda s: s == "10"]
        resultado = grover_search(oraculo, n_iters=1)
        assert 0.0 <= resultado["probabilidad"] <= 1.0

    def test_oracles_vacios(self):
        """Con lista de oráculos vacía, el estado encontrado debe ser vacío."""
        resultado = grover_search([], n_iters=1)
        assert resultado["estado_encontrado"] == ""
        assert resultado["probabilidad"] == 0.0

    def test_conteos_suman_shots(self):
        """Los conteos deben sumar 1024 (shots por defecto)."""
        oraculo = [lambda s: s == "11"]
        resultado = grover_search(oraculo, n_iters=1)
        total_shots = sum(resultado["conteos"].values())
        assert total_shots == 1024

    def test_estado_encontrado_es_bitstring(self):
        """El estado encontrado debe ser un bitstring válido."""
        oraculo = [lambda s: s == "10"]
        resultado = grover_search(oraculo)
        estado = resultado["estado_encontrado"]
        assert all(c in "01" for c in estado)
        assert len(estado) > 0
