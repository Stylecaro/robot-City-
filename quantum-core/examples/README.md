# Ejemplos de Integración - quantum-core

Esta carpeta contiene ejemplos completos de integración del módulo quantum-core
con el resto del sistema Ciudad Robot.

## Ejemplos Disponibles

### `quantum_traffic_light_demo.py`

Demo CLI del semáforo cuántico. Construye un circuito cuántico de control de
tráfico y lo ejecuta en el simulador local.

**Uso básico:**
```bash
cd quantum-core
python examples/quantum_traffic_light_demo.py
```

**Con parámetros personalizados:**
```bash
python examples/quantum_traffic_light_demo.py --params '{"theta": 1.0, "n_qubits": 4}'
```

**Via stdin (usado por el endpoint backend):**
```bash
echo '{"theta": 0.8, "phi": 0.2}' | python examples/quantum_traffic_light_demo.py
```

**Opciones disponibles:**
```
--params  JSON con parámetros del circuito
--shots   Número de disparos del simulador (default: 1024)
--seed    Semilla aleatoria para reproducibilidad (default: 42)
```

**Salida de ejemplo:**
```json
{
  "exito": true,
  "circuito": {
    "nombre": "traffic_light",
    "n_qubits": 3,
    "n_puertas": 5,
    "params": {"theta": 0.5, "phi": 0.0}
  },
  "resultado": {
    "conteos": {"000": 145, "001": 132, "010": 128, ...},
    "shots": 1024,
    "n_qubits": 3,
    "backend": "local_simulator"
  }
}
```

## Cómo Añadir Nuevos Ejemplos

1. Crea un nuevo archivo `.py` en esta carpeta.
2. Importa los módulos necesarios desde `quantum-core/`.
3. Añade docstring con instrucciones de uso.
4. Documenta el ejemplo en este README.

## Integración con el Backend Node.js

El endpoint `POST /api/quantum/run-circuit` en `backend/routes/quantum.js` ejecuta
`quantum_traffic_light_demo.py` automáticamente, enviando los parámetros por stdin
y recibiendo el JSON de salida.

Para probar el endpoint completo:
```bash
# Levantar el servidor backend
cd backend && node server.js

# Llamar al endpoint
curl -X POST http://localhost:8000/api/quantum/run-circuit \
  -H 'Content-Type: application/json' \
  -d '{"circuit_name": "traffic_light", "theta": 0.8}'
```
