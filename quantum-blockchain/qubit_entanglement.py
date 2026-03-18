"""
Entrelazamiento de Qubits — Robot City
=======================================
Módulo para simular el entrelazamiento cuántico entre qubits:
estados de Bell, pares EPR, puertas CNOT y Hadamard,
teletransportación cuántica y estados GHZ.

Requisitos: numpy
"""

import numpy as np


# ─────────────────────────────────────────────
#  Puertas cuánticas básicas (constantes)
# ─────────────────────────────────────────────

PUERTA_HADAMARD = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
PUERTA_X = np.array([[0, 1], [1, 0]], dtype=complex)          # Pauli X / NOT
PUERTA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)       # Pauli Y
PUERTA_Z = np.array([[1, 0], [0, -1]], dtype=complex)         # Pauli Z
PUERTA_IDENTIDAD = np.eye(2, dtype=complex)


class Qubit:
    """
    Representa un qubit individual con su estado de superposición.

    El estado se almacena como un vector complejo [α, β] donde:
        α = amplitud del estado |0⟩
        β = amplitud del estado |1⟩
        |α|² + |β|² = 1
    """

    def __init__(self, alpha: complex = 1.0, beta: complex = 0.0):
        """
        Inicializa el qubit con amplitudes α y β.

        Por defecto el qubit está en el estado base |0⟩.

        Args:
            alpha: Amplitud compleja del estado |0⟩.
            beta: Amplitud compleja del estado |1⟩.
        """
        self.state = np.array([alpha, beta], dtype=complex)
        self._normalizar()

    def _normalizar(self) -> None:
        """Normaliza el vector de estado para que ‖|ψ⟩‖ = 1."""
        norma = np.linalg.norm(self.state)
        if norma > 1e-12:
            self.state = self.state / norma

    def apply_gate(self, gate_matrix: np.ndarray) -> "Qubit":
        """
        Aplica una puerta cuántica (matriz 2×2) al estado del qubit.

        Args:
            gate_matrix: Matriz unitaria 2×2 que representa la puerta.

        Returns:
            Qubit: El mismo qubit (modificado in-place) para encadenamiento.

        Raises:
            ValueError: Si la matriz no es 2×2.
        """
        m = np.asarray(gate_matrix, dtype=complex)
        if m.shape != (2, 2):
            raise ValueError("La puerta debe ser una matriz 2×2.")
        self.state = m @ self.state
        self._normalizar()
        return self

    def measure(self) -> int:
        """
        Colapsa el estado del qubit y devuelve el resultado de la medición.

        La probabilidad de medir 0 es |α|² y la de medir 1 es |β|².
        Tras la medición el qubit colapsa al estado medido.

        Returns:
            int: 0 o 1 según el resultado de la medición.
        """
        prob_1 = float(np.abs(self.state[1]) ** 2)
        resultado = int(np.random.random() < prob_1)
        # Colapsar al estado medido
        self.state = np.array([1.0, 0.0], dtype=complex) if resultado == 0 \
            else np.array([0.0, 1.0], dtype=complex)
        return resultado

    def copy(self) -> "Qubit":
        """
        Crea una copia independiente del qubit.

        Returns:
            Qubit: Nuevo qubit con el mismo estado.
        """
        q = Qubit.__new__(Qubit)
        q.state = self.state.copy()
        return q

    def __repr__(self) -> str:
        alpha, beta = self.state
        prob0 = np.abs(alpha) ** 2
        prob1 = np.abs(beta) ** 2
        return (
            f"Qubit(α={alpha:.4f}, β={beta:.4f} | "
            f"P(|0⟩)={prob0:.4f}, P(|1⟩)={prob1:.4f})"
        )


