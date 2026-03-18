# Referencia de API — quantum-core

Módulo cuántico de Ciudad Robot. Todos los módulos están en Python y solo
requieren `numpy` como dependencia principal.

---

## `circuits.traffic_light_circuit`

### `build_traffic_light_circuit() → dict`

Construye el circuito cuántico de semáforo con 2 qubits.

**Devuelve:**

```python
{
    "nombre": "SemaforoQuantico",
    "qubits": 2,
    "estados": ["|00> -> rojo", "|01> -> amarillo", "|10> -> verde", "|11> -> no_usado"],
    "amplitudes": [0.707, 0.707, 0.0, 0.0],
    "matriz": [[...]]  # 4x4
}
```

**Ejemplo:**

```python
from circuits.traffic_light_circuit import build_traffic_light_circuit
circuito = build_traffic_light_circuit()
print(circuito["nombre"])  # "SemaforoQuantico"
```

---

## `circuits.entanglement_layer`

### `entanglement_layer(n_qubits: int) → numpy.ndarray`

Genera la matriz unitaria de una capa de entrelazamiento CNOT en cadena.

**Parámetros:** `n_qubits` (int, ≥ 2)

**Devuelve:** `ndarray` de forma `(2**n_qubits, 2**n_qubits)`

**Ejemplo:**

```python
import numpy as np
from circuits.entanglement_layer import entanglement_layer
M = entanglement_layer(3)
print(M.shape)  # (8, 8)
print(np.allclose(M @ M.conj().T, np.eye(8)))  # True
```

---

## `backends.local_simulator`

### `LocalSimulator(shots=1024)`

Simulador cuántico local sin hardware real.

#### `run(circuit: dict) → dict`

**Parámetros:** `circuit` con claves `amplitudes` y `matriz`.

**Devuelve:**

```python
{
    "backend": "LocalSimulator",
    "shots": 1024,
    "estado_final": [...],
    "probabilidades": [...],
    "conteos": {"00": 512, "01": 512, ...}
}
```

**Ejemplo:**

```python
from backends.local_simulator import LocalSimulator
from circuits.traffic_light_circuit import build_traffic_light_circuit
sim = LocalSimulator(shots=512)
resultado = sim.run(build_traffic_light_circuit())
print(resultado["conteos"])
```

---

## `backends.ibm_quantum`

### `IBMQBackend(backend_name="ibm_brisbane")`

Plantilla para IBM Quantum. Requiere Qiskit y API key.

#### `submit_circuit(circuit, api_key=None)`

Lanza `NotImplementedError`. Ver docstring para instrucciones de integración.

---

## `algorithms.qaoa_maxcut`

### `run_qaoa_maxcut(graph: dict, p: int = 1) → dict`

Plantilla QAOA para Max-Cut. Devuelve resultado placeholder.

**Ejemplo:**

```python
from algorithms.qaoa_maxcut import run_qaoa_maxcut
grafo = {"nodos": [0, 1, 2], "aristas": [(0, 1), (1, 2)]}
resultado = run_qaoa_maxcut(grafo, p=2)
print(resultado["algoritmo"])  # "QAOA-MaxCut"
```

---

## `algorithms.grover_search`

### `grover_search(oracles: list, n_iters: int = 1) → dict`

Plantilla del algoritmo de Grover. Devuelve resultado placeholder.

---

## `hybrid.quantum_neural_layer`

### `QuantumNeuralLayer(n_qubits=4, n_outputs=2, seed=None)`

Capa neuronal cuántica simulada.

#### `forward(inputs: array-like) → numpy.ndarray`

Aplica transformación cuántica simulada y devuelve vector de salida de longitud `n_outputs`.

**Ejemplo:**

```python
import numpy as np
from hybrid.quantum_neural_layer import QuantumNeuralLayer
capa = QuantumNeuralLayer(n_qubits=2, n_outputs=2, seed=42)
salida = capa.forward([1.0, 0.0, 0.0, 0.0])
print(salida.shape)  # (2,)
```

---

## Endpoint REST

`POST /api/quantum/run-circuit`

```json
{
    "circuit_name": "traffic_light",
    "params": {}
}
```

Respuesta:

```json
{
    "success": true,
    "circuit_name": "traffic_light",
    "resultado": { "circuito": "SemaforoQuantico", ... }
}
```
