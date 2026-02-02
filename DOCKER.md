# 🐳 Docker Support para Ciudad Robot

## Build

### Backend API (Node.js)
```bash
docker build -t ciudad-robot-backend -f backend/Dockerfile .
docker run -p 8000:8000 ciudad-robot-backend
```

### AI Engine (Python)
```bash
docker build -t ciudad-robot-ai -f ai-engine/Dockerfile .
docker run -p 8765:8765 ciudad-robot-ai
```

### Frontend
```bash
docker build -t ciudad-robot-frontend -f frontend/Dockerfile .
docker run -p 3000:3000 ciudad-robot-frontend
```

## Docker Compose (Recomendado)

```bash
# Iniciar todos los servicios
docker-compose up

# En background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

## Servicios Disponibles

- **Backend**: http://localhost:8000
- **AI Engine**: http://localhost:8765
- **Frontend**: http://localhost:3000
- **MongoDB**: localhost:27017
- **Redis**: localhost:6379

## Volúmenes

- `robot_data` - Persistencia de datos
- `logs` - Logs de aplicación

## Variables de Entorno

Ver `.env.docker` para configuración completa.

## Notas

- Los contenedores están conectados en una red `ciudad-robot-network`
- La base de datos persiste entre reinicios
- Los logs se guardan en `./logs/`
