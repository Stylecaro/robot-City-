"""
Simulador cuántico local usando numpy para Ciudad Robot.

Descripción:
    Simula la ejecución de circuitos cuánticos de forma local sin necesidad
    de hardware real ni licencias externas. Útil para desarrollo y pruebas.

Dependencias:
    numpy >= 1.21

Uso de ejemplo::

    from quantum_core.backends.local_simulator import LocalSimulator
    from quantum_core.circuits.traffic_light_circuit import build_traffic_light_circuit

    sim = LocalSimulator()
    circuito = build_traffic_light_circuit()
    resultado = sim.run(circuito)
    print(resultado)
"""

# MIT License — Copyright (c) 2026 Ciudad Robot Team

import numpy as np


class LocalSimulator:
    """Simulador cuántico local basado en numpy.

    Simula la aplicación de la matriz del circuito al vector de estado inicial
    y devuelve las probabilidades de medición de cada estado de base.

    Atributos:
        shots (int): Número de mediciones simuladas. Por defecto 1024.

    Ejemplo::

        >>> sim = LocalSimulator(shots=512)
        >>> circuito = {"amplitudes": [0.707, 0.707, 0.0, 0.0], "matriz": None}
        >>> resultado = sim.run(circuito)
        >>> "conteos" in resultado
        True
    """

    def __init__(self, shots=1024):
        """Inicializa el simulador.

        Parámetros:
            shots (int): Número de muestras de medición. Por defecto 1024.
        """
        self.shots = shots

    def run(self, circuit):
        """Ejecuta un circuito cuántico simulado y devuelve resultados ficticios.

        Aplica la matriz del circuito al vector de estado inicial (|0⟩^n),
        calcula las probabilidades y simula mediciones aleatorias.

        Parámetros:
            circuit (dict): Representación del circuito con claves:
                - ``amplitudes`` (list): Amplitudes del estado inicial.
                - ``matriz`` (list | None): Matriz de transformación (lista de listas)
                  o None para usar las amplitudes directamente.

        Devuelve:
            dict: Resultado de la simulación con:
                - ``backend`` (str): Nombre del backend.
                - ``shots`` (int): Número de shots usados.
                - ``estado_final`` (list): Vector de estado final (partes reales).
                - ``probabilidades`` (list): Probabilidades de cada estado de base.
                - ``conteos`` (dict): Conteos simulados por estado.

        Ejemplo::

            >>> sim = LocalSimulator(shots=100)
            >>> circuito = {"amplitudes": [1.0, 0.0], "matriz": None}
            >>> res = sim.run(circuito)
            >>> sum(res["conteos"].values())
            100
        """
        amplitudes = np.array(circuit.get("amplitudes", [1.0]), dtype=complex)
        matriz_raw = circuit.get("matriz")

        if matriz_raw is not None:
            matriz = np.array(matriz_raw, dtype=complex)
            estado_final = matriz @ amplitudes
        else:
            estado_final = amplitudes

        # Normalizar por si acaso
        norma = np.linalg.norm(estado_final)
        if norma > 0:
            estado_final = estado_final / norma

        probabilidades = np.abs(estado_final) ** 2

        # Simular mediciones aleatorias
        n_estados = len(probabilidades)
        etiquetas = [format(i, f"0{max(1, int(np.log2(n_estados + 1)))}b") for i in range(n_estados)]
        conteos_array = np.random.multinomial(self.shots, probabilidades)
        conteos = {etiquetas[i]: int(conteos_array[i]) for i in range(n_estados)}

        return {
            "backend": "LocalSimulator",
            "shots": self.shots,
            "estado_final": estado_final.real.tolist(),
            "probabilidades": probabilidades.tolist(),
            "conteos": conteos,
        }
