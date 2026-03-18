"""
Circuito cuántico de semáforo para Ciudad Robot.

Descripción:
    Representa el estado de un semáforo (rojo, amarillo, verde) como superposición
    cuántica de qubits. La representación simulada se devuelve como una lista de
    estados posibles con sus amplitudes asociadas.

Uso de ejemplo::

    circuito = build_traffic_light_circuit()
    print(circuito)
    # {
    #   "nombre": "SemaforoQuantico",
    #   "qubits": 2,
    #   "estados": ["|00> -> rojo", "|01> -> amarillo", "|10> -> verde"],
    #   "amplitudes": [0.5, 0.5, 0.0, 0.0],
    #   "matriz": [[...]]
    # }
"""

# MIT License — Copyright (c) 2026 Ciudad Robot Team

import math


def build_traffic_light_circuit():
    """Construye una representación simulada de un circuito cuántico de semáforo.

    El circuito usa 2 qubits para codificar 3 estados de semáforo:
        - |00⟩ → rojo
        - |01⟩ → amarillo
        - |10⟩ → verde

    La amplitud inicial reparte probabilidad equiprobable entre rojo y amarillo.

    Devuelve:
        dict: Representación del circuito con:
            - ``nombre`` (str): Identificador del circuito.
            - ``qubits`` (int): Número de qubits.
            - ``estados`` (list): Descripción de cada estado de base.
            - ``amplitudes`` (list): Lista de amplitudes (floats) para cada estado.
            - ``matriz`` (list): Matriz de transformación 4×4 (lista de listas).

    Ejemplo::

        >>> circuito = build_traffic_light_circuit()
        >>> circuito["nombre"]
        'SemaforoQuantico'
        >>> len(circuito["amplitudes"])
        4
    """
    # Amplitudes iniciales: superposición equiprobable entre rojo y amarillo
    amp = 1.0 / math.sqrt(2)
    amplitudes = [amp, amp, 0.0, 0.0]

    # Matriz de Hadamard en primer qubit (simplificado 4x4)
    h = 1.0 / math.sqrt(2)
    matriz = [
        [h,  h,  0.0, 0.0],
        [h, -h,  0.0, 0.0],
        [0.0, 0.0,  h,  h],
        [0.0, 0.0,  h, -h],
    ]

    return {
        "nombre": "SemaforoQuantico",
        "qubits": 2,
        "estados": ["|00> -> rojo", "|01> -> amarillo", "|10> -> verde", "|11> -> no_usado"],
        "amplitudes": amplitudes,
        "matriz": matriz,
    }
