# quantum-core

Módulo cuántico para **Ciudad Robot** — algoritmos, circuitos, backends y modelos
híbridos cuántico-clásicos, todo simulado con `numpy` sin requerir hardware real.

---

## Instalación

```bash
pip install -r quantum-core/requirements.txt
```

Para habilitar integración con Qiskit (opcional):
```bash
pip install qiskit qiskit-aer qiskit-ibm-runtime
```

---

## Estructura

```
quantum-core/
  algorithms/       # QAOA MaxCut, Grover Search
  circuits/         # Semáforo cuántico, capa de entrelazamiento
  backends/         # Simulador local (numpy), stub IBM Quantum
  hybrid/           # Capa neuronal cuántica simulada
  tests/            # Tests con pytest
  notebooks/        # Notebooks Jupyter (placeholders)
  docs/             # Documentación técnica
  examples/         # Scripts de ejemplo completos
  quantum_core_config.json
  requirements.txt
```

---

## Ejecutar el ejemplo principal

```bash
python quantum-core/examples/quantum_traffic_light_demo.py
# Con parámetros personalizados:
python quantum-core/examples/quantum_traffic_light_demo.py --qubits 3 --shots 512
```

---

## Ejecutar los tests

```bash
pip install -r quantum-core/requirements.txt
pytest quantum-core/tests
```

---

## Integración con el backend Node.js

El endpoint REST `POST /api/quantum/run-circuit` ejecuta el script de ejemplo
y devuelve el resultado JSON:

```bash
curl -X POST http://localhost:3000/api/quantum/run-circuit \
  -H 'Content-Type: application/json' \
  -d '{"circuit_name": "traffic_light", "params": {"qubits": 3}}'
```

---

## Integración futura con IBM Quantum

1. Instalar: `pip install qiskit qiskit-ibm-runtime`
2. Obtener API key en [https://quantum-computing.ibm.com/](https://quantum-computing.ibm.com/)
3. Pasar la clave como variable de entorno `IBM_QUANTUM_API_KEY`
4. Implementar `backends/ibm_quantum.py` usando `QiskitRuntimeService`

> ⚠️ **Nunca** incluir claves de API directamente en el código fuente.

---

## Integración futura con ai-engine

El módulo `hybrid/quantum_neural_layer.py` puede integrarse con los modelos
del directorio `ai-engine/` para añadir capas cuánticas a las redes neuronales
existentes.

---

## Licencia

Misma licencia que el repositorio principal — MIT License.
