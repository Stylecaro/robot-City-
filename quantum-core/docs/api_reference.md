# Referencia de API - quantum-core

Documentación de referencia de las funciones y clases públicas del módulo quantum-core.

---

## Módulo `algorithms`

### `run_qaoa_maxcut(graph, p=1)`

Ejecuta el algoritmo QAOA para resolver el problema MaxCut.

**Parámetros:**
| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `graph` | `dict` | Grafo con claves `"nodos"` (list) y `"aristas"` (list de tuplas) |
| `p` | `int` | Número de capas del ansatz QAOA (default: 1) |

**Retorna:** `dict` con claves `corte_maximo`, `particion`, `probabilidades`, `capas_p`

**Ejemplo:**
```python
from quantum_core.algorithms import run_qaoa_maxcut

grafo = {"nodos": [0, 1, 2, 3], "aristas": [(0,1), (1,2), (2,3), (3,0)]}
resultado = run_qaoa_maxcut(grafo, p=2)
print(resultado["corte_maximo"])  # entero
```

---

### `grover_search(oracles, n_iters=1)`

Ejecuta el algoritmo de búsqueda de Grover.

**Parámetros:**
| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `oracles` | `list[callable]` | Lista de funciones oráculo que reciben un bitstring y retornan bool |
| `n_iters` | `int` | Número de iteraciones del operador de Grover (default: 1) |

**Retorna:** `dict` con claves `estado_encontrado`, `probabilidad`, `iteraciones`, `conteos`

---

## Módulo `circuits`

### `build_traffic_light_circuit(params=None)`

Construye el circuito cuántico de semáforo.

**Parámetros:**
| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `params` | `dict` o `None` | Parámetros: `theta`, `phi`, `n_qubits`, `circuit_name` |

**Retorna:** `dict` con `circuit_name`, `n_qubits`, `gates`, `measurements`, `params`

---

### `entanglement_layer(n_qubits)`

Construye una capa de entrelazamiento cuántico.

**Parámetros:**
| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `n_qubits` | `int` | Número de qubits (≥ 1) |

**Retorna:** `numpy.ndarray` de forma `(2^n_qubits,)` con el estado cuántico normalizado.

**Lanza:** `ValueError` si `n_qubits < 1`

---

### `hadamard(n_qubits=1)`

Devuelve la matriz Hadamard para `n_qubits` qubits.

**Retorna:** `numpy.ndarray` de forma `(2^n_qubits, 2^n_qubits)`

---

### `cnot(n_qubits=2)`

Devuelve la matriz CNOT extendida al sistema de `n_qubits` qubits.

**Retorna:** `numpy.ndarray` de forma `(2^n_qubits, 2^n_qubits)`

---

## Módulo `backends`

### Clase `LocalSimulator`

Simulador cuántico local basado en numpy.

**Constructor:** `LocalSimulator(shots=1024, seed=42)`

**Método `run(circuit)`:**
- **Parámetros:** `circuit` (dict) — representación del circuito
- **Retorna:** `dict` con `conteos`, `shots`, `n_qubits`, `backend`
- **Lanza:** `TypeError` si el circuito no es un diccionario

---

### Clase `IBMQBackend`

Backend stub para IBM Quantum.

**Constructor:** `IBMQBackend(backend_name="ibmq_qasm_simulator", max_shots=1024, timeout=300)`

**Métodos:** `connect(token=None)`, `submit_circuit(circuit)`, `get_available_backends()`

> ⚠️ Todos los métodos lanzan `NotImplementedError`. Requiere configurar qiskit-ibm-runtime.

---

## Módulo `hybrid`

### Clase `QuantumNeuralLayer`

Capa neuronal cuántica simulada.

**Constructor:** `QuantumNeuralLayer(n_qubits=4, n_layers=2, seed=None)`

**Método `forward(inputs)`:**
- **Parámetros:** `inputs` — array de forma `(n_qubits,)`
- **Retorna:** `numpy.ndarray` de forma `(n_qubits,)` con valores en `[-1, 1]`
- **Lanza:** `ValueError` si `inputs` no tiene la forma correcta

**Otros métodos:** `get_weights()`, `set_weights(new_weights)`

---

## Endpoint Backend

### `POST /api/quantum/run-circuit`

Ejecuta el script `quantum_traffic_light_demo.py` y devuelve el resultado JSON.

**Request body:**
```json
{
  "circuit_name": "traffic_light",
  "theta": 0.8,
  "phi": 0.2,
  "n_qubits": 3
}
```

**Response (200):**
```json
{
  "success": true,
  "data": { ... }
}
```

**Errores:**
- `400` — Parámetros inválidos
- `504` — Timeout (> 30s)
- `500` — Error interno del script Python
