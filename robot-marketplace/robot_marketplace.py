"""
Sistema de Marketplace de Robots - Ciudad Robot Metaverso
Compra y venta de robots personalizados
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import uuid
import random

class RobotTier(Enum):
    """Niveles/Tiers de robots"""
    STARTER = "starter"        # Nivel 1-10, 500-2000 ROBOT
    ADVANCED = "advanced"      # Nivel 10-50, 2000-10000 ROBOT
    PROFESSIONAL = "professional"  # Nivel 50-100, 10000-50000 ROBOT
    LEGENDARY = "legendary"    # Nivel 100+, 50000+ ROBOT

class RobotModel(Enum):
    """Modelos de robots disponibles"""
    DEFENDER = "defender"
    SPEEDSTER = "speedster"
    TANK = "tank"
    SNIPER = "sniper"
    PALADIN = "paladin"
    SHADOW = "shadow"
    TITAN = "titan"
    PHOENIX = "phoenix"
    CYBORG = "cyborg"
    ANDROID = "android"

class RobotSpecialization(Enum):
    """Especializaciones de robots"""
    COMBAT = "combat"
    SPEED = "speed"
    DEFENSE = "defense"
    BALANCE = "balance"
    INTELLIGENCE = "intelligence"
    STRENGTH = "strength"

class Robot:
    """Robot vendible en el marketplace"""
    def __init__(self, model: RobotModel, tier: RobotTier, specialization: RobotSpecialization):
        self.robot_id = str(uuid.uuid4())
        self.model = model
        self.tier = tier
        self.specialization = specialization
        self.name = f"{model.value.capitalize()} - {tier.value.upper()}"
        self.level = self._calculate_level()
        self.experience = 0
        self.price = self._calculate_price()
        
        # Stats iniciales
        self.attack = self._generate_stat("attack")
        self.defense = self._generate_stat("defense")
        self.speed = self._generate_stat("speed")
        self.intelligence = self._generate_stat("intelligence")
        self.health = self._generate_stat("health")
        self.energy = 100
        
        # Customización
        self.color_primary = self._random_color()
        self.color_secondary = self._random_color()
        self.skin_texture = random.choice(["metallic", "carbon", "crystal", "organic"])
        self.custom_name = ""
        self.owner_id: Optional[str] = None
        self.purchase_date: Optional[datetime] = None
        self.special_abilities: List[str] = self._generate_abilities()
        
    def _calculate_level(self) -> int:
        """Calcula nivel base del robot"""
        level_map = {
            RobotTier.STARTER: random.randint(1, 10),
            RobotTier.ADVANCED: random.randint(10, 50),
            RobotTier.PROFESSIONAL: random.randint(50, 100),
            RobotTier.LEGENDARY: random.randint(100, 150)
        }
        return level_map.get(self.tier, 1)
    
    def _calculate_price(self) -> float:
        """Calcula precio en ROBOT tokens"""
        tier_prices = {
            RobotTier.STARTER: random.randint(500, 2000),
            RobotTier.ADVANCED: random.randint(2000, 10000),
            RobotTier.PROFESSIONAL: random.randint(10000, 50000),
            RobotTier.LEGENDARY: random.randint(50000, 200000)
        }
        base_price = tier_prices.get(self.tier, 500)
        
        # Variación por modelo
        model_multiplier = {
            RobotModel.DEFENDER: 1.0,
            RobotModel.SPEEDSTER: 1.1,
            RobotModel.TANK: 1.2,
            RobotModel.SNIPER: 1.15,
            RobotModel.PALADIN: 1.3,
            RobotModel.SHADOW: 1.25,
            RobotModel.TITAN: 1.5,
            RobotModel.PHOENIX: 1.4,
            RobotModel.CYBORG: 1.35,
            RobotModel.ANDROID: 1.2
        }
        
        return int(base_price * model_multiplier.get(self.model, 1.0))
    
    def _generate_stat(self, stat_type: str) -> int:
        """Genera stat del robot"""
        base_stats = {
            "attack": (30, 100),
            "defense": (20, 80),
            "speed": (25, 90),
            "intelligence": (30, 100),
            "health": (50, 150)
        }
        
        min_val, max_val = base_stats.get(stat_type, (20, 80))
        return random.randint(min_val, max_val)
    
    def _random_color(self) -> str:
        """Color aleatorio"""
        colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", 
                  "#00FFFF", "#FFA500", "#800080", "#FFC0CB", "#A52A2A"]
        return random.choice(colors)
    
    def _generate_abilities(self) -> List[str]:
        """Genera habilidades especiales"""
        abilities_map = {
            RobotSpecialization.COMBAT: ["Power Strike", "Combo Attack", "Battle Rage"],
            RobotSpecialization.SPEED: ["Dash", "Sprint", "Lightning Speed"],
            RobotSpecialization.DEFENSE: ["Shield Wall", "Barrier", "Protective Aura"],
            RobotSpecialization.BALANCE: ["Equilibrium", "Balanced Strike", "Harmony"],
            RobotSpecialization.INTELLIGENCE: ["Analysis", "Hack", "Data Breach"],
            RobotSpecialization.STRENGTH: ["Heavy Impact", "Crush", "Titan Punch"]
        }
        
        abilities = abilities_map.get(self.specialization, ["Basic Attack"])
        return random.sample(abilities, k=min(3, len(abilities)))
    
    def customize(self, custom_name: str = "", color_primary: str = "", 
                  color_secondary: str = "", skin_texture: str = "") -> Dict:
        """Personaliza el robot"""
        if custom_name:
            self.custom_name = custom_name
        if color_primary:
            self.color_primary = color_primary
        if color_secondary:
            self.color_secondary = color_secondary
        if skin_texture:
            self.skin_texture = skin_texture
        
        return {
            "success": True,
            "robot_id": self.robot_id,
            "customization": {
                "name": self.custom_name or self.name,
                "color_primary": self.color_primary,
                "color_secondary": self.color_secondary,
                "skin_texture": self.skin_texture
            }
        }
    
    def purchase(self, player_id: str) -> Dict:
        """Marca robot como comprado"""
        self.owner_id = player_id
        self.purchase_date = datetime.now()
        
        return {
            "success": True,
            "robot": self.to_dict(),
            "purchase_date": self.purchase_date.isoformat()
        }
    
    def to_dict(self) -> Dict:
        return {
            "robot_id": self.robot_id,
            "model": self.model.value,
            "tier": self.tier.value,
            "specialization": self.specialization.value,
            "name": self.custom_name or self.name,
            "level": self.level,
            "experience": self.experience,
            "price": self.price,
            "stats": {
                "attack": self.attack,
                "defense": self.defense,
                "speed": self.speed,
                "intelligence": self.intelligence,
                "health": self.health,
                "energy": self.energy
            },
            "appearance": {
                "color_primary": self.color_primary,
                "color_secondary": self.color_secondary,
                "skin_texture": self.skin_texture
            },
            "special_abilities": self.special_abilities,
            "owner_id": self.owner_id,
            "purchase_date": self.purchase_date.isoformat() if self.purchase_date else None
        }

class RobotMarketplace:
    """Marketplace central de robots"""
    def __init__(self):
        self.inventory: Dict[str, Robot] = {}
        self.player_robots: Dict[str, List[str]] = {}  # player_id -> [robot_ids]
        self.total_sales = 0
        self.total_revenue = 0.0
        self._initialize_inventory()
    
    def _initialize_inventory(self):
        """Inicializa inventario con robots iniciales"""
        # 3 robots de cada tier
        for tier in RobotTier:
            for _ in range(3):
                for model in random.sample(list(RobotModel), k=3):
                    specialization = random.choice(list(RobotSpecialization))
                    robot = Robot(model, tier, specialization)
                    self.inventory[robot.robot_id] = robot
    
    def get_robot(self, robot_id: str) -> Optional[Robot]:
        """Obtiene robot por ID"""
        return self.inventory.get(robot_id)
    
    def get_available_robots(self, 
                            tier: Optional[RobotTier] = None,
                            model: Optional[RobotModel] = None,
                            specialization: Optional[RobotSpecialization] = None,
                            max_price: Optional[float] = None) -> List[Robot]:
        """Obtiene robots disponibles con filtros"""
        available = [r for r in self.inventory.values() if r.owner_id is None]
        
        if tier:
            available = [r for r in available if r.tier == tier]
        if model:
            available = [r for r in available if r.model == model]
        if specialization:
            available = [r for r in available if r.specialization == specialization]
        if max_price:
            available = [r for r in available if r.price <= max_price]
        
        return available
    
    def get_player_robots(self, player_id: str) -> List[Robot]:
        """Obtiene robots del jugador"""
        robot_ids = self.player_robots.get(player_id, [])
        return [self.inventory.get(rid) for rid in robot_ids if rid in self.inventory]
    
    def purchase_robot(self, player_id: str, robot_id: str) -> Dict:
        """Compra un robot"""
        robot = self.get_robot(robot_id)
        
        if not robot:
            return {"error": "Robot no encontrado"}
        
        if robot.owner_id is not None:
            return {"error": "Robot ya fue comprado"}
        
        # Registrar compra
        robot.purchase(player_id)
        
        if player_id not in self.player_robots:
            self.player_robots[player_id] = []
        
        self.player_robots[player_id].append(robot_id)
        self.total_sales += 1
        self.total_revenue += robot.price
        
        return {
            "success": True,
            "message": "Robot comprado exitosamente",
            "robot": robot.to_dict(),
            "price": robot.price
        }
    
    def customize_robot(self, player_id: str, robot_id: str,
                       custom_name: str = "", color_primary: str = "",
                       color_secondary: str = "", skin_texture: str = "") -> Dict:
        """Personaliza un robot del jugador"""
        robot = self.get_robot(robot_id)
        
        if not robot:
            return {"error": "Robot no encontrado"}
        
        if robot.owner_id != player_id:
            return {"error": "No eres dueño de este robot"}
        
        return robot.customize(custom_name, color_primary, color_secondary, skin_texture)
    
    def sell_robot(self, player_id: str, robot_id: str, price: float) -> Dict:
        """Vende robot a otro jugador (entre jugadores)"""
        robot = self.get_robot(robot_id)
        
        if not robot:
            return {"error": "Robot no encontrado"}
        
        if robot.owner_id != player_id:
            return {"error": "No eres dueño de este robot"}
        
        # Crear listado de venta
        return {
            "success": True,
            "robot_id": robot_id,
            "seller_id": player_id,
            "asking_price": price,
            "robot_details": robot.to_dict()
        }
    
    def get_marketplace_stats(self) -> Dict:
        """Estadísticas del marketplace"""
        available_count = len([r for r in self.inventory.values() if r.owner_id is None])
        sold_count = len([r for r in self.inventory.values() if r.owner_id is not None])
        
        return {
            "total_robots_available": available_count,
            "total_robots_sold": sold_count,
            "total_sales": self.total_sales,
            "total_revenue": round(self.total_revenue, 2),
            "average_price": round(self.total_revenue / max(1, self.total_sales), 2),
            "total_players": len(self.player_robots)
        }

# Instancia global
robot_marketplace = RobotMarketplace()
