# Algoritmos Cuánticos Explicados — quantum-core

Guía introductoria sobre los algoritmos cuánticos implementados en Ciudad Robot.

---

## 1. QAOA — Quantum Approximate Optimization Algorithm

### ¿Qué es?

QAOA es un algoritmo cuántico **variacional** diseñado para resolver problemas de
optimización combinatoria de forma aproximada. Combina circuitos cuánticos parametrizados
con un optimizador clásico.

### Cómo funciona

1. **Codificación**: El problema (ej. Max-Cut en un grafo de tráfico) se codifica como
   un Hamiltoniano de costo `H_C` en qubits.
2. **Circuito**: Se alternan capas de dos unitarios:
   - `U_C(γ)` = exp(-iγH_C): aplica el Hamiltoniano de costo.
   - `U_B(β)` = exp(-iβH_B): aplica el Hamiltoniano de mezcla (suma de X-Pauli).
3. **Optimización**: Un optimizador clásico ajusta los parámetros `(γ, β)` para
   minimizar `⟨ψ|H_C|ψ⟩`.
4. **Medición**: Se mide el estado final y se extrae la solución.

### Aplicación en Ciudad Robot

Optimizar el flujo de tráfico representando intersecciones como nodos y rutas como
aristas. Max-Cut divide el grafo en dos grupos de semáforos que no interfieren.

### Complejidad

- **Clásico**: O(2^n) para n variables.
- **QAOA**: Polinomial en el número de capas `p`; calidad mejora con `p → ∞`.

---

## 2. Algoritmo de Grover

### ¿Qué es?

El algoritmo de Grover busca un elemento marcado en una base de datos no estructurada.
Proporciona una aceleración **cuadrática**: O(√N) vs O(N) clásico.

### Cómo funciona

1. **Inicialización**: Estado inicial = superposición uniforme de todos los N estados.
2. **Oráculo** `U_f`: Marca el estado solución invirtiendo su fase.
3. **Difusor** `D`: Amplifica la amplitud del estado marcado (inversión sobre la media).
4. **Iteración**: Repetir oráculo + difusor ~(π/4)√N veces.
5. **Medición**: El estado marcado tiene probabilidad ≈ 1.

### Aplicación en Ciudad Robot

- Buscar el robot más eficiente para una tarea.
- Localizar la ruta óptima entre dos puntos de la ciudad.
- Encontrar el estado de menor energía en un sistema de optimización.

---

## 3. Entrelazamiento Cuántico

### ¿Qué es?

Dos o más qubits están entrelazados cuando su estado conjunto **no puede describirse**
como el producto de estados individuales. La medición de un qubit afecta instantáneamente
al estado del otro.

### Estados de Bell

Los 4 estados de Bell son los estados de 2 qubits máximamente entrelazados:

| Estado | Fórmula |
|--------|---------|
| Φ+ | (|00⟩ + |11⟩) / √2 |
| Φ- | (|00⟩ - |11⟩) / √2 |
| Ψ+ | (|01⟩ + |10⟩) / √2 |
| Ψ- | (|01⟩ - |10⟩) / √2 |

### Capa de Entrelazamiento en quantum-core

`entanglement_layer(n_qubits)` aplica puertas CNOT encadenadas:
- Qubit 0 controla qubit 1
- Qubit 1 controla qubit 2
- ...hasta qubit n-2 controla qubit n-1

Resultado: una matriz unitaria que crea correlaciones entre todos los qubits vecinos.

---

## 4. Capas Neuronales Cuánticas (QNN)

### ¿Qué es?

Una red neuronal cuántica reemplaza capas densas clásicas por circuitos cuánticos
parametrizados. Los parámetros del circuito se optimizan con gradiente (backprop cuántico).

### Estructura en quantum-core

`QuantumNeuralLayer`:
1. **Codificación**: Las entradas se cargan como amplitudes del estado cuántico.
2. **Transformación**: Se aplican rotaciones parametrizadas y la unitaria del circuito.
3. **Medición**: Se calculan valores de expectativa de observables (σ_z).
4. **Salida**: Vector de valores en [-1, 1] para la capa siguiente.

### Ventajas potenciales

- Menor número de parámetros que capas clásicas equivalentes.
- Correlaciones exponencialmente ricas en el espacio de Hilbert.
- Natural para datos con estructura cuántica (química, física).
