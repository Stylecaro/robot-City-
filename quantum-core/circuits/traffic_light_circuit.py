# MIT License - Copyright (c) 2026 Ciudad Robot Team
"""
Módulo de Circuito de Semáforo Cuántico
=========================================
Construye una representación de circuito cuántico para control de tráfico
basado en semáforos, usando una arquitectura de qubits parametrizada.
"""


def build_traffic_light_circuit(params=None):
    """
    Construye y devuelve la representación dict de un circuito cuántico de semáforo.

    El circuito modela los estados de un semáforo (rojo, amarillo, verde) como
    estados cuánticos en superposición. Los parámetros permiten ajustar los ángulos
    de rotación de las puertas para optimizar el flujo de tráfico.

    Parámetros
    ----------
    params : dict o None, opcional
        Parámetros del circuito. Claves reconocidas:
        - "theta": ángulo de rotación RY para el qubit de estado (default: 0.5)
        - "phi": ángulo de fase para la puerta RZ (default: 0.0)
        - "n_qubits": número de qubits del circuito (default: 3)
        - "circuit_name": nombre descriptivo (default: "traffic_light")
        Si es None se usan los valores por defecto.

    Retorna
    -------
    dict
        Representación del circuito con la siguiente estructura:
        {
          "circuit_name": str,
          "n_qubits": int,
          "gates": list[dict],   # lista de puertas en orden de aplicación
          "measurements": list,  # qubits a medir
          "params": dict         # parámetros usados
        }

    Ejemplo
    -------
    >>> circuito = build_traffic_light_circuit({"theta": 1.0})
    >>> print(circuito["circuit_name"])
    'traffic_light'
    >>> print(len(circuito["gates"]))
    5
    """
    if params is None:
        params = {}

    theta = float(params.get("theta", 0.5))
    phi = float(params.get("phi", 0.0))
    n_qubits = int(params.get("n_qubits", 3))
    circuit_name = str(params.get("circuit_name", "traffic_light"))

    # Construir lista de puertas del circuito
    # Qubit 0: estado del semáforo (rojo=|0⟩, verde=|1⟩)
    # Qubit 1: detector de vehículos
    # Qubit 2: señal de emergencia
    gates = [
        {"gate": "H", "qubits": [0], "descripcion": "Superposición inicial del semáforo"},
        {"gate": "RY", "qubits": [0], "params": {"theta": theta}, "descripcion": "Rotación según densidad de tráfico"},
        {"gate": "H", "qubits": [1], "descripcion": "Superposición del detector de vehículos"},
        {"gate": "CNOT", "control": 0, "target": 1, "descripcion": "Entrelazar semáforo con detector"},
        {"gate": "RZ", "qubits": [2], "params": {"phi": phi}, "descripcion": "Fase para señal de emergencia"},
    ]

    # Añadir puertas extra si hay más qubits
    for q in range(3, n_qubits):
        gates.append({
            "gate": "H",
            "qubits": [q],
            "descripcion": f"Qubit auxiliar {q} en superposición",
        })

    return {
        "circuit_name": circuit_name,
        "n_qubits": n_qubits,
        "gates": gates,
        "measurements": list(range(n_qubits)),
        "params": {"theta": theta, "phi": phi},
    }


if __name__ == "__main__":
    circuito = build_traffic_light_circuit({"theta": 0.8, "phi": 0.2})
    import json
    print("=== Circuito de Semáforo Cuántico ===")
    print(json.dumps(circuito, indent=2, ensure_ascii=False))
