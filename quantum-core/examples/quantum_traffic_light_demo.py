"""
Script de demostración del semáforo cuántico en Ciudad Robot.

Importa el circuito de semáforo cuántico y lo ejecuta en el simulador local.
Demuestra el flujo completo: construcción del circuito → ejecución → resultados.

Uso::

    cd quantum-core
    python examples/quantum_traffic_light_demo.py

Salida esperada::

    === Demo Semáforo Cuántico ===
    Circuito: SemaforoQuantico (2 qubits)
    Estados posibles: ['|00> -> rojo', '|01> -> amarillo', ...]
    Backend: LocalSimulator (1024 shots)
    Probabilidades: {'00': 0.5, '01': 0.5, ...}
    Conteos: {'00': 512, '01': 512, ...}
"""

# MIT License — Copyright (c) 2026 Ciudad Robot Team

import sys
import os
import json

# Asegurar que el paquete quantum-core sea importable desde este script
QUANTUM_CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if QUANTUM_CORE_DIR not in sys.path:
    sys.path.insert(0, QUANTUM_CORE_DIR)

from circuits.traffic_light_circuit import build_traffic_light_circuit
from backends.local_simulator import LocalSimulator


def main():
    """Ejecuta la demostración del semáforo cuántico y muestra los resultados."""
    print("=" * 50)
    print("  === Demo Semáforo Cuántico - Ciudad Robot ===")
    print("=" * 50)

    # 1. Construir circuito
    circuito = build_traffic_light_circuit()
    print(f"\nCircuito: {circuito['nombre']} ({circuito['qubits']} qubits)")
    print(f"Estados posibles:")
    for estado in circuito["estados"]:
        print(f"  {estado}")

    # 2. Ejecutar en simulador local
    sim = LocalSimulator(shots=1024)
    resultado = sim.run(circuito)

    # 3. Mostrar resultados
    print(f"\nBackend: {resultado['backend']} ({resultado['shots']} shots)")
    print("\nProbabilidades por estado:")
    for i, (estado, prob) in enumerate(
        zip(circuito["estados"], resultado["probabilidades"])
    ):
        barra = "#" * int(prob * 30)
        print(f"  {estado}: {prob:.4f}  {barra}")

    print("\nConteos simulados:")
    conteos_ordenados = sorted(resultado["conteos"].items(), key=lambda x: -x[1])
    for clave, conteo in conteos_ordenados:
        barra = "#" * int(conteo / resultado["shots"] * 30)
        print(f"  |{clave}>: {conteo:5d}  {barra}")

    print("\n" + "=" * 50)
    print("Resultado JSON completo:")
    # Serializar para salida estándar (útil cuando se llama desde Node.js)
    # Formato esperado de 'estados': "|XX> -> nombre", donde XX es el identificador binario.
    salida = {
        "circuito": circuito["nombre"],
        "qubits": circuito["qubits"],
        "backend": resultado["backend"],
        "shots": resultado["shots"],
        "probabilidades": dict(
            zip([e.split(">")[0].lstrip("|") for e in circuito["estados"]],
                resultado["probabilidades"])
        ),
        "conteos": resultado["conteos"],
        "estado": "ok",
    }
    print(json.dumps(salida, indent=2))
    return salida


if __name__ == "__main__":
    main()
