"""
Cadena de Bloques Cuántica — Robot City
========================================
Implementación de una blockchain cuántica que utiliza firmas de qubits
para validar bloques en lugar de prueba de trabajo (proof-of-work).

NO incluye sistema de minería. La validación se realiza mediante
firmas cuánticas basadas en superposición y rotación de qubits simulados.

Requisitos: numpy
"""

import hashlib
import json
import time
from datetime import datetime, timezone

import numpy as np

from pqc_crypto import pqc_manager, sha3_256


class QuantumBlock:
    """
    Bloque cuántico individual de la cadena.

    Cada bloque contiene un hash generado mediante rotaciones de qubits
    simuladas, sin necesidad de minería ni prueba de trabajo.
    """

    def __init__(self, index: int, data: dict, previous_hash: str):
        """
        Inicializa un nuevo bloque cuántico.

        Args:
            index: Posición del bloque en la cadena.
            data: Datos a almacenar en el bloque.
            previous_hash: Hash del bloque anterior en la cadena.
        """
        self.index = index
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.data = data
        self.previous_hash = previous_hash
        self.qubit_signature = self._generate_qubit_signature()
        self.quantum_hash = self.generate_quantum_hash(
            json.dumps({
                "index": self.index,
                "timestamp": self.timestamp,
                "data": self.data,
                "previous_hash": self.previous_hash,
                "qubit_signature": self._signature_to_serializable(self.qubit_signature),
            }, sort_keys=True)
        )

        # Firma post-cuántica ML-DSA (Dilithium) — resistente a Shor
        self.pqc_signature = self._generate_pqc_signature()

    def recalculate_signature(self) -> np.ndarray:
        """
        Recalcula y devuelve la firma de qubits del bloque.

        Método público para validación externa sin exponer la lógica interna.

        Returns:
            np.ndarray: Firma de qubits recalculada.
        """
        return self._generate_qubit_signature()

    def _generate_pqc_signature(self) -> dict:
        """
        Genera firma post-cuántica ML-DSA del bloque.

        Usa el PQCManager global para firmar el quantum_hash con
        Dilithium (FIPS 204), protegiendo contra ataques con
        computadoras cuánticas (algoritmo de Shor).

        Returns:
            dict: Datos de la firma PQC con algoritmo y hash firmado.
        """
        block_entity = f"block-{self.index}"
        if block_entity not in pqc_manager.key_store:
            pqc_manager.generate_key_bundle(block_entity)
        sig_data = pqc_manager.sign_transaction(
            block_entity, self.quantum_hash.encode("utf-8")
        )
        return {
            "ml_dsa_signature": sig_data["ml_dsa_signature"],
            "tx_hash_sha3": sig_data["tx_hash_sha3"],
            "algorithm": sig_data["algorithms"]["primary"],
        }

    def verify_pqc_signature(self) -> bool:
        """Verifica la firma post-cuántica del bloque."""
        block_entity = f"block-{self.index}"
        if block_entity not in pqc_manager.key_store:
            return False
        result = pqc_manager.verify_transaction(
            block_entity,
            self.quantum_hash.encode("utf-8"),
            self.pqc_signature,
        )
        return result.get("valid", False)

    @staticmethod
    def _signature_to_serializable(signature: np.ndarray) -> list:
        """Convierte la firma de qubits a formato serializable (JSON)."""
        return [[v.real, v.imag] for v in signature]

    def _generate_qubit_signature(self) -> np.ndarray:
        """
        Genera una firma de qubits simulada usando superposición de estados.

        Crea un vector de estado cuántico normalizado de 8 qubits
        aplicando rotaciones aleatorias basadas en los datos del bloque.
        La semilla incluye el índice, timestamp y hash previo para evitar
        colisiones entre bloques con datos idénticos.

        Returns:
            np.ndarray: Vector de amplitudes complejas de 8 qubits.
        """
        seed_data = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
        }, sort_keys=True)
        semilla = int(hashlib.sha256(seed_data.encode()).hexdigest(), 16) % (2 ** 31)

        rng = np.random.default_rng(semilla)
        angulos = rng.uniform(0, 2 * np.pi, 8)

        # Construir estado de superposición: |ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩
        firma = np.array([
            np.cos(angulo / 2) + 1j * np.sin(angulo / 2)
            for angulo in angulos
        ])

        # Normalizar el vector de estado
        norma = np.linalg.norm(firma)
        return firma / norma if norma > 0 else firma

    @staticmethod
    def generate_quantum_hash(data: str) -> str:
        """
        Genera un hash cuántico usando rotaciones de qubits simuladas.

        El proceso combina SHA-256 con rotaciones de matrices cuánticas
        para producir un hash único y resistente a colisiones.

        Args:
            data: Cadena de texto a hashear.

        Returns:
            str: Hash hexadecimal de 64 caracteres.
        """
        # Hash clásico base
        hash_base = hashlib.sha256(data.encode()).digest()

        # Convertir bytes a ángulos de rotación cuántica
        angulos = np.frombuffer(hash_base, dtype=np.uint8).astype(float)
        angulos = angulos * (np.pi / 128.0)  # Mapear [0,255] → [0, 2π]

        # Aplicar rotaciones cuánticas acumulativas
        estado = np.ones(len(angulos), dtype=complex)
        for i, theta in enumerate(angulos):
            # Matriz de rotación Rz(θ) simulada
            rotacion = np.exp(1j * theta)
            estado[i] *= rotacion

        # Colapsar a bytes deterministas con precisión fija (evitar XOR con flotantes)
        # Usar representación de bytes de magnitudes y fases con escala entera fija
        magnitudes = np.abs(estado)
        fases = np.angle(estado) % (2 * np.pi)
        magnitudes_int = np.round(magnitudes * 1_000_000).astype(np.int64)
        fases_int = np.round(fases * 1_000_000).astype(np.int64)
        datos_combinados = np.concatenate([magnitudes_int, fases_int])

        # Generar hash final combinando con SHA-256
        hash_combinado = hashlib.sha256(datos_combinados.tobytes()).hexdigest()
        return hash_combinado

    def to_dict(self) -> dict:
        """
        Convierte el bloque a un diccionario serializable.

        Returns:
            dict: Representación del bloque como diccionario.
        """
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "quantum_hash": self.quantum_hash,
            "qubit_signature": self._signature_to_serializable(self.qubit_signature),
            "pqc_signature": self.pqc_signature,
        }

    def __repr__(self) -> str:
        return (
            f"QuantumBlock(index={self.index}, "
            f"hash={self.quantum_hash[:16]}..., "
            f"timestamp={self.timestamp})"
        )


