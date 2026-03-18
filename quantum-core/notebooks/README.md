# Notebooks de Experimentación - quantum-core

Esta carpeta contiene (o contendrá) notebooks Jupyter para experimentación,
visualización y demostración de los algoritmos cuánticos del módulo quantum-core.

## Notebooks Planificados

### `01_primer_circuito.ipynb` _(próximamente)_

Introducción al módulo quantum-core:
- Construir el primer circuito de semáforo con `build_traffic_light_circuit`
- Ejecutarlo en `LocalSimulator`
- Visualizar los resultados con matplotlib

### `02_qaoa_optimizacion_trafico.ipynb` _(próximamente)_

Optimización de tráfico con QAOA:
- Definir un grafo de intersecciones de Ciudad Robot
- Resolver el problema MaxCut con `run_qaoa_maxcut`
- Visualizar la partición óptima de semáforos
- Comparar con solución clásica

## Cómo Ejecutar los Notebooks

```bash
# Instalar dependencias
pip install -r quantum-core/requirements.txt
pip install jupyter matplotlib

# Lanzar Jupyter
cd quantum-core/notebooks
jupyter notebook
```

## Contribuir con Notebooks

Para añadir un nuevo notebook de experimentación:
1. Crea el archivo `.ipynb` en esta carpeta con nombre descriptivo y número de orden.
2. Asegúrate de que funcione con las dependencias de `requirements.txt`.
3. Añade una descripción en este README.
4. **No incluir datos sensibles ni claves API** en los notebooks.
