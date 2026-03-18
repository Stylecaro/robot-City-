# quantum-core — Módulo Cuántico para Ciudad Robot

Módulo de computación cuántica simulada integrado en el ecosistema Ciudad Robot.
Proporciona algoritmos, circuitos, backends y utilidades para experimentar con
computación cuántica sin necesidad de hardware real.

## Características

- 🔬 **Algoritmos cuánticos**: QAOA (Max-Cut), Búsqueda de Grover
- ⚡ **Circuitos**: Semáforo cuántico, capa de entrelazamiento
- 💻 **Backends**: Simulador local (numpy) + plantilla IBM Quantum
- 🧠 **Híbrido**: Capa neuronal cuántica para modelos QNN
- 🧪 **Tests**: Suite completa con pytest
- 📚 **Documentación**: Docstrings en español, guías y referencia de API

## Estructura

```
quantum-core/
├── algorithms/          # QAOA, Grover
├── circuits/            # Semáforo cuántico, entrelazamiento
├── backends/            # Simulador local, IBM Quantum (plantilla)
├── hybrid/              # Capa neuronal cuántica
├── tests/               # Tests con pytest
├── notebooks/           # Jupyter notebooks interactivos
├── docs/                # Referencia API y explicaciones
├── examples/            # Scripts de demostración
├── requirements.txt     # Dependencias (numpy, pytest)
└── quantum_core_config.json
```

## Instalación

```bash
# Instalar dependencias (solo numpy es obligatorio)
pip install -r quantum-core/requirements.txt

# Opcional: hardware real con IBM Quantum
# pip install qiskit qiskit-ibm-runtime
```

## Uso rápido

### Ejecutar la demostración del semáforo cuántico

```bash
cd quantum-core
python examples/quantum_traffic_light_demo.py
```

### Usar en Python

```python
# Simular un circuito de semáforo cuántico
from circuits.traffic_light_circuit import build_traffic_light_circuit
from backends.local_simulator import LocalSimulator

circuito = build_traffic_light_circuit()
sim = LocalSimulator(shots=1024)
resultado = sim.run(circuito)
print(resultado["conteos"])
```

### Entrelazamiento de qubits

```python
import numpy as np
from circuits.entanglement_layer import entanglement_layer

M = entanglement_layer(3)  # 8x8 para 3 qubits
print(f"Unitaria: {np.allclose(M @ M.conj().T, np.eye(8))}")
```

### Capa neuronal cuántica

```python
import numpy as np
from hybrid.quantum_neural_layer import QuantumNeuralLayer

capa = QuantumNeuralLayer(n_qubits=4, n_outputs=2)
salida = capa.forward(np.random.randn(16))
print(salida)  # array de 2 valores
```

## Tests

```bash
cd quantum-core
pytest tests/ -v
```

## Endpoint REST

El módulo expone un endpoint en el backend Node.js:

```
POST /api/quantum/run-circuit
```

```json
{
    "circuit_name": "traffic_light",
    "params": {}
}
```

Ver `backend/routes/quantum.js` para detalles.

## Integración con IBM Quantum (futuro)

Para usar hardware real:
1. Crear cuenta en https://quantum.ibm.com
2. Obtener API key
3. Configurar `IBMQ_API_KEY` como variable de entorno
4. Descomentar `qiskit` en `requirements.txt`
5. Implementar `IBMQBackend.submit_circuit` según el docstring

## Licencia

MIT License — Copyright (c) 2026 Ciudad Robot Team
