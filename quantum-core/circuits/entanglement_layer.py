# MIT License - Copyright (c) 2026 Ciudad Robot Team
"""
Módulo de Capa de Entrelazamiento
===================================
Proporciona funciones para construir capas de entrelazamiento cuántico
usando matrices numpy como representación simbólica de los circuitos.
"""

import numpy as np


# ---------------------------------------------------------------------------
# Puertas elementales
# ---------------------------------------------------------------------------

def hadamard(n_qubits=1):
    """
    Devuelve la matriz de Hadamard de un qubit (2x2) o el producto tensorial
    de n_qubits puertas Hadamard.

    Parámetros
    ----------
    n_qubits : int
        Número de qubits sobre los que aplicar Hadamard en paralelo.

    Retorna
    -------
    numpy.ndarray
        Matriz Hadamard de dimensión (2^n_qubits, 2^n_qubits).
    """
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    result = H
    for _ in range(n_qubits - 1):
        result = np.kron(result, H)
    return result


def cnot(n_qubits=2):
    """
    Devuelve la matriz de la puerta CNOT (controlled-NOT) de dos qubits.

    Parámetros
    ----------
    n_qubits : int
        Tamaño total del sistema. La puerta CNOT actúa sobre los primeros 2 qubits;
        el resto se extiende con la identidad.

    Retorna
    -------
    numpy.ndarray
        Matriz CNOT de dimensión (2^n_qubits, 2^n_qubits).
    """
    cx = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ], dtype=complex)

    if n_qubits <= 2:
        return cx

    # Extender con identidad para qubits adicionales
    identity = np.eye(2 ** (n_qubits - 2), dtype=complex)
    return np.kron(cx, identity)


# ---------------------------------------------------------------------------
# Capa de entrelazamiento principal
# ---------------------------------------------------------------------------

def entanglement_layer(n_qubits):
    """
    Construye una capa de entrelazamiento para n_qubits qubits.

    La capa aplica primero Hadamard a todos los qubits y luego puertas CNOT
    encadenadas (qubit i → qubit i+1) para crear correlaciones cuánticas entre
    qubits vecinos. El resultado es una matriz placeholder que representa el
    estado cuántico inicial del sistema entrelazado.

    Parámetros
    ----------
    n_qubits : int
        Número de qubits del sistema. Debe ser >= 1.

    Retorna
    -------
    numpy.ndarray
        Matriz (vector de estado) de dimensión (2^n_qubits,) representando
        el estado cuántico tras aplicar la capa de entrelazamiento al estado |0...0⟩.

    Ejemplo
    -------
    >>> estado = entanglement_layer(2)
    >>> print(estado.shape)
    (4,)
    >>> print(np.abs(estado).sum())
    2.0

    Notas
    -----
    Esta es una representación placeholder usando álgebra matricial numpy.
    Para simulación cuántica real se debe usar Qiskit o Cirq.
    """
    if n_qubits < 1:
        raise ValueError("n_qubits debe ser al menos 1")

    dim = 2**n_qubits
    # Estado inicial |0...0⟩
    estado = np.zeros(dim, dtype=complex)
    estado[0] = 1.0

    # Aplicar Hadamard a todos los qubits
    H_total = hadamard(n_qubits)
    estado = H_total @ estado

    # Aplicar CNOT encadenado entre qubits vecinos
    for i in range(n_qubits - 1):
        # Construir CNOT entre qubit i y qubit i+1 en el espacio completo
        cx = cnot(n_qubits)
        estado = cx @ estado

    return estado


if __name__ == "__main__":
    print("=== Capa de Entrelazamiento Cuántico ===")
    for n in [1, 2, 3]:
        estado = entanglement_layer(n)
        print(f"\nn_qubits={n}")
        print(f"  Dimensión del estado: {estado.shape}")
        print(f"  Norma del estado: {np.linalg.norm(estado):.4f}")
        print(f"  Probabilidades: {np.abs(estado)**2}")
