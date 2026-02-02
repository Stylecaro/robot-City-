"""
City Zones System - Diferentes zonas/distritos de la ciudad tecnológica metaverso
Cada zona con características, actividades, NPCs, y mini-juegos
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import uuid


class ZoneType(Enum):
    """Tipos de zonas en la ciudad"""
    INDUSTRIAL = "industrial"      # Fabricación, robots
    COMMERCIAL = "commercial"      # Tiendas, marketplace
    RESEARCH = "research"          # Laboratorios
    ENTERTAINMENT = "entertainment" # Juegos, casinos
    COMBAT = "combat"              # Arena de batalla
    RESIDENTIAL = "residential"    # Hogares de usuarios
    NATURE = "nature"              # Parques, bosques simulados
    SPACE = "space"                # Estación espacial
    UNDERWATER = "underwater"      # Ciudad submarina
    VIRTUAL = "virtual"            # Realidad virtual dentro del metaverso
    ENERGY = "energy"              # Plantas de energía y rendimiento
    WORK_DISTRICT = "work_district" # Distrito de trabajo y empleos
    MEDICAL = "medical"            # Investigación médica real
    REAL_ESTATE = "real_estate"    # Compra/venta de propiedades
    FINANCIAL = "financial"        # Wall Street y bolsa de valores
    DATA_VAULT = "data_vault"      # Almacenamiento de datos ultra seguro
    AUTONOMOUS_CONTROL = "autonomous_control"  # Centro autónomo de ciudad


class BuildingAccessLevel(Enum):
    """Nivel de acceso requerido para edificios"""
    PUBLIC = 1
    STAFF = 2
    ADMIN = 3
    QUANTUM = 4


class ZoneTier(Enum):
    """Nivel de acceso a zona"""
    PUBLIC = 1         # Acceso público
    MEMBER = 2         # Requiere membresía
    VETERAN = 3        # Robots nivel 10+
    ELITE = 4          # Robots nivel 50+
    LEGENDARY = 5      # Robots nivel 100+


@dataclass
class NPC:
    """Non-Player Character en una zona"""
    npc_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    role: str = ""  # "merchant", "quest_giver", "trainer", etc
    dialogue: str = ""
    location: Tuple[float, float, float] = (0, 0, 0)  # x, y, z


@dataclass
class MiniGame:
    """Mini-juego dentro de una zona"""
    game_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    game_type: str = ""  # "puzzle", "racing", "shooting", "trading", etc
    difficulty: int = 1  # 1-5
    
    # Rewards
    exp_reward: int = 100
    credits_reward: int = 500
    
    # Acceso
    min_level: int = 1
    
    def to_dict(self) -> Dict:
        return {
            "game_id": self.game_id,
            "name": self.name,
            "type": self.game_type,
            "difficulty": self.difficulty,
            "exp_reward": self.exp_reward,
            "credits_reward": self.credits_reward
        }


@dataclass
class Building:
    """Edificio dentro de una zona"""
    building_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    purpose: str = ""
    access_level: BuildingAccessLevel = BuildingAccessLevel.PUBLIC
    allowed_roles: List[str] = field(default_factory=list)
    capacity: int = 50
    current_occupants: List[str] = field(default_factory=list)

    def can_enter(self, player_id: str, roles: List[str]) -> bool:
        if len(self.current_occupants) >= self.capacity:
            return False
        if self.access_level == BuildingAccessLevel.PUBLIC:
            return True
        if not self.allowed_roles:
            return False
        return any(role in self.allowed_roles for role in roles)

    def enter(self, player_id: str) -> bool:
        if player_id not in self.current_occupants:
            self.current_occupants.append(player_id)
            return True
        return False

    def exit(self, player_id: str) -> bool:
        if player_id in self.current_occupants:
            self.current_occupants.remove(player_id)
            return True
        return False

    def to_dict(self) -> Dict:
        return {
            "building_id": self.building_id,
            "name": self.name,
            "purpose": self.purpose,
            "access_level": self.access_level.name,
            "allowed_roles": self.allowed_roles,
            "capacity": self.capacity,
            "occupancy": len(self.current_occupants)
        }


@dataclass
class CityZone:
    """Zona/Distrito de la ciudad"""
    zone_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    zone_type: ZoneType = ZoneType.INDUSTRIAL
    tier: ZoneTier = ZoneTier.PUBLIC
    
    # Ubicación y tamaño
    location: Tuple[float, float, float] = (0, 0, 0)  # Centro
    size: float = 100.0  # Radio
    
    # Contenido
    npcs: List[NPC] = field(default_factory=list)
    mini_games: List[MiniGame] = field(default_factory=list)
    buildings: List[Building] = field(default_factory=list)
    shops: List[Dict] = field(default_factory=list)
    quests: List[Dict] = field(default_factory=list)
    
    # Dinámico
    active_players: List[str] = field(default_factory=list)
    weather: str = "clear"
    time_of_day: str = "day"
    
    # Estadísticas
    created_at: datetime = field(default_factory=datetime.now)
    daily_visitors: int = 0
    
    def add_player(self, player_id: str) -> bool:
        """Añade jugador a la zona"""
        if player_id not in self.active_players:
            self.active_players.append(player_id)
            self.daily_visitors += 1
            return True
        return False
    
    def remove_player(self, player_id: str) -> bool:
        """Remueve jugador de la zona"""
        if player_id in self.active_players:
            self.active_players.remove(player_id)
            return True
        return False
    
    def to_dict(self) -> Dict:
        return {
            "zone_id": self.zone_id,
            "name": self.name,
            "type": self.zone_type.value,
            "tier": self.tier.name,
            "location": self.location,
            "size": self.size,
            "active_players": len(self.active_players),
            "weather": self.weather,
            "mini_games": [g.to_dict() for g in self.mini_games],
            "npcs": len(self.npcs),
            "buildings": [b.to_dict() for b in self.buildings]
        }


class CityManager:
    """Gestor de la ciudad tecnológica"""
    
    def __init__(self):
        self.zones: Dict[str, CityZone] = {}
        self.player_locations: Dict[str, str] = {}  # player_id -> zone_id
        self.player_roles: Dict[str, List[str]] = {}  # player_id -> roles
        
        # Crear zonas de la ciudad
        self._init_zones()
    
    def _init_zones(self):
        """Inicializa zonas de la ciudad"""
        zones_config = [
            # INDUSTRIAL DISTRICT
            {
                "name": "Factory District",
                "description": "Centro de manufactura y construcción de robots",
                "zone_type": ZoneType.INDUSTRIAL,
                "tier": ZoneTier.PUBLIC,
                "location": (-600, 0, 0),
                "size": 150.0,
                "games": [
                    MiniGame(
                        name="Robot Assembly Puzzle",
                        description="Arma robots correctamente",
                        game_type="puzzle",
                        difficulty=2,
                        exp_reward=150,
                        credits_reward=800
                    )
                ]
            },
            # COMMERCIAL DISTRICT
            {
                "name": "Market Hub",
                "description": "Centro comercial con tiendas y marketplace",
                "zone_type": ZoneType.COMMERCIAL,
                "tier": ZoneTier.PUBLIC,
                "location": (600, 0, 0),
                "size": 120.0,
                "games": [
                    MiniGame(
                        name="Trading Challenge",
                        description="Compra bajo y vende alto",
                        game_type="trading",
                        difficulty=2,
                        exp_reward=100,
                        credits_reward=1000
                    )
                ]
            },
            # RESEARCH DISTRICT
            {
                "name": "Research Laboratories",
                "description": "Laboratorios avanzados de investigación",
                "zone_type": ZoneType.RESEARCH,
                "tier": ZoneTier.MEMBER,
                "location": (-600, 200, 0),
                "size": 100.0,
                "games": [
                    MiniGame(
                        name="Quantum Puzzle",
                        description="Resuelve acertijos cuánticos",
                        game_type="puzzle",
                        difficulty=4,
                        min_level=10,
                        exp_reward=300,
                        credits_reward=2000
                    )
                ]
            },
            # ENTERTAINMENT DISTRICT
            {
                "name": "Entertainment Zone",
                "description": "Zona de entretenimiento con casinos y juegos",
                "zone_type": ZoneType.ENTERTAINMENT,
                "tier": ZoneTier.PUBLIC,
                "location": (0, 600, 0),
                "size": 140.0,
                "games": [
                    MiniGame(
                        name="Cyber Racing",
                        description="Carrera de alta velocidad",
                        game_type="racing",
                        difficulty=3,
                        exp_reward=200,
                        credits_reward=1500
                    ),
                    MiniGame(
                        name="Slots & Luck",
                        description="Máquinas tragamonedas",
                        game_type="casino",
                        difficulty=1,
                        exp_reward=50,
                        credits_reward=500
                    ),
                    MiniGame(
                        name="Hologram Shooter",
                        description="Dispara hologramas",
                        game_type="shooting",
                        difficulty=3,
                        exp_reward=180,
                        credits_reward=1200
                    )
                ]
            },
            # COMBAT DISTRICT
            {
                "name": "Battle Arena District",
                "description": "Centro de combate y entrenamientos",
                "zone_type": ZoneType.COMBAT,
                "tier": ZoneTier.PUBLIC,
                "location": (0, -600, 0),
                "size": 130.0,
                "games": [
                    MiniGame(
                        name="Deathmatch Arena",
                        description="Batalla a muerte",
                        game_type="combat",
                        difficulty=4,
                        min_level=5,
                        exp_reward=250,
                        credits_reward=2000
                    )
                ]
            },
            # RESIDENTIAL DISTRICT
            {
                "name": "Residential Sector",
                "description": "Hogares y espacios personales",
                "zone_type": ZoneType.RESIDENTIAL,
                "tier": ZoneTier.MEMBER,
                "location": (600, 200, 0),
                "size": 100.0
            },
            # NATURE DISTRICT
            {
                "name": "Virtual Gardens",
                "description": "Parques y naturaleza simulada",
                "zone_type": ZoneType.NATURE,
                "tier": ZoneTier.PUBLIC,
                "location": (-600, -200, 0),
                "size": 120.0,
                "games": [
                    MiniGame(
                        name="Nature Explorer",
                        description="Explora y recolecta recursos",
                        game_type="exploration",
                        difficulty=1,
                        exp_reward=100,
                        credits_reward=600
                    )
                ]
            },
            # SPACE STATION
            {
                "name": "Orbital Station",
                "description": "Estación espacial con gravedad cero",
                "zone_type": ZoneType.SPACE,
                "tier": ZoneTier.VETERAN,
                "location": (0, 0, 1200),
                "size": 150.0,
                "games": [
                    MiniGame(
                        name="Zero-G Combat",
                        description="Combate sin gravedad",
                        game_type="combat",
                        difficulty=5,
                        min_level=50,
                        exp_reward=500,
                        credits_reward=5000
                    )
                ]
            },
            # UNDERWATER CITY
            {
                "name": "Deep Ocean City",
                "description": "Ciudad bajo agua con flora submarina",
                "zone_type": ZoneType.UNDERWATER,
                "tier": ZoneTier.ELITE,
                "location": (900, 900, -600),
                "size": 160.0,
                "games": [
                    MiniGame(
                        name="Abyssal Survival",
                        description="Supervivencia en el abismo",
                        game_type="survival",
                        difficulty=5,
                        min_level=70,
                        exp_reward=400,
                        credits_reward=4000
                    )
                ]
            },
            # VIRTUAL REALITY REALM
            {
                "name": "VR Metaverse",
                "description": "Realidad virtual dentro del metaverso",
                "zone_type": ZoneType.VIRTUAL,
                "tier": ZoneTier.LEGENDARY,
                "location": (0, 0, 2000),
                "size": 200.0,
                "games": [
                    MiniGame(
                        name="Matrix Challenge",
                        description="Desafío definitivo en la matriz",
                        game_type="puzzle",
                        difficulty=5,
                        min_level=100,
                        exp_reward=1000,
                        credits_reward=10000
                    )
                ]
            },
            # ENERGY & PERFORMANCE ZONE
            {
                "name": "Energy Power Plant",
                "description": "Planta de energía y gestión de rendimiento",
                "zone_type": ZoneType.ENERGY,
                "tier": ZoneTier.MEMBER,
                "location": (-900, 0, 0),
                "size": 180.0,
                "games": [
                    MiniGame(
                        name="Energy Management",
                        description="Gestiona reactores de energía",
                        game_type="puzzle",
                        difficulty=4,
                        min_level=15,
                        exp_reward=250,
                        credits_reward=2000
                    ),
                    MiniGame(
                        name="Reactor Maintenance",
                        description="Mantén los reactores operativos",
                        game_type="puzzle",
                        difficulty=3,
                        exp_reward=200,
                        credits_reward=1500
                    )
                ]
            },
            # WORK DISTRICT
            {
                "name": "Work & Employment Center",
                "description": "Centro de trabajo donde ganas criptomonedas",
                "zone_type": ZoneType.WORK_DISTRICT,
                "tier": ZoneTier.PUBLIC,
                "location": (900, 0, 0),
                "size": 200.0,
                "buildings": [
                    Building(
                        name="Worker Registry",
                        purpose="Registro de trabajadores",
                        access_level=BuildingAccessLevel.PUBLIC,
                        allowed_roles=["worker", "assistant"],
                        capacity=200
                    ),
                    Building(
                        name="Assistant Hub",
                        purpose="Centro de ayudantes y coordinación",
                        access_level=BuildingAccessLevel.STAFF,
                        allowed_roles=["assistant", "manager"],
                        capacity=100
                    )
                ],
                "games": [
                    MiniGame(
                        name="Factory Shift",
                        description="Trabaja en la fábrica",
                        game_type="work",
                        difficulty=2,
                        exp_reward=150,
                        credits_reward=1000
                    ),
                    MiniGame(
                        name="Data Analysis",
                        description="Analiza datos para ganar tokens",
                        game_type="work",
                        difficulty=4,
                        exp_reward=300,
                        credits_reward=2500
                    )
                ]
            },
            # MEDICAL RESEARCH ZONE
            {
                "name": "Medical Research Labs",
                "description": "Investigación médica real y experimentos simulados",
                "zone_type": ZoneType.MEDICAL,
                "tier": ZoneTier.MEMBER,
                "location": (-900, 200, 0),
                "size": 170.0,
                "games": [
                    MiniGame(
                        name="Medical Simulation",
                        description="Simulaciones médicas reales",
                        game_type="simulation",
                        difficulty=5,
                        min_level=20,
                        exp_reward=400,
                        credits_reward=3500
                    ),
                    MiniGame(
                        name="Drug Development",
                        description="Desarrollo de medicamentos",
                        game_type="research",
                        difficulty=5,
                        min_level=30,
                        exp_reward=500,
                        credits_reward=4000
                    )
                ]
            },
            # REAL ESTATE DISTRICT
            {
                "name": "Real Estate Hub",
                "description": "Compra, vende y gestiona propiedades",
                "zone_type": ZoneType.REAL_ESTATE,
                "tier": ZoneTier.PUBLIC,
                "location": (900, 200, 0),
                "size": 150.0,
                "games": [
                    MiniGame(
                        name="Property Trading",
                        description="Compra y vende propiedades",
                        game_type="trading",
                        difficulty=3,
                        exp_reward=200,
                        credits_reward=1500
                    ),
                    MiniGame(
                        name="Real Estate Tycoon",
                        description="Conviértete en magnate inmobiliario",
                        game_type="strategy",
                        difficulty=4,
                        min_level=25,
                        exp_reward=350,
                        credits_reward=3000
                    )
                ]
            },
            # WALL STREET - FINANCIAL DISTRICT
            {
                "name": "Wall Street District",
                "description": "Bolsa de valores en vivo, análisis financiero y trading",
                "zone_type": ZoneType.FINANCIAL,
                "tier": ZoneTier.MEMBER,
                "location": (0, 900, 0),
                "size": 180.0,
                "buildings": [
                    Building(
                        name="Trading Exchange",
                        purpose="Ejecución de órdenes en vivo",
                        access_level=BuildingAccessLevel.STAFF,
                        allowed_roles=["trader", "analyst", "manager"],
                        capacity=150
                    ),
                    Building(
                        name="Market Intelligence",
                        purpose="Análisis financiero avanzado",
                        access_level=BuildingAccessLevel.ADMIN,
                        allowed_roles=["analyst", "admin"],
                        capacity=80
                    )
                ],
                "games": [
                    MiniGame(
                        name="Trading Floor",
                        description="Compra y vende acciones en tiempo real",
                        game_type="trading",
                        difficulty=4,
                        min_level=20,
                        exp_reward=300,
                        credits_reward=2500
                    ),
                    MiniGame(
                        name="Market Analysis Lab",
                        description="Analiza la bolsa con IA",
                        game_type="analysis",
                        difficulty=5,
                        min_level=25,
                        exp_reward=400,
                        credits_reward=3500
                    ),
                    MiniGame(
                        name="Defense Index",
                        description="Optimiza el índice de defensa",
                        game_type="strategy",
                        difficulty=5,
                        min_level=30,
                        exp_reward=450,
                        credits_reward=4000
                    )
                ]
            },
            # DATA VAULT - QUANTUM SECURITY
            {
                "name": "Quantum Data Vault",
                "description": "Superzona de almacenamiento de datos con máxima seguridad cuántica",
                "zone_type": ZoneType.DATA_VAULT,
                "tier": ZoneTier.ELITE,
                "location": (0, -900, 0),
                "size": 200.0,
                "buildings": [
                    Building(
                        name="Qubit Core",
                        purpose="Núcleo cuántico de datos",
                        access_level=BuildingAccessLevel.QUANTUM,
                        allowed_roles=["quantum_admin"],
                        capacity=20
                    ),
                    Building(
                        name="Data Guardians",
                        purpose="Seguridad y defensa de datos",
                        access_level=BuildingAccessLevel.ADMIN,
                        allowed_roles=["security", "admin"],
                        capacity=60
                    )
                ],
                "games": [
                    MiniGame(
                        name="Qubit Encryption",
                        description="Protege datos con cifrado cuántico",
                        game_type="security",
                        difficulty=5,
                        min_level=50,
                        exp_reward=500,
                        credits_reward=4500
                    ),
                    MiniGame(
                        name="Data Fortress",
                        description="Defiende el núcleo de datos",
                        game_type="defense",
                        difficulty=5,
                        min_level=60,
                        exp_reward=600,
                        credits_reward=5500
                    )
                ]
            },
            # AUTONOMOUS CONTROL CENTER
            {
                "name": "Autonomous City Control",
                "description": "Centro autónomo de gestión de ciudad inteligente",
                "zone_type": ZoneType.AUTONOMOUS_CONTROL,
                "tier": ZoneTier.ELITE,
                "location": (-900, -900, 0),
                "size": 220.0,
                "buildings": [
                    Building(
                        name="City AI Core",
                        purpose="Control central de la ciudad",
                        access_level=BuildingAccessLevel.ADMIN,
                        allowed_roles=["admin", "city_operator"],
                        capacity=30
                    ),
                    Building(
                        name="Maintenance Operations",
                        purpose="Mantenimiento de infraestructura",
                        access_level=BuildingAccessLevel.STAFF,
                        allowed_roles=["worker", "engineer", "assistant"],
                        capacity=120
                    ),
                    Building(
                        name="Restricted Systems",
                        purpose="Sistemas críticos restringidos",
                        access_level=BuildingAccessLevel.QUANTUM,
                        allowed_roles=["quantum_admin", "admin"],
                        capacity=15
                    )
                ]
            }
        ]
        
        for zone_config in zones_config:
            zone = CityZone(
                name=zone_config["name"],
                description=zone_config.get("description", ""),
                zone_type=ZoneType[zone_config["zone_type"].value.upper()],
                tier=ZoneTier[zone_config["tier"].name],
                location=zone_config["location"],
                size=zone_config["size"]
            )
            
            # Añadir mini-games
            for game in zone_config.get("games", []):
                zone.mini_games.append(game)

            # Añadir edificios
            for building in zone_config.get("buildings", []):
                zone.buildings.append(building)
            
            self.zones[zone.zone_id] = zone
    
    def get_zone(self, zone_id: str) -> Optional[CityZone]:
        """Obtiene una zona"""
        return self.zones.get(zone_id)
    
    def get_zone_by_name(self, name: str) -> Optional[CityZone]:
        """Obtiene zona por nombre"""
        for zone in self.zones.values():
            if zone.name.lower() == name.lower():
                return zone
        return None
    
    def get_all_zones(self) -> List[CityZone]:
        """Obtiene todas las zonas"""
        return list(self.zones.values())
    
    def get_zones_by_type(self, zone_type: ZoneType) -> List[CityZone]:
        """Obtiene zonas por tipo"""
        return [z for z in self.zones.values() if z.zone_type == zone_type]

    def set_player_roles(self, player_id: str, roles: List[str]) -> None:
        """Define roles del jugador para accesos"""
        self.player_roles[player_id] = roles

    def _get_roles(self, player_id: str) -> List[str]:
        return self.player_roles.get(player_id, [])

    def enter_building(self, player_id: str, zone_id: str, building_id: str) -> Tuple[bool, str]:
        """Intento de entrar a un edificio con control de acceso"""
        zone = self.get_zone(zone_id)
        if not zone:
            return False, "Zone not found"

        building = next((b for b in zone.buildings if b.building_id == building_id), None)
        if not building:
            return False, "Building not found"

        roles = self._get_roles(player_id)
        if not building.can_enter(player_id, roles):
            return False, "Access denied"

        building.enter(player_id)
        return True, f"Entered {building.name}"

    def exit_building(self, player_id: str, zone_id: str, building_id: str) -> Tuple[bool, str]:
        """Salir de edificio"""
        zone = self.get_zone(zone_id)
        if not zone:
            return False, "Zone not found"

        building = next((b for b in zone.buildings if b.building_id == building_id), None)
        if not building:
            return False, "Building not found"

        building.exit(player_id)
        return True, f"Exited {building.name}"
    
    def enter_zone(self, player_id: str, zone_id: str) -> Tuple[bool, str]:
        """Jugador entra a una zona"""
        zone = self.get_zone(zone_id)
        if not zone:
            return False, "Zone not found"
        
        # Remover de zona anterior si está en una
        if player_id in self.player_locations:
            old_zone = self.get_zone(self.player_locations[player_id])
            if old_zone:
                old_zone.remove_player(player_id)
        
        # Entrar a nueva zona
        zone.add_player(player_id)
        self.player_locations[player_id] = zone_id
        
        return True, f"Entered {zone.name}"
    
    def exit_zone(self, player_id: str) -> bool:
        """Jugador sale de la zona"""
        if player_id in self.player_locations:
            zone = self.get_zone(self.player_locations[player_id])
            if zone:
                zone.remove_player(player_id)
            del self.player_locations[player_id]
            return True
        return False
    
    def get_player_zone(self, player_id: str) -> Optional[CityZone]:
        """Obtiene zona actual del jugador"""
        zone_id = self.player_locations.get(player_id)
        if zone_id:
            return self.get_zone(zone_id)
        return None
    
    def play_mini_game(self, player_id: str, zone_id: str, game_id: str) -> Optional[Dict]:
        """Inicia un mini-juego"""
        zone = self.get_zone(zone_id)
        if not zone:
            return None
        
        game = None
        for g in zone.mini_games:
            if g.game_id == game_id:
                game = g
                break
        
        if not game:
            return None
        
        return {
            "game_id": game.game_id,
            "name": game.name,
            "description": game.description,
            "type": game.game_type,
            "zone": zone.name,
            "status": "started"
        }
    
    def get_city_stats(self) -> Dict:
        """Obtiene estadísticas de la ciudad"""
        total_players = len(self.player_locations)
        total_active = sum(len(z.active_players) for z in self.zones.values())
        
        return {
            "total_zones": len(self.zones),
            "total_players_online": total_players,
            "total_active_players": total_active,
            "zones": [z.to_dict() for z in self.zones.values()],
            "by_type": {
                zt.value: len(self.get_zones_by_type(zt))
                for zt in ZoneType
            }
        }
    
    def get_zone_info(self, zone_id: str) -> Dict:
        """Obtiene información detallada de una zona"""
        zone = self.get_zone(zone_id)
        if not zone:
            return {}
        
        return {
            "zone_id": zone.zone_id,
            "name": zone.name,
            "description": zone.description,
            "type": zone.zone_type.value,
            "tier": zone.tier.name,
            "location": zone.location,
            "size": zone.size,
            "active_players": zone.active_players,
            "weather": zone.weather,
            "time": zone.time_of_day,
            "daily_visitors": zone.daily_visitors,
            "buildings": [b.to_dict() for b in zone.buildings],
            "mini_games": [
                {
                    "game_id": g.game_id,
                    "name": g.name,
                    "type": g.game_type,
                    "difficulty": g.difficulty,
                    "min_level": g.min_level,
                    "exp_reward": g.exp_reward,
                    "credits_reward": g.credits_reward
                }
                for g in zone.mini_games
            ]
        }


# Instancia global
city_manager = CityManager()
