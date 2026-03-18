# MIT License - Usar misma licencia que el repositorio
"""
Simulador local cuántico.

Usa numpy para simular la ejecución de circuitos cuánticos y devolver
resultados ficticios en formato JSON serializable (conteos o amplitudes).

Uso:
    from quantum_core.backends.local_simulator import LocalSimulator
    sim = LocalSimulator()
    resultados = sim.run(circuit)
"""

import json
import numpy as np


class LocalSimulator:
    """
    Simulador cuántico local basado en numpy.

    Simula el vector de estado de un sistema de n qubits y aplica
    las puertas definidas en el circuito de forma matricial.
    """

    # Matrices de puertas básicas
    _GATES = {
        "H": np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2),
        "X": np.array([[0, 1], [1, 0]], dtype=complex),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "Z": np.array([[1, 0], [0, -1]], dtype=complex),
        "I": np.eye(2, dtype=complex),
    }

    def __init__(self, shots=1024):
        """
        Inicializa el simulador local.

        Parámetros
        ----------
        shots : int
            Número de mediciones simuladas. Por defecto 1024.
        """
        self.shots = shots

    def run(self, circuit):
        """
        Ejecuta un circuito cuántico y devuelve resultados simulados.

        Parámetros
        ----------
        circuit : dict
            Representación del circuito con claves:
            - "qubits" (int): número de qubits.
            - "gates" (list): lista de dicts con puertas a aplicar.

        Retorna
        -------
        dict
            Resultados con claves:
            - "counts": dict de estado -> número de mediciones
            - "probabilities": dict de estado -> probabilidad
            - "shots": número de shots realizados
            - "backend": "local_simulator"
        """
        n_qubits = int(circuit.get("qubits", 1))
        gates = circuit.get("gates", [])
        dim = 2 ** n_qubits

        # Estado inicial |0...0>
        state = np.zeros(dim, dtype=complex)
        state[0] = 1.0

        # Aplicar puertas
        for gate_info in gates:
            gate_name = gate_info.get("gate", "I").upper()
            if gate_name in ("H", "X", "Y", "Z", "I"):
                qubit = int(gate_info.get("qubit", 0))
                state = self._apply_single_qubit_gate(
                    state, self._GATES[gate_name], qubit, n_qubits
                )
            elif gate_name == "CNOT":
                control = int(gate_info.get("control", 0))
                target = int(gate_info.get("target", 1))
                state = self._apply_cnot(state, control, target, n_qubits)
            # RZ y otras puertas de rotación: ignorar en simulación básica

        # Calcular probabilidades
        probabilities = np.abs(state) ** 2

        # Simular mediciones
        indices = np.arange(dim)
        sampled = np.random.choice(indices, size=self.shots, p=probabilities)
        counts_array = np.bincount(sampled, minlength=dim)

        fmt = f"0{n_qubits}b"
        counts = {format(i, fmt): int(counts_array[i]) for i in range(dim) if counts_array[i] > 0}
        probs = {format(i, fmt): float(round(probabilities[i], 6)) for i in range(dim)}

        return {
            "counts": counts,
            "probabilities": probs,
            "shots": self.shots,
            "backend": "local_simulator",
        }

    def _apply_single_qubit_gate(self, state, gate_matrix, qubit, n_qubits):
        """Aplica una puerta de un qubit al vector de estado completo."""
        matrices = [self._GATES["I"]] * n_qubits
        matrices[qubit] = gate_matrix
        full_matrix = matrices[0]
        for m in matrices[1:]:
            full_matrix = np.kron(full_matrix, m)
        return full_matrix @ state

    def _apply_cnot(self, state, control, target, n_qubits):
        """Aplica una puerta CNOT al vector de estado."""
        dim = 2 ** n_qubits
        cnot_matrix = np.eye(dim, dtype=complex)
        for i in range(dim):
            bits = format(i, f"0{n_qubits}b")
            if bits[control] == "1":
                # Voltear el bit del qubit target
                flipped_bits = list(bits)
                flipped_bits[target] = "0" if bits[target] == "1" else "1"
                j = int("".join(flipped_bits), 2)
                cnot_matrix[i, i] = 0
                cnot_matrix[j, i] = 1
        return cnot_matrix @ state


if __name__ == "__main__":
    from quantum_core.circuits.traffic_light_circuit import build_traffic_light_circuit
    circuito = build_traffic_light_circuit(params={"qubits": 2})
    sim = LocalSimulator(shots=512)
    resultado = sim.run(circuito)
    print(json.dumps(resultado, indent=2))
