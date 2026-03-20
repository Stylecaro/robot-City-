# 🔗 Robot City — Sistema de Cadena de Bloques Cuántica

> Sistema cuántico de validación de bloques basado en firmas de qubits y matrices cuánticas.
> **Sin minería. Sin proof-of-work. Solo física cuántica simulada.**

---

## 📋 Índice

1. [¿Qué es la Blockchain Cuántica?](#-qué-es-la-blockchain-cuántica)
2. [¿Por qué no hay minería?](#-por-qué-no-hay-minería)
3. [Estructura del sistema](#-estructura-del-sistema)
4. [Guía de uso — Blockchain Cuántica](#-guía-de-uso--blockchain-cuántica)
5. [Guía de uso — Creador de Matrices](#-guía-de-uso--creador-de-matrices)
6. [Guía de uso — Entrelazamiento de Qubits](#-guía-de-uso--entrelazamiento-de-qubits)
7. [Ejemplos de código](#-ejemplos-de-código)
8. [Requisitos](#-requisitos)

---

## ⚛️ ¿Qué es la Blockchain Cuántica?

La **Cadena de Bloques Cuántica** de Robot City es un sistema de registro
distribuido que utiliza principios de la mecánica cuántica simulada para
garantizar la integridad de los datos.

### Características principales

| Característica | Descripción |
|---|---|
| **Sin minería** | No se utiliza proof-of-work ni nonce. Los bloques son válidos por firma cuántica. |
| **Firmas de qubits** | Cada bloque lleva una firma generada mediante superposición de 8 qubits. |
| **Hash cuántico** | El hash se calcula aplicando rotaciones de matrices cuánticas sobre SHA-256. |
| **Validación instantánea** | La cadena se puede validar en tiempo O(n) sin cálculos costosos. |
| **Solo numpy** | No requiere Qiskit, Cirq ni otras librerías de computación cuántica. |

---

## 🚫 ¿Por qué no hay minería?

Los sistemas de blockchain clásicos (Bitcoin, Ethereum PoW) utilizan
**prueba de trabajo (proof-of-work)**, que requiere resolver puzzles
matemáticos costosos computacionalmente para añadir un bloque.

### Problemas de la minería clásica

- 🔋 **Enorme consumo energético** — Las redes de prueba de trabajo pueden consumir decenas de TWh anuales.
- ⏱️ **Lentitud** — Confirmaciones en minutos u horas.
- 💰 **Centralización económica** — Favorece a quienes tienen más hardware.
- ♻️ **No sostenible** — Impacto ambiental masivo.

### Ventajas de la validación cuántica

En su lugar, Robot City usa **firmas cuánticas** basadas en:

1. **Superposición de estados** — Cada bloque genera un estado cuántico
   único basado en sus datos, imposible de falsificar sin modificar los datos.

2. **Rotaciones de qubits** — El hash se obtiene aplicando rotaciones de
   matrices cuánticas (Rz, Rx, Ry) sobre el hash SHA-256, produciendo
   un resultado determinista pero cuánticamente robusto.

3. **Verificación instantánea** — Validar una firma cuántica es O(1)
   mientras que minar un bloque es O(2^dificultad).

```
Blockchain clásica: Datos → SHA-256 → Nonce mining (costoso) → Hash válido
Blockchain cuántica: Datos → SHA-256 + rotaciones cuánticas → Firma de qubits → Hash válido (instantáneo)
```

---

## 📁 Estructura del sistema

```
quantum-blockchain/
├── quantum_blockchain.py          # Cadena de bloques cuántica principal
├── matrix_creator.py              # Creador de matrices cuánticas
├── qubit_entanglement.py          # Entrelazamiento de qubits
├── quantum_blockchain_config.json # Configuración del sistema
└── README_QUANTUM.md              # Esta documentación
```

---

## 🔗 Guía de uso — Blockchain Cuántica

### Crear una blockchain

```python
from quantum_blockchain import QuantumBlockchain

# Crear la blockchain (genera el bloque génesis automáticamente)
blockchain = QuantumBlockchain(nombre="Mi Blockchain Cuántica")
```

### Añadir bloques

```python
# Añadir un bloque con datos arbitrarios (sin minería)
bloque = blockchain.add_block({
    "tipo": "transaccion",
    "robot_id": "R-001",
    "accion": "patrulla",
    "energia": 12.5
})

print(bloque)
# QuantumBlock(index=1, hash=a3f8c2d1..., timestamp=2024-01-01T00:00:00)
```

### Validar la cadena

```python
# Validar toda la cadena (sin mining, verificación por firma cuántica)
es_valida = blockchain.validate_chain()
print(f"Cadena válida: {es_valida}")  # True
```

### Obtener estado de la cadena

```python
estado = blockchain.get_chain_state()
print(f"Bloques: {estado['longitud']}")
print(f"Último hash: {estado['ultimo_hash']}")
```

### Generar hash cuántico manualmente

```python
from quantum_blockchain import QuantumBlockchain

hash_cuantico = QuantumBlockchain.generate_quantum_hash("Hola Robot City")
print(hash_cuantico)
```

---

## 🔢 Guía de uso — Creador de Matrices

```python
from matrix_creator import QuantumMatrixCreator
import numpy as np

creador = QuantumMatrixCreator()
```

### Matriz de Hadamard

```python
# Hadamard de 1 qubit (2×2)
H = creador.create_hadamard_matrix(1)

# Hadamard de 2 qubits (4×4) — H⊗H
H2 = creador.create_hadamard_matrix(2)

creador.print_matrix(H, "Hadamard H")
```

### Matrices de Pauli

```python
paulis = creador.create_pauli_matrices()
# Claves: 'I' (identidad), 'X' (NOT), 'Y', 'Z'

creador.print_matrix(paulis['X'], "Pauli X")
creador.print_matrix(paulis['Z'], "Pauli Z")
```

### Matrices de rotación

```python
import math

# Rotación de π/2 alrededor del eje X
Rx = creador.create_rotation_matrix(math.pi / 2, "x")

# Rotación de π alrededor del eje Z (puerta de fase)
Rz = creador.create_rotation_matrix(math.pi, "z")
```

### Matriz de entrelazamiento

```python
# Genera el circuito de entrelazamiento para 2 qubits (produce estado Bell)
M_ent = creador.create_entanglement_matrix(2)
```

### Producto tensorial

```python
I = paulis['I']
X = paulis['X']

# I⊗X — actúa con I en el primer qubit y X en el segundo
IX = creador.tensor_product(I, X)
```

### Aplicar matriz a un estado

```python
# Estado |0⟩
estado_0 = np.array([1.0, 0.0], dtype=complex)

# Aplicar Hadamard → |+⟩ = (|0⟩ + |1⟩)/√2
estado_plus = creador.apply_matrix(estado_0, H)
print(estado_plus)  # [0.707+0j, 0.707+0j]
```

### Normalizar un estado

```python
estado = np.array([3.0, 4.0], dtype=complex)
normalizado = creador.normalize_state(estado)
print(normalizado)  # [0.6+0j, 0.8+0j]
```

---

## ⚛️ Guía de uso — Entrelazamiento de Qubits

```python
from qubit_entanglement import Qubit, QubitEntanglement

ent = QubitEntanglement()
```

### Crear y visualizar qubits

```python
# Qubit en estado |0⟩
q = Qubit()
print(q)
# Qubit(α=1.0000+0j, β=0.0000+0j | P(|0⟩)=1.0000, P(|1⟩)=0.0000)

# Visualizar en la esfera de Bloch (texto)
ent.visualize_state(q)
```

### Aplicar puertas cuánticas

```python
# Puerta Hadamard → superposición
q_super = Qubit()
ent.apply_hadamard(q_super)
print(q_super)

# Medir el qubit (colapsa la superposición)
resultado = q_super.measure()
print(f"Medido: {resultado}")  # 0 o 1 con prob. 50%
```

### Estados de Bell

```python
# Los 4 estados de Bell maximalmente entrelazados
phi_plus  = ent.create_bell_state("phi_plus")   # (|00⟩ + |11⟩)/√2
phi_minus = ent.create_bell_state("phi_minus")  # (|00⟩ - |11⟩)/√2
psi_plus  = ent.create_bell_state("psi_plus")   # (|01⟩ + |10⟩)/√2
psi_minus = ent.create_bell_state("psi_minus")  # (|01⟩ - |10⟩)/√2
```

### Entrelazamiento EPR

```python
# Entrelazar dos qubits (resultado: estado Bell Φ+)
qa = Qubit()  # |0⟩
qb = Qubit()  # |0⟩
estado_epr = ent.entangle_qubits(qa, qb)
print(f"Par EPR: {estado_epr}")

# Medir el par (resultados siempre correlacionados)
r_a, r_b = ent.measure_entangled_pair(qa, qb)
print(f"A={r_a}, B={r_b}")  # Siempre iguales: 00 o 11
```

### Estado GHZ (N qubits)

```python
# Estado GHZ de 3 qubits: (|000⟩ + |111⟩)/√2
ghz_3 = ent.create_ghz_state(3)

# Estado GHZ de 5 qubits
ghz_5 = ent.create_ghz_state(5)
```

### Teletransportación cuántica

```python
import numpy as np

# Estado a teletransportar
q_origen = Qubit(alpha=0.6, beta=0.8)

# Par EPR auxiliar para el canal cuántico
q_aux    = Qubit()
q_destino = Qubit()

# Teletransportar estado de q_origen a q_destino
q_result = ent.teleport_state(q_origen, q_aux, q_destino)
print(f"Destino tras teletransportación: {q_result}")
```

---

## 📦 Requisitos

```
numpy>=1.21.0
Python>=3.8
```

### Instalación

```bash
pip install numpy
```

### Ejecutar los módulos directamente

```bash
# Demostración de la blockchain cuántica
python quantum-blockchain/quantum_blockchain.py

# Demostración del creador de matrices
python quantum-blockchain/matrix_creator.py

# Demostración del entrelazamiento de qubits
python quantum-blockchain/qubit_entanglement.py
```

---

## 📄 Licencia

Este módulo forma parte del proyecto **Robot City** y está bajo la misma
licencia que el repositorio principal.

---

*Desarrollado para Robot City — Sistema de IA Avanzada* 🤖⚛️
