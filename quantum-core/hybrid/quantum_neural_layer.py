# MIT License - Usar misma licencia que el repositorio
"""
Capa neuronal cuántica híbrida (simulada).

Implementa una capa neuronal cuántica-clásica simulada usando numpy.
Puede usarse como bloque en modelos híbridos junto con TensorFlow o PyTorch.

Uso:
    from quantum_core.hybrid.quantum_neural_layer import QuantumNeuralLayer
    capa = QuantumNeuralLayer(n_qubits=4)
    salida = capa.forward(inputs=[0.5, 0.3, 0.8, 0.1])
"""

import numpy as np


class QuantumNeuralLayer:
    """
    Capa neuronal cuántica híbrida simulada.

    Aplica una transformación cuántica simulada a un vector de entrada
    usando una matriz unitaria generada con numpy. La transformación
    consiste en una capa Hadamard seguida de una rotación parametrizada.
    """

    def __init__(self, n_qubits=4, seed=None):
        """
        Inicializa la capa cuántica neuronal.

        Parámetros
        ----------
        n_qubits : int
            Número de qubits de la capa (determina la dimensión). Por defecto 4.
        seed : int o None
            Semilla para reproducibilidad. Por defecto None.
        """
        self.n_qubits = n_qubits
        rng = np.random.default_rng(seed)
        # Parámetros de rotación entrenables (simulados)
        self._theta = rng.uniform(0, 2 * np.pi, size=n_qubits)

    def _hadamard_matrix(self):
        """Genera la matriz Hadamard para n_qubits."""
        H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
        resultado = H
        for _ in range(self.n_qubits - 1):
            resultado = np.kron(resultado, H)
        return resultado

    def forward(self, inputs):
        """
        Aplica la transformación cuántica simulada al vector de entrada.

        Parámetros
        ----------
        inputs : array-like
            Vector de entrada de longitud n_qubits.

        Retorna
        -------
        np.ndarray
            Vector de salida de longitud n_qubits (valores reales normalizados).
        """
        x = np.array(inputs, dtype=complex)
        if len(x) != self.n_qubits:
            raise ValueError(
                f"La longitud de inputs ({len(x)}) debe ser igual a n_qubits ({self.n_qubits})."
            )

        # Paso 1: codificar la entrada clásica como estado cuántico inicial.
        # Se construye un estado de amplitud en el espacio de 2^n dimensiones
        # usando codificación de ángulo: |ψ⟩ = ⊗_i (cos(x_i)|0⟩ + sin(x_i)|1⟩)
        estado = np.ones(1, dtype=complex)
        for xi in x:
            qubit = np.array([np.cos(xi), np.sin(xi)], dtype=complex)
            estado = np.kron(estado, qubit)

        # Paso 2: aplicar rotaciones RZ parametrizadas (expandidas al espacio completo)
        # Cada rotación actúa sobre un qubit individual del estado completo
        dim = 2 ** self.n_qubits
        rotacion_total = np.eye(dim, dtype=complex)
        I = np.eye(2, dtype=complex)
        for i, theta in enumerate(self._theta):
            Rz = np.diag(np.array([np.exp(-1j * theta / 2), np.exp(1j * theta / 2)], dtype=complex))
            matrices = [I] * self.n_qubits
            matrices[i] = Rz
            Rz_total = matrices[0]
            for m in matrices[1:]:
                Rz_total = np.kron(Rz_total, m)
            rotacion_total = Rz_total @ rotacion_total

        estado = rotacion_total @ estado

        # Paso 3: aplicar capa Hadamard completa al estado
        H = self._hadamard_matrix()
        amplitudes = H @ estado

        # Paso 4: reducir de vuelta a n_qubits valores midiendo parcialmente.
        # Se calcula la probabilidad marginal del primer qubit de cada par
        # agrupando los 2^n amplitudes en n grupos para obtener n salidas.
        probs = np.abs(amplitudes) ** 2
        # Agrupar en n_qubits grupos de tamaño 2^n / n_qubits (o usar traza parcial)
        grupo = dim // self.n_qubits
        salida = np.array([probs[i * grupo:(i + 1) * grupo].sum() for i in range(self.n_qubits)])

        # Normalizar salida
        suma = salida.sum()
        if suma > 0:
            salida = salida / suma
        return salida.real


if __name__ == "__main__":
    capa = QuantumNeuralLayer(n_qubits=4, seed=42)
    entrada = [0.5, 0.3, 0.8, 0.1]
    salida = capa.forward(entrada)
    print("Entrada:", entrada)
    print("Salida cuántica:", salida)