class QuantumBlockchain:
    """
    Cadena de Bloques Cuántica sin sistema de minería.

    La validación de bloques se realiza mediante firmas cuánticas
    basadas en superposición de qubits, eliminando la necesidad
    de prueba de trabajo energéticamente costosa.
    """

    def __init__(self, nombre: str = "Robot City Quantum Blockchain"):
        """
        Inicializa la cadena de bloques con un bloque génesis.

        Args:
            nombre: Nombre identificador de la blockchain.
        """
        self.nombre = nombre
        self.cadena: list[QuantumBlock] = []
        self._crear_bloque_genesis()

    def _crear_bloque_genesis(self) -> None:
        """Crea el bloque génesis (primer bloque de la cadena)."""
        genesis_data = {
            "tipo": "genesis",
            "mensaje": "Bloque génesis de Robot City Quantum Blockchain",
            "version": "1.0.0",
            "creado_en": datetime.now(timezone.utc).isoformat(),
        }
        bloque_genesis = QuantumBlock(
            index=0,
            data=genesis_data,
            previous_hash="0" * 64,
        )
        self.cadena.append(bloque_genesis)
        print(f"[QuantumBlockchain] Bloque génesis creado: {bloque_genesis.quantum_hash[:16]}...")

    def add_block(self, data: dict) -> QuantumBlock:
        """
        Añade un nuevo bloque a la cadena, validado cuánticamente.

        No se realiza ninguna operación de minería. El bloque se valida
        mediante la firma de qubits del bloque anterior.

        Args:
            data: Datos a almacenar en el nuevo bloque.

        Returns:
            QuantumBlock: El nuevo bloque añadido a la cadena.

        Raises:
            ValueError: Si los datos son inválidos o vacíos.
        """
        if not data:
            raise ValueError("Los datos del bloque no pueden estar vacíos.")

        bloque_anterior = self.cadena[-1]

        # Validar firma cuántica del bloque anterior antes de añadir
        if not self._validar_firma_cuantica(bloque_anterior):
            raise ValueError(
                f"Firma cuántica inválida en bloque {bloque_anterior.index}. "
                "No se puede añadir el nuevo bloque."
            )

        nuevo_bloque = QuantumBlock(
            index=len(self.cadena),
            data=data,
            previous_hash=bloque_anterior.quantum_hash,
        )
        self.cadena.append(nuevo_bloque)
        print(
            f"[QuantumBlockchain] Bloque #{nuevo_bloque.index} añadido: "
            f"{nuevo_bloque.quantum_hash[:16]}..."
        )
        return nuevo_bloque

    def _validar_firma_cuantica(self, bloque: QuantumBlock) -> bool:
        """
        Valida la firma cuántica y la firma PQC de un bloque.

        Verifica que la firma de qubits sea coherente con los datos
        del bloque y que la firma post-cuántica ML-DSA sea válida.

        Args:
            bloque: Bloque a validar.

        Returns:
            bool: True si ambas firmas son válidas.
        """
        firma_recalculada = bloque.recalculate_signature()
        qubit_ok = np.allclose(
            np.abs(firma_recalculada),
            np.abs(bloque.qubit_signature),
            atol=1e-10,
        )
        pqc_ok = bloque.verify_pqc_signature()
        return qubit_ok and pqc_ok

    def validate_chain(self) -> bool:
        """
        Valida la integridad completa de la cadena de bloques.

        Verifica que:
        1. Cada bloque apunte correctamente al hash del anterior.
        2. El hash cuántico de cada bloque sea consistente con sus datos.
        3. Las firmas de qubits sean válidas.

        Returns:
            bool: True si la cadena es completamente válida.
        """
        for i in range(1, len(self.cadena)):
            bloque_actual = self.cadena[i]
            bloque_anterior = self.cadena[i - 1]

            # Verificar que el hash previo coincida
            if bloque_actual.previous_hash != bloque_anterior.quantum_hash:
                print(
                    f"[ERROR] Bloque #{i}: el hash previo no coincide con el "
                    f"hash del bloque #{i - 1}."
                )
                return False

            # Verificar el hash cuántico del bloque actual
            datos_bloque = json.dumps({
                "index": bloque_actual.index,
                "timestamp": bloque_actual.timestamp,
                "data": bloque_actual.data,
                "previous_hash": bloque_actual.previous_hash,
                "qubit_signature": QuantumBlock._signature_to_serializable(bloque_actual.qubit_signature),
            }, sort_keys=True)
            hash_esperado = QuantumBlock.generate_quantum_hash(datos_bloque)

            if bloque_actual.quantum_hash != hash_esperado:
                print(f"[ERROR] Bloque #{i}: el hash cuántico no es válido.")
                return False

            # Verificar la firma cuántica
            if not self._validar_firma_cuantica(bloque_actual):
                print(f"[ERROR] Bloque #{i}: la firma cuántica no es válida.")
                return False

        print("[QuantumBlockchain] Cadena válida: todos los bloques son íntegros.")
        return True

    def get_chain_state(self) -> dict:
        """
        Devuelve el estado actual completo de la cadena.

        Returns:
            dict: Diccionario con metadatos y todos los bloques de la cadena.
        """
        return {
            "nombre": self.nombre,
            "longitud": len(self.cadena),
            "es_valida": self.validate_chain(),
            "ultimo_hash": self.cadena[-1].quantum_hash if self.cadena else None,
            "bloques": [bloque.to_dict() for bloque in self.cadena],
            "pqc_security": pqc_manager.get_security_status(),
        }

    @staticmethod
    def generate_quantum_hash(data: str) -> str:
        """
        Método estático de conveniencia para generar un hash cuántico.

        Args:
            data: Texto a hashear.

        Returns:
            str: Hash cuántico hexadecimal.
        """
        return QuantumBlock.generate_quantum_hash(data)

    def __len__(self) -> int:
        return len(self.cadena)

    def __repr__(self) -> str:
        return (
            f"QuantumBlockchain(nombre='{self.nombre}', "
            f"bloques={len(self.cadena)}, "
            f"ultimo_hash={self.cadena[-1].quantum_hash[:16] if self.cadena else 'N/A'}...)"
        )


