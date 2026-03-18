# MIT License - Usar misma licencia que el repositorio
"""
Tests para los algoritmos cuánticos de quantum-core.

Ejecutar con:
    pytest quantum-core/tests/test_algorithms.py
"""

import sys
import os

# Añadir la raíz del módulo al path para importación directa
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from algorithms.qaoa_maxcut import run_qaoa_maxcut
from algorithms.grover_search import grover_search


class TestQAOAMaxcut:
    """Tests para el algoritmo QAOA MaxCut."""

    def test_retorna_dict(self):
        """El resultado debe ser un diccionario."""
        resultado = run_qaoa_maxcut(graph=[(0, 1)])
        assert isinstance(resultado, dict)

    def test_claves_esperadas(self):
        """El resultado debe contener las claves esperadas."""
        resultado = run_qaoa_maxcut(graph=[(0, 1), (1, 2)])
        assert "result" in resultado
        assert "info" in resultado
        assert "graph" in resultado
        assert "p" in resultado

    def test_info_es_stub(self):
        """El campo info debe indicar que es un stub."""
        resultado = run_qaoa_maxcut(graph=[])
        assert "stub" in resultado["info"].lower()

    def test_graph_se_conserva(self):
        """El grafo recibido debe conservarse en el resultado."""
        grafo = [(0, 1), (2, 3)]
        resultado = run_qaoa_maxcut(graph=grafo, p=2)
        assert resultado["p"] == 2
        assert len(resultado["graph"]) == 2

    def test_grafo_vacio(self):
        """Debe funcionar con un grafo vacío."""
        resultado = run_qaoa_maxcut(graph=[])
        assert resultado["graph"] == []


class TestGroverSearch:
    """Tests para el algoritmo de búsqueda de Grover."""

    def test_retorna_dict(self):
        """El resultado debe ser un diccionario."""
        resultado = grover_search(oracles=["estado_0"])
        assert isinstance(resultado, dict)

    def test_claves_esperadas(self):
        """El resultado debe contener las claves esperadas."""
        resultado = grover_search(oracles=["estado_0"])
        assert "result" in resultado
        assert "info" in resultado
        assert "oracles" in resultado
        assert "n_iters" in resultado

    def test_info_es_stub(self):
        """El campo info debe indicar que es un stub."""
        resultado = grover_search(oracles=[])
        assert "stub" in resultado["info"].lower()

    def test_n_iters_por_defecto(self):
        """El valor por defecto de n_iters debe ser 1."""
        resultado = grover_search(oracles=["x"])
        assert resultado["n_iters"] == 1

    def test_n_iters_personalizado(self):
        """Debe respetar el valor de n_iters proporcionado."""
        resultado = grover_search(oracles=["x", "y"], n_iters=5)
        assert resultado["n_iters"] == 5
        assert len(resultado["oracles"]) == 2
