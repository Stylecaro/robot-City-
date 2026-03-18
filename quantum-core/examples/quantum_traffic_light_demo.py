#!/usr/bin/env python3
# MIT License - Copyright (c) 2026 Ciudad Robot Team
"""
Demo CLI: Semáforo Cuántico
============================
Script de demostración que construye un circuito de semáforo cuántico
usando build_traffic_light_circuit() y lo ejecuta en el LocalSimulator.

Uso
---
    # Ejecutar con parámetros por defecto:
    python quantum_traffic_light_demo.py

    # Pasar parámetros por argumento:
    python quantum_traffic_light_demo.py --params '{"theta": 1.0, "n_qubits": 3}'

    # Pasar parámetros por stdin (JSON):
    echo '{"theta": 0.8, "phi": 0.2}' | python quantum_traffic_light_demo.py

    # El script imprime el resultado como JSON a stdout.
"""

import argparse
import json
import sys
import os

# Añadir el directorio padre (quantum-core/) al path de Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from circuits.traffic_light_circuit import build_traffic_light_circuit
from backends.local_simulator import LocalSimulator


def leer_params(args_params=None):
    """
    Lee los parámetros del circuito desde --params o desde stdin.

    Orden de precedencia:
    1. Argumento --params (cadena JSON)
    2. stdin si no es un terminal (pipes)
    3. Parámetros por defecto (None)

    Parámetros
    ----------
    args_params : str o None
        Cadena JSON del argumento --params.

    Retorna
    -------
    dict o None
        Diccionario de parámetros o None para usar valores por defecto.
    """
    if args_params:
        try:
            return json.loads(args_params)
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"JSON inválido en --params: {e}"}), flush=True)
            sys.exit(1)

    # Leer de stdin si hay datos disponibles (pipe)
    if not sys.stdin.isatty():
        try:
            stdin_data = sys.stdin.read().strip()
            if stdin_data:
                return json.loads(stdin_data)
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"JSON inválido en stdin: {e}"}), flush=True)
            sys.exit(1)

    return None


def main():
    """Punto de entrada principal del script de demostración."""
    parser = argparse.ArgumentParser(
        description="Demo del semáforo cuántico - quantum-core Ciudad Robot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--params",
        type=str,
        default=None,
        help='Parámetros del circuito en formato JSON. Ejemplo: \'{"theta": 1.0, "n_qubits": 3}\'',
    )
    parser.add_argument(
        "--shots",
        type=int,
        default=1024,
        help="Número de disparos para el simulador (default: 1024)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Semilla aleatoria para reproducibilidad (default: 42)",
    )
    args = parser.parse_args()

    # Leer parámetros
    params = leer_params(args.params)

    # Construir circuito de semáforo
    circuito = build_traffic_light_circuit(params)

    # Ejecutar en simulador local
    simulador = LocalSimulator(shots=args.shots, seed=args.seed)
    resultado = simulador.run(circuito)

    # Construir respuesta completa
    respuesta = {
        "exito": True,
        "circuito": {
            "nombre": circuito["circuit_name"],
            "n_qubits": circuito["n_qubits"],
            "n_puertas": len(circuito["gates"]),
            "params": circuito["params"],
        },
        "resultado": resultado,
    }

    # Imprimir JSON a stdout
    print(json.dumps(respuesta, indent=2, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