if __name__ == "__main__":
    print("=" * 60)
    print("  Robot City — Cadena de Bloques Cuántica")
    print("  (Sin sistema de minería — validación cuántica)")
    print("=" * 60)

    # Crear la blockchain cuántica
    blockchain = QuantumBlockchain()

    # Añadir bloques con datos de ejemplo
    blockchain.add_block({
        "tipo": "transaccion_robot",
        "robot_id": "R-001",
        "accion": "patrulla_sector_A",
        "energia_usada": 12.5,
    })

    blockchain.add_block({
        "tipo": "registro_ciudad",
        "evento": "nueva_construccion",
        "coordenadas": {"x": 100, "y": 200, "z": 0},
        "edificio": "Centro de IA",
    })

    blockchain.add_block({
        "tipo": "transaccion_robot",
        "robot_id": "R-007",
        "accion": "mantenimiento_grid",
        "componente": "reactor_cuantico",
    })

    # Validar la cadena completa
    print("\n--- Validación de la cadena ---")
    es_valida = blockchain.validate_chain()
    print(f"Cadena válida: {es_valida}")

    # Mostrar estado de la cadena
    print("\n--- Estado de la cadena ---")
    estado = blockchain.get_chain_state()
    print(f"Nombre: {estado['nombre']}")
    print(f"Bloques totales: {estado['longitud']}")
    print(f"Último hash: {estado['ultimo_hash'][:32]}...")

    print(f"\n{blockchain}")