class QubitEntanglement:
    """
    Módulo de entrelazamiento cuántico para Robot City.

    Implementa estados de Bell, pares EPR, teletransportación cuántica
    y estados GHZ mediante simulación matricial con numpy.
    """

    # ─── Puertas cuánticas de instancia ───────────────────────────────

    def apply_hadamard(self, qubit: Qubit) -> Qubit:
        """
        Aplica la puerta Hadamard a un qubit.

        H|0⟩ = |+⟩ = (|0⟩ + |1⟩)/√2  →  superposición equiprobable.
        H|1⟩ = |−⟩ = (|0⟩ - |1⟩)/√2

        Args:
            qubit: Qubit al que aplicar la puerta.

        Returns:
            Qubit: El mismo qubit tras aplicar Hadamard (modificado in-place).
        """
        return qubit.apply_gate(PUERTA_HADAMARD)

    def apply_cnot(self, control: Qubit, target: Qubit) -> tuple:
        """
        Aplica la puerta CNOT (Controlled-NOT) a un par de qubits.

        Si el qubit de control está en |1⟩, aplica X (NOT) al objetivo.
        Opera sobre el vector de estado de 2 qubits (4 dimensiones).
        El estado resultante puede ser entrelazado y no factorizable;
        en ese caso se almacena el estado conjunto en ambos qubits.

        CNOT = [[1,0,0,0],
                [0,1,0,0],
                [0,0,0,1],
                [0,0,1,0]]

        Args:
            control: Qubit de control.
            target: Qubit objetivo.

        Returns:
            tuple: (control, target) con referencia al estado entrelazado.
        """
        CNOT = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0],
        ], dtype=complex)

        # Producto tensorial de los estados individuales
        estado_2q = np.kron(control.state, target.state)
        nuevo_estado = CNOT @ estado_2q

        # El estado resultante puede ser entrelazado (no factorizable).
        # Almacenarlo completo en ambos qubits para medición correlacionada.
        control._estado_entrelazado = nuevo_estado
        target._estado_entrelazado = nuevo_estado

        # Actualizar estados individuales con probabilidades marginales
        # (representación aproximada para uso independiente)
        prob_c0 = float(np.abs(nuevo_estado[0]) ** 2 + np.abs(nuevo_estado[1]) ** 2)
        prob_c1 = 1.0 - prob_c0
        norma_c = np.sqrt(max(prob_c0, 1e-15))
        norma_t0 = np.linalg.norm(nuevo_estado[:2])
        norma_t1 = np.linalg.norm(nuevo_estado[2:])
        control.state = np.array([np.sqrt(prob_c0), np.sqrt(prob_c1)], dtype=complex)
        target.state = (
            nuevo_estado[:2] / norma_t0 if norma_t0 > 1e-12
            else nuevo_estado[2:] / max(norma_t1, 1e-12)
        )

        return control, target

    # ─── Estados de Bell ──────────────────────────────────────────────

    def create_bell_state(self, tipo: str = "phi_plus") -> np.ndarray:
        """
        Crea uno de los cuatro estados de Bell (base de entrelazamiento máximo).

        Los cuatro estados de Bell forman una base ortonormal del espacio
        de 2 qubits:
            Φ+ = (|00⟩ + |11⟩) / √2
            Φ- = (|00⟩ - |11⟩) / √2
            Ψ+ = (|01⟩ + |10⟩) / √2
            Ψ- = (|01⟩ - |10⟩) / √2

        Args:
            tipo: Tipo de estado Bell: 'phi_plus', 'phi_minus',
                  'psi_plus' o 'psi_minus'.

        Returns:
            np.ndarray: Vector de estado Bell de 4 componentes.

        Raises:
            ValueError: Si el tipo de estado no es reconocido.
        """
        estados = {
            "phi_plus":  np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2),
            "phi_minus": np.array([1, 0, 0, -1], dtype=complex) / np.sqrt(2),
            "psi_plus":  np.array([0, 1, 1, 0], dtype=complex) / np.sqrt(2),
            "psi_minus": np.array([0, 1, -1, 0], dtype=complex) / np.sqrt(2),
        }
        if tipo not in estados:
            raise ValueError(
                f"Estado Bell '{tipo}' desconocido. "
                f"Opciones: {list(estados.keys())}"
            )
        return estados[tipo]

    def entangle_qubits(self, qubit_a: Qubit, qubit_b: Qubit) -> np.ndarray:
        """
        Entrelaza dos qubits creando un par EPR (Einstein-Podolsky-Rosen).

        Proceso:
        1. Aplica Hadamard al qubit A → superposición.
        2. Aplica CNOT con A como control y B como objetivo.

        El resultado es el estado de Bell Φ+: (|00⟩ + |11⟩)/√2.

        Args:
            qubit_a: Primer qubit (se usará como control).
            qubit_b: Segundo qubit (se usará como objetivo).

        Returns:
            np.ndarray: Estado entrelazado de 4 componentes (sistema AB).
        """
        # Paso 1: Hadamard en qubit A
        self.apply_hadamard(qubit_a)

        # Paso 2: CNOT con A como control
        CNOT = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0],
        ], dtype=complex)

        estado_2q = np.kron(qubit_a.state, qubit_b.state)
        estado_entrelazado = CNOT @ estado_2q

        # Almacenar referencia cruzada del estado entrelazado
        qubit_a._estado_entrelazado = estado_entrelazado
        qubit_b._estado_entrelazado = estado_entrelazado

        return estado_entrelazado

    def measure_entangled_pair(self, qubit_a: Qubit, qubit_b: Qubit) -> tuple:
        """
        Mide un par entrelazado con colapso correlacionado.

        En un par EPR, medir qubit A colapsa instantáneamente el estado de B.
        Para Φ+: si A → 0, entonces B → 0; si A → 1, entonces B → 1.

        Args:
            qubit_a: Primer qubit del par entrelazado.
            qubit_b: Segundo qubit del par entrelazado.

        Returns:
            tuple: (resultado_a, resultado_b) — resultados correlacionados.
        """
        # Verificar si tienen un estado entrelazado compartido
        estado_ent = getattr(qubit_a, "_estado_entrelazado", None)

        if estado_ent is not None and len(estado_ent) == 4:
            # Medir sobre el estado conjunto de 4 dimensiones
            probs = np.abs(estado_ent) ** 2
            probs /= probs.sum()  # Renormalizar por precisión numérica

            # Los 4 estados posibles: |00⟩, |01⟩, |10⟩, |11⟩
            indice = int(np.random.choice(4, p=probs))
            resultado_a = indice >> 1
            resultado_b = indice & 1
        else:
            # Medir de forma independiente si no están entrelazados
            resultado_a = qubit_a.measure()
            resultado_b = qubit_b.measure()

        # Colapsar ambos qubits al estado medido
        estado_a = np.array([1.0, 0.0] if resultado_a == 0 else [0.0, 1.0])
        estado_b = np.array([1.0, 0.0] if resultado_b == 0 else [0.0, 1.0])
        qubit_a.state = estado_a.astype(complex)
        qubit_b.state = estado_b.astype(complex)

        # Eliminar referencia al estado entrelazado (ya colapsado)
        qubit_a._estado_entrelazado = None
        qubit_b._estado_entrelazado = None

        return resultado_a, resultado_b

    def create_ghz_state(self, n_qubits: int = 3) -> np.ndarray:
        """
        Crea el estado GHZ (Greenberger-Horne-Zeilinger) para n qubits.

        El estado GHZ es una superposición máximamente entrelazada:
            |GHZ⟩ = (|00...0⟩ + |11...1⟩) / √2

        Es la generalización de los estados de Bell para más de 2 qubits.

        Args:
            n_qubits: Número de qubits entrelazados (mínimo 2).

        Returns:
            np.ndarray: Vector de estado GHZ de 2^n componentes.

        Raises:
            ValueError: Si n_qubits < 2.
        """
        if n_qubits < 2:
            raise ValueError("Se necesitan al menos 2 qubits para el estado GHZ.")

        dim = 2 ** n_qubits
        estado_ghz = np.zeros(dim, dtype=complex)
        estado_ghz[0] = 1.0 / np.sqrt(2)      # |00...0⟩
        estado_ghz[-1] = 1.0 / np.sqrt(2)     # |11...1⟩
        return estado_ghz

    def teleport_state(
        self,
        source_qubit: Qubit,
        qubit_a: Qubit,
        qubit_b: Qubit,
        verbose: bool = False,
    ) -> Qubit:
        """
        Simula la teletransportación cuántica del estado de source_qubit a qubit_b.

        Protocolo de teletransportación (Bennett et al., 1993):
        1. qubit_a y qubit_b forman un par EPR.
        2. Se miden source_qubit y qubit_a juntos (medición de Bell).
        3. Basándose en los resultados, se aplican correcciones a qubit_b.
        4. qubit_b adquiere el estado original de source_qubit.

        Args:
            source_qubit: Qubit cuyo estado se desea teletransportar.
            qubit_a: Qubit auxiliar del par EPR (lado del emisor).
            qubit_b: Qubit destino del par EPR (lado del receptor).
            verbose: Si True, imprime información de depuración del proceso.

        Returns:
            Qubit: qubit_b con el estado teletransportado.
        """
        # Estado original a teletransportar
        estado_original = source_qubit.state.copy()
        alpha, beta = estado_original

        # Paso 1: Crear par EPR entre qubit_a y qubit_b
        self.entangle_qubits(qubit_a, qubit_b)

        # Paso 2: Medición de Bell en (source, qubit_a)
        # Aplicar CNOT con source como control y qubit_a como objetivo
        CNOT = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0],
        ], dtype=complex)
        estado_sa = np.kron(source_qubit.state, qubit_a.state)
        estado_sa = CNOT @ estado_sa

        # Aplicar Hadamard al qubit source
        H_total = np.kron(PUERTA_HADAMARD, PUERTA_IDENTIDAD)
        estado_sa = H_total @ estado_sa

        # Medir los qubits source y qubit_a (colapso)
        probs = np.abs(estado_sa) ** 2
        probs /= probs.sum()
        indice = int(np.random.choice(4, p=probs))
        m0 = indice >> 1   # resultado de source_qubit
        m1 = indice & 1    # resultado de qubit_a

        # Paso 3: Aplicar correcciones clásicas a qubit_b
        # Las correcciones dependen de los bits medidos (m0, m1):
        #   m1=1 → aplicar X (bit-flip)
        #   m0=1 → aplicar Z (phase-flip)
        if m1 == 1:
            qubit_b.apply_gate(PUERTA_X)
        if m0 == 1:
            qubit_b.apply_gate(PUERTA_Z)

        if verbose:
            print(
                f"[Teletransportación] Estado original: α={alpha:.4f}, β={beta:.4f}"
            )
            print(
                f"[Teletransportación] Estado recibido: α={qubit_b.state[0]:.4f}, "
                f"β={qubit_b.state[1]:.4f}"
            )
            print(f"[Teletransportación] Bits medidos: m0={m0}, m1={m1}")

        return qubit_b

    def visualize_state(self, qubit: Qubit) -> None:
        """
        Muestra una representación textual del estado del qubit.

        Muestra las amplitudes, probabilidades y una representación
        visual simplificada de la esfera de Bloch.

        Args:
            qubit: Qubit a visualizar.
        """
        alpha, beta = qubit.state
        prob0 = float(np.abs(alpha) ** 2)
        prob1 = float(np.abs(beta) ** 2)

        # Calcular coordenadas de la esfera de Bloch
        theta = 2 * np.arccos(np.clip(np.abs(alpha), 0, 1))
        phi = float(np.angle(beta) - np.angle(alpha))

        # Barra de probabilidad visual (20 caracteres)
        barra_len = 20
        n0 = int(prob0 * barra_len)
        n1 = barra_len - n0
        barra = "█" * n0 + "░" * n1

        print("\n┌─────────────────────────────────────────┐")
        print("│        Esfera de Bloch (Texto)          │")
        print("├─────────────────────────────────────────┤")
        print(f"│  α = {alpha:+.4f}  (P(|0⟩) = {prob0:.4f})        │")
        print(f"│  β = {beta:+.4f}  (P(|1⟩) = {prob1:.4f})        │")
        print(f"│  θ = {np.degrees(theta):.2f}°   φ = {np.degrees(phi):.2f}°           │")
        print(f"│  |0⟩ [{barra}] |1⟩  │")
        print("│                                         │")

        # Estado dominante
        if prob0 > 0.99:
            estado_desc = "Estado base |0⟩ (polo norte)"
        elif prob1 > 0.99:
            estado_desc = "Estado base |1⟩ (polo sur)"
        elif np.isclose(prob0, 0.5, atol=0.01):
            estado_desc = "Superposición equiprobable |±⟩"
        else:
            estado_desc = f"Superposición (domina |{'0' if prob0 > prob1 else '1'}⟩)"

        print(f"│  Estado: {estado_desc:<32}│")
        print("└─────────────────────────────────────────┘")


