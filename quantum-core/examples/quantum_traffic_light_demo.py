# MIT License - Usar misma licencia que el repositorio
"""
Demo: Semáforo cuántico con simulador local.

Este script importa el circuito de semáforo cuántico y el simulador local,
ejecuta la simulación y muestra los resultados en formato JSON por stdout.

Uso:
    python quantum_traffic_light_demo.py [--qubits N] [--shots N]

Argumentos:
    --qubits  Número de qubits del circuito (por defecto: 3)
    --shots   Número de mediciones simuladas (por defecto: 1024)

Ejemplo:
    python quantum_traffic_light_demo.py --qubits 3 --shots 512
"""

import sys
import os
import json
import argparse

# Añadir el directorio raíz de quantum-core al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from circuits.traffic_light_circuit import build_traffic_light_circuit
from backends.local_simulator import LocalSimulator


def main():
    """Punto de entrada principal del demo."""
    parser = argparse.ArgumentParser(
        description="Demo de semáforo cuántico con simulador local."
    )
    parser.add_argument(
        "--qubits",
        type=int,
        default=3,
        help="Número de qubits del circuito (por defecto: 3).",
    )
    parser.add_argument(
        "--shots",
        type=int,
        default=1024,
        help="Número de mediciones simuladas (por defecto: 1024).",
    )
    args = parser.parse_args()

    # Validar argumentos
    if args.qubits < 1 or args.qubits > 16:
        print(
            json.dumps({"error": "El número de qubits debe estar entre 1 y 16."}),
            file=sys.stderr,
        )
        sys.exit(1)

    if args.shots < 1 or args.shots > 100000:
        print(
            json.dumps({"error": "El número de shots debe estar entre 1 y 100000."}),
            file=sys.stderr,
        )
        sys.exit(1)

    # Construir circuito
    circuito = build_traffic_light_circuit(params={"qubits": args.qubits})

    # Ejecutar simulador
    simulador = LocalSimulator(shots=args.shots)
    resultado = simulador.run(circuito)

    # Añadir información del circuito al resultado
    resultado["circuit_name"] = "traffic_light"
    resultado["circuit_qubits"] = args.qubits

    # Salida JSON en stdout
    print(json.dumps(resultado, indent=2))


if __name__ == "__main__":
    main()
