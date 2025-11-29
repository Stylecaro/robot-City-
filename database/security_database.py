"""
Configuración de Base de Datos para Sistema de Seguridad
Esquemas MongoDB para humanoides, amenazas, zonas e incidentes
"""

from pymongo import MongoClient, IndexModel, ASCENDING, DESCENDING, GEO2D, TEXT
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Optional
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityDatabaseConfig:
    """
    Configurador de base de datos para el sistema de seguridad
    """
    
    def __init__(self, connection_string: str = None):
        self.connection_string = connection_string or os.getenv(
            'MONGODB_URI', 
            'mongodb://localhost:27017/'
        )
        self.db_name = 'ciudad_robot_security'
        self.client = None
        self.db = None
        
    async def initialize_database(self) -> bool:
        """Inicializar base de datos y colecciones"""
        try:
            # Conectar a MongoDB
            self.client = MongoClient(self.connection_string)
            self.db = self.client[self.db_name]
            
            # Verificar conexión
            self.client.admin.command('ping')
            logger.info(f"Conectado a MongoDB: {self.db_name}")
            
            # Crear colecciones y esquemas
            await self._create_collections()
            await self._create_indexes()
            await self._insert_initial_data()
            
            logger.info("Base de datos de seguridad inicializada exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error inicializando base de datos: {e}")
            return False
    
    async def _create_collections(self):
        """Crear colecciones principales"""
        collections = {
            'humanoids': self._get_humanoid_schema(),
            'security_zones': self._get_zone_schema(),
            'threats': self._get_threat_schema(),
            'incidents': self._get_incident_schema(),
            'security_logs': self._get_log_schema(),
            'performance_metrics': self._get_metrics_schema(),
            'alert_history': self._get_alert_schema(),
            'command_history': self._get_command_schema()
        }
        
        for collection_name, schema in collections.items():
            try:
                # Crear colección si no existe
                if collection_name not in self.db.list_collection_names():
                    self.db.create_collection(
                        collection_name,
                        validator={'$jsonSchema': schema}
                    )
                    logger.info(f"Colección creada: {collection_name}")
                else:
                    logger.info(f"Colección ya existe: {collection_name}")
                    
            except Exception as e:
                logger.warning(f"Error creando colección {collection_name}: {e}")
    
    async def _create_indexes(self):
        """Crear índices para optimización"""
        
        # Índices para humanoides
        humanoid_indexes = [
            IndexModel([("humanoid_id", ASCENDING)], unique=True),
            IndexModel([("type", ASCENDING)]),
            IndexModel([("status", ASCENDING)]),
            IndexModel([("position", GEO2D)]),
            IndexModel([("assigned_zone", ASCENDING)]),
            IndexModel([("deployed_at", DESCENDING)]),
            IndexModel([("energy", ASCENDING)]),
            IndexModel([("last_updated", DESCENDING)])
        ]
        
        # Índices para zonas de seguridad
        zone_indexes = [
            IndexModel([("zone_id", ASCENDING)], unique=True),
            IndexModel([("type", ASCENDING)]),
            IndexModel([("security_level", DESCENDING)]),
            IndexModel([("boundaries", GEO2D)]),
            IndexModel([("active", ASCENDING)]),
            IndexModel([("created_at", DESCENDING)])
        ]
        
        # Índices para amenazas
        threat_indexes = [
            IndexModel([("threat_id", ASCENDING)], unique=True),
            IndexModel([("type", ASCENDING)]),
            IndexModel([("severity", DESCENDING)]),
            IndexModel([("status", ASCENDING)]),
            IndexModel([("location", GEO2D)]),
            IndexModel([("detected_at", DESCENDING)]),
            IndexModel([("resolved_at", DESCENDING)]),
            IndexModel([("description", TEXT)])
        ]
        
        # Índices para incidentes
        incident_indexes = [
            IndexModel([("incident_id", ASCENDING)], unique=True),
            IndexModel([("status", ASCENDING)]),
            IndexModel([("priority", DESCENDING)]),
            IndexModel([("created_at", DESCENDING)]),
            IndexModel([("resolved_at", DESCENDING)]),
            IndexModel([("assigned_humanoids", ASCENDING)]),
            IndexModel([("zone_id", ASCENDING)])
        ]
        
        # Índices para logs de seguridad
        log_indexes = [
            IndexModel([("timestamp", DESCENDING)]),
            IndexModel([("level", ASCENDING)]),
            IndexModel([("source", ASCENDING)]),
            IndexModel([("event_type", ASCENDING)]),
            IndexModel([("humanoid_id", ASCENDING)]),
            IndexModel([("message", TEXT)])
        ]
        
        # Índices para métricas de rendimiento
        metrics_indexes = [
            IndexModel([("timestamp", DESCENDING)]),
            IndexModel([("metric_type", ASCENDING)]),
            IndexModel([("humanoid_id", ASCENDING)]),
            IndexModel([("zone_id", ASCENDING)])
        ]
        
        # Índices para historial de alertas
        alert_indexes = [
            IndexModel([("timestamp", DESCENDING)]),
            IndexModel([("level", ASCENDING)]),
            IndexModel([("changed_by", ASCENDING)]),
            IndexModel([("active", ASCENDING)])
        ]
        
        # Índices para historial de comandos
        command_indexes = [
            IndexModel([("timestamp", DESCENDING)]),
            IndexModel([("humanoid_id", ASCENDING)]),
            IndexModel([("command", ASCENDING)]),
            IndexModel([("executed_by", ASCENDING)]),
            IndexModel([("status", ASCENDING)])
        ]
        
        # Crear todos los índices
        index_sets = [
            ('humanoids', humanoid_indexes),
            ('security_zones', zone_indexes),
            ('threats', threat_indexes),
            ('incidents', incident_indexes),
            ('security_logs', log_indexes),
            ('performance_metrics', metrics_indexes),
            ('alert_history', alert_indexes),
            ('command_history', command_indexes)
        ]
        
        for collection_name, indexes in index_sets:
            try:
                collection = self.db[collection_name]
                collection.create_indexes(indexes)
                logger.info(f"Índices creados para {collection_name}")
            except Exception as e:
                logger.warning(f"Error creando índices para {collection_name}: {e}")
    
    async def _insert_initial_data(self):
        """Insertar datos iniciales del sistema"""
        
        # Zonas de seguridad predeterminadas
        default_zones = [
            {
                "zone_id": "ZONE-CENTRAL",
                "name": "Centro de Ciudad",
                "type": "public",
                "security_level": 5,
                "boundaries": [
                    {"x": -50, "y": -50},
                    {"x": 50, "y": -50},
                    {"x": 50, "y": 50},
                    {"x": -50, "y": 50}
                ],
                "access_permissions": ["public", "security"],
                "patrol_frequency": 15.0,
                "special_protocols": [],
                "active": True,
                "created_at": datetime.now(),
                "threat_history": [],
                "current_status": "secure",
                "assigned_humanoids": []
            },
            {
                "zone_id": "ZONE-INDUSTRIAL",
                "name": "Sector Industrial",
                "type": "industrial",
                "security_level": 7,
                "boundaries": [
                    {"x": 100, "y": -100},
                    {"x": 200, "y": -100},
                    {"x": 200, "y": 100},
                    {"x": 100, "y": 100}
                ],
                "access_permissions": ["authorized", "security"],
                "patrol_frequency": 10.0,
                "special_protocols": ["hazmat_detection", "fire_suppression"],
                "active": True,
                "created_at": datetime.now(),
                "threat_history": [],
                "current_status": "secure",
                "assigned_humanoids": []
            },
            {
                "zone_id": "ZONE-RESIDENTIAL",
                "name": "Zona Residencial",
                "type": "residential",
                "security_level": 3,
                "boundaries": [
                    {"x": -200, "y": -200},
                    {"x": -50, "y": -200},
                    {"x": -50, "y": 200},
                    {"x": -200, "y": 200}
                ],
                "access_permissions": ["residents", "security"],
                "patrol_frequency": 20.0,
                "special_protocols": ["noise_monitoring", "privacy_protection"],
                "active": True,
                "created_at": datetime.now(),
                "threat_history": [],
                "current_status": "secure",
                "assigned_humanoids": []
            },
            {
                "zone_id": "ZONE-CRITICAL",
                "name": "Infraestructura Crítica",
                "type": "critical_infrastructure",
                "security_level": 10,
                "boundaries": [
                    {"x": -25, "y": -25},
                    {"x": 25, "y": -25},
                    {"x": 25, "y": 25},
                    {"x": -25, "y": 25}
                ],
                "access_permissions": ["security", "admin"],
                "patrol_frequency": 5.0,
                "special_protocols": ["maximum_security", "biometric_scanning", "ai_monitoring"],
                "active": True,
                "created_at": datetime.now(),
                "threat_history": [],
                "current_status": "secure",
                "assigned_humanoids": []
            }
        ]
        
        # Configuración inicial del sistema
        system_config = {
            "config_id": "SECURITY_SYSTEM_CONFIG",
            "alert_level": "GREEN",
            "auto_deployment": True,
            "threat_response_time": 30,
            "max_humanoids_per_zone": 5,
            "energy_warning_threshold": 20,
            "maintenance_interval": 24,
            "performance_monitoring": True,
            "ai_integration_enabled": True,
            "real_time_updates": True,
            "created_at": datetime.now(),
            "last_updated": datetime.now()
        }
        
        # Insertar datos si las colecciones están vacías
        try:
            # Insertar zonas
            zones_collection = self.db['security_zones']
            if zones_collection.count_documents({}) == 0:
                zones_collection.insert_many(default_zones)
                logger.info(f"Insertadas {len(default_zones)} zonas predeterminadas")
            
            # Insertar configuración del sistema
            config_collection = self.db['system_config']
            if config_collection.count_documents({}) == 0:
                config_collection.insert_one(system_config)
                logger.info("Configuración del sistema insertada")
                
        except Exception as e:
            logger.warning(f"Error insertando datos iniciales: {e}")
    
    def _get_humanoid_schema(self) -> Dict:
        """Esquema para colección de humanoides"""
        return {
            "bsonType": "object",
            "required": ["humanoid_id", "type", "position", "status", "deployed_at"],
            "properties": {
                "humanoid_id": {
                    "bsonType": "string",
                    "description": "ID único del humanoide"
                },
                "type": {
                    "bsonType": "string",
                    "enum": ["guardian", "sentinel", "interceptor", "scout", "commander", "medic", "cyber_defender", "heavy_guardian"],
                    "description": "Tipo de humanoide"
                },
                "position": {
                    "bsonType": "object",
                    "required": ["x", "y", "z"],
                    "properties": {
                        "x": {"bsonType": "number"},
                        "y": {"bsonType": "number"},
                        "z": {"bsonType": "number"}
                    }
                },
                "status": {
                    "bsonType": "string",
                    "enum": ["active", "patrol", "responding", "maintenance", "charging", "offline"],
                    "description": "Estado actual del humanoide"
                },
                "energy": {
                    "bsonType": "number",
                    "minimum": 0,
                    "maximum": 100,
                    "description": "Nivel de energía en porcentaje"
                },
                "armor": {
                    "bsonType": "number",
                    "minimum": 0,
                    "maximum": 100,
                    "description": "Nivel de armadura en porcentaje"
                },
                "shields": {
                    "bsonType": "number",
                    "minimum": 0,
                    "maximum": 100,
                    "description": "Nivel de escudos en porcentaje"
                },
                "assigned_zone": {
                    "bsonType": ["string", "null"],
                    "description": "ID de zona asignada"
                },
                "current_protocol": {
                    "bsonType": "string",
                    "description": "Protocolo actual en ejecución"
                },
                "deployed_at": {
                    "bsonType": "date",
                    "description": "Fecha y hora de despliegue"
                },
                "last_updated": {
                    "bsonType": "date",
                    "description": "Última actualización de estado"
                },
                "performance_metrics": {
                    "bsonType": "object",
                    "properties": {
                        "threats_neutralized": {"bsonType": "number"},
                        "response_time_avg": {"bsonType": "number"},
                        "success_rate": {"bsonType": "number"},
                        "uptime_percentage": {"bsonType": "number"}
                    }
                },
                "capabilities": {
                    "bsonType": "object",
                    "description": "Capacidades específicas del humanoide"
                },
                "sensor_data": {
                    "bsonType": "object",
                    "description": "Datos de sensores en tiempo real"
                }
            }
        }
    
    def _get_zone_schema(self) -> Dict:
        """Esquema para colección de zonas de seguridad"""
        return {
            "bsonType": "object",
            "required": ["zone_id", "name", "type", "security_level", "boundaries"],
            "properties": {
                "zone_id": {
                    "bsonType": "string",
                    "description": "ID único de la zona"
                },
                "name": {
                    "bsonType": "string",
                    "description": "Nombre descriptivo de la zona"
                },
                "type": {
                    "bsonType": "string",
                    "enum": ["public", "restricted", "high_security", "critical_infrastructure", "residential", "industrial"],
                    "description": "Tipo de zona"
                },
                "security_level": {
                    "bsonType": "number",
                    "minimum": 1,
                    "maximum": 10,
                    "description": "Nivel de seguridad requerido"
                },
                "boundaries": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "required": ["x", "y"],
                        "properties": {
                            "x": {"bsonType": "number"},
                            "y": {"bsonType": "number"}
                        }
                    },
                    "description": "Puntos que definen los límites de la zona"
                },
                "access_permissions": {
                    "bsonType": "array",
                    "items": {"bsonType": "string"},
                    "description": "Permisos de acceso requeridos"
                },
                "patrol_frequency": {
                    "bsonType": "number",
                    "minimum": 1,
                    "description": "Frecuencia de patrullaje en minutos"
                },
                "special_protocols": {
                    "bsonType": "array",
                    "items": {"bsonType": "string"},
                    "description": "Protocolos especiales para la zona"
                },
                "active": {
                    "bsonType": "bool",
                    "description": "Si la zona está activa"
                },
                "created_at": {
                    "bsonType": "date",
                    "description": "Fecha de creación"
                },
                "threat_history": {
                    "bsonType": "array",
                    "description": "Historial de amenazas en la zona"
                },
                "current_status": {
                    "bsonType": "string",
                    "enum": ["secure", "alert", "threat_detected", "under_attack", "compromised"],
                    "description": "Estado actual de la zona"
                },
                "assigned_humanoids": {
                    "bsonType": "array",
                    "items": {"bsonType": "string"},
                    "description": "IDs de humanoides asignados"
                }
            }
        }
    
    def _get_threat_schema(self) -> Dict:
        """Esquema para colección de amenazas"""
        return {
            "bsonType": "object",
            "required": ["threat_id", "type", "location", "severity", "detected_at"],
            "properties": {
                "threat_id": {
                    "bsonType": "string",
                    "description": "ID único de la amenaza"
                },
                "type": {
                    "bsonType": "string",
                    "enum": ["intrusion_physical", "cyber_attack", "hostile_entity", "system_malfunction", "natural_disaster", "unknown"],
                    "description": "Tipo de amenaza"
                },
                "location": {
                    "bsonType": "object",
                    "required": ["x", "y", "z"],
                    "properties": {
                        "x": {"bsonType": "number"},
                        "y": {"bsonType": "number"},
                        "z": {"bsonType": "number"}
                    }
                },
                "severity": {
                    "bsonType": "string",
                    "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL", "IMMINENT"],
                    "description": "Nivel de severidad"
                },
                "status": {
                    "bsonType": "string",
                    "enum": ["detected", "analyzing", "responding", "contained", "neutralized", "false_alarm"],
                    "description": "Estado actual de la amenaza"
                },
                "detected_at": {
                    "bsonType": "date",
                    "description": "Fecha y hora de detección"
                },
                "resolved_at": {
                    "bsonType": ["date", "null"],
                    "description": "Fecha y hora de resolución"
                },
                "description": {
                    "bsonType": "string",
                    "description": "Descripción detallada de la amenaza"
                },
                "evidence": {
                    "bsonType": "object",
                    "description": "Evidencia y datos de detección"
                },
                "confidence_level": {
                    "bsonType": "number",
                    "minimum": 0,
                    "maximum": 1,
                    "description": "Nivel de confianza en la detección"
                },
                "assigned_humanoids": {
                    "bsonType": "array",
                    "items": {"bsonType": "string"},
                    "description": "Humanoides asignados para responder"
                },
                "response_actions": {
                    "bsonType": "array",
                    "description": "Acciones de respuesta tomadas"
                },
                "reporter": {
                    "bsonType": "string",
                    "description": "Quién reportó la amenaza"
                }
            }
        }
    
    def _get_incident_schema(self) -> Dict:
        """Esquema para colección de incidentes"""
        return {
            "bsonType": "object",
            "required": ["incident_id", "title", "status", "priority", "created_at"],
            "properties": {
                "incident_id": {
                    "bsonType": "string",
                    "description": "ID único del incidente"
                },
                "title": {
                    "bsonType": "string",
                    "description": "Título del incidente"
                },
                "description": {
                    "bsonType": "string",
                    "description": "Descripción detallada"
                },
                "status": {
                    "bsonType": "string",
                    "enum": ["open", "investigating", "responding", "resolved", "closed"],
                    "description": "Estado del incidente"
                },
                "priority": {
                    "bsonType": "string",
                    "enum": ["low", "medium", "high", "critical", "emergency"],
                    "description": "Prioridad del incidente"
                },
                "created_at": {
                    "bsonType": "date",
                    "description": "Fecha de creación"
                },
                "updated_at": {
                    "bsonType": "date",
                    "description": "Última actualización"
                },
                "resolved_at": {
                    "bsonType": ["date", "null"],
                    "description": "Fecha de resolución"
                },
                "assigned_humanoids": {
                    "bsonType": "array",
                    "items": {"bsonType": "string"},
                    "description": "Humanoides asignados"
                },
                "related_threats": {
                    "bsonType": "array",
                    "items": {"bsonType": "string"},
                    "description": "IDs de amenazas relacionadas"
                },
                "zone_id": {
                    "bsonType": ["string", "null"],
                    "description": "Zona donde ocurrió el incidente"
                },
                "resolution_summary": {
                    "bsonType": "string",
                    "description": "Resumen de la resolución"
                },
                "lessons_learned": {
                    "bsonType": "string",
                    "description": "Lecciones aprendidas"
                }
            }
        }
    
    def _get_log_schema(self) -> Dict:
        """Esquema para logs de seguridad"""
        return {
            "bsonType": "object",
            "required": ["timestamp", "level", "source", "message"],
            "properties": {
                "timestamp": {"bsonType": "date"},
                "level": {
                    "bsonType": "string",
                    "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "SECURITY"]
                },
                "source": {"bsonType": "string"},
                "event_type": {"bsonType": "string"},
                "humanoid_id": {"bsonType": ["string", "null"]},
                "zone_id": {"bsonType": ["string", "null"]},
                "threat_id": {"bsonType": ["string", "null"]},
                "message": {"bsonType": "string"},
                "details": {"bsonType": "object"}
            }
        }
    
    def _get_metrics_schema(self) -> Dict:
        """Esquema para métricas de rendimiento"""
        return {
            "bsonType": "object",
            "required": ["timestamp", "metric_type", "value"],
            "properties": {
                "timestamp": {"bsonType": "date"},
                "metric_type": {"bsonType": "string"},
                "value": {"bsonType": "number"},
                "humanoid_id": {"bsonType": ["string", "null"]},
                "zone_id": {"bsonType": ["string", "null"]},
                "metadata": {"bsonType": "object"}
            }
        }
    
    def _get_alert_schema(self) -> Dict:
        """Esquema para historial de alertas"""
        return {
            "bsonType": "object",
            "required": ["timestamp", "level", "changed_by"],
            "properties": {
                "timestamp": {"bsonType": "date"},
                "level": {
                    "bsonType": "string",
                    "enum": ["GREEN", "YELLOW", "ORANGE", "RED", "BLACK"]
                },
                "previous_level": {"bsonType": "string"},
                "reason": {"bsonType": "string"},
                "changed_by": {"bsonType": "string"},
                "active": {"bsonType": "bool"},
                "protocols_activated": {
                    "bsonType": "array",
                    "items": {"bsonType": "string"}
                }
            }
        }
    
    def _get_command_schema(self) -> Dict:
        """Esquema para historial de comandos"""
        return {
            "bsonType": "object",
            "required": ["timestamp", "humanoid_id", "command", "executed_by"],
            "properties": {
                "timestamp": {"bsonType": "date"},
                "humanoid_id": {"bsonType": "string"},
                "command": {"bsonType": "string"},
                "parameters": {"bsonType": "object"},
                "executed_by": {"bsonType": "string"},
                "status": {
                    "bsonType": "string",
                    "enum": ["pending", "executing", "completed", "failed", "cancelled"]
                },
                "result": {"bsonType": "object"},
                "execution_time": {"bsonType": "number"}
            }
        }
    
    def get_database(self):
        """Obtener instancia de la base de datos"""
        return self.db
    
    def close_connection(self):
        """Cerrar conexión a la base de datos"""
        if self.client:
            self.client.close()
            logger.info("Conexión a MongoDB cerrada")

