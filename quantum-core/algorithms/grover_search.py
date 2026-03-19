# MIT License - Copyright (c) 2026 Ciudad Robot Team
"""
Módulo de Búsqueda de Grover
=============================
Implementación stub del algoritmo de búsqueda de Grover para computación cuántica.

El algoritmo de Grover ofrece una aceleración cuadrática (O(√N)) respecto a la
búsqueda clásica no estructurada (O(N)). Se aplica mediante oráculos que marcan
el elemento buscado.
"""

import numpy as np


def grover_search(oracles, n_iters=1):
    """
    Ejecuta el algoritmo de búsqueda de Grover usando los oráculos proporcionados.

    El algoritmo amplifica la probabilidad de los estados marcados por los oráculos
    después de n_iters iteraciones del operador de difusión de Grover.

    Parámetros
    ----------
    oracles : list
        Lista de funciones oráculo. Cada oráculo es un callable que recibe un
        estado (str de bits) y devuelve True si ese estado es el objetivo.
        Ejemplo: [lambda s: s == "101"]
    n_iters : int, opcional
        Número de iteraciones del operador de Grover. El óptimo es
        aproximadamente π/4 * √(2^n_qubits / n_soluciones). Por defecto 1.

    Retorna
    -------
    dict
        Diccionario con los resultados:
        - "estado_encontrado": bitstring del estado más probable
        - "probabilidad": probabilidad del estado encontrado
        - "iteraciones": número de iteraciones realizadas
        - "conteos": dict con conteos simulados de medición

    Ejemplo
    -------
    >>> oraculo = [lambda s: s == "11"]
    >>> resultado = grover_search(oraculo, n_iters=1)
    >>> print(resultado["estado_encontrado"])
    '11'

    Notas
    -----
    Esta es una implementación stub con simulación numpy.
    Para hardware real, instalar qiskit y construir el circuito Grover con
    QuantumCircuit y los oráculos de fase correspondientes.
    """
    if not oracles:
        return {
            "estado_encontrado": "",
            "probabilidad": 0.0,
            "iteraciones": n_iters,
            "conteos": {},
        }

    # Determinar número de qubits basado en el número de oráculos
    n_qubits = max(2, len(oracles) + 1)
    n_estados = 2**n_qubits

    rng = np.random.default_rng(seed=7)

    # Generar amplitudes iniciales uniformes
    amplitudes = np.ones(n_estados) / np.sqrt(n_estados)

    # Simular iteraciones de Grover (stub simplificado)
    for _ in range(n_iters):
        # Aplicar oráculo: invertir fase de estados marcados
        for idx in range(n_estados):
            bits = format(idx, f"0{n_qubits}b")
            if any(oracle(bits) for oracle in oracles):
                amplitudes[idx] *= -1

        # Aplicar difusión de Grover (reflexión sobre el estado promedio)
        media = np.mean(amplitudes)
        amplitudes = 2 * media - amplitudes

    # Calcular probabilidades
    probabilidades = np.abs(amplitudes) ** 2
    probabilidades /= probabilidades.sum()  # Renormalizar

    # Simular medición
    shots = 1024
    conteos_raw = rng.multinomial(shots, probabilidades)
    conteos = {
        format(i, f"0{n_qubits}b"): int(conteos_raw[i])
        for i in range(n_estados)
        if conteos_raw[i] > 0
    }

    idx_max = int(np.argmax(probabilidades))
    estado_encontrado = format(idx_max, f"0{n_qubits}b")

    return {
        "estado_encontrado": estado_encontrado,
        "probabilidad": round(float(probabilidades[idx_max]), 4),
        "iteraciones": n_iters,
        "conteos": conteos,
    }


if __name__ == "__main__":
    # Ejemplo: buscar el estado "101" en un espacio de 3 qubits
    objetivo = "101"
    oraculo = [lambda s: s == objetivo]

    resultado = grover_search(oraculo, n_iters=2)
    print("=== Algoritmo de Grover - Ejemplo ===")
    print(f"Estado objetivo: {objetivo}")
    print(f"Estado encontrado: {resultado['estado_encontrado']}")
    print(f"Probabilidad: {resultado['probabilidad']:.4f}")
    print(f"Iteraciones: {resultado['iteraciones']}")
    print(f"Conteos (top 3): {sorted(resultado['conteos'].items(), key=lambda x: -x[1])[:3]}")
