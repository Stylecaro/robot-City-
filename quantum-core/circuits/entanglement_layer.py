# MIT License - Usar misma licencia que el repositorio
"""
Capa de entrelazamiento cuántico simulada.

Construye una matriz de entrelazamiento para n qubits usando numpy,
simulando la aplicación de puertas Hadamard y CNOT mediante producto
tensorial de matrices.

Uso:
    from quantum_core.circuits.entanglement_layer import entanglement_layer
    matriz = entanglement_layer(n_qubits=2)
"""

import numpy as np


# Puertas cuánticas básicas
HADAMARD = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
PAULI_X = np.array([[0, 1], [1, 0]], dtype=complex)
IDENTITY = np.eye(2, dtype=complex)


def _tensor_product(matrices):
    """
    Calcula el producto tensorial de una lista de matrices.

    Parámetros
    ----------
    matrices : list of np.ndarray
        Lista de matrices cuadradas.

    Retorna
    -------
    np.ndarray
        Producto tensorial resultante.
    """
    resultado = matrices[0]
    for m in matrices[1:]:
        resultado = np.kron(resultado, m)
    return resultado


def entanglement_layer(n_qubits):
    """
    Construye y devuelve la matriz unitaria de la capa de entrelazamiento.

    Aplica puertas Hadamard en todos los qubits seguido de una capa de
    puertas CNOT simuladas entre qubits consecutivos (par-impar).

    Parámetros
    ----------
    n_qubits : int
        Número de qubits del sistema.

    Retorna
    -------
    np.ndarray
        Matriz unitaria compleja de dimensión (2**n_qubits, 2**n_qubits).
    """
    if n_qubits < 1:
        raise ValueError("n_qubits debe ser mayor o igual a 1.")

    dim = 2 ** n_qubits

    # Capa Hadamard: H ⊗ H ⊗ ... ⊗ H
    hadamard_layer = _tensor_product([HADAMARD] * n_qubits)

    # Capa CNOT simulada: entrelazamiento de paridad entre vecinos.
    # Aplica CNOT en los pares (0,1), (2,3), (4,5), ...
    # (qubits de índice par como control, impares como objetivo).
    # Este es un esquema estándar de primera capa; para entrelazamiento
    # completo de todos los vecinos se pueden añadir capas adicionales con
    # desplazamiento impar: range(1, n_qubits-1, 2).
    # Se construye como la suma de proyecciones |0><0| ⊗ I + |1><1| ⊗ X.
    cnot_layer = np.eye(dim, dtype=complex)
    for control in range(0, n_qubits - 1, 2):
        target = control + 1
        # Proyector |0><0| para el qubit de control
        P0 = np.array([[1, 0], [0, 0]], dtype=complex)
        # Proyector |1><1| para el qubit de control
        P1 = np.array([[0, 0], [0, 1]], dtype=complex)

        # Construir operador CNOT para este par
        mats_ctrl_0 = [IDENTITY] * n_qubits
        mats_ctrl_0[control] = P0

        mats_ctrl_1 = [IDENTITY] * n_qubits
        mats_ctrl_1[control] = P1
        mats_ctrl_1[target] = PAULI_X

        cnot_op = _tensor_product(mats_ctrl_0) + _tensor_product(mats_ctrl_1)
        cnot_layer = cnot_op @ cnot_layer

    # Capa de entrelazamiento final: CNOT_layer · Hadamard_layer
    return cnot_layer @ hadamard_layer


if __name__ == "__main__":
    matriz = entanglement_layer(n_qubits=2)
    print("Matriz de entrelazamiento (2 qubits):")
    print(np.round(matriz, 4))
