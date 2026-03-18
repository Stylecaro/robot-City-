"""
Capa neuronal cuántica simulada para modelos híbridos en Ciudad Robot.

Descripción:
    Implementa una capa neuronal que aplica una transformación cuántica
    simulada a las entradas. En un modelo híbrido real, esta capa reemplazaría
    una subred clásica por un circuito cuántico parametrizado (PQC).

Dependencias:
    numpy >= 1.21

Uso de ejemplo::

    import numpy as np
    capa = QuantumNeuralLayer(n_qubits=4, n_outputs=2)
    entradas = np.array([0.5, -0.3, 0.8, 0.1])
    salida = capa.forward(entradas)
    print(salida)  # array de 2 valores en [-1, 1]
"""

# MIT License — Copyright (c) 2026 Ciudad Robot Team

import numpy as np


class QuantumNeuralLayer:
    """Capa neuronal cuántica simulada con transformación matricial.

    Simula el comportamiento de un circuito cuántico parametrizado (PQC) mediante
    una transformación unitaria aleatoria fija seguida de una proyección.
    Los parámetros del circuito (ángulos de rotación) se inicializan aleatoriamente.

    Atributos:
        n_qubits (int): Número de qubits de la capa.
        n_outputs (int): Número de salidas (debe ser <= 2**n_qubits).
        _theta (numpy.ndarray): Parámetros de rotación internos.
        _U (numpy.ndarray): Matriz unitaria de la transformación cuántica simulada.

    Ejemplo::

        >>> import numpy as np
        >>> capa = QuantumNeuralLayer(n_qubits=2, n_outputs=2)
        >>> x = np.array([0.0, 1.0, 0.0, 0.0])
        >>> salida = capa.forward(x)
        >>> salida.shape
        (2,)
    """

    def __init__(self, n_qubits=4, n_outputs=2, seed=None):
        """Inicializa la capa neuronal cuántica.

        Parámetros:
            n_qubits (int): Número de qubits. Por defecto 4.
            n_outputs (int): Dimensión de la salida. Por defecto 2.
            seed (int | None): Semilla para reproducibilidad. Por defecto None.
        """
        if n_outputs > 2 ** n_qubits:
            raise ValueError(
                f"n_outputs ({n_outputs}) no puede superar 2**n_qubits ({2**n_qubits})."
            )

        self.n_qubits = n_qubits
        self.n_outputs = n_outputs

        rng = np.random.default_rng(seed)
        # Parámetros de rotación (ángulos) en [0, 2π)
        self._theta = rng.uniform(0, 2 * np.pi, size=n_qubits)
        # Construir matriz unitaria simulada mediante descomposición QR
        M = rng.standard_normal((2 ** n_qubits, 2 ** n_qubits)) + 1j * rng.standard_normal(
            (2 ** n_qubits, 2 ** n_qubits)
        )
        self._U, _ = np.linalg.qr(M)

    def forward(self, inputs):
        """Aplica la transformación cuántica simulada a las entradas.

        Codifica las entradas como amplitudes de un estado cuántico, aplica la
        transformación unitaria y proyecta sobre los primeros ``n_outputs`` qubits.

        Parámetros:
            inputs (array-like): Vector de entrada de longitud 2**n_qubits o
                cualquier longitud (se rellena/recorta automáticamente).

        Devuelve:
            numpy.ndarray: Vector de salida real de longitud ``n_outputs`` con
                valores en [-1, 1] (expectativa sobre eje Z simulada).

        Ejemplo::

            >>> import numpy as np
            >>> capa = QuantumNeuralLayer(n_qubits=2, n_outputs=2, seed=0)
            >>> x = np.array([1.0, 0.0, 0.0, 0.0])
            >>> out = capa.forward(x)
            >>> out.shape
            (2,)
            >>> np.all(np.abs(out) <= 1.0)
            True
        """
        dim = 2 ** self.n_qubits
        estado = np.zeros(dim, dtype=complex)

        inp = np.asarray(inputs, dtype=float).flatten()
        longitud = min(len(inp), dim)
        estado[:longitud] = inp[:longitud]

        # Normalizar estado
        norma = np.linalg.norm(estado)
        if norma > 0:
            estado = estado / norma
        else:
            estado[0] = 1.0  # estado |0>

        # Aplicar rotaciones por qubit (Rz simulado)
        for i, theta in enumerate(self._theta):
            estado[i % dim] *= np.exp(1j * theta)

        # Aplicar transformación unitaria
        estado_salida = self._U @ estado

        # Calcular expectativa: Re(<ψ|σz|ψ>) por output
        prob = np.abs(estado_salida) ** 2
        salida = np.zeros(self.n_outputs)
        for k in range(self.n_outputs):
            # Expectativa simplificada: diferencia de probabilidades de mitades
            mitad = dim // (2 * self.n_outputs) if self.n_outputs > 1 else dim // 2
            idx0 = k * (dim // self.n_outputs)
            idx1 = idx0 + mitad
            salida[k] = np.sum(prob[idx0:idx1]) - np.sum(prob[idx1: idx0 + dim // self.n_outputs])

        return salida
