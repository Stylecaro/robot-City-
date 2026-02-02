#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Corregir CONTRIBUTING.md
contributing = """# 🤝 Contribuir a Ciudad Robot

¡Gracias por tu interés en contribuir al proyecto Ciudad Robot!

## 📋 Código de Conducta

Este proyecto se adhiere a un código de conducta. Al participar, se espera que mantengas este código.

## 🚀 Cómo Contribuir

### 1. Fork del Repositorio

```bash
git clone https://github.com/Stylecaro/robot-City-.git
cd robot-City-
```

### 2. Crear una Rama

```bash
git checkout -b feature/mi-nueva-caracteristica
```

### 3. Realizar Cambios

- Escribe código limpio y bien documentado
- Sigue las convenciones de estilo del proyecto
- Agrega tests si es aplicable

### 4. Commit

```bash
git add .
git commit -m "✨ Agregar nueva característica: descripción"
```

Usa emojis en los commits:

- ✨ `:sparkles:` - Nueva característica
- 🐛 `:bug:` - Corrección de bug
- 📚 `:books:` - Documentación
- 🎨 `:art:` - Mejora de estilo/formato
- ⚡ `:zap:` - Mejora de rendimiento
- 🔧 `:wrench:` - Configuración
- ✅ `:white_check_mark:` - Tests

### 5. Push y Pull Request

```bash
git push origin feature/mi-nueva-caracteristica
```

Luego crea un Pull Request en GitHub.

## 🏗️ Estructura del Proyecto

```
robot-City-/
├── ai-engine/          # Motor de IA en Python
├── backend/            # API REST Node.js
├── frontend/           # Interfaz React + Three.js
├── robot-system/       # Sistema de robots
├── avatar-system/      # Gestión de avatares
├── blockchain/         # Contratos inteligentes
├── battle-arena-system/# Sistema de combate
└── docs/              # Documentación
```

## 🧪 Tests

### Backend (Node.js)

```bash
cd backend
npm test
```

### AI Engine (Python)

```bash
cd ai-engine
pytest tests/
```

### Frontend (React)

```bash
cd frontend
npm test
```

## 📝 Guías de Estilo

### JavaScript/Node.js

- Usar ESLint
- Seguir Airbnb Style Guide
- Usar async/await para promesas

### Python

- Seguir PEP 8
- Usar type hints
- Documentar con docstrings

### React

- Componentes funcionales con hooks
- PropTypes o TypeScript
- CSS Modules o styled-components

## 🐛 Reportar Bugs

Usa el [Issue Tracker](https://github.com/Stylecaro/robot-City-/issues) y proporciona:

1. **Descripción clara** del bug
2. **Pasos para reproducir**
3. **Comportamiento esperado** vs actual
4. **Screenshots** si aplica
5. **Ambiente** (OS, versión de Node, Python, etc.)

## 💡 Solicitar Características

Crea un Issue con:

- Descripción detallada de la característica
- Caso de uso
- Beneficio esperado

## 📞 Contacto

- GitHub Issues: Para bugs y características
- Discussions: Para preguntas generales

## 📜 Licencia

Al contribuir, aceptas que tus contribuciones serán licenciadas bajo la licencia MIT del proyecto.

---

¡Gracias por hacer Ciudad Robot mejor! 🤖🏙️
"""

bug_report = """---
name: Bug Report
about: Reportar un bug o error en el sistema
title: '[BUG] '
labels: bug
assignees: ''

---

## 🐛 Descripción del Bug

Una descripción clara y concisa del bug.

## 🔄 Pasos para Reproducir

1. Ve a '...'
2. Ejecuta '...'
3. Haz clic en '...'
4. Ver error

## ✅ Comportamiento Esperado

Descripción de lo que esperabas que sucediera.

## ❌ Comportamiento Actual

Descripción de lo que realmente sucede.

## 📸 Screenshots

Si aplica, agrega screenshots para ayudar a explicar el problema.

## 💻 Ambiente

- **SO**: [e.g. Windows 11, macOS, Ubuntu 22.04]
- **Node.js**: [e.g. 18.17.0]
- **Python**: [e.g. 3.9.7]
- **Unity**: [e.g. 2021.3.25f1]
- **Navegador**: [e.g. Chrome 120, Firefox 121]

## 📋 Logs

```
Pega aquí los logs relevantes
```

## 🔍 Contexto Adicional

Agrega cualquier otro contexto sobre el problema aquí.
"""

feature_request = """---
name: Feature Request
about: Sugerir una nueva característica para el proyecto
title: '[FEATURE] '
labels: enhancement
assignees: ''

---

## 💡 Descripción de la Característica

Una descripción clara y concisa de la característica que deseas.

## 🎯 Problema que Resuelve

¿Qué problema resuelve esta característica? ¿Por qué es necesaria?

## 🔧 Solución Propuesta

Describe cómo te gustaría que funcione la característica.

## 🎨 Alternativas Consideradas

Describe alternativas que hayas considerado.

## 📊 Casos de Uso

1. Como [tipo de usuario], quiero [acción] para [beneficio]
2. ...

## 🖼️ Mockups/Ejemplos

Si tienes mockups, wireframes o ejemplos, agrégalos aquí.

## 🔗 Referencias

- Links a documentación relacionada
- Ejemplos de implementaciones similares

## ⚠️ Consideraciones

- Posibles impactos en rendimiento
- Dependencias necesarias
- Cambios breaking

## 📝 Tareas

- [ ] Diseño
- [ ] Implementación Backend
- [ ] Implementación Frontend
- [ ] Tests
- [ ] Documentación
"""

# Escribir archivos
with open("CONTRIBUTING.md", "w", encoding="utf-8") as f:
    f.write(contributing)
    
with open(".github/ISSUE_TEMPLATE/bug_report.md", "w", encoding="utf-8") as f:
    f.write(bug_report)
    
with open(".github/ISSUE_TEMPLATE/feature_request.md", "w", encoding="utf-8") as f:
    f.write(feature_request)

print("✓ CONTRIBUTING.md corregido")
print("✓ bug_report.md corregido")
print("✓ feature_request.md corregido")
