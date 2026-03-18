# Algoritmos Cuánticos Explicados

Breve introducción a los algoritmos implementados en `quantum-core`,
con explicaciones en español para facilitar la comprensión.

---

## 1. QAOA — Quantum Approximate Optimization Algorithm

### ¿Qué es?

QAOA es un algoritmo cuántico híbrido diseñado para resolver problemas de
optimización combinatoria. Mezcla capas de operadores de problema (*cost operator*)
con capas de mezcla (*mixer operator*), controladas por parámetros entrenables
(γ y β), en un circuito de profundidad `p`.

### Aplicación: MaxCut

El problema **MaxCut** consiste en dividir los nodos de un grafo en dos grupos
de modo que el número de aristas cortadas (que conectan nodos de grupos distintos)
sea máximo.

**En Ciudad Robot:** MaxCut puede modelar la asignación óptima de semáforos en
una intersección para minimizar el tráfico cruzado.

### Pseudocódigo simplificado

```
Estado inicial: |+⟩^n  (superposición uniforme)
Para i en 1..p:
    Aplicar operador de coste C(γ_i)
    Aplicar operador mezcla B(β_i)
Medir el estado final y elegir la solución con mayor probabilidad
```

### Estado actual en quantum-core

El módulo `algorithms/qaoa_maxcut.py` implementa un **stub** que devuelve
un marcador de posición. Para una implementación real, se recomienda usar
`qiskit` con el optimizador `COBYLA` o `L-BFGS-B`.

---

## 2. Algoritmo de Grover

### ¿Qué es?

El algoritmo de Grover ofrece una aceleración cuadrática para la búsqueda
no estructurada. En una base de datos de N elementos, encuentra el elemento
objetivo en O(√N) evaluaciones en lugar de O(N) clásicamente.

### Pasos principales

1. **Inicialización:** Aplicar Hadamard a todos los qubits → superposición uniforme.
2. **Oráculo:** Invierte la fase del estado objetivo.
3. **Difusión de Grover:** Invierte amplitudes respecto a la media.
4. Repetir pasos 2-3 aproximadamente √N veces.
5. **Medición:** El estado objetivo tiene probabilidad alta.

### Aplicación en Ciudad Robot

Puede usarse para búsqueda rápida en bases de datos de robots o rutas óptimas.

---

## 3. Capa de Entrelazamiento

El entrelazamiento cuántico es el fenómeno por el cual dos qubits quedan
correlacionados de manera que el estado de uno no puede describirse
independientemente del otro.

La función `entanglement_layer(n_qubits)` construye la matriz unitaria de:
- Una capa **Hadamard** aplicada a todos los qubits (crea superposición).
- Una capa de **puertas CNOT** entre qubits consecutivos (crea entrelazamiento).

### Estados de Bell

Para 2 qubits, esta capa genera estados cercanos a los estados de Bell:
- |Φ⁺⟩ = (|00⟩ + |11⟩) / √2
- |Φ⁻⟩ = (|00⟩ - |11⟩) / √2

---

## 4. Red Neuronal Cuántica (QNN)

La clase `QuantumNeuralLayer` simula una capa neuronal que usa operaciones
cuánticas como transformaciones de datos. En modelos híbridos reales:

- Las **capas clásicas** procesan datos de entrada y salida.
- La **capa cuántica** (QNN) aplica rotaciones parametrizadas entrenadas
  mediante gradientes clásicos (parameter-shift rule).

Esto permite explotar la expresividad de los circuitos cuánticos como
espacio de hipótesis para aprendizaje automático.

---

## Referencias

- Farhi, E. et al. (2014). *A Quantum Approximate Optimization Algorithm*.
- Grover, L. K. (1996). *A fast quantum mechanical algorithm for database search*.
- Schuld, M. et al. (2019). *Evaluating analytic gradients on quantum hardware*.
