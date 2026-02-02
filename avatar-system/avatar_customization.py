"""
Sistema Avanzado de Avatares - Ciudad Robot Metaverso
Creación y personalización completa de avatares de usuario
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import uuid
import random

class Gender(Enum):
    """Género del avatar"""
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non_binary"
    ANDROID = "android"

class AvatarRace(Enum):
    """Raza/tipo de avatar"""
    HUMAN = "human"
    CYBORG = "cyborg"
    ANDROID = "android"
    ALIEN = "alien"
    HOLOGRAM = "hologram"
    HYBRID = "hybrid"

class AvatarClass(Enum):
    """Clase del avatar"""
    WARRIOR = "warrior"
    MAGE = "mage"
    ROGUE = "rogue"
    PALADIN = "paladin"
    RANGER = "ranger"
    SCIENTIST = "scientist"
    HACKER = "hacker"
    ENTREPRENEUR = "entrepreneur"

class BodyPart(Enum):
    """Partes del cuerpo customizables"""
    HEAD = "head"
    TORSO = "torso"
    ARMS = "arms"
    LEGS = "legs"
    HANDS = "hands"
    FEET = "feet"
    EYES = "eyes"
    HAIR = "hair"
    SKIN = "skin"
    ACCESSORIES = "accessories"

class Accessory(Enum):
    """Accesorios para avatares"""
    HELMET = "helmet"
    GLASSES = "glasses"
    HAT = "hat"
    CAPE = "cape"
    WINGS = "wings"
    AURA = "aura"
    CROWN = "crown"
    HALO = "halo"
    MASK = "mask"
    EARRINGS = "earrings"

class Avatar:
    """Avatar personalizable del jugador"""
    def __init__(self, player_id: str, display_name: str):
        self.avatar_id = str(uuid.uuid4())
        self.player_id = player_id
        self.display_name = display_name
        self.creation_date = datetime.now()
        self.last_modified = datetime.now()
        
        # Características base
        self.gender = Gender.ANDROID
        self.race = AvatarRace.CYBORG
        self.avatar_class = AvatarClass.ENTREPRENEUR
        self.level = 1
        self.experience = 0
        
        # Apariencia
        self.customization: Dict[str, str] = self._initialize_appearance()
        self.accessories: List[Accessory] = []
        self.emotes: List[str] = ["wave", "dance", "salute"]
        self.voice_settings = {
            "pitch": 1.0,  # 0.5 - 2.0
            "accent": "neutral",
            "language": "english"
        }
        
        # Stats
        self.stats = {
            "charisma": 50,
            "intelligence": 50,
            "creativity": 50,
            "social": 50,
            "leadership": 50
        }
        
        # Social
        self.friends: List[str] = []
        self.followers: List[str] = []
        self.bio = ""
        self.status = "online"
        self.last_online = datetime.now()
        
        # Cosmética
        self.skins_owned: List[str] = []
        self.emotes_owned: List[str] = ["wave", "dance", "salute"]
        self.pets: List[Dict] = []
        self.active_pet_id: Optional[str] = None
        self.premium_cosmetics: List[str] = []
        
    def _initialize_appearance(self) -> Dict[str, str]:
        """Inicializa apariencia por defecto"""
        return {
            "head": self._random_color(),
            "torso": self._random_color(),
            "arms": self._random_color(),
            "legs": self._random_color(),
            "hands": self._random_color(),
            "feet": self._random_color(),
            "eye_color": random.choice(["blue", "green", "brown", "amber", "purple", "red"]),
            "hair_style": random.choice(["short", "long", "bald", "spiky", "curly", "wavy"]),
            "hair_color": self._random_color(),
            "skin_tone": random.choice(["pale", "light", "tan", "dark", "gray", "metallic"]),
            "facial_hair": random.choice(["none", "beard", "stubble", "mustache"]),
            "body_build": random.choice(["slim", "athletic", "muscular", "curvy", "average"])
        }
    
    def _random_color(self) -> str:
        """Genera color aleatorio"""
        colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", 
                  "#00FFFF", "#FFA500", "#800080", "#FFC0CB", "#A52A2A",
                  "#808080", "#FFFFFF", "#000000"]
        return random.choice(colors)
    
    def customize_appearance(self, **kwargs) -> Dict:
        """Personaliza apariencia del avatar"""
        valid_parts = {
            "head", "torso", "arms", "legs", "hands", "feet",
            "eye_color", "hair_style", "hair_color", "skin_tone",
            "facial_hair", "body_build"
        }
        
        updated = {}
        for part, value in kwargs.items():
            if part in valid_parts:
                self.customization[part] = str(value)
                updated[part] = value
        
        self.last_modified = datetime.now()
        
        return {
            "success": True,
            "avatar_id": self.avatar_id,
            "updated_parts": updated,
            "appearance": self.customization
        }
    
    def add_accessory(self, accessory: Accessory, color: str = "", style: str = "") -> Dict:
        """Añade accesorio al avatar"""
        if accessory not in self.accessories:
            self.accessories.append(accessory)
            
            return {
                "success": True,
                "accessory": accessory.value,
                "total_accessories": len(self.accessories)
            }
        
        return {"error": "Accesorio ya equipado"}
    
    def remove_accessory(self, accessory: Accessory) -> bool:
        """Remueve accesorio"""
        if accessory in self.accessories:
            self.accessories.remove(accessory)
            return True
        return False
    
    def add_friend(self, friend_id: str) -> bool:
        """Añade amigo"""
        if friend_id not in self.friends:
            self.friends.append(friend_id)
            return True
        return False
    
    def add_follower(self, follower_id: str) -> bool:
        """Añade seguidor"""
        if follower_id not in self.followers:
            self.followers.append(follower_id)
            return True
        return False
    
    def adopt_pet(self, pet_name: str, pet_type: str) -> Dict:
        """Adopta mascota virtual"""
        pet = {
            "pet_id": str(uuid.uuid4()),
            "name": pet_name,
            "type": pet_type,
            "level": 1,
            "happiness": 100,
            "energy": 100,
            "adopted_date": datetime.now().isoformat()
        }
        
        self.pets.append(pet)
        if self.active_pet_id is None:
            self.active_pet_id = pet["pet_id"]
        
        return {
            "success": True,
            "pet": pet
        }
    
    def unlock_emote(self, emote: str) -> Dict:
        """Desbloquea nuevo emote"""
        if emote not in self.emotes_owned:
            self.emotes_owned.append(emote)
            return {"success": True, "emote": emote}
        return {"error": "Emote ya desbloqueado"}
    
    def purchase_skin(self, skin_name: str, cost: float) -> Dict:
        """Compra skin cosmético"""
        if skin_name not in self.skins_owned:
            self.skins_owned.append(skin_name)
            return {
                "success": True,
                "skin": skin_name,
                "cost": cost,
                "total_skins": len(self.skins_owned)
            }
        return {"error": "Skin ya posee"}
    
    def update_stats(self, stat_name: str, increase: int) -> Dict:
        """Actualiza stats del avatar"""
        if stat_name in self.stats:
            old_value = self.stats[stat_name]
            self.stats[stat_name] = min(100, self.stats[stat_name] + increase)
            return {
                "success": True,
                "stat": stat_name,
                "old_value": old_value,
                "new_value": self.stats[stat_name]
            }
        return {"error": "Stat no válido"}
    
    def to_dict(self) -> Dict:
        return {
            "avatar_id": self.avatar_id,
            "player_id": self.player_id,
            "display_name": self.display_name,
            "creation_date": self.creation_date.isoformat(),
            "last_modified": self.last_modified.isoformat(),
            "characteristics": {
                "gender": self.gender.value,
                "race": self.race.value,
                "class": self.avatar_class.value,
                "level": self.level
            },
            "appearance": self.customization,
            "accessories": [a.value for a in self.accessories],
            "stats": self.stats,
            "social": {
                "friends": len(self.friends),
                "followers": len(self.followers),
                "status": self.status,
                "bio": self.bio
            },
            "cosmetics": {
                "skins_owned": len(self.skins_owned),
                "emotes_owned": len(self.emotes_owned),
                "pets": len(self.pets),
                "active_pet": self.active_pet_id,
                "premium_items": len(self.premium_cosmetics)
            }
        }

class AvatarCreator:
    """Sistema de creación y gestión de avatares"""
    def __init__(self):
        self.avatars: Dict[str, Avatar] = {}  # avatar_id -> Avatar
        self.player_avatars: Dict[str, List[str]] = {}  # player_id -> [avatar_ids]
        self.total_avatars_created = 0
        self.cosmetic_shop: Dict[str, float] = self._initialize_shop()
    
    def _initialize_shop(self) -> Dict[str, float]:
        """Inicializa tienda de cosméticos"""
        return {
            "skin_neon": 500,
            "skin_hologram": 750,
            "skin_metallic": 600,
            "skin_crystal": 800,
            "emote_dance": 250,
            "emote_laugh": 250,
            "emote_facepalm": 200,
            "accessory_wings": 1000,
            "accessory_halo": 800,
            "accessory_crown": 1200,
            "pet_dragon": 2000,
            "pet_phoenix": 2500,
            "pet_robot": 1500
        }
    
    def create_avatar(self, player_id: str, display_name: str,
                     gender: Gender, race: AvatarRace, avatar_class: AvatarClass) -> Avatar:
        """Crea nuevo avatar"""
        avatar = Avatar(player_id, display_name)
        avatar.gender = gender
        avatar.race = race
        avatar.avatar_class = avatar_class
        
        self.avatars[avatar.avatar_id] = avatar
        
        if player_id not in self.player_avatars:
            self.player_avatars[player_id] = []
        
        self.player_avatars[player_id].append(avatar.avatar_id)
        self.total_avatars_created += 1
        
        return avatar
    
    def get_avatar(self, avatar_id: str) -> Optional[Avatar]:
        """Obtiene avatar por ID"""
        return self.avatars.get(avatar_id)
    
    def get_player_avatars(self, player_id: str) -> List[Avatar]:
        """Obtiene avatares del jugador"""
        avatar_ids = self.player_avatars.get(player_id, [])
        return [self.avatars.get(aid) for aid in avatar_ids if aid in self.avatars]
    
    def customize_avatar(self, avatar_id: str, **customization) -> Dict:
        """Personaliza avatar"""
        avatar = self.get_avatar(avatar_id)
        
        if not avatar:
            return {"error": "Avatar no encontrado"}
        
        return avatar.customize_appearance(**customization)
    
    def add_avatar_accessory(self, avatar_id: str, accessory: Accessory) -> Dict:
        """Añade accesorio a avatar"""
        avatar = self.get_avatar(avatar_id)
        
        if not avatar:
            return {"error": "Avatar no encontrado"}
        
        return avatar.add_accessory(accessory)
    
    def purchase_cosmetic(self, avatar_id: str, cosmetic_name: str) -> Dict:
        """Compra cosmético para avatar"""
        avatar = self.get_avatar(avatar_id)
        
        if not avatar:
            return {"error": "Avatar no encontrado"}
        
        if cosmetic_name not in self.cosmetic_shop:
            return {"error": "Cosmético no disponible"}
        
        price = self.cosmetic_shop[cosmetic_name]
        
        # Añadir a lista de premium
        avatar.premium_cosmetics.append(cosmetic_name)
        
        return {
            "success": True,
            "cosmetic": cosmetic_name,
            "price": price,
            "avatar_id": avatar_id,
            "total_premium_items": len(avatar.premium_cosmetics)
        }
    
    def get_cosmetic_shop(self) -> Dict:
        """Lista de cosméticos disponibles"""
        return {
            "skins": {k: v for k, v in self.cosmetic_shop.items() if "skin" in k},
            "emotes": {k: v for k, v in self.cosmetic_shop.items() if "emote" in k},
            "accessories": {k: v for k, v in self.cosmetic_shop.items() if "accessory" in k},
            "pets": {k: v for k, v in self.cosmetic_shop.items() if "pet" in k}
        }
    
    def get_global_stats(self) -> Dict:
        """Estadísticas globales"""
        return {
            "total_avatars": len(self.avatars),
            "total_players": len(self.player_avatars),
            "average_avatars_per_player": round(len(self.avatars) / max(1, len(self.player_avatars)), 2),
            "total_avatars_created": self.total_avatars_created
        }

# Instancia global
avatar_creator = AvatarCreator()
