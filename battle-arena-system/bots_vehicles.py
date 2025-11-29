"""
Sistema de Bots AI y Vehículos para Battle Arena
Integración con backend Python
"""

from dataclasses import dataclass
from typing import List, Dict
import random
import asyncio

@dataclass
class BotPlayer:
    """Representación de un bot en el servidor"""
    bot_id: str
    bot_type: str  # humanoid, terminator, combat_drone
    player_name: str
    skill_level: float
    health: float
    kills: int
    damage_dealt: float
    tokens_carried: float
    is_alive: bool
    current_vehicle: str = None

@dataclass
class Vehicle:
    """Vehículo en la arena"""
    vehicle_id: str
    vehicle_type: str  # combat_tank, armored_car, attack_drone, destroyer_mech, excavator
    health: float
    max_health: float
    driver: str = None  # player_id o bot_id
    passengers: List[str] = None
    position: tuple = (0, 0, 0)
    is_destroyed: bool = False

class BotAISystem:
    """Sistema de gestión de bots AI"""
    
    def __init__(self):
        self.active_bots: Dict[str, BotPlayer] = {}
        self.bot_count = 0
        
    def spawn_bot(self, bot_type: str, skill_level: float) -> BotPlayer:
        """Crear un nuevo bot"""
        self.bot_count += 1
        
        # Configurar según tipo
        bot_config = self.get_bot_config(bot_type)
        
        bot = BotPlayer(
            bot_id=f"bot_{self.bot_count}",
            bot_type=bot_type,
            player_name=self.generate_bot_name(bot_type),
            skill_level=skill_level,
            health=bot_config['health'],
            kills=0,
            damage_dealt=0,
            tokens_carried=random.uniform(10, 50),
            is_alive=True
        )
        
        self.active_bots[bot.bot_id] = bot
        print(f"🤖 Bot spawneado: {bot.player_name} ({bot.bot_type})")
        
        return bot
    
    def get_bot_config(self, bot_type: str) -> Dict:
        """Configuración de stats según tipo"""
        configs = {
            "humanoid": {
                "health": 100,
                "speed": 5,
                "detection_range": 40,
                "aim_accuracy": 0.65
            },
            "terminator": {
                "health": 200,
                "armor": 50,
                "speed": 4,
                "detection_range": 60,
                "aim_accuracy": 0.85
            },
            "combat_drone": {
                "health": 75,
                "speed": 8,
                "detection_range": 70,
                "aim_accuracy": 0.90,
                "flight_enabled": True
            }
        }
        
        return configs.get(bot_type, configs["humanoid"])
    
    def generate_bot_name(self, bot_type: str) -> str:
        """Generar nombre para bot"""
        names = {
            "humanoid": ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot"],
            "terminator": ["T-800", "T-1000", "T-X", "Rev-9", "T-3000"],
            "combat_drone": ["Drone-01", "Drone-02", "Reaper-1", "Predator-1"]
        }
        
        name_list = names.get(bot_type, names["humanoid"])
        return f"Bot-{random.choice(name_list)}-{random.randint(100, 999)}"
    
    def calculate_bot_kill_reward(self) -> float:
        """Recompensa por eliminar un bot"""
        return 15.0  # EVT
    
    def bot_death(self, bot_id: str, killer_name: str) -> Dict:
        """Manejar muerte de bot"""
        bot = self.active_bots.get(bot_id)
        
        if not bot:
            return {}
        
        bot.is_alive = False
        
        # Loot drop
        loot = {
            "tokens": bot.tokens_carried,
            "weapons": ["random_weapon"],
            "position": (0, 0, 0)  # Actualizar con posición real
        }
        
        print(f"🤖💀 {bot.player_name} eliminado por {killer_name}")
        print(f"💰 Loot: {loot['tokens']} EVT")
        
        # Remover del sistema
        del self.active_bots[bot_id]
        
        return loot
    
    def auto_fill_match(self, current_players: int, max_players: int, skill_level: float):
        """Auto-rellenar partida con bots"""
        bots_needed = max_players - current_players
        
        if bots_needed <= 0:
            return
        
        # Distribución de tipos de bots
        bot_distribution = {
            "humanoid": 0.6,
            "terminator": 0.3,
            "combat_drone": 0.1
        }
        
        for _ in range(bots_needed):
            # Seleccionar tipo aleatorio según distribución
            rand = random.random()
            if rand < 0.6:
                bot_type = "humanoid"
            elif rand < 0.9:
                bot_type = "terminator"
            else:
                bot_type = "combat_drone"
            
            self.spawn_bot(bot_type, skill_level)
        
        print(f"🤖 Auto-fill: {bots_needed} bots añadidos")

