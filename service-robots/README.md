# 🤖 Robots de Servicio — Ciudad Robot

Sistema completo de **robots de servicio para la vida real**, implementado con [FastAPI](https://fastapi.tiangolo.com/). Cada robot expone una API REST y un sitio web propio.

---

## 🛠️ Robots disponibles

| Robot | Puerto | Archivo | Sitio web |
|---|---|---|---|
| 🏥 Robot Médico | `8001` | `medical_robot.py` | `/web/medical.html` |
| 🚔 Robot Policía | `8002` | `security_robot.py` | `/web/security.html` |
| 🚌 Robot Transporte | `8003` | `transport_robot.py` | `/web/transport.html` |
| 🛒 Robot Comerciante | `8004` | `commerce_robot.py` | `/web/commerce.html` |
| 🏗️ Robot Constructor | `8005` | `builder_robot.py` | `/web/builder.html` |
| 🎓 Robot Maestro | `8006` | `teacher_robot.py` | `/web/teacher.html` |

---

## 🚀 Inicio rápido

### Opción 1 — Docker Compose (recomendado)

```bash
# Desde la raíz del repositorio
docker-compose up -d robot-medico robot-policia robot-transporte \
                     robot-comerciante robot-constructor robot-maestro

# Verificar que están corriendo
docker-compose ps
```

Accede al panel principal: **http://localhost:8001/web/index.html**

### Opción 2 — Ejecución local con Python

```bash
cd service-robots

# Instalar dependencias
pip install -r requirements.txt

# Iniciar todos los robots en paralelo (terminales separadas o en background)
python medical_robot.py &
python security_robot.py &
python transport_robot.py &
python commerce_robot.py &
python builder_robot.py &
python teacher_robot.py &
```

### Opción 3 — Iniciar un robot individual

```bash
cd service-robots
pip install -r requirements.txt
python medical_robot.py    # Puerto 8001
```

---

## 📡 Endpoints y ejemplos `curl`

### 🏥 Robot Médico (puerto 8001)

```bash
# Estado del robot
curl http://localhost:8001/health

# Reportar emergencia médica
curl -X POST http://localhost:8001/api/medical/emergency \
  -H "Content-Type: application/json" \
  -d '{"patient_name":"Juan García","location":"Calle Mayor 10","description":"Dolor en el pecho","severity":"critical","contact_phone":"+34600000001"}'

# Estado de salud general
curl http://localhost:8001/api/medical/status

# Solicitar cita médica
curl -X POST http://localhost:8001/api/medical/appointment \
  -H "Content-Type: application/json" \
  -d '{"patient_name":"María López","doctor_type":"Cardiología","preferred_date":"2025-07-15","symptoms":"Fatiga crónica"}'
```

---

### 🚔 Robot Policía (puerto 8002)

```bash
# Estado del robot
curl http://localhost:8002/health

# Enviar alerta de seguridad
curl -X POST http://localhost:8002/api/security/alert \
  -H "Content-Type: application/json" \
  -d '{"location":"Plaza Central 3","alert_type":"theft","description":"Robo en tienda","reporter_name":"Testigo"}'

# Estado de patrullaje
curl http://localhost:8002/api/security/patrol-status

# Reportar incidente
curl -X POST http://localhost:8002/api/security/report \
  -H "Content-Type: application/json" \
  -d '{"incident_type":"accidente_trafico","location":"Av. Libertad 22","description":"Colisión entre dos vehículos"}'
```

---

### 🚌 Robot Transporte (puerto 8003)

```bash
# Estado del robot
curl http://localhost:8003/health

# Solicitar transporte
curl -X POST http://localhost:8003/api/transport/request \
  -H "Content-Type: application/json" \
  -d '{"pickup_location":"Aeropuerto T2","destination":"Centro Comercial Norte","cargo_type":"person","contact_name":"Carlos Ruiz"}'

# Ver rutas disponibles
curl http://localhost:8003/api/transport/routes

# Rastrear envío (sustituye <ID> por el id devuelto al solicitar)
curl http://localhost:8003/api/transport/track/<ID>
```

---

### 🛒 Robot Comerciante (puerto 8004)

```bash
# Estado del robot
curl http://localhost:8004/health

# Listar productos
curl http://localhost:8004/api/commerce/products

# Filtrar por categoría
curl "http://localhost:8004/api/commerce/products?category=robots"

# Realizar pedido
curl -X POST http://localhost:8004/api/commerce/order \
  -H "Content-Type: application/json" \
  -d '{"customer_name":"Ana Martínez","product_id":"P001","quantity":2,"delivery_address":"Calle Sol 5, Madrid"}'

# Consultar estado del pedido
curl http://localhost:8004/api/commerce/order/<ID>
```

---

### 🏗️ Robot Constructor (puerto 8005)

```bash
# Estado del robot
curl http://localhost:8005/health

# Crear proyecto
curl -X POST http://localhost:8005/api/builder/project \
  -H "Content-Type: application/json" \
  -d '{"project_name":"Torre Solar","project_type":"commercial","location":"Polígono Norte","budget":800000,"start_date":"2025-06-01","client_name":"Inmobiliaria XYZ"}'

# Listar proyectos activos
curl http://localhost:8005/api/builder/projects

# Actualizar progreso
curl -X PUT http://localhost:8005/api/builder/project/<ID>/progress \
  -H "Content-Type: application/json" \
  -d '{"progress_percent":45,"notes":"Estructura terminada al 45%"}'
```

---

### 🎓 Robot Maestro (puerto 8006)

```bash
# Estado del robot
curl http://localhost:8006/health

# Listar cursos
curl http://localhost:8006/api/teacher/courses

# Filtrar por nivel
curl "http://localhost:8006/api/teacher/courses?level=beginner"

# Inscribirse en un curso
curl -X POST http://localhost:8006/api/teacher/enroll \
  -H "Content-Type: application/json" \
  -d '{"student_name":"Luis Torres","course_id":"C001","email":"luis@email.com","experience_level":"beginner"}'

# Obtener lección
curl http://localhost:8006/api/teacher/lesson/C001-L01
```

---

## 📖 Documentación interactiva (Swagger UI)

Cada robot expone documentación automática en `/docs`:

| Robot | Swagger UI |
|---|---|
| 🏥 Médico | http://localhost:8001/docs |
| 🚔 Policía | http://localhost:8002/docs |
| 🚌 Transporte | http://localhost:8003/docs |
| 🛒 Comerciante | http://localhost:8004/docs |
| 🏗️ Constructor | http://localhost:8005/docs |
| 🎓 Maestro | http://localhost:8006/docs |

---

## ☁️ Despliegue en la nube

### Railway (más fácil, gratis)

1. Crea una cuenta en [railway.app](https://railway.app)
2. Conecta tu repositorio de GitHub
3. Agrega un nuevo servicio → selecciona `service-robots/`
4. Configura la variable `PORT` y el comando de inicio:
   ```
   CMD: python medical_robot.py
   ```
5. Railway asigna una URL pública automáticamente

### Render

1. Crea cuenta en [render.com](https://render.com)
2. Nuevo servicio → **Web Service** → conecta GitHub
3. Build command: `pip install -r service-robots/requirements.txt`
4. Start command: `python service-robots/medical_robot.py`
5. Expone el puerto `8001`

### AWS EC2 / Azure VM

```bash
# En el servidor
git clone https://github.com/Stylecaro/robot-City-
cd robot-City-
docker-compose up -d robot-medico robot-policia robot-transporte \
                     robot-comerciante robot-constructor robot-maestro

# Abre los puertos 8001–8006 en el Security Group / Firewall
```

### Google Cloud Run (serverless)

```bash
# Construir imagen
docker build -f service-robots/Dockerfile -t gcr.io/TU_PROYECTO/robot-medico .

# Subir imagen
docker push gcr.io/TU_PROYECTO/robot-medico

# Desplegar
gcloud run deploy robot-medico \
  --image gcr.io/TU_PROYECTO/robot-medico \
  --platform managed \
  --port 8001 \
  --allow-unauthenticated \
  --command="python,medical_robot.py"
```

---

## 🔧 Conectar con hardware real

### Raspberry Pi

```bash
# En la Raspberry Pi (Python 3.9+)
git clone https://github.com/Stylecaro/robot-City-
cd robot-City-/service-robots
pip3 install -r requirements.txt

# Iniciar robot en la red local
python3 medical_robot.py
# Ahora accesible desde http://<IP_RASPBERRY>:8001
```

Integración con GPIO desde el robot:
```python
# Dentro del endpoint FastAPI
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)  # Pin 18 → LED/Buzzer de emergencia

@app.post("/api/medical/emergency")
def report_emergency(req: EmergencyRequest):
    GPIO.output(18, GPIO.HIGH)  # Activa alarma física
    # ... resto de la lógica
```

### Arduino (vía Serial/USB)

```python
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)

@app.post("/api/security/alert")
def send_alert(req: AlertRequest):
    ser.write(b'ALERT\n')  # Envía señal al Arduino
    # ... resto de la lógica
```

### MQTT (IoT / sensores remotos)

```bash
pip install paho-mqtt
```

```python
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("broker.hivemq.com", 1883)

@app.post("/api/transport/request")
def request_transport(req: TransportRequest):
    client.publish("ciudad-robot/transport/new", req.json())
    # ... resto de la lógica
```

---

## 🏗️ Estructura del módulo

```
service-robots/
├── medical_robot.py      # 🏥 Robot Médico — puerto 8001
├── security_robot.py     # 🚔 Robot Policía — puerto 8002
├── transport_robot.py    # 🚌 Robot Transporte — puerto 8003
├── commerce_robot.py     # 🛒 Robot Comerciante — puerto 8004
├── builder_robot.py      # 🏗️ Robot Constructor — puerto 8005
├── teacher_robot.py      # 🎓 Robot Maestro — puerto 8006
├── requirements.txt      # Dependencias Python
├── Dockerfile            # Imagen Docker compartida
├── README.md             # Esta documentación
└── web/
    ├── index.html        # Panel principal con todos los robots
    ├── medical.html      # Portal del Robot Médico
    ├── security.html     # Portal del Robot Policía
    ├── transport.html    # Portal del Robot Transporte
    ├── commerce.html     # Tienda del Robot Comerciante
    ├── builder.html      # Gestor del Robot Constructor
    └── teacher.html      # Plataforma del Robot Maestro
```

---

## 📦 Dependencias

```
fastapi==0.115.12
uvicorn==0.34.0
pydantic==2.12.5
python-dotenv==1.0.0
```

---

> 🤖 **Ciudad Robot** — Robots de Servicio para la Vida Real
> [github.com/Stylecaro/robot-City-](https://github.com/Stylecaro/robot-City-)
