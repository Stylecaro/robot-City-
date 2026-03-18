"""
Capa de entrelazamiento cuántico para Ciudad Robot.

Descripción:
    Genera la matriz unitaria que representa una capa de entrelazamiento
    (puertas CNOT encadenadas) para n qubits. Se usa en circuitos cuánticos
    híbridos para crear correlaciones entre qubits vecinos.

Dependencias:
    numpy >= 1.21

Uso de ejemplo::

    import numpy as np
    matriz = entanglement_layer(3)
    print(matriz.shape)  # (8, 8)
"""

# MIT License — Copyright (c) 2026 Ciudad Robot Team

import numpy as np


def entanglement_layer(n_qubits):
    """Genera la matriz de entrelazamiento para n qubits (puertas CNOT en cadena).

    Construye la representación matricial del producto tensorial de puertas CNOT
    aplicadas entre qubits vecinos (qubit i como control, qubit i+1 como objetivo),
    partiendo de la identidad e iterando sobre todos los pares.

    Parámetros:
        n_qubits (int): Número de qubits. Debe ser >= 2.

    Devuelve:
        numpy.ndarray: Matriz unitaria compleja de tamaño (2**n_qubits, 2**n_qubits)
            que representa la capa de entrelazamiento.

    Lanza:
        ValueError: Si ``n_qubits`` es menor que 2.

    Ejemplo::

        >>> import numpy as np
        >>> M = entanglement_layer(2)
        >>> M.shape
        (4, 4)
        >>> np.allclose(M @ M.conj().T, np.eye(4))
        True
    """
    if n_qubits < 2:
        raise ValueError("Se necesitan al menos 2 qubits para el entrelazamiento.")

    dim = 2 ** n_qubits
    # Comenzar con la identidad
    resultado = np.eye(dim, dtype=complex)

    # Puerta CNOT en el espacio de 2 qubits
    cnot_2q = np.array(
        [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 1],
         [0, 0, 1, 0]],
        dtype=complex,
    )

    # Aplicar CNOT entre pares vecinos (control=i, objetivo=i+1)
    for i in range(n_qubits - 1):
        # Construir operador para todo el espacio: I⊗...⊗CNOT⊗...⊗I
        if i == 0:
            operador = cnot_2q
        else:
            operador = np.eye(2, dtype=complex)
            for _ in range(i - 1):
                operador = np.kron(operador, np.eye(2, dtype=complex))
            operador = np.kron(operador, cnot_2q)

        # Completar con identidades a la derecha si es necesario
        qubits_restantes = n_qubits - i - 2
        for _ in range(qubits_restantes):
            operador = np.kron(operador, np.eye(2, dtype=complex))

        resultado = operador @ resultado

    return resultado
