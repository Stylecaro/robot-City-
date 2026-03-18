# Referencia de API - quantum-core

Documentación de las funciones y clases principales del módulo `quantum-core`.

---

## algorithms

### `run_qaoa_maxcut(graph, p=1)`

Ejecuta el algoritmo QAOA para el problema de corte máximo en grafos (stub).

**Parámetros:**
- `graph` (list of tuple): Lista de aristas. Ej: `[(0,1),(1,2)]`
- `p` (int): Profundidad del circuito. Por defecto `1`.

**Retorna:** `dict` con claves `result`, `info`, `graph`, `p`.

**Ejemplo:**
```python
from quantum_core.algorithms import run_qaoa_maxcut
res = run_qaoa_maxcut([(0,1),(1,2)], p=2)
```

---

### `grover_search(oracles, n_iters=1)`

Stub del algoritmo de búsqueda de Grover.

**Parámetros:**
- `oracles` (list): Lista de oráculos (estados marcados).
- `n_iters` (int): Número de iteraciones.

**Retorna:** `dict` con claves `result`, `info`, `oracles`, `n_iters`.

---

## circuits

### `build_traffic_light_circuit(params=None)`

Construye un circuito de semáforo cuántico simulado.

**Parámetros:**
- `params` (dict, opcional): `{"qubits": 3}` por defecto.

**Retorna:** `dict` con `name`, `qubits`, `gates`, `measurements`.

**Ejemplo:**
```python
from quantum_core.circuits import build_traffic_light_circuit
import json
circuito = build_traffic_light_circuit({"qubits": 3})
print(json.dumps(circuito, indent=2))
```

---

### `entanglement_layer(n_qubits)`

Construye la matriz unitaria de entrelazamiento para `n_qubits`.

**Parámetros:**
- `n_qubits` (int): Número de qubits (≥ 1).

**Retorna:** `numpy.ndarray` de forma `(2**n, 2**n)`.

**Ejemplo:**
```python
from quantum_core.circuits import entanglement_layer
mat = entanglement_layer(2)
print(mat.shape)  # (4, 4)
```

---

## backends

### `LocalSimulator(shots=1024)`

Simulador cuántico local basado en numpy.

**Métodos:**
- `run(circuit) -> dict`: Ejecuta el circuito y devuelve `counts`, `probabilities`, `shots`, `backend`.

**Ejemplo:**
```python
from quantum_core.backends import LocalSimulator
from quantum_core.circuits import build_traffic_light_circuit
sim = LocalSimulator(shots=512)
resultado = sim.run(build_traffic_light_circuit())
```

---

### `IBMQBackend(backend_name="ibmq_qasm_simulator")`

Cliente stub para IBM Quantum. Lanza `NotImplementedError`.

**Métodos:**
- `submit_circuit(circuit, api_key=None)`: Stub — lanza `NotImplementedError`.

---

## hybrid

### `QuantumNeuralLayer(n_qubits=4, seed=None)`

Capa neuronal cuántica híbrida simulada.

**Métodos:**
- `forward(inputs) -> numpy.ndarray`: Aplica transformación cuántica simulada.

**Ejemplo:**
```python
from quantum_core.hybrid import QuantumNeuralLayer
capa = QuantumNeuralLayer(n_qubits=4, seed=42)
salida = capa.forward([0.5, 0.3, 0.8, 0.1])
```