# Función de utilidad para inicialización rápida
async def initialize_security_database(connection_string: str = None) -> SecurityDatabaseConfig:
    """
    Inicializar base de datos de seguridad
    """
    db_config = SecurityDatabaseConfig(connection_string)
    success = await db_config.initialize_database()
    
    if success:
        logger.info("Base de datos de seguridad lista para uso")
        return db_config
    else:
        logger.error("Falló la inicialización de la base de datos")
        return None

# Ejemplo de uso
if __name__ == "__main__":
    import asyncio
    
    async def main():
        # Inicializar base de datos
        db_config = await initialize_security_database()
        
        if db_config:
            # Ejemplo de inserción de datos
            db = db_config.get_database()
            
            # Insertar un humanoide de ejemplo
            example_humanoid = {
                "humanoid_id": "SEC-001",
                "type": "guardian",
                "position": {"x": 0, "y": 0, "z": 0},
                "status": "active",
                "energy": 100,
                "armor": 100,
                "shields": 100,
                "assigned_zone": "ZONE-CENTRAL",
                "current_protocol": "patrol",
                "deployed_at": datetime.now(),
                "last_updated": datetime.now(),
                "performance_metrics": {
                    "threats_neutralized": 0,
                    "response_time_avg": 0,
                    "success_rate": 1.0,
                    "uptime_percentage": 100
                }
            }
            
            try:
                result = db.humanoids.insert_one(example_humanoid)
                print(f"Humanoide insertado con ID: {result.inserted_id}")
                
                # Consultar humanoides
                humanoids = list(db.humanoids.find({}))
                print(f"Total de humanoides: {len(humanoids)}")
                
            except Exception as e:
                print(f"Error en ejemplo: {e}")
            
            # Cerrar conexión
            db_config.close_connection()
    
    # Ejecutar ejemplo
    asyncio.run(main())