if __name__ == "__main__":
    print("=" * 60)
    print("  Robot City — Entrelazamiento de Qubits")
    print("=" * 60)

    ent = QubitEntanglement()

    # --- Estado inicial |0⟩ ---
    print("\n--- Qubit en estado |0⟩ ---")
    q = Qubit()
    print(q)
    ent.visualize_state(q)

    # --- Aplicar Hadamard → superposición ---
    print("\n--- Aplicar Hadamard → superposición ---")
    q_super = Qubit()
    ent.apply_hadamard(q_super)
    print(q_super)
    ent.visualize_state(q_super)

    # --- Estados de Bell ---
    print("\n--- Estados de Bell ---")
    for tipo in ["phi_plus", "phi_minus", "psi_plus", "psi_minus"]:
        estado = ent.create_bell_state(tipo)
        print(f"  {tipo}: {estado}")

    # --- Entrelazamiento EPR ---
    print("\n--- Entrelazamiento EPR ---")
    qa = Qubit()  # |0⟩
    qb = Qubit()  # |0⟩
    estado_epr = ent.entangle_qubits(qa, qb)
    print(f"Estado EPR (Φ+): {estado_epr}")

    # --- Medir par entrelazado ---
    print("\n--- Medición de par entrelazado ---")
    qa2 = Qubit()
    qb2 = Qubit()
    ent.entangle_qubits(qa2, qb2)
    r_a, r_b = ent.measure_entangled_pair(qa2, qb2)
    print(f"Resultado: qubit_A={r_a}, qubit_B={r_b} (deben ser iguales en Φ+)")

    # --- Estado GHZ de 3 qubits ---
    print("\n--- Estado GHZ (3 qubits) ---")
    ghz = ent.create_ghz_state(3)
    print(f"GHZ = {ghz}")

    # --- Teletransportación cuántica ---
    print("\n--- Teletransportación cuántica ---")
    q_origen = Qubit(alpha=0.6, beta=0.8)  # Estado arbitrario
    q_aux = Qubit()
    q_destino = Qubit()
    print(f"Qubit origen: {q_origen}")
    q_teletransportado = ent.teleport_state(q_origen, q_aux, q_destino, verbose=True)
    print(f"Qubit destino: {q_teletransportado}")
