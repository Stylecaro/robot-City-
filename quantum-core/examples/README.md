# Ejemplos de quantum-core

Esta carpeta contiene scripts de ejemplo completos que demuestran la integración
del módulo `quantum-core`.

## Ejemplos disponibles

### `quantum_traffic_light_demo.py`

Simula un semáforo cuántico usando el simulador local y muestra los resultados
en formato JSON.

**Uso:**
```bash
# Instalar dependencias
pip install -r ../requirements.txt

# Ejecutar con parámetros por defecto (3 qubits, 1024 shots)
python quantum_traffic_light_demo.py

# Ejecutar con parámetros personalizados
python quantum_traffic_light_demo.py --qubits 4 --shots 512
```

**Salida esperada (ejemplo):**
```json
{
  "counts": {
    "000": 132,
    "001": 128,
    "010": 130,
    "011": 127,
    "100": 126,
    "101": 131,
    "110": 124,
    "111": 126
  },
  "probabilities": {...},
  "shots": 1024,
  "backend": "local_simulator",
  "circuit_name": "traffic_light",
  "circuit_qubits": 3
}
```

## Integración con el backend

Para llamar al script desde el backend Node.js, usa el endpoint:

```bash
curl -X POST http://localhost:3000/api/quantum/run-circuit \
  -H 'Content-Type: application/json' \
  -d '{"circuit_name": "traffic_light", "params": {"qubits": 3}}'
```
