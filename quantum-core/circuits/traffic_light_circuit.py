# MIT License - Usar misma licencia que el repositorio
"""
Circuito de semáforo cuántico simulado.

Genera una representación simulada de un circuito cuántico que modela
el estado de un semáforo (rojo, amarillo, verde) mediante superposición
de qubits.

Uso:
    from quantum_core.circuits.traffic_light_circuit import build_traffic_light_circuit
    circuito = build_traffic_light_circuit(params={"qubits": 3})
    import json
    print(json.dumps(circuito, indent=2))
"""

import json


def build_traffic_light_circuit(params=None):
    """
    Construye una representación simulada de un circuito de semáforo cuántico.

    Parámetros
    ----------
    params : dict, opcional
        Parámetros de configuración del circuito.
        Claves reconocidas:
        - "qubits" (int): número de qubits (por defecto 3).

    Retorna
    -------
    dict
        Representación del circuito con claves:
        - "name": nombre del circuito
        - "qubits": número de qubits
        - "gates": lista de puertas aplicadas
        - "measurements": lista de mediciones
    """
    if params is None:
        params = {}

    n_qubits = int(params.get("qubits", 3))

    # Construir representación simulada del circuito
    gates = []

    # Puerta Hadamard en cada qubit (superposición)
    for q in range(n_qubits):
        gates.append({"gate": "H", "qubit": q})

    # Puertas CNOT para entrelazamiento entre qubits consecutivos
    for q in range(n_qubits - 1):
        gates.append({"gate": "CNOT", "control": q, "target": q + 1})

    # Puerta de rotación para codificar el estado del semáforo
    gates.append({"gate": "RZ", "qubit": 0, "angle": 1.5708})  # π/2

    measurements = [{"qubit": q, "classical_bit": q} for q in range(n_qubits)]

    circuito = {
        "name": "traffic_light_circuit",
        "qubits": n_qubits,
        "gates": gates,
        "measurements": measurements,
    }
    return circuito


if __name__ == "__main__":
    circuito = build_traffic_light_circuit(params={"qubits": 3})
    print(json.dumps(circuito, indent=2))
