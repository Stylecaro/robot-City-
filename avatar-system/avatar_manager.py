"""
Gestor de Avatares - Sistema de gestión centralizada de avatares
Maneja la creación, modificación y coordinación de todos los avatares en la ciudad
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import asdict
import logging
import uuid

from avatar import VirtualAvatar, AvatarType, AvatarStyle

logger = logging.getLogger("avatar_manager")

class AvatarManager:
    """Gestor principal de avatares"""
    
    def __init__(self):
        self.avatars: Dict[str, VirtualAvatar] = {}  # avatar_id -> avatar
        self.user_avatars: Dict[str, List[str]] = {}  # user_id -> [avatar_ids]
        self.active_sessions: Dict[str, str] = {}  # user_id -> active_avatar_id
        
        # Configuración del sistema
        self.max_avatars_per_user = 5
        self.avatar_update_interval = 1.0  # segundos
        self.cleanup_interval = 300.0  # 5 minutos
        
        # Estadísticas
        self.total_avatars_created = 0
        self.total_interactions = 0
        self.total_customizations = 0
        
        # Sistema de eventos
        self.event_listeners = []
        
        logger.info("Avatar Manager inicializado")
    
    async def start_system(self):
        """Iniciar sistema de gestión de avatares"""
        asyncio.create_task(self._avatar_update_loop())
        asyncio.create_task(self._cleanup_loop())
        logger.info("Sistema de avatares iniciado")
    
    async def create_avatar(self, user_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Crear un nuevo avatar para un usuario"""
        try:
            # Verificar límite de avatares por usuario
            current_count = len(self.user_avatars.get(user_id, []))
            if current_count >= self.max_avatars_per_user:
                return {
                    "success": False,
                    "error": f"Límite de avatares alcanzado ({self.max_avatars_per_user})"
                }
            
            # Crear avatar
            avatar = VirtualAvatar(user_id, config)
            
            # Registrar avatar
            self.avatars[avatar.id] = avatar
            
            if user_id not in self.user_avatars:
                self.user_avatars[user_id] = []
            self.user_avatars[user_id].append(avatar.id)
            
            # Si es el primer avatar, activarlo automáticamente
            if user_id not in self.active_sessions:
                self.active_sessions[user_id] = avatar.id
            
            # Estadísticas
            self.total_avatars_created += 1
            
            # Evento de creación
            await self._emit_event("avatar_created", {
                "avatar_id": avatar.id,
                "user_id": user_id,
                "avatar_data": avatar.get_avatar_status()
            })
            
            logger.info(f"Avatar creado: {avatar.name} para usuario {user_id}")
            
            return {
                "success": True,
                "avatar": avatar.to_dict()
            }
            
        except Exception as e:
            logger.error(f"Error creando avatar para usuario {user_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_avatar(self, avatar_id: str) -> Optional[Dict[str, Any]]:
        """Obtener información de un avatar específico"""
        avatar = self.avatars.get(avatar_id)
        return avatar.to_dict() if avatar else None
    
    async def get_user_avatars(self, user_id: str) -> List[Dict[str, Any]]:
        """Obtener todos los avatares de un usuario"""
        avatar_ids = self.user_avatars.get(user_id, [])
        avatars = []
        
        for avatar_id in avatar_ids:
            avatar = self.avatars.get(avatar_id)
            if avatar:
                avatars.append(avatar.to_dict())
        
        return avatars
    
    async def get_active_avatar(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Obtener el avatar activo de un usuario"""
        active_avatar_id = self.active_sessions.get(user_id)
        if active_avatar_id:
            return await self.get_avatar(active_avatar_id)
        return None
    
    async def switch_active_avatar(self, user_id: str, avatar_id: str) -> bool:
        """Cambiar el avatar activo de un usuario"""
        # Verificar que el avatar pertenece al usuario
        user_avatar_ids = self.user_avatars.get(user_id, [])
        if avatar_id not in user_avatar_ids:
            logger.warning(f"Usuario {user_id} intentó activar avatar {avatar_id} que no le pertenece")
            return False
        
        # Verificar que el avatar existe
        if avatar_id not in self.avatars:
            logger.warning(f"Avatar {avatar_id} no encontrado")
            return False
        
        # Cambiar avatar activo
        old_avatar_id = self.active_sessions.get(user_id)
        self.active_sessions[user_id] = avatar_id
        
        # Eventos
        await self._emit_event("avatar_switched", {
            "user_id": user_id,
            "old_avatar_id": old_avatar_id,
            "new_avatar_id": avatar_id
        })
        
        logger.info(f"Usuario {user_id} cambió a avatar {avatar_id}")
        return True
    
    async def update_avatar_position(self, avatar_id: str, position: Dict[str, float]) -> bool:
        """Actualizar posición de un avatar"""
        avatar = self.avatars.get(avatar_id)
        if not avatar:
            return False
        
        success = await avatar.update_position(position)
        
        if success:
            # Evento de movimiento
            await self._emit_event("avatar_moved", {
                "avatar_id": avatar_id,
                "new_position": position,
                "user_id": avatar.user_id
            })
        
        return success
    
    async def avatar_interact_object(self, avatar_id: str, object_id: str, interaction_type: str) -> Dict[str, Any]:
        """Avatar interactúa con un objeto"""
        avatar = self.avatars.get(avatar_id)
        if not avatar:
            return {"success": False, "error": "Avatar no encontrado"}
        
        result = await avatar.interact_with_object(object_id, interaction_type)
        
        if result["success"]:
            self.total_interactions += 1
            
            # Evento de interacción
            await self._emit_event("avatar_object_interaction", {
                "avatar_id": avatar_id,
                "object_id": object_id,
                "interaction_type": interaction_type,
                "result": result
            })
        
        return result
    
    async def avatar_interact_avatar(self, avatar_id: str, target_avatar_id: str, interaction_type: str) -> Dict[str, Any]:
        """Avatar interactúa con otro avatar"""
        avatar = self.avatars.get(avatar_id)
        target_avatar = self.avatars.get(target_avatar_id)
        
        if not avatar:
            return {"success": False, "error": "Avatar origen no encontrado"}
        
        if not target_avatar:
            return {"success": False, "error": "Avatar destino no encontrado"}
        
        # Verificar rango de interacción
        distance = self._calculate_distance(avatar.position, target_avatar.position)
        if distance > avatar.capabilities.interaction_range:
            return {"success": False, "error": "Avatar fuera del rango de interacción"}
        
        result = await avatar.interact_with_avatar(target_avatar_id, interaction_type)
        
        if result["success"]:
            self.total_interactions += 1
            
            # Evento de interacción social
            await self._emit_event("avatar_social_interaction", {
                "avatar_id": avatar_id,
                "target_avatar_id": target_avatar_id,
                "interaction_type": interaction_type,
                "result": result
            })
            
            # Notificar al avatar destino si está activo
            if target_avatar.is_active:
                await self._notify_avatar_interaction(target_avatar, avatar_id, interaction_type)
        
        return result
    
    def _calculate_distance(self, pos1: Dict[str, float], pos2: Dict[str, float]) -> float:
        """Calcular distancia entre dos posiciones"""
        import math
        
        dx = pos1["x"] - pos2["x"]
        dy = pos1["y"] - pos2["y"]
        dz = pos1["z"] - pos2["z"]
        
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    async def _notify_avatar_interaction(self, target_avatar: VirtualAvatar, source_avatar_id: str, interaction_type: str):
        """Notificar a un avatar sobre una interacción recibida"""
        # El avatar destino puede reaccionar a la interacción
        source_avatar = self.avatars.get(source_avatar_id)
        if source_avatar:
            # Simular reacción automática basada en personalidad
            if target_avatar.behavior.personality_traits["friendliness"] > 0.7:
                # Avatar amigable responde positivamente
                await self._emit_event("avatar_reaction", {
                    "avatar_id": target_avatar.id,
                    "source_avatar_id": source_avatar_id,
                    "reaction": "positive",
                    "message": target_avatar.behavior.auto_responses.get("greeting", "Hello!")
                })
    
    async def customize_avatar(self, avatar_id: str, updates: Dict[str, Any]) -> bool:
        """Personalizar apariencia de un avatar"""
        avatar = self.avatars.get(avatar_id)
        if not avatar:
            return False
        
        success = await avatar.customize_appearance(updates)
        
        if success:
            self.total_customizations += 1
            
            # Evento de personalización
            await self._emit_event("avatar_customized", {
                "avatar_id": avatar_id,
                "updates": updates,
                "user_id": avatar.user_id
            })
        
        return success
    
    async def delete_avatar(self, avatar_id: str, user_id: str) -> bool:
        """Eliminar un avatar"""
        # Verificar permisos
        user_avatar_ids = self.user_avatars.get(user_id, [])
        if avatar_id not in user_avatar_ids:
            return False
        
        # Remover de estructuras de datos
        if avatar_id in self.avatars:
            del self.avatars[avatar_id]
        
        user_avatar_ids.remove(avatar_id)
        
        # Si era el avatar activo, cambiar a otro
        if self.active_sessions.get(user_id) == avatar_id:
            if user_avatar_ids:
                self.active_sessions[user_id] = user_avatar_ids[0]
            else:
                del self.active_sessions[user_id]
        
        # Evento de eliminación
        await self._emit_event("avatar_deleted", {
            "avatar_id": avatar_id,
            "user_id": user_id
        })
        
        logger.info(f"Avatar {avatar_id} eliminado por usuario {user_id}")
        return True
    
    async def get_nearby_avatars(self, avatar_id: str, radius: float = 10.0) -> List[Dict[str, Any]]:
        """Obtener avatares cercanos a una posición"""
        avatar = self.avatars.get(avatar_id)
        if not avatar:
            return []
        
        nearby_avatars = []
        
        for other_id, other_avatar in self.avatars.items():
            if other_id == avatar_id:
                continue
            
            distance = self._calculate_distance(avatar.position, other_avatar.position)
            if distance <= radius:
                nearby_avatars.append({
                    **other_avatar.get_avatar_status(),
                    "distance": round(distance, 2)
                })
        
        # Ordenar por distancia
        nearby_avatars.sort(key=lambda x: x["distance"])
        
        return nearby_avatars
    
    async def get_avatar_analytics(self, user_id: str) -> Dict[str, Any]:
        """Obtener analíticas de avatares de un usuario"""
        user_avatar_ids = self.user_avatars.get(user_id, [])
        
        if not user_avatar_ids:
            return {"status": "no_avatars"}
        
        avatars_data = []
        total_interactions = 0
        total_experience = 0
        total_levels = 0
        
        for avatar_id in user_avatar_ids:
            avatar = self.avatars.get(avatar_id)
            if avatar:
                avatars_data.append(avatar.get_avatar_status())
                total_interactions += avatar.interactions_count
                total_experience += avatar.experience_points
                total_levels += avatar.level
        
        return {
            "total_avatars": len(avatars_data),
            "total_interactions": total_interactions,
            "total_experience": total_experience,
            "average_level": total_levels / len(avatars_data) if avatars_data else 0,
            "most_active_avatar": max(avatars_data, key=lambda x: x["interactions_count"], default=None),
            "highest_level_avatar": max(avatars_data, key=lambda x: x["level"], default=None),
            "avatars": avatars_data
        }
    
    async def get_system_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del sistema de avatares"""
        active_avatars = sum(1 for avatar in self.avatars.values() if avatar.is_active)
        
        # Estadísticas por tipo de avatar
        type_counts = {}
        for avatar in self.avatars.values():
            avatar_type = avatar.avatar_type.value
            type_counts[avatar_type] = type_counts.get(avatar_type, 0) + 1
        
        # Usuarios activos (con sesión)
        active_users = len(self.active_sessions)
        
        return {
            "total_avatars": len(self.avatars),
            "active_avatars": active_avatars,
            "total_users": len(self.user_avatars),
            "active_users": active_users,
            "total_interactions": self.total_interactions,
            "total_customizations": self.total_customizations,
            "avatars_by_type": type_counts,
            "average_avatars_per_user": len(self.avatars) / max(len(self.user_avatars), 1),
            "system_uptime": "active"
        }
    
    async def _avatar_update_loop(self):
        """Loop de actualización de avatares"""
        while True:
            try:
                await asyncio.sleep(self.avatar_update_interval)
                
                # Actualizar todos los avatares activos
                for avatar in self.avatars.values():
                    if avatar.is_active:
                        # Verificar si el avatar ha estado inactivo por mucho tiempo
                        inactive_time = datetime.now() - avatar.last_activity
                        if inactive_time > timedelta(hours=1):
                            avatar.is_active = False
                            logger.info(f"Avatar {avatar.name} marcado como inactivo")
                
            except Exception as e:
                logger.error(f"Error en avatar update loop: {e}")
    
    async def _cleanup_loop(self):
        """Loop de limpieza del sistema"""
        while True:
            try:
                await asyncio.sleep(self.cleanup_interval)
                await self._cleanup_inactive_avatars()
                
            except Exception as e:
                logger.error(f"Error en cleanup loop: {e}")
    
    async def _cleanup_inactive_avatars(self):
        """Limpiar avatares inactivos"""
        cutoff_time = datetime.now() - timedelta(days=7)  # 7 días de inactividad
        
        avatars_to_remove = []
        
        for avatar_id, avatar in self.avatars.items():
            if avatar.last_activity < cutoff_time and not avatar.is_active:
                avatars_to_remove.append(avatar_id)
        
        for avatar_id in avatars_to_remove:
            avatar = self.avatars[avatar_id]
            user_id = avatar.user_id
            
            # Remover avatar inactivo
            await self.delete_avatar(avatar_id, user_id)
            
            logger.info(f"Avatar inactivo removido: {avatar_id}")
    
    async def add_event_listener(self, listener_func):
        """Añadir listener para eventos del sistema"""
        self.event_listeners.append(listener_func)
    
    async def _emit_event(self, event_type: str, data: Dict[str, Any]):
        """Emitir evento a todos los listeners"""
        event_data = {
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        for listener in self.event_listeners:
            try:
                await listener(event_data)
            except Exception as e:
                logger.error(f"Error en event listener: {e}")
    
    async def export_avatar_data(self, avatar_id: str) -> Optional[Dict[str, Any]]:
        """Exportar datos completos de un avatar"""
        avatar = self.avatars.get(avatar_id)
        if not avatar:
            return None
        
        return {
            "avatar_data": avatar.to_dict(),
            "export_timestamp": datetime.now().isoformat(),
            "version": "1.0"
        }
    
    async def import_avatar_data(self, user_id: str, avatar_data: Dict[str, Any]) -> Dict[str, Any]:
        """Importar datos de avatar"""
        try:
            # Validar datos
            if "avatar_data" not in avatar_data:
                return {"success": False, "error": "Datos de avatar inválidos"}
            
            data = avatar_data["avatar_data"]
            
            # Crear configuración para nuevo avatar
            config = {
                "name": data.get("name", "Imported Avatar"),
                "type": data.get("type", "humanoid"),
                "style": data.get("style", "realistic"),
                "appearance": data.get("appearance", {}),
                "capabilities": data.get("capabilities", {}),
                "behavior": data.get("behavior", {})
            }
            
            # Crear avatar importado
            result = await self.create_avatar(user_id, config)
            
            if result["success"]:
                # Restaurar estado adicional si es posible
                imported_avatar = self.avatars[result["avatar"]["id"]]
                
                # Restaurar experiencia y nivel (con límites)
                imported_avatar.experience_points = min(data.get("experience_points", 0), 1000)
                imported_avatar.level = min(data.get("level", 1), 10)
                
                logger.info(f"Avatar importado exitosamente para usuario {user_id}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error importando avatar: {e}")
            return {"success": False, "error": str(e)}