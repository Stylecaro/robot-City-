"""
Sistema de Avatares Personalizados
Gestiona la creación, customización y control de avatares virtuales para usuarios
"""

import uuid
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import random
import numpy as np

logger = logging.getLogger("avatar_system")

class AvatarType(Enum):
    """Tipos de avatares disponibles"""
    HUMANOID = "humanoid"
    ROBOTIC = "robotic"
    ABSTRACT = "abstract"
    CREATURE = "creature"
    HYBRID = "hybrid"

class AvatarStyle(Enum):
    """Estilos de avatares"""
    REALISTIC = "realistic"
    CARTOON = "cartoon"
    CYBERPUNK = "cyberpunk"
    FANTASY = "fantasy"
    MINIMALIST = "minimalist"
    FUTURISTIC = "futuristic"

@dataclass
class AvatarAppearance:
    """Configuración de apariencia del avatar"""
    # Características físicas básicas
    height: float  # 0.5 - 2.5 (metros)
    body_type: str  # slim, athletic, robust, etc.
    
    # Colores
    primary_color: str  # Hex color
    secondary_color: str
    accent_color: str
    
    # Características específicas
    head_shape: str
    eye_type: str
    eye_color: str
    
    # Accesorios
    accessories: List[str]
    clothing: List[str]
    
    # Efectos especiales
    glow_effect: bool
    particle_effects: List[str]
    aura_color: Optional[str]

@dataclass
class AvatarCapabilities:
    """Capacidades del avatar en el mundo virtual"""
    movement_speed: float  # 0.1 - 3.0
    interaction_range: float  # metros
    communication_range: float
    special_abilities: List[str]
    permissions: List[str]
    energy_level: float
    intelligence_level: float

@dataclass
class AvatarBehavior:
    """Comportamiento y personalidad del avatar"""
    personality_traits: Dict[str, float]  # extroversion, friendliness, etc.
    preferred_activities: List[str]
    social_preferences: Dict[str, Any]
    learning_rate: float
    adaptation_speed: float
    
    # Comportamientos automáticos
    auto_responses: Dict[str, str]
    gesture_frequency: float
    expression_variety: float

