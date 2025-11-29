"""
Gestor de base de datos para el sistema de IA
Maneja conexiones y operaciones con MongoDB
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import json

logger = logging.getLogger("database_manager")

class DatabaseManager:
    """Gestor de base de datos para Ciudad Robot"""
    
    def __init__(self, connection_string: str = "mongodb://localhost:27017/", db_name: str = "ciudad_robot"):
        self.connection_string = connection_string
        self.db_name = db_name
        self.client: Optional[MongoClient] = None
        self.db = None
        self.connected = False
        
    async def connect(self) -> bool:
        """Conectar a la base de datos"""
        try:
            self.client = MongoClient(
                self.connection_string,
                serverSelectionTimeoutMS=5000,  # 5 segundos timeout
                connectTimeoutMS=5000
            )
            
            # Probar conexión
            self.client.admin.command('ping')
            
            self.db = self.client[self.db_name]
            self.connected = True
            
            logger.info(f"Conectado a MongoDB: {self.db_name}")
            return True
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.warning(f"No se pudo conectar a MongoDB: {e}")
            logger.info("Funcionando en modo sin base de datos")
            self.connected = False
            return False
        except Exception as e:
            logger.error(f"Error inesperado conectando a MongoDB: {e}")
            self.connected = False
            return False
    
    async def disconnect(self):
        """Desconectar de la base de datos"""
        if self.client:
            self.client.close()
            self.connected = False
            logger.info("Desconectado de MongoDB")
    
    async def save_robot_data(self, robot_data: Dict[str, Any]) -> bool:
        """Guardar datos de robot"""
        if not self.connected:
            logger.debug("Base de datos no conectada, datos no guardados")
            return False
        
        try:
            collection = self.db.robots
            
            # Añadir timestamp
            robot_data['last_updated'] = datetime.now()
            
            # Upsert (insertar o actualizar)
            result = collection.replace_one(
                {"id": robot_data["id"]},
                robot_data,
                upsert=True
            )
            
            return result.acknowledged
            
        except Exception as e:
            logger.error(f"Error guardando datos de robot: {e}")
            return False
    
    async def get_robot_data(self, robot_id: str) -> Optional[Dict[str, Any]]:
        """Obtener datos de un robot"""
        if not self.connected:
            return None
        
        try:
            collection = self.db.robots
            result = collection.find_one({"id": robot_id})
            
            if result:
                # Remover _id de MongoDB
                result.pop('_id', None)
            
            return result
            
        except Exception as e:
            logger.error(f"Error obteniendo datos de robot: {e}")
            return None
    
    async def get_all_robots(self) -> List[Dict[str, Any]]:
        """Obtener todos los robots"""
        if not self.connected:
            return []
        
        try:
            collection = self.db.robots
            robots = list(collection.find())
            
            # Remover _id de MongoDB
            for robot in robots:
                robot.pop('_id', None)
            
            return robots
            
        except Exception as e:
            logger.error(f"Error obteniendo robots: {e}")
            return []
    
    async def save_decision_history(self, decision_data: Dict[str, Any]) -> bool:
        """Guardar historial de decisiones"""
        if not self.connected:
            return False
        
        try:
            collection = self.db.decisions
            result = collection.insert_one(decision_data)
            return result.acknowledged
            
        except Exception as e:
            logger.error(f"Error guardando decisión: {e}")
            return False
    
    async def get_decision_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Obtener historial de decisiones"""
        if not self.connected:
            return []
        
        try:
            collection = self.db.decisions
            decisions = list(collection.find().sort("timestamp", -1).limit(limit))
            
            # Remover _id de MongoDB
            for decision in decisions:
                decision.pop('_id', None)
            
            return decisions
            
        except Exception as e:
            logger.error(f"Error obteniendo historial de decisiones: {e}")
            return []
    
    async def save_city_metrics(self, metrics_data: Dict[str, Any]) -> bool:
        """Guardar métricas de la ciudad"""
        if not self.connected:
            return False
        
        try:
            collection = self.db.city_metrics
            
            # Añadir timestamp
            metrics_data['timestamp'] = datetime.now()
            
            result = collection.insert_one(metrics_data)
            return result.acknowledged
            
        except Exception as e:
            logger.error(f"Error guardando métricas de ciudad: {e}")
            return False
    
    async def get_city_metrics_history(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Obtener historial de métricas de la ciudad"""
        if not self.connected:
            return []
        
        try:
            collection = self.db.city_metrics
            
            # Filtrar por tiempo
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            metrics = list(collection.find({
                "timestamp": {"$gte": cutoff_time}
            }).sort("timestamp", -1))
            
            # Remover _id de MongoDB
            for metric in metrics:
                metric.pop('_id', None)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error obteniendo métricas de ciudad: {e}")
            return []
    
    async def save_optimization_result(self, optimization_data: Dict[str, Any]) -> bool:
        """Guardar resultado de optimización"""
        if not self.connected:
            return False
        
        try:
            collection = self.db.optimizations
            
            # Añadir timestamp
            optimization_data['timestamp'] = datetime.now()
            
            result = collection.insert_one(optimization_data)
            return result.acknowledged
            
        except Exception as e:
            logger.error(f"Error guardando optimización: {e}")
            return False
    
    async def get_optimization_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Obtener historial de optimizaciones"""
        if not self.connected:
            return []
        
        try:
            collection = self.db.optimizations
            optimizations = list(collection.find().sort("timestamp", -1).limit(limit))
            
            # Remover _id de MongoDB
            for opt in optimizations:
                opt.pop('_id', None)
            
            return optimizations
            
        except Exception as e:
            logger.error(f"Error obteniendo historial de optimizaciones: {e}")
            return []
    
    async def save_user_session(self, session_data: Dict[str, Any]) -> bool:
        """Guardar sesión de usuario"""
        if not self.connected:
            return False
        
        try:
            collection = self.db.user_sessions
            
            # Añadir timestamp
            session_data['last_activity'] = datetime.now()
            
            # Upsert por session_id
            result = collection.replace_one(
                {"session_id": session_data["session_id"]},
                session_data,
                upsert=True
            )
            
            return result.acknowledged
            
        except Exception as e:
            logger.error(f"Error guardando sesión de usuario: {e}")
            return False
    
    async def get_active_sessions(self) -> List[Dict[str, Any]]:
        """Obtener sesiones activas"""
        if not self.connected:
            return []
        
        try:
            collection = self.db.user_sessions
            
            # Sesiones activas en las últimas 4 horas
            cutoff_time = datetime.now() - timedelta(hours=4)
            
            sessions = list(collection.find({
                "last_activity": {"$gte": cutoff_time}
            }))
            
            # Remover _id de MongoDB
            for session in sessions:
                session.pop('_id', None)
            
            return sessions
            
        except Exception as e:
            logger.error(f"Error obteniendo sesiones activas: {e}")
            return []
    
    async def cleanup_old_data(self, days: int = 30):
        """Limpiar datos antiguos"""
        if not self.connected:
            return
        
        try:
            cutoff_time = datetime.now() - timedelta(days=days)
            
            # Limpiar métricas antiguas
            self.db.city_metrics.delete_many({
                "timestamp": {"$lt": cutoff_time}
            })
            
            # Limpiar decisiones antiguas (mantener más tiempo)
            old_cutoff = datetime.now() - timedelta(days=days*2)
            self.db.decisions.delete_many({
                "timestamp": {"$lt": old_cutoff}
            })
            
            # Limpiar sesiones antiguas
            session_cutoff = datetime.now() - timedelta(days=7)
            self.db.user_sessions.delete_many({
                "last_activity": {"$lt": session_cutoff}
            })
            
            logger.info(f"Limpieza de datos completada (datos anteriores a {cutoff_time})")
            
        except Exception as e:
            logger.error(f"Error en limpieza de datos: {e}")
    
    async def get_database_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de la base de datos"""
        if not self.connected:
            return {"status": "disconnected"}
        
        try:
            stats = {
                "status": "connected",
                "database": self.db_name,
                "collections": {}
            }
            
            # Estadísticas por colección
            for collection_name in self.db.list_collection_names():
                collection = self.db[collection_name]
                count = collection.count_documents({})
                stats["collections"][collection_name] = {
                    "document_count": count,
                    "size_mb": round(collection.stats().get("size", 0) / (1024*1024), 2)
                }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas de BD: {e}")
            return {"status": "error", "error": str(e)}