class VehicleSystem:
    """Sistema de gestión de vehículos"""
    
    def __init__(self):
        self.active_vehicles: Dict[str, Vehicle] = {}
        self.vehicle_count = 0
    
    def spawn_vehicle(self, vehicle_type: str, position: tuple) -> Vehicle:
        """Spawnear vehículo"""
        self.vehicle_count += 1
        
        config = self.get_vehicle_config(vehicle_type)
        
        vehicle = Vehicle(
            vehicle_id=f"vehicle_{self.vehicle_count}",
            vehicle_type=vehicle_type,
            health=config['health'],
            max_health=config['health'],
            position=position,
            passengers=[]
        )
        
        self.active_vehicles[vehicle.vehicle_id] = vehicle
        print(f"🚗 Vehículo spawneado: {vehicle_type} en {position}")
        
        return vehicle
    
    def get_vehicle_config(self, vehicle_type: str) -> Dict:
        """Configuración de vehículo"""
        configs = {
            "combat_tank": {
                "health": 1000,
                "max_speed": 15,
                "damage": 100,
                "fire_rate": 1.0,
                "passengers": 2
            },
            "armored_car": {
                "health": 300,
                "max_speed": 40,
                "damage": 30,
                "fire_rate": 5.0,
                "passengers": 4
            },
            "attack_drone": {
                "health": 200,
                "max_speed": 50,
                "damage": 25,
                "fire_rate": 10.0,
                "passengers": 1
            },
            "destroyer_mech": {
                "health": 1500,
                "max_speed": 10,
                "damage": 150,
                "fire_rate": 0.5,
                "passengers": 1
            },
            "excavator": {
                "health": 800,
                "max_speed": 8,
                "damage": 200,
                "fire_rate": 2.0,
                "passengers": 1,
                "special": "building_destruction"
            }
        }
        
        return configs.get(vehicle_type, configs["armored_car"])
    
    def enter_vehicle(self, vehicle_id: str, player_id: str) -> bool:
        """Jugador/bot entra a vehículo"""
        vehicle = self.active_vehicles.get(vehicle_id)
        
        if not vehicle or vehicle.is_destroyed:
            return False
        
        # Verificar si hay espacio
        config = self.get_vehicle_config(vehicle.vehicle_type)
        max_passengers = config['passengers']
        
        if vehicle.driver is None:
            vehicle.driver = player_id
            print(f"🚗 {player_id} subió como conductor a {vehicle.vehicle_type}")
            return True
        elif len(vehicle.passengers) < max_passengers - 1:
            vehicle.passengers.append(player_id)
            print(f"🚗 {player_id} subió como pasajero a {vehicle.vehicle_type}")
            return True
        
        return False
    
    def exit_vehicle(self, vehicle_id: str, player_id: str):
        """Jugador/bot sale de vehículo"""
        vehicle = self.active_vehicles.get(vehicle_id)
        
        if not vehicle:
            return
        
        if vehicle.driver == player_id:
            vehicle.driver = None
            print(f"🚗 {player_id} salió del {vehicle.vehicle_type}")
        elif player_id in vehicle.passengers:
            vehicle.passengers.remove(player_id)
            print(f"🚗 {player_id} salió del {vehicle.vehicle_type}")
    
    def vehicle_take_damage(self, vehicle_id: str, damage: float) -> bool:
        """Vehículo recibe daño"""
        vehicle = self.active_vehicles.get(vehicle_id)
        
        if not vehicle or vehicle.is_destroyed:
            return False
        
        vehicle.health -= damage
        
        if vehicle.health <= 0:
            self.destroy_vehicle(vehicle_id)
            return True
        
        return False
    
    def destroy_vehicle(self, vehicle_id: str) -> Dict:
        """Destruir vehículo"""
        vehicle = self.active_vehicles.get(vehicle_id)
        
        if not vehicle:
            return {}
        
        vehicle.is_destroyed = True
        
        print(f"💥 {vehicle.vehicle_type} destruido!")
        
        # Expulsar pasajeros
        ejected = []
        if vehicle.driver:
            ejected.append(vehicle.driver)
        ejected.extend(vehicle.passengers)
        
        # Explosión
        explosion_data = {
            "position": vehicle.position,
            "radius": 10,
            "damage": 100,
            "ejected_players": ejected
        }
        
        # Remover vehículo después de delay
        # En producción usaríamos asyncio.create_task
        del self.active_vehicles[vehicle_id]
        
        return explosion_data
    
    def calculate_vehicle_kill_reward(self, vehicle_type: str) -> float:
        """Recompensa por kill con vehículo"""
        base_reward = 25.0
        
        multipliers = {
            "combat_tank": 2.0,      # 50 EVT
            "armored_car": 1.5,      # 37.5 EVT
            "attack_drone": 1.8,     # 45 EVT
            "destroyer_mech": 2.5,   # 62.5 EVT
            "excavator": 2.2         # 55 EVT
        }
        
        multiplier = multipliers.get(vehicle_type, 1.0)
        return base_reward * multiplier

