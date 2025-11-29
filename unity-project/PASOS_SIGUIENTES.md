# 🎮 PASOS SIGUIENTES - Mundo Virtual Battle Arena

## ✅ YA COMPLETADO
- Unity Hub instalado
- Unity Editor instalado
- Proyecto creado en: `C:\Users\Brian Carlisle\mundo virtual\unity-project`
- 15 scripts C# importados
- PlayerMovement.cs creado
- Unity está cargando el proyecto (5-10 minutos)

---

## 🚀 CUANDO UNITY TERMINE DE CARGAR

### Paso 1: Verificar que todo cargó bien (2 minutos)

**En Unity, verifica:**
1. Ventana **Project** (abajo) - deberías ver carpetas: Assets, Scenes, Scripts, Prefabs
2. Ventana **Console** (abajo) - no debería haber errores rojos
3. Si hay warnings amarillos, es normal (los arreglaremos después)

**Si ves errores rojos:**
- Ignora errores sobre "Photon" o "PUN" - es porque aún no lo instalamos
- Ignora "namespace not found" - es normal sin Photon

---

### Paso 2: Crear tu primera escena (5 minutos)

**Crea la escena MainMenu:**

1. Click derecho en `Assets/Scenes` (ventana Project)
2. Selecciona: **Create → Scene**
3. Nómbrala: `MainMenu`
4. Doble click en `MainMenu` para abrirla

**Agrega UI básico:**

1. Click derecho en **Hierarchy** (ventana izquierda)
2. Selecciona: **UI → Canvas**
3. Click derecho en **Canvas**
4. Selecciona: **UI → Text - TextMeshPro**
5. Si pregunta "Import TMP Essentials" → Click **Import**
6. Renombra el texto a "TitleText"
7. En **Inspector** (derecha), cambia el texto a: "MUNDO VIRTUAL - BATTLE ARENA"

**Guarda:**
- Presiona **Ctrl + S**

---

### Paso 3: Crear escena de juego BattleArena (10 minutos)

**Crea la escena de batalla:**

1. Click derecho en `Assets/Scenes`
2. **Create → Scene**
3. Nómbrala: `BattleArena`
4. Doble click para abrirla

**Crea el terreno:**

1. Click derecho en **Hierarchy**
2. Selecciona: **3D Object → Terrain**
3. Selecciona el Terrain en Hierarchy
4. En **Inspector**, click en el ícono de engranaje (Terrain Settings)
5. Cambia **Terrain Width**: `5000`
6. Cambia **Terrain Length**: `5000`
7. Cambia **Terrain Height**: `600`

**Agrega iluminación:**

1. Click derecho en **Hierarchy**
2. **Light → Directional Light** (si no existe ya)
3. En **Inspector**, ajusta:
   - Rotation: X=50, Y=-30, Z=0
   - Intensity: 1.5

**Guarda:**
- Presiona **Ctrl + S**

---

### Paso 4: Crear el Player Prefab (10 minutos)

**Crea el jugador:**

1. Click derecho en **Hierarchy**
2. **Create Empty** → Nómbralo: `Player`
3. Selecciona `Player` en Hierarchy
4. En **Inspector**, click **Add Component**
5. Busca y agrega: **Character Controller**
6. Ajusta Character Controller:
   - Height: `2`
   - Radius: `0.5`
   - Center: Y=`1`

**Agrega modelo visual temporal:**

1. Click derecho en `Player` (Hierarchy)
2. **3D Object → Capsule**
3. Renombra a: `PlayerModel`
4. Ajusta Transform:
   - Position: X=`0`, Y=`0`, Z=`0`
   - Scale: X=`1`, Y=`1`, Z=`1`

**Agrega la cámara:**

1. Click derecho en `Player` (Hierarchy)
2. **Camera**
3. Renombra a: `PlayerCamera`
4. Ajusta Transform:
   - Position: X=`0`, Y=`0.6`, Z=`0`
   - Rotation: X=`0`, Y=`0`, Z=`0`

**Agrega el script de movimiento:**

1. Selecciona `Player` en Hierarchy
2. En **Inspector**, click **Add Component**
3. Busca: `PlayerMovement`
4. Arrastra `PlayerCamera` al campo **Player Camera** del script

**Crea el Prefab:**

1. Arrastra `Player` desde **Hierarchy** a `Assets/Prefabs/Characters`
2. El objeto se vuelve azul (es un prefab ahora)
3. Ya puedes eliminar `Player` de la Hierarchy

**Guarda:**
- Presiona **Ctrl + S**

---

### Paso 5: Probar el movimiento (5 minutos)

**Prepara la escena:**

1. Asegúrate de estar en `BattleArena` scene
2. Arrastra el prefab `Player` desde `Assets/Prefabs/Characters` a la **Hierarchy**
3. Selecciona `Player` en Hierarchy
4. Ajusta Position: X=`0`, Y=`10`, Z=`0` (para que aparezca sobre el terreno)

