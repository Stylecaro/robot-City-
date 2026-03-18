# Módulo Cuántico — quantum-core

Documentación de instalación y ejecución del módulo cuántico de Ciudad Robot.

## Instalación

```bash
# 1. Instalar dependencias Python del módulo cuántico
pip install -r quantum-core/requirements.txt

# 2. (Opcional) Para hardware real IBM Quantum
# pip install qiskit qiskit-ibm-runtime
```

## Ejecutar el ejemplo del semáforo cuántico

```bash
cd quantum-core
python examples/quantum_traffic_light_demo.py
```

Salida esperada:
```
==================================================
  === Demo Semáforo Cuántico - Ciudad Robot ===
==================================================

Circuito: SemaforoQuantico (2 qubits)
Estados posibles:
  |00> -> rojo
  |01> -> amarillo
  |10> -> verde
  |11> -> no_usado

Backend: LocalSimulator (1024 shots)
...
```

## Ejecutar los tests

```bash
cd quantum-core
pytest tests/ -v
```

## Exponer el endpoint cuántico en el backend

El backend Node.js ya incluye el endpoint `/api/quantum/run-circuit` en
`backend/routes/quantum.js`. Se activa automáticamente al iniciar el servidor:

```bash
cd backend
npm install
npm start
```

Luego llamar al endpoint:

```bash
curl -X POST http://localhost:8000/api/quantum/run-circuit \
  -H "Content-Type: application/json" \
  -d '{"circuit_name": "traffic_light", "params": {}}'
```

## Usar el componente React

```jsx
import QuantumTrafficLight from './components/QuantumTrafficLight';

function App() {
  return <QuantumTrafficLight />;
}
```

## Estructura del módulo

```
quantum-core/
├── algorithms/          # QAOA, Grover (plantillas)
├── circuits/            # Semáforo cuántico, entrelazamiento
├── backends/            # Simulador local, IBM Quantum (plantilla)
├── hybrid/              # Capa neuronal cuántica simulada
├── tests/               # Tests con pytest
├── notebooks/           # Jupyter notebooks
├── docs/                # Referencia API y algoritmos
├── examples/            # Scripts de demostración
├── requirements.txt
├── quantum_core_config.json
└── README.md
```

## Futuras integraciones

- **IBM Quantum**: Implementar `IBMQBackend.submit_circuit` con Qiskit
- **ai-engine**: Integrar `QuantumNeuralLayer` como capa en los modelos de IA
- **blockchain cuántica**: Conectar con el módulo `quantum-blockchain/`
- **QAOA para optimización**: Aplicar a rutas de robots en la ciudad

## Seguridad y licencias

- No se incluyen claves de API en el código fuente.
- Configurar `IBMQ_API_KEY` como variable de entorno para IBM Quantum.
- MIT License — Copyright (c) 2026 Ciudad Robot Team