# Integración con combat_arena.py existente
class EnhancedCombatArenaSystem:
    """Extensión del sistema de arena con bots y vehículos"""
    
    def __init__(self):
        self.bot_system = BotAISystem()
        self.vehicle_system = VehicleSystem()
    
    def start_match_with_bots(self, mode: str, current_players: int):
        """Iniciar match con bots de relleno"""
        max_players = 100 if mode != "high_stakes" else 50
        
        # Skill level según modo
        skill_levels = {
            "casual": 0.3,
            "ranked": 0.6,
            "tournament": 0.8,
            "high_stakes": 0.9
        }
        
        skill = skill_levels.get(mode, 0.5)
        
        # Auto-rellenar con bots
        self.bot_system.auto_fill_match(current_players, max_players, skill)
        
        # Spawnear vehículos
        self.spawn_arena_vehicles(mode)
    
    def spawn_arena_vehicles(self, mode: str):
        """Spawnear vehículos en la arena"""
        # Número de vehículos según modo
        vehicle_count = 10 if mode in ["ranked", "tournament", "high_stakes"] else 5
        
        for i in range(vehicle_count):
            # Tipo aleatorio según distribución
            rand = random.random()
            if rand < 0.15:
                vehicle_type = "combat_tank"
            elif rand < 0.50:
                vehicle_type = "armored_car"
            elif rand < 0.70:
                vehicle_type = "attack_drone"
            elif rand < 0.80:
                vehicle_type = "destroyer_mech"
            else:
                vehicle_type = "excavator"
            
            # Posición aleatoria (simplificada)
            position = (
                random.uniform(-2500, 2500),
                0,
                random.uniform(-2500, 2500)
            )
            
            self.vehicle_system.spawn_vehicle(vehicle_type, position)

# Ejemplo de uso
if __name__ == "__main__":
    print("🎮 Sistema de Bots y Vehículos - Battle Arena")
    print("=" * 50)
    
    arena = EnhancedCombatArenaSystem()
    
    # Simular inicio de match ranked con 20 jugadores
    print("\n📊 Iniciando match RANKED con 20 jugadores...")
    arena.start_match_with_bots("ranked", 20)
    
    print(f"\n🤖 Bots activos: {len(arena.bot_system.active_bots)}")
    print(f"🚗 Vehículos spawneados: {len(arena.vehicle_system.active_vehicles)}")
    
    # Simular bot subiendo a vehículo
    if arena.bot_system.active_bots and arena.vehicle_system.active_vehicles:
        bot_id = list(arena.bot_system.active_bots.keys())[0]
        vehicle_id = list(arena.vehicle_system.active_vehicles.keys())[0]
        
        print(f"\n🤖➡️🚗 Bot {bot_id} intentando subir a vehículo...")
        success = arena.vehicle_system.enter_vehicle(vehicle_id, bot_id)
        
        if success:
            print("✅ Bot subió al vehículo exitosamente")