class VirtualAvatar:
    """Clase principal para avatares virtuales"""
    
    def __init__(self, user_id: str, config: Dict[str, Any]):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.name = config.get("name", f"Avatar-{self.id[:8]}")
        self.avatar_type = AvatarType(config.get("type", "humanoid"))
        self.style = AvatarStyle(config.get("style", "realistic"))
        
        # Configuración de apariencia
        self.appearance = self._generate_appearance(config.get("appearance", {}))
        
        # Capacidades
        self.capabilities = self._generate_capabilities(config.get("capabilities", {}))
        
        # Comportamiento
        self.behavior = self._generate_behavior(config.get("behavior", {}))
        
        # Estado actual
        self.position = {
            "x": config.get("x", 0.0),
            "y": config.get("y", 0.0), 
            "z": config.get("z", 0.0)
        }
        self.rotation = {
            "x": 0.0, "y": 0.0, "z": 0.0
        }
        self.current_animation = "idle"
        self.is_active = True
        self.last_activity = datetime.now()
        
        # Interacciones y experiencia
        self.interactions_count = 0
        self.experience_points = 0
        self.level = 1
        self.achievements = []
        self.friends_list = []
        self.visited_locations = []
        
        # Personalization learning
        self.preference_data = {}
        self.usage_patterns = {}
        
        logger.info(f"Avatar {self.name} creado para usuario {user_id}")
    
    def _generate_appearance(self, config: Dict[str, Any]) -> AvatarAppearance:
        """Generar configuración de apariencia"""
        
        # Valores por defecto basados en el tipo de avatar
        defaults = self._get_default_appearance_for_type(self.avatar_type)
        
        # Aplicar configuración personalizada
        appearance_config = {**defaults, **config}
        
        return AvatarAppearance(
            height=appearance_config.get("height", 1.75),
            body_type=appearance_config.get("body_type", "athletic"),
            primary_color=appearance_config.get("primary_color", "#4A90E2"),
            secondary_color=appearance_config.get("secondary_color", "#7ED321"),
            accent_color=appearance_config.get("accent_color", "#F5A623"),
            head_shape=appearance_config.get("head_shape", "oval"),
            eye_type=appearance_config.get("eye_type", "normal"),
            eye_color=appearance_config.get("eye_color", "#2E86AB"),
            accessories=appearance_config.get("accessories", []),
            clothing=appearance_config.get("clothing", ["basic_outfit"]),
            glow_effect=appearance_config.get("glow_effect", False),
            particle_effects=appearance_config.get("particle_effects", []),
            aura_color=appearance_config.get("aura_color")
        )
    
    def _get_default_appearance_for_type(self, avatar_type: AvatarType) -> Dict[str, Any]:
        """Obtener apariencia por defecto según el tipo"""
        defaults = {
            AvatarType.HUMANOID: {
                "height": 1.75,
                "body_type": "athletic",
                "primary_color": "#FFE4C4",
                "secondary_color": "#8B4513",
                "head_shape": "oval",
                "eye_type": "human",
                "accessories": ["casual_clothes"],
                "glow_effect": False
            },
            AvatarType.ROBOTIC: {
                "height": 1.80,
                "body_type": "mechanical",
                "primary_color": "#708090",
                "secondary_color": "#4169E1",
                "head_shape": "angular",
                "eye_type": "led",
                "accessories": ["armor_plating", "led_strips"],
                "glow_effect": True,
                "particle_effects": ["energy_sparks"]
            },
            AvatarType.ABSTRACT: {
                "height": 1.50,
                "body_type": "geometric",
                "primary_color": "#FF69B4",
                "secondary_color": "#00CED1",
                "head_shape": "geometric",
                "eye_type": "glowing_orbs",
                "accessories": ["floating_elements"],
                "glow_effect": True,
                "particle_effects": ["color_trails", "geometric_patterns"]
            },
            AvatarType.CREATURE: {
                "height": 1.65,
                "body_type": "organic",
                "primary_color": "#32CD32",
                "secondary_color": "#228B22",
                "head_shape": "unique",
                "eye_type": "creature",
                "accessories": ["natural_features"],
                "glow_effect": False,
                "particle_effects": ["nature_effects"]
            },
            AvatarType.HYBRID: {
                "height": 1.70,
                "body_type": "mixed",
                "primary_color": "#8A2BE2",
                "secondary_color": "#FF1493",
                "head_shape": "custom",
                "eye_type": "hybrid",
                "accessories": ["tech_bio_fusion"],
                "glow_effect": True,
                "particle_effects": ["energy_bio_mix"]
            }
        }
        
        return defaults.get(avatar_type, defaults[AvatarType.HUMANOID])
    
    def _generate_capabilities(self, config: Dict[str, Any]) -> AvatarCapabilities:
        """Generar capacidades del avatar"""
        base_capabilities = self._get_base_capabilities_for_type(self.avatar_type)
        
        # Aplicar configuración personalizada
        capabilities_config = {**base_capabilities, **config}
        
        return AvatarCapabilities(
            movement_speed=capabilities_config.get("movement_speed", 1.0),
            interaction_range=capabilities_config.get("interaction_range", 2.0),
            communication_range=capabilities_config.get("communication_range", 10.0),
            special_abilities=capabilities_config.get("special_abilities", []),
            permissions=capabilities_config.get("permissions", ["basic_interaction"]),
            energy_level=capabilities_config.get("energy_level", 100.0),
            intelligence_level=capabilities_config.get("intelligence_level", 1.0)
        )
    
    def _get_base_capabilities_for_type(self, avatar_type: AvatarType) -> Dict[str, Any]:
        """Obtener capacidades base según el tipo"""
        capabilities = {
            AvatarType.HUMANOID: {
                "movement_speed": 1.0,
                "interaction_range": 1.5,
                "communication_range": 10.0,
                "special_abilities": ["human_gestures", "emotional_expressions"],
                "permissions": ["basic_interaction", "social_features"]
            },
            AvatarType.ROBOTIC: {
                "movement_speed": 1.5,
                "interaction_range": 3.0,
                "communication_range": 50.0,
                "special_abilities": ["data_analysis", "system_interface", "enhanced_vision"],
                "permissions": ["basic_interaction", "tech_interface", "robot_communication"]
            },
            AvatarType.ABSTRACT: {
                "movement_speed": 2.0,
                "interaction_range": 2.5,
                "communication_range": 25.0,
                "special_abilities": ["reality_manipulation", "visual_effects", "dimension_shift"],
                "permissions": ["basic_interaction", "creative_tools", "reality_effects"]
            },
            AvatarType.CREATURE: {
                "movement_speed": 1.3,
                "interaction_range": 2.0,
                "communication_range": 15.0,
                "special_abilities": ["nature_connection", "environmental_adaptation", "unique_senses"],
                "permissions": ["basic_interaction", "nature_interface", "creature_communication"]
            },
            AvatarType.HYBRID: {
                "movement_speed": 1.7,
                "interaction_range": 2.5,
                "communication_range": 30.0,
                "special_abilities": ["adaptive_features", "multi_mode_interaction", "enhanced_learning"],
                "permissions": ["basic_interaction", "advanced_features", "cross_system_access"]
            }
        }
        
        return capabilities.get(avatar_type, capabilities[AvatarType.HUMANOID])
    
    def _generate_behavior(self, config: Dict[str, Any]) -> AvatarBehavior:
        """Generar comportamiento del avatar"""
        
        # Rasgos de personalidad por defecto
        default_traits = {
            "extroversion": 0.5,
            "friendliness": 0.7,
            "curiosity": 0.6,
            "creativity": 0.5,
            "assertiveness": 0.4,
            "empathy": 0.6,
            "adventurousness": 0.5,
            "patience": 0.6
        }
        
        # Aplicar variaciones aleatorias y configuración personal
        personality_traits = {}
        for trait, default_value in default_traits.items():
            variation = random.uniform(-0.2, 0.2)
            custom_value = config.get("personality_traits", {}).get(trait)
            
            if custom_value is not None:
                personality_traits[trait] = max(0.0, min(1.0, custom_value))
            else:
                personality_traits[trait] = max(0.0, min(1.0, default_value + variation))
        
        return AvatarBehavior(
            personality_traits=personality_traits,
            preferred_activities=config.get("preferred_activities", ["exploration", "socializing"]),
            social_preferences=config.get("social_preferences", {
                "group_size_preference": "small",
                "communication_style": "friendly",
                "interaction_frequency": "moderate"
            }),
            learning_rate=config.get("learning_rate", 0.1),
            adaptation_speed=config.get("adaptation_speed", 0.05),
            auto_responses=config.get("auto_responses", {
                "greeting": "Hello there!",
                "farewell": "See you later!",
                "thanks": "You're welcome!",
                "confused": "I'm not sure I understand..."
            }),
            gesture_frequency=config.get("gesture_frequency", 0.3),
            expression_variety=config.get("expression_variety", 0.7)
        )
    
    async def update_position(self, new_position: Dict[str, float]):
        """Actualizar posición del avatar"""
        old_position = self.position.copy()
        
        # Validar límites de movimiento
        max_speed = self.capabilities.movement_speed * 5.0  # metros por segundo
        
        distance = np.sqrt(
            (new_position["x"] - old_position["x"])**2 +
            (new_position["y"] - old_position["y"])**2 +
            (new_position["z"] - old_position["z"])**2
        )
        
        if distance <= max_speed:
            self.position = new_position
            self.last_activity = datetime.now()
            
            # Añadir ubicación a lugares visitados
            location_key = f"{int(new_position['x']/10)},{int(new_position['z']/10)}"
            if location_key not in self.visited_locations:
                self.visited_locations.append(location_key)
            
            return True
        else:
            logger.warning(f"Movimiento demasiado rápido para avatar {self.name}: {distance:.2f}m")
            return False
    
    async def interact_with_object(self, object_id: str, interaction_type: str) -> Dict[str, Any]:
        """Interactuar con un objeto en el mundo virtual"""
        self.interactions_count += 1
        self.last_activity = datetime.now()
        
        # Ganar experiencia por interacción
        self.experience_points += 10
        await self._check_level_up()
        
        # Aprender preferencias
        self._learn_interaction_preference(object_id, interaction_type)
        
        return {
            "success": True,
            "interaction_id": str(uuid.uuid4()),
            "object_id": object_id,
            "interaction_type": interaction_type,
            "avatar_response": await self._generate_interaction_response(interaction_type),
            "experience_gained": 10
        }
    
    async def interact_with_avatar(self, other_avatar_id: str, interaction_type: str) -> Dict[str, Any]:
        """Interactuar con otro avatar"""
        self.interactions_count += 1
        self.last_activity = datetime.now()
        
        # Ganar más experiencia por interacciones sociales
        exp_gained = 15
        self.experience_points += exp_gained
        await self._check_level_up()
        
        # Posible nueva amistad
        if other_avatar_id not in self.friends_list and random.random() < 0.1:
            self.friends_list.append(other_avatar_id)
            exp_gained += 25
            self.experience_points += 25
        
        return {
            "success": True,
            "interaction_id": str(uuid.uuid4()),
            "other_avatar_id": other_avatar_id,
            "interaction_type": interaction_type,
            "avatar_response": await self._generate_social_response(interaction_type),
            "experience_gained": exp_gained,
            "new_friendship": other_avatar_id in self.friends_list
        }
    
    def _learn_interaction_preference(self, object_id: str, interaction_type: str):
        """Aprender preferencias de interacción"""
        if object_id not in self.preference_data:
            self.preference_data[object_id] = {}
        
        if interaction_type not in self.preference_data[object_id]:
            self.preference_data[object_id][interaction_type] = 0
        
        self.preference_data[object_id][interaction_type] += 1
    
    async def _generate_interaction_response(self, interaction_type: str) -> str:
        """Generar respuesta de interacción basada en personalidad"""
        responses = {
            "examine": [
                "Interesting...", "Let me take a closer look.", "This is fascinating!",
                "I wonder what this does.", "Hmm, curious."
            ],
            "use": [
                "Let's try this!", "Here goes nothing!", "This should work.",
                "Perfect!", "Exactly what I needed."
            ],
            "collect": [
                "This might be useful later.", "Added to my collection!",
                "Nice find!", "I'll keep this.", "Good catch!"
            ]
        }
        
        available_responses = responses.get(interaction_type, ["Interesting interaction."])
        
        # Modificar respuesta basada en personalidad
        if self.behavior.personality_traits["curiosity"] > 0.7:
            available_responses.extend([
                "I need to understand this better!", "What secrets does this hold?",
                "There's more to this than meets the eye!"
            ])
        
        if self.behavior.personality_traits["enthusiasm"] > 0.7:
            available_responses = [response + "!" for response in available_responses]
        
        return random.choice(available_responses)
    
    async def _generate_social_response(self, interaction_type: str) -> str:
        """Generar respuesta social basada en personalidad"""
        base_responses = {
            "greeting": ["Hello!", "Hi there!", "Good to see you!", "Hey!"],
            "conversation": ["That's interesting!", "Tell me more!", "I see!", "Really?"],
            "collaboration": ["Let's work together!", "Great idea!", "I can help with that!"],
            "farewell": ["See you later!", "Goodbye!", "Take care!", "Until next time!"]
        }
        
        responses = base_responses.get(interaction_type, ["Nice to interact with you!"])
        
        # Personalizar basado en rasgos
        friendliness = self.behavior.personality_traits["friendliness"]
        extroversion = self.behavior.personality_traits["extroversion"]
        
        if friendliness > 0.8:
            responses = [f"{response} It's wonderful to meet you!" for response in responses]
        elif friendliness < 0.3:
            responses = [response.lower() for response in responses]  # Más reservado
        
        if extroversion > 0.8:
            responses.extend([
                "I love meeting new people!", "This is so exciting!",
                "We should definitely hang out more!"
            ])
        
        return random.choice(responses)
    
    async def _check_level_up(self):
        """Verificar si el avatar sube de nivel"""
        required_exp = self.level * 100  # Experiencia requerida aumenta con el nivel
        
        if self.experience_points >= required_exp:
            self.level += 1
            self.experience_points -= required_exp
            
            # Mejorar capacidades al subir de nivel
            await self._apply_level_up_bonuses()
            
            logger.info(f"Avatar {self.name} subió al nivel {self.level}!")
    
    async def _apply_level_up_bonuses(self):
        """Aplicar bonificaciones por subir de nivel"""
        # Pequeñas mejoras en capacidades
        self.capabilities.energy_level = min(150.0, self.capabilities.energy_level + 5.0)
        self.capabilities.interaction_range = min(5.0, self.capabilities.interaction_range + 0.1)
        self.capabilities.intelligence_level = min(2.0, self.capabilities.intelligence_level + 0.05)
        
        # Desbloquear nuevas habilidades cada ciertos niveles
        if self.level % 5 == 0:
            new_abilities = self._get_level_abilities(self.level)
            for ability in new_abilities:
                if ability not in self.capabilities.special_abilities:
                    self.capabilities.special_abilities.append(ability)
        
        # Logro por nivel
        level_achievement = f"level_{self.level}"
        if level_achievement not in self.achievements:
            self.achievements.append(level_achievement)
    
    def _get_level_abilities(self, level: int) -> List[str]:
        """Obtener habilidades desbloqueables por nivel"""
        abilities_by_level = {
            5: ["enhanced_interaction"],
            10: ["group_leadership"],
            15: ["creative_expression"],
            20: ["advanced_communication"],
            25: ["reality_influence"],
            30: ["master_socializer"]
        }
        
        return abilities_by_level.get(level, [])
    
    async def customize_appearance(self, updates: Dict[str, Any]) -> bool:
        """Personalizar apariencia del avatar"""
        try:
            # Validar actualizaciones
            valid_updates = {}
            
            appearance_fields = asdict(self.appearance).keys()
            for field, value in updates.items():
                if field in appearance_fields:
                    valid_updates[field] = value
            
            # Aplicar actualizaciones
            for field, value in valid_updates.items():
                setattr(self.appearance, field, value)
            
            self.last_activity = datetime.now()
            
            logger.info(f"Avatar {self.name} personalización actualizada: {list(valid_updates.keys())}")
            return True
            
        except Exception as e:
            logger.error(f"Error personalizando avatar {self.name}: {e}")
            return False
    
    async def learn_from_interaction(self, interaction_data: Dict[str, Any]):
        """Aprender y adaptarse de las interacciones"""
        interaction_type = interaction_data.get("type")
        success = interaction_data.get("success", True)
        user_feedback = interaction_data.get("user_feedback")
        
        # Ajustar comportamiento basado en feedback
        if user_feedback:
            await self._process_user_feedback(user_feedback)
        
        # Ajustar preferencias de actividad
        if success and interaction_type:
            if interaction_type not in self.behavior.preferred_activities:
                # Chance de añadir nueva actividad preferida
                if random.random() < self.behavior.learning_rate:
                    self.behavior.preferred_activities.append(interaction_type)
        
        # Evolucionar personalidad lentamente
        await self._evolve_personality(interaction_data)
    
    async def _process_user_feedback(self, feedback: str):
        """Procesar feedback del usuario para mejorar comportamiento"""
        positive_keywords = ["good", "great", "nice", "love", "awesome", "perfect"]
        negative_keywords = ["bad", "annoying", "stop", "wrong", "hate", "terrible"]
        
        feedback_lower = feedback.lower()
        
        # Ajustar rasgos de personalidad basado en feedback
        if any(word in feedback_lower for word in positive_keywords):
            # Reforzar comportamientos actuales
            for trait in self.behavior.personality_traits:
                current_value = self.behavior.personality_traits[trait]
                adjustment = self.behavior.learning_rate * 0.1
                self.behavior.personality_traits[trait] = min(1.0, current_value + adjustment)
        
        elif any(word in feedback_lower for word in negative_keywords):
            # Moderar comportamientos
            for trait in ["assertiveness", "extroversion"]:
                if trait in self.behavior.personality_traits:
                    current_value = self.behavior.personality_traits[trait]
                    adjustment = self.behavior.learning_rate * 0.1
                    self.behavior.personality_traits[trait] = max(0.0, current_value - adjustment)
    
    async def _evolve_personality(self, interaction_data: Dict[str, Any]):
        """Evolucionar personalidad gradualmente basada en experiencias"""
        if random.random() < self.behavior.adaptation_speed:
            # Pequeños cambios aleatorios en personalidad
            trait_to_modify = random.choice(list(self.behavior.personality_traits.keys()))
            current_value = self.behavior.personality_traits[trait_to_modify]
            
            # Cambio muy pequeño
            change = random.uniform(-0.01, 0.01)
            new_value = max(0.0, min(1.0, current_value + change))
            
            self.behavior.personality_traits[trait_to_modify] = new_value
    
    def get_avatar_status(self) -> Dict[str, Any]:
        """Obtener estado completo del avatar"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "type": self.avatar_type.value,
            "style": self.style.value,
            "level": self.level,
            "experience_points": self.experience_points,
            "position": self.position,
            "rotation": self.rotation,
            "current_animation": self.current_animation,
            "is_active": self.is_active,
            "last_activity": self.last_activity.isoformat(),
            "interactions_count": self.interactions_count,
            "friends_count": len(self.friends_list),
            "achievements_count": len(self.achievements),
            "locations_visited": len(self.visited_locations),
            "capabilities": asdict(self.capabilities),
            "personality_summary": self._get_personality_summary()
        }
    
    def _get_personality_summary(self) -> Dict[str, str]:
        """Obtener resumen de personalidad"""
        traits = self.behavior.personality_traits
        
        summary = {}
        for trait, value in traits.items():
            if value >= 0.8:
                summary[trait] = "very high"
            elif value >= 0.6:
                summary[trait] = "high"
            elif value >= 0.4:
                summary[trait] = "moderate"
            elif value >= 0.2:
                summary[trait] = "low"
            else:
                summary[trait] = "very low"
        
        return summary
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir avatar a diccionario completo"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "type": self.avatar_type.value,
            "style": self.style.value,
            "appearance": asdict(self.appearance),
            "capabilities": asdict(self.capabilities),
            "behavior": asdict(self.behavior),
            "status": self.get_avatar_status(),
            "created_at": self.last_activity.isoformat()  # Placeholder for creation time
        }