**¡Prueba el juego!**

1. Click en el botón **Play** (▶️ arriba en el centro)
2. Deberías poder:
   - **WASD** - Mover
   - **Espacio** - Saltar
   - **Mouse** - Mirar alrededor
3. Si funciona, ¡perfecto! 🎉
4. Click **Play** de nuevo para detener

---

### Paso 6: Instalar Photon PUN 2 (10 minutos)

**IMPORTANTE:** Photon es necesario para el multijugador

**Instalación:**

1. Ve a **Window → Asset Store** (menú superior)
2. Busca: `Photon PUN 2 FREE`
3. Click en **Add to My Assets** (necesitas cuenta de Unity)
4. Una vez agregado, click **Import**
5. En la ventana de import, deja todo seleccionado
6. Click **Import**
7. Espera 2-3 minutos

**Configuración inicial:**

1. Cuando termine, aparecerá ventana **PUN Wizard**
2. Click en **Create New Photon Account** (si no tienes)
3. O click en **Setup Project** (si ya tienes cuenta)
4. Copia tu **AppId** de Photon
5. Pega en el campo y click **Setup Project**

**Registrarse en Photon (GRATIS):**
- Ve a: https://www.photonengine.com/pun
- Click **Start Now - Free**
- Crea cuenta (email, contraseña)
- En Dashboard, crea nueva App:
  - Photon Type: **PUN**
  - Name: `MundoVirtualArena`
  - Copia el **App ID**

---

## 📋 CHECKLIST DE VERIFICACIÓN

Marca cuando completes cada uno:

- [ ] Unity cargó sin errores críticos
- [ ] Carpetas Assets/Scenes/Scripts/Prefabs visibles
- [ ] Escena MainMenu creada con título
- [ ] Escena BattleArena creada con terreno 5000x5000
- [ ] Player Prefab creado con cámara
- [ ] PlayerMovement script asignado
- [ ] Probado movimiento con WASD y mouse
- [ ] Salto funciona con Espacio
- [ ] Photon PUN 2 instalado
- [ ] Photon configurado con App ID

---

## 🎯 DESPUÉS DE COMPLETAR TODO ARRIBA

### Opción A: Descargar Assets 3D Gratis (Recomendado para empezar)

**Personajes:**
1. Mixamo (gratis): https://www.mixamo.com
   - Descarga modelos con animaciones
   - Formato: FBX
   - Importa a `Assets/Models`

**Armas:**
1. Unity Asset Store - busca "Free Weapons"
2. Polygon Arsenal (gratis): https://syntystore.com

**Vehículos:**
1. Unity Asset Store - busca "Free Vehicles"
2. Simple Apocalypse (gratis)

### Opción B: Usar Primitivas de Unity (Para probar rápido)

Por ahora puedes usar:
- **Capsules** para jugadores y bots
- **Cubes** para vehículos
- **Cylinders** para armas

¡Lo importante es que funcione primero!

---

## 🆘 PROBLEMAS COMUNES

### Error: "Photon namespace not found"
- **Solución:** Instala Photon PUN 2 desde Asset Store

### El jugador cae infinitamente
- **Solución:** Verifica que el Terrain esté en Y=0

### No puedo mover al jugador
- **Solución:** Verifica que PlayerMovement esté asignado y PlayerCamera también

### Unity se congela
- **Solución:** Espera 1-2 minutos, está importando assets

### Errores de compilación
- **Solución:** Ve a Edit → Preferences → External Tools → Regenerate project files

---

## 💰 PRÓXIMOS PASOS (Después de probar movimiento)

1. **Importar los otros 15 scripts** de batalla
2. **Configurar Photon** para multijugador
3. **Crear sistema de spawn** de jugadores
4. **Añadir UI** de HUD (vida, munición)
5. **Importar modelos 3D** profesionales
6. **Conectar con blockchain** (backend Python)

---

## 🔥 ATAJOS ÚTILES DE UNITY

- **Ctrl + S** - Guardar
- **Ctrl + D** - Duplicar objeto
- **F** - Focus en objeto seleccionado
- **Q** - Mano (mover cámara)
- **W** - Move tool
- **E** - Rotate tool
- **R** - Scale tool
- **Ctrl + P** - Play/Stop
- **Ctrl + Shift + F** - Alinear objeto con vista

---

## 📞 CUANDO TERMINES

Avísame cuando completes los pasos y te ayudaré con:
1. Configurar el sistema de combate multijugador
2. Conectar con el backend Python (Flask)
3. Integrar blockchain (EVT tokens)
4. Configurar los bots AI
5. Añadir vehículos

**¡Éxito! 🚀 Cualquier duda, pregunta!**
