# Algoritmos Cuánticos Explicados

Documentación técnica en español sobre los algoritmos cuánticos implementados
en el módulo `quantum-core` de Ciudad Robot.

---

## 1. QAOA - Quantum Approximate Optimization Algorithm

### ¿Qué es?

QAOA (Quantum Approximate Optimization Algorithm) es un algoritmo cuántico variacional
diseñado para resolver problemas de optimización combinatoria. Fue propuesto por
Farhi, Goldstone y Gutmann en 2014.

### ¿Cómo funciona?

El algoritmo construye un estado cuántico parametrizado mediante p capas alternadas de:
1. **Operador de problema (U_C):** Aplica la función de costo del problema.
2. **Operador de mezcla (U_B):** Aplica rotaciones X para mezclar los estados.

Los parámetros γ (gamma) y β (beta) se optimizan clásicamente para maximizar
el valor esperado de la función de costo ⟨C⟩.

### Problema MaxCut

El problema MaxCut divide los nodos de un grafo en dos conjuntos S y T de forma
que el número de aristas entre S y T sea máximo.

**Hamiltoniano de costo:**
```
H_C = Σ_(i,j)∈E  (1 - Z_i Z_j) / 2
```

Donde Z_i son operadores de Pauli-Z aplicados al qubit i.

### Implementación en quantum-core

```python
from quantum_core.algorithms import run_qaoa_maxcut

grafo = {
    "nodos": [0, 1, 2, 3],
    "aristas": [(0, 1), (1, 2), (2, 3), (3, 0)]
}
resultado = run_qaoa_maxcut(grafo, p=2)
```

### Aplicación en Ciudad Robot

QAOA se aplica para optimizar:
- Asignación de robots a zonas de trabajo (MaxCut para minimizar conflictos)
- Optimización de rutas de tráfico (partición de intersecciones)
- Planificación de tareas en la ciudad (scheduling cuántico)

### Estado actual

- ✅ Stub funcional con numpy
- ⏳ Pendiente: implementación real con Qiskit y circuito QAOA parametrizado
- ⏳ Pendiente: optimizador clásico (COBYLA, SPSA)

---

## 2. Algoritmo de Grover

### ¿Qué es?

El algoritmo de búsqueda de Grover es un algoritmo cuántico que encuentra
un elemento marcado en una base de datos no estructurada de N elementos
en O(√N) pasos, comparado con O(N) clásico.

### ¿Cómo funciona?

El algoritmo opera en tres fases:
1. **Preparación:** Aplica Hadamard a todos los qubits para crear una superposición uniforme.
2. **Oráculo (U_ω):** Invierte la fase del estado marcado (-|ω⟩ → |ω⟩ con signo negativo).
3. **Difusión de Grover (U_s):** Amplifica la amplitud del estado marcado.

Los pasos 2 y 3 se repiten aproximadamente π/4 × √N veces.

### Oráculo de Grover

El oráculo es una función f: {0,1}^n → {0,1} que devuelve 1 para el estado objetivo:
```
U_ω |x⟩ = -|x⟩ si f(x) = 1
U_ω |x⟩ = |x⟩  si f(x) = 0
```

### Implementación en quantum-core

```python
from quantum_core.algorithms import grover_search

# Buscar el estado "101" en un espacio de 3 qubits
oraculo = [lambda s: s == "101"]
resultado = grover_search(oraculo, n_iters=2)
print(resultado["estado_encontrado"])
```

### Aplicación en Ciudad Robot

Grover se aplica para:
- Búsqueda de patrones de comportamiento en registros de robots
- Identificación de anomalías en el sistema de sensores
- Búsqueda óptima en espacios de configuración de avatares

---

## 3. Circuito de Semáforo Cuántico

### Diseño del Circuito

El circuito de semáforo modela los estados de un semáforo como superposición cuántica:

| Qubit | Rol | Estado base |
|-------|-----|-------------|
| Q0 | Estado del semáforo | \|0⟩=rojo, \|1⟩=verde |
| Q1 | Detector de vehículos | \|0⟩=libre, \|1⟩=ocupado |
| Q2 | Señal de emergencia | \|0⟩=normal, \|1⟩=emergencia |

**Puertas usadas:**
- **Hadamard (H):** Crea superposición entre rojo y verde
- **RY(θ):** Ajusta la probabilidad según densidad de tráfico
- **CNOT:** Correlaciona el semáforo con el detector de vehículos
- **RZ(φ):** Añade fase para la señal de emergencia

### Interpretación Cuántica

Al medir el circuito, la probabilidad de obtener `|1⟩` en Q0 (semáforo verde)
aumenta con el ángulo θ, que representa la densidad de tráfico normalizada.
El entrelazamiento con Q1 garantiza que el semáforo responde al estado del detector.

---

## 4. Capa Neuronal Cuántica (VQC)

### Variational Quantum Circuit (VQC)

Un VQC (Circuito Cuántico Variacional) es un circuito parametrizado que puede
actuar como una capa en una red neuronal. Los pesos de la capa son ángulos de
rotación que se optimizan mediante descenso de gradiente cuántico (parameter shift rule).

### Arquitectura

```
Entrada clásica → Encoding Layer → Capa RY + RZ → CNOT Entrelazamiento → Medición → Salida
```

### Integración con ai-engine

La `QuantumNeuralLayer` está diseñada para reemplazar capas densas en las redes
neuronales del módulo `ai-engine`. Para integración completa se recomienda:

1. **PennyLane + PyTorch:** `qml.qnn.TorchLayer`
2. **Qiskit Machine Learning:** `SamplerQNN` o `EstimatorQNN`
3. **TensorFlow Quantum:** `tfq.layers.PQC`

---

## Referencias

- [Farhi et al., 2014] "A Quantum Approximate Optimization Algorithm"
- [Grover, 1996] "A fast quantum mechanical algorithm for database search"
- [Cerezo et al., 2021] "Variational quantum algorithms" (Nature Reviews Physics)
- [Qiskit Documentation](https://qiskit.org/documentation/) — Guía oficial de Qiskit
