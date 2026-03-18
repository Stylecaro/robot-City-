"""
Creador de Matrices Cuánticas — Robot City
==========================================
Módulo para crear y manipular matrices cuánticas fundamentales:
Hadamard, Pauli (X, Y, Z, I), rotación, entrelazamiento y producto tensorial.

Requisitos: numpy
"""

import numpy as np


class QuantumMatrixCreator:
    """
    Creador de matrices cuánticas para simulación de circuitos cuánticos.

    Proporciona todas las matrices de puertas cuánticas fundamentales
    y operaciones de álgebra lineal sobre vectores de estado cuántico.
    """

    def create_hadamard_matrix(self, n: int = 1) -> np.ndarray:
        """
        Genera la matriz de Hadamard de tamaño n×n (potencia de 2).

        La matriz de Hadamard de un qubit es:
            H = (1/√2) * [[1,  1],
                           [1, -1]]

        Para n qubits se calcula el producto tensorial iterado H⊗n.

        Args:
            n: Número de qubits (el tamaño de la matriz será 2^n × 2^n).

        Returns:
            np.ndarray: Matriz de Hadamard de dimensión (2^n) × (2^n).

        Raises:
            ValueError: Si n no es un entero positivo.
        """
        if not isinstance(n, int) or n < 1:
            raise ValueError("n debe ser un entero positivo.")

        H1 = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
        resultado = H1
        for _ in range(n - 1):
            resultado = np.kron(resultado, H1)
        return resultado

    def create_pauli_matrices(self) -> dict:
        """
        Devuelve las cuatro matrices de Pauli fundamentales.

        - I (Identidad): [[1, 0], [0, 1]]
        - X (NOT cuántico / bit-flip): [[0, 1], [1, 0]]
        - Y (bit+phase-flip): [[0, -i], [i, 0]]
        - Z (phase-flip): [[1, 0], [0, -1]]

        Returns:
            dict: Diccionario con claves 'I', 'X', 'Y', 'Z' y sus matrices.
        """
        return {
            "I": np.eye(2, dtype=complex),
            "X": np.array([[0, 1], [1, 0]], dtype=complex),
            "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
            "Z": np.array([[1, 0], [0, -1]], dtype=complex),
        }

    def create_rotation_matrix(self, theta: float, axis: str = "z") -> np.ndarray:
        """
        Crea la matriz de rotación cuántica R_eje(θ) para un qubit.

        Fórmulas:
            Rx(θ) = cos(θ/2)·I - i·sin(θ/2)·X
            Ry(θ) = cos(θ/2)·I - i·sin(θ/2)·Y
            Rz(θ) = cos(θ/2)·I - i·sin(θ/2)·Z

        Args:
            theta: Ángulo de rotación en radianes.
            axis: Eje de rotación ('x', 'y' o 'z').

        Returns:
            np.ndarray: Matriz de rotación 2×2 compleja.

        Raises:
            ValueError: Si el eje no es 'x', 'y' o 'z'.
        """
        eje = axis.lower()
        if eje not in ("x", "y", "z"):
            raise ValueError("El eje debe ser 'x', 'y' o 'z'.")

        paulis = self.create_pauli_matrices()
        identidad = paulis["I"]
        sigma = paulis[eje.upper()]

        # R_eje(θ) = cos(θ/2)·I - i·sin(θ/2)·σ
        return np.cos(theta / 2) * identidad - 1j * np.sin(theta / 2) * sigma

    def create_entanglement_matrix(self, n_qubits: int = 2) -> np.ndarray:
        """
        Genera la matriz de entrelazamiento para n qubits.

        Construye el circuito de entrelazamiento estándar:
        1. Aplica Hadamard al primer qubit (superposición).
        2. Aplica CNOT entre el primer qubit (control) y los demás (objetivo).

        Para n=2 produce la puerta Bell: CNOT · (H⊗I).

        Args:
            n_qubits: Número de qubits del sistema (mínimo 2).

        Returns:
            np.ndarray: Matriz unitaria de entrelazamiento (2^n × 2^n).

        Raises:
            ValueError: Si n_qubits < 2.
        """
        if n_qubits < 2:
            raise ValueError("Se necesitan al menos 2 qubits para el entrelazamiento.")

        # Hadamard en el primer qubit, identidad en el resto
        H = self.create_hadamard_matrix(1)
        I_resto = np.eye(2 ** (n_qubits - 1), dtype=complex)
        H_total = np.kron(H, I_resto)

        # Construir CNOT extendido: control=qubit 0, objetivo=qubit 1
        CNOT = self._build_cnot_matrix(n_qubits)

        return CNOT @ H_total

    def _build_cnot_matrix(self, n_qubits: int) -> np.ndarray:
        """
        Construye la matriz CNOT extendida para el primer par de qubits.

        Args:
            n_qubits: Número total de qubits en el sistema.

        Returns:
            np.ndarray: Matriz CNOT de dimensión (2^n × 2^n).
        """
        dim = 2 ** n_qubits
        cnot = np.zeros((dim, dim), dtype=complex)

        for estado in range(dim):
            # Extraer bit del qubit de control (qubit 0, bit más significativo)
            bit_control = (estado >> (n_qubits - 1)) & 1

            if bit_control == 1:
                # Voltear el qubit objetivo (qubit 1, segundo bit más significativo)
                estado_flip = estado ^ (1 << (n_qubits - 2))
                cnot[estado_flip, estado] = 1
            else:
                # Sin cambio cuando el control es |0⟩
                cnot[estado, estado] = 1

        return cnot

    def apply_matrix(self, state_vector: np.ndarray, matrix: np.ndarray) -> np.ndarray:
        """
        Aplica una matriz cuántica a un vector de estado cuántico.

        Realiza la operación: |ψ'⟩ = M|ψ⟩

        Args:
            state_vector: Vector de estado cuántico (columna).
            matrix: Matriz de la puerta cuántica a aplicar.

        Returns:
            np.ndarray: Nuevo vector de estado tras aplicar la matriz.

        Raises:
            ValueError: Si las dimensiones son incompatibles.
        """
        sv = np.asarray(state_vector, dtype=complex)
        m = np.asarray(matrix, dtype=complex)

        if m.shape[0] != sv.shape[0]:
            raise ValueError(
                f"Dimensión de la matriz ({m.shape}) incompatible con el "
                f"vector de estado ({sv.shape})."
            )

        return m @ sv

    def tensor_product(self, matrix_a: np.ndarray, matrix_b: np.ndarray) -> np.ndarray:
        """
        Calcula el producto tensorial (producto de Kronecker) de dos matrices.

        El producto tensorial A⊗B representa el espacio de Hilbert combinado
        de dos sistemas cuánticos independientes.

        Args:
            matrix_a: Primera matriz cuántica.
            matrix_b: Segunda matriz cuántica.

        Returns:
            np.ndarray: Producto tensorial A⊗B.
        """
        return np.kron(
            np.asarray(matrix_a, dtype=complex),
            np.asarray(matrix_b, dtype=complex),
        )

    def normalize_state(self, state_vector: np.ndarray) -> np.ndarray:
        """
        Normaliza un vector de estado cuántico.

        Garantiza que ‖|ψ⟩‖ = 1 dividiendo por la norma euclidiana.

        Args:
            state_vector: Vector de estado a normalizar.

        Returns:
            np.ndarray: Vector de estado normalizado.

        Raises:
            ValueError: Si el vector es el vector cero.
        """
        sv = np.asarray(state_vector, dtype=complex)
        norma = np.linalg.norm(sv)
        if np.isclose(norma, 0.0):
            raise ValueError("No se puede normalizar el vector cero.")
        return sv / norma

    def print_matrix(self, matrix: np.ndarray, name: str = "Matriz") -> None:
        """
        Imprime una matriz cuántica con formato legible.

        Args:
            matrix: Matriz a imprimir.
            name: Nombre descriptivo para mostrar.
        """
        m = np.asarray(matrix)
        filas, cols = m.shape
        print(f"\n{'─' * 40}")
        print(f"  {name}  ({filas}×{cols})")
        print(f"{'─' * 40}")
        for fila in m:
            valores = []
            for v in fila:
                if np.isclose(v.imag, 0):
                    valores.append(f"{v.real:+.4f}     ")
                elif np.isclose(v.real, 0):
                    valores.append(f"{v.imag:+.4f}j    ")
                else:
                    valores.append(f"{v.real:+.4f}{v.imag:+.4f}j")
            print("  [ " + "  ".join(valores) + " ]")
        print(f"{'─' * 40}")


