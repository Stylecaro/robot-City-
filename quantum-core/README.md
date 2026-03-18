# quantum-core — Módulo Cuántico de Ciudad Robot

Módulo central de computación cuántica para el proyecto **Ciudad Robot**.
Proporciona algoritmos cuánticos, circuitos reutilizables, backends de ejecución
y capas híbridas clásico-cuánticas para integrarse con el sistema de IA.

## Estructura del Módulo

```
quantum-core/
├── algorithms/          # Algoritmos cuánticos (QAOA, Grover)
├── circuits/            # Circuitos reutilizables (semáforo, entrelazamiento)
├── backends/            # Backends de ejecución (simulador local, IBM Quantum stub)
├── hybrid/              # Capas híbridas clásico-cuánticas
├── tests/               # Tests pytest
├── examples/            # Scripts de demostración
├── notebooks/           # Notebooks Jupyter (placeholders)
├── docs/                # Documentación técnica
├── requirements.txt     # Dependencias
└── quantum_core_config.json  # Configuración del módulo
```

## Instalación Rápida

```bash
# Instalar dependencias mínimas (solo numpy y pytest)
pip install -r quantum-core/requirements.txt
```

Para usar hardware real de IBM Quantum (opcional):
```bash
pip install qiskit qiskit-aer qiskit-ibm-runtime
```

## Uso Rápido

### Ejecutar demo del semáforo cuántico

```bash
python quantum-core/examples/quantum_traffic_light_demo.py
```

Con parámetros personalizados:
```bash
python quantum-core/examples/quantum_traffic_light_demo.py --params '{"theta": 1.0}'
```

### Usar los módulos directamente

```python
from quantum_core.circuits import build_traffic_light_circuit
from quantum_core.backends import LocalSimulator

# Construir circuito
circuito = build_traffic_light_circuit({"theta": 0.8})

# Simular localmente
sim = LocalSimulator(shots=1024)
resultado = sim.run(circuito)
print(resultado["conteos"])
```

### Algoritmos cuánticos

```python
from quantum_core.algorithms import run_qaoa_maxcut, grover_search

# QAOA para optimización de tráfico
grafo = {"nodos": [0,1,2,3], "aristas": [(0,1),(1,2),(2,3),(3,0)]}
resultado_qaoa = run_qaoa_maxcut(grafo, p=2)

# Búsqueda de Grover
oraculo = [lambda s: s == "101"]
resultado_grover = grover_search(oraculo, n_iters=2)
```

## Ejecutar Tests

```bash
# Desde la raíz del repositorio
pip install -r quantum-core/requirements.txt
pytest quantum-core/tests -v
```

## Integración con el Backend Node.js

El endpoint `POST /api/quantum/run-circuit` en `backend/routes/quantum.js`
ejecuta automáticamente el script de demostración y devuelve el resultado JSON.

Para habilitar el endpoint, asegúrate de que en `backend/server.js` esté montada la ruta:
```javascript
const quantumRouter = require('./routes/quantum');
app.use('/api/quantum', quantumRouter);
```

Probar con curl:
```bash
curl -X POST http://localhost:8000/api/quantum/run-circuit \
  -H 'Content-Type: application/json' \
  -d '{"circuit_name": "traffic_light", "theta": 0.8}'
```

## Configuración

El archivo `quantum_core_config.json` controla el comportamiento por defecto:

```json
{
  "default_backend": "local_simulator",
  "max_qubits": 16,
  "version": "1.0.0"
}
```

## Integración Futura

- **IBM Quantum:** Completar `IBMQBackend` con `qiskit-ibm-runtime` y configurar token.
- **ai-engine:** Integrar `QuantumNeuralLayer` con las redes neuronales del módulo ai-engine.
- **Qiskit real:** Reemplazar los stubs numpy con circuitos Qiskit reales.
- **VQE:** Añadir algoritmo VQE para optimización de energía en planificación de ciudad.

## Licencia

MIT License — Copyright (c) 2026 Ciudad Robot Team.
Ver archivo `LICENSE` en la raíz del repositorio.

## Notas de Seguridad

- ⚠️ **No incluir claves API** en el código ni en archivos de configuración.
- ⚠️ El hardware real de IBM Quantum está **deshabilitado por defecto**.
- ⚠️ No hay ningún sistema de minería en este módulo.
