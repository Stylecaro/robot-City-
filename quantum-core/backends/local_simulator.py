# MIT License - Copyright (c) 2026 Ciudad Robot Team
"""
Simulador Local de Circuitos Cuánticos
========================================
Clase LocalSimulator para ejecutar circuitos cuánticos localmente usando numpy,
sin necesidad de hardware real ni conexión a servicios externos.
"""

import numpy as np


class LocalSimulator:
    """
    Simulador cuántico local basado en numpy.

    Simula la ejecución de circuitos cuánticos representados como diccionarios
    (formato interno de quantum-core) generando conteos de medición ficticios
    que reflejan la estructura del circuito de forma determinista.

    Este simulador es útil para desarrollo, pruebas y demostraciones cuando
    no se dispone de Qiskit Aer o acceso a IBM Quantum.

    Atributos
    ---------
    shots : int
        Número de disparos (mediciones) simulados por ejecución.
    seed : int o None
        Semilla para el generador de números aleatorios (reproducibilidad).
    """

    def __init__(self, shots=1024, seed=42):
        """
        Inicializa el simulador local.

        Parámetros
        ----------
        shots : int
            Número de disparos para la simulación. Por defecto 1024.
        seed : int o None
            Semilla aleatoria para reproducibilidad. Por defecto 42.
        """
        self.shots = shots
        self.seed = seed
        self._rng = np.random.default_rng(seed=seed)

    def run(self, circuit):
        """
        Simula la ejecución de un circuito cuántico y devuelve conteos ficticios.

        El simulador extrae el número de qubits del circuito y genera una
        distribución de probabilidad uniforme ponderada por las puertas presentes.
        Puertas como Hadamard aumentan la entropía (distribución más plana),
        mientras que puertas de fase concentran la probabilidad.

        Parámetros
        ----------
        circuit : dict
            Diccionario del circuito con al menos las claves:
            - "n_qubits": int — número de qubits
            - "gates": list[dict] — lista de puertas aplicadas
            - "measurements": list — qubits a medir (opcional)

        Retorna
        -------
        dict
            Diccionario con los resultados de la simulación:
            - "conteos": dict[str, int] — bitstring → número de conteos
            - "shots": int — total de disparos realizados
            - "n_qubits": int — número de qubits medidos
            - "backend": str — "local_simulator"

        Ejemplo
        -------
        >>> sim = LocalSimulator(shots=512, seed=0)
        >>> circuito = {"n_qubits": 2, "gates": [{"gate": "H", "qubits": [0]}], "measurements": [0, 1]}
        >>> resultado = sim.run(circuito)
        >>> print(sum(resultado["conteos"].values()))
        512
        """
        if not isinstance(circuit, dict):
            raise TypeError("El circuito debe ser un diccionario.")

        n_qubits = int(circuit.get("n_qubits", 1))
        gates = circuit.get("gates", [])
        measurements = circuit.get("measurements", list(range(n_qubits)))
        n_medidos = len(measurements)
        n_estados = 2**n_medidos

        # Calcular pesos de probabilidad según las puertas del circuito
        pesos = self._calcular_pesos(gates, n_medidos)

        # Simular mediciones
        conteos_raw = self._rng.multinomial(self.shots, pesos)
        conteos = {
            format(i, f"0{n_medidos}b"): int(conteos_raw[i])
            for i in range(n_estados)
            if conteos_raw[i] > 0
        }

        return {
            "conteos": conteos,
            "shots": self.shots,
            "n_qubits": n_medidos,
            "backend": "local_simulator",
        }

    def _calcular_pesos(self, gates, n_qubits):
        """
        Calcula pesos de probabilidad para los estados de medición.

        Parámetros
        ----------
        gates : list[dict]
            Lista de puertas del circuito.
        n_qubits : int
            Número de qubits medidos.

        Retorna
        -------
        numpy.ndarray
            Array de probabilidades normalizado de longitud 2^n_qubits.
        """
        n_estados = 2**n_qubits
        pesos = np.ones(n_estados, dtype=float)

        # Contar puertas que generan superposición
        n_hadamard = sum(1 for g in gates if g.get("gate") == "H")
        n_cnot = sum(1 for g in gates if g.get("gate") in ("CNOT", "CX"))

        if n_hadamard > 0:
            # Con puertas Hadamard: distribución más uniforme
            ruido = self._rng.uniform(0.5, 1.5, size=n_estados)
            pesos *= ruido
        else:
            # Sin Hadamard: concentrar probabilidad en primeros estados
            pesos[0] *= 3.0

        if n_cnot > 0:
            # CNOT crea entrelazamiento: aumentar probabilidad de estados correlacionados
            for i in range(0, n_estados, 2):
                pesos[i] *= 1.2

        # Normalizar
        pesos /= pesos.sum()
        return pesos

    def __repr__(self):
        return f"LocalSimulator(shots={self.shots}, seed={self.seed})"
