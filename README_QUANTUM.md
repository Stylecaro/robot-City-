# ⚛️ Módulo Quantum-Core — Ciudad Robot

Bienvenido al módulo de computación cuántica de **Ciudad Robot**. Este módulo integra
circuitos cuánticos con la infraestructura de tráfico inteligente de la ciudad,
permitiendo optimizar semáforos y rutas mediante algoritmos cuánticos.

---

## 📁 Estructura del módulo

```
quantum-core/
  algorithms/          # Algoritmos cuánticos (QAOA, Grover)
  circuits/            # Circuitos cuánticos de semáforo y entrelazamiento
  backends/            # Simuladores locales y backend IBM Quantum (stub)
  hybrid/              # Capa neuronal cuántica híbrida
  tests/               # Tests pytest
  notebooks/           # Notebooks de demostración
  docs/                # Documentación de API y algoritmos
  examples/            # Ejemplos ejecutables
  requirements.txt     # Dependencias (numpy, pytest)
  quantum_core_config.json  # Configuración por defecto
```

---

## 🚀 Inicio rápido

### Requisitos

- Python 3.8+
- `numpy` y `pytest` (incluidos en `requirements.txt`)
- *(Opcional)* `qiskit` para backends reales

### Instalación

```bash
pip install -r quantum-core/requirements.txt
```

### Ejecutar demostración

```bash
python quantum-core/examples/quantum_traffic_light_demo.py
```

### Ejecutar tests

```bash
pytest quantum-core/tests/ -v
```

---

## 🌐 Integración con el backend Node.js

El endpoint REST expone el circuito cuántico de semáforo:

```
POST /api/quantum/run-circuit
Content-Type: application/json

{
  "circuit_name": "traffic_light",
  "theta": 0.8,
  "phi": 0.2,
  "n_qubits": 3,
  "shots": 1024
}
```

### Respuesta exitosa

```json
{
  "success": true,
  "data": {
    "circuito": { "nombre": "semaforo_cuantico", "n_qubits": 3, "n_puertas": 5 },
    "resultado": { "backend": "local_simulator", "shots": 1024, "conteos": { ... } }
  }
}
```

---

## ⚛️ Componente React

Importa `QuantumTrafficLight` desde el frontend para visualizar el semáforo cuántico:

```jsx
import QuantumTrafficLight from './components/QuantumTrafficLight';

// En tu JSX:
<QuantumTrafficLight />
```

El componente incluye controles de parámetros, spinner de carga y semáforo visual.

---

## 📖 Algoritmos implementados

| Algoritmo | Archivo | Descripción |
|---|---|---|
| QAOA MaxCut | `algorithms/qaoa_maxcut.py` | Optimización de partición de grafo de tráfico |
| Búsqueda de Grover | `algorithms/grover_search.py` | Búsqueda cuántica en espacio de rutas |
| Circuito semáforo | `circuits/traffic_light_circuit.py` | Circuito cuántico de control de semáforo |
| Capa entrelazamiento | `circuits/entanglement_layer.py` | Capa de entrelazamiento para circuitos profundos |
| Neurona cuántica | `hybrid/quantum_neural_layer.py` | Capa neuronal cuántica híbrida |

---

## ⚙️ Configuración

Edita `quantum-core/quantum_core_config.json` para ajustar parámetros:

```json
{
  "default_backend": "local_simulator",
  "max_qubits": 16,
  "default_shots": 1024,
  "timeout_seconds": 30
}
```

---

## 🔒 Seguridad

- **No se incluyen credenciales ni claves API** en este módulo.
- Para usar IBM Quantum, configura la variable de entorno `IBM_QUANTUM_TOKEN`.
- El backend `IBMQBackend` lanza `NotImplementedError` hasta que se provea el token.

---

## 📚 Documentación adicional

- [Referencia de API](quantum-core/docs/api_reference.md)
- [Explicación de algoritmos](quantum-core/docs/algoritmos_explicados.md)
- [Notebooks de demostración](quantum-core/notebooks/)

---

*Ciudad Robot — Módulo Cuántico · Licencia MIT*