if __name__ == "__main__":
    creador = QuantumMatrixCreator()

    print("=" * 60)
    print("  Robot City — Creador de Matrices Cuánticas")
    print("=" * 60)

    # --- Matriz de Hadamard ---
    H1 = creador.create_hadamard_matrix(1)
    creador.print_matrix(H1, "Hadamard H(1 qubit)")

    H2 = creador.create_hadamard_matrix(2)
    creador.print_matrix(H2, "Hadamard H⊗H (2 qubits)")

    # --- Matrices de Pauli ---
    paulis = creador.create_pauli_matrices()
    for nombre, matriz in paulis.items():
        creador.print_matrix(matriz, f"Pauli {nombre}")

    # --- Matrices de rotación ---
    import math
    Rx90 = creador.create_rotation_matrix(math.pi / 2, "x")
    creador.print_matrix(Rx90, "Rotación Rx(π/2)")

    Rz180 = creador.create_rotation_matrix(math.pi, "z")
    creador.print_matrix(Rz180, "Rotación Rz(π)")

    # --- Matriz de entrelazamiento (2 qubits) ---
    M_ent = creador.create_entanglement_matrix(2)
    creador.print_matrix(M_ent, "Entrelazamiento 2 qubits (Bell)")

    # --- Producto tensorial ---
    I = paulis["I"]
    X = paulis["X"]
    IX = creador.tensor_product(I, X)
    creador.print_matrix(IX, "Producto Tensorial I⊗X")

    # --- Aplicar Hadamard al estado |0⟩ ---
    estado_0 = np.array([1.0, 0.0], dtype=complex)
    estado_superposicion = creador.apply_matrix(estado_0, H1)
    print(f"\nH|0⟩ = {estado_superposicion}  (superposición |+⟩)")

    # --- Normalización ---
    estado_no_normalizado = np.array([3.0, 4.0], dtype=complex)
    normalizado = creador.normalize_state(estado_no_normalizado)
    print(f"Normalizado [3, 4] → {normalizado}  (norma={np.linalg.norm(normalizado):.6f})")
