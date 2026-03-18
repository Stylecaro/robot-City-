# Ejemplos de uso — quantum-core

Este directorio contiene scripts de demostración para el módulo cuántico de Ciudad Robot.

## Scripts disponibles

### `quantum_traffic_light_demo.py`
Demostración del circuito cuántico de semáforo ejecutado en el simulador local.

```bash
# Desde la raíz del repositorio:
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

Probabilidades por estado:
  |00> -> rojo: 0.5000  ###############
  |01> -> amarillo: 0.5000  ###############
  |10> -> verde: 0.0000
  |11> -> no_usado: 0.0000
...
```

## Requisitos

```bash
pip install numpy
```

## Integración con el endpoint REST

El script es invocado por `backend/routes/quantum.js` mediante `child_process`.
Ver la documentación en `quantum-core/docs/api_reference.md`.
