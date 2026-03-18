"""
Tests unitarios para los algoritmos cuánticos de quantum-core.

Ejecutar con::

    cd quantum-core
    pytest tests/test_algorithms.py -v
"""

# MIT License — Copyright (c) 2026 Ciudad Robot Team

import sys
import os

# Añadir la carpeta raíz de quantum-core al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from algorithms.qaoa_maxcut import run_qaoa_maxcut
from algorithms.grover_search import grover_search


class TestQAOAMaxCut:
    """Tests para la función run_qaoa_maxcut."""

    def test_devuelve_dict(self):
        """El resultado debe ser un diccionario."""
        grafo = {"nodos": [0, 1], "aristas": [(0, 1)]}
        resultado = run_qaoa_maxcut(grafo)
        assert isinstance(resultado, dict)

    def test_campo_algoritmo(self):
        """El campo 'algoritmo' debe ser 'QAOA-MaxCut'."""
        grafo = {"nodos": [0, 1, 2], "aristas": [(0, 1), (1, 2)]}
        resultado = run_qaoa_maxcut(grafo, p=2)
        assert resultado["algoritmo"] == "QAOA-MaxCut"

    def test_campo_p(self):
        """El campo 'p' debe coincidir con el parámetro pasado."""
        grafo = {"nodos": [0], "aristas": []}
        resultado = run_qaoa_maxcut(grafo, p=3)
        assert resultado["p"] == 3

    def test_nodos_y_aristas_en_resultado(self):
        """Los nodos y aristas del grafo deben aparecer en el resultado."""
        nodos = [0, 1, 2]
        aristas = [(0, 1), (1, 2)]
        resultado = run_qaoa_maxcut({"nodos": nodos, "aristas": aristas})
        assert resultado["nodos"] == nodos
        assert resultado["aristas"] == aristas

    def test_grafo_vacio(self):
        """Debe funcionar con un grafo vacío sin lanzar excepciones."""
        resultado = run_qaoa_maxcut({})
        assert resultado["nodos"] == []
        assert resultado["aristas"] == []

    def test_solucion_placeholder(self):
        """La solución aproximada debe ser None (plantilla)."""
        resultado = run_qaoa_maxcut({"nodos": [0, 1], "aristas": [(0, 1)]})
        assert resultado["solucion_aproximada"] is None


class TestGroverSearch:
    """Tests para la función grover_search."""

    def test_devuelve_dict(self):
        """El resultado debe ser un diccionario."""
        resultado = grover_search([], n_iters=1)
        assert isinstance(resultado, dict)

    def test_campo_algoritmo(self):
        """El campo 'algoritmo' debe ser 'Grover'."""
        resultado = grover_search([lambda x: x == 1], n_iters=2)
        assert resultado["algoritmo"] == "Grover"

    def test_n_iteraciones(self):
        """El campo 'n_iteraciones' debe coincidir con el parámetro."""
        resultado = grover_search([], n_iters=5)
        assert resultado["n_iteraciones"] == 5

    def test_n_oraculos(self):
        """El campo 'n_oraculos' debe reflejar el número de oráculos."""
        oraculos = [lambda x: x == 0, lambda x: x == 1]
        resultado = grover_search(oraculos)
        assert resultado["n_oraculos"] == 2

    def test_sin_oraculos(self):
        """Debe funcionar sin oráculos."""
        resultado = grover_search([])
        assert resultado["n_oraculos"] == 0

    def test_estado_encontrado_placeholder(self):
        """El estado encontrado debe ser None (plantilla)."""
        resultado = grover_search([lambda x: True])
        assert resultado["estado_encontrado"] is None
