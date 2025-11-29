"""
Sistema de Arenas de Combate Battle Royale - Estilo Population One
Integrado con criptomonedas y NFTs para Meta Horizon y Spatial.io
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class ArenaType(Enum):
    BATTLE_ROYALE = "battle_royale"
    TEAM_DEATHMATCH = "team_deathmatch"
    CAPTURE_FLAG = "capture_flag"
    SURVIVAL = "survival"
    TOURNAMENT = "tournament"

class WeaponType(Enum):
    RIFLE = "rifle"
    SHOTGUN = "shotgun"
    SNIPER = "sniper"
    PISTOL = "pistol"
    ENERGY = "energy"
    MELEE = "melee"

@dataclass
class Player:
    id: str
    username: str
    wallet_address: str
    vr_headset: str  # Meta Quest, Valve Index, etc.
    position: tuple
    health: int = 100
    armor: int = 0
    weapons: List[WeaponType] = None
    kills: int = 0
    deaths: int = 0
    team: Optional[str] = None
    
    def __post_init__(self):
        if self.weapons is None:
            self.weapons = []

@dataclass
class Arena:
    id: str
    name: str
    arena_type: ArenaType
    max_players: int
    map_size: tuple  # (width, height, depth) en metros
    safe_zones: List[Dict]
    spawn_points: List[tuple]
    power_ups: List[Dict]
    active_players: List[Player] = None
    start_time: Optional[datetime] = None
    prize_pool: float = 0.0  # En tokens EVT
    
    def __post_init__(self):
        if self.active_players is None:
            self.active_players = []

class CombatArenaSystem:
    """Sistema de Arenas de Combate con integración Blockchain"""
    
    def __init__(self):
        self.active_arenas: Dict[str, Arena] = {}
        self.player_stats: Dict[str, Dict] = {}
        self.tournament_schedule: List[Dict] = []
        self.nft_rewards_config = self._load_nft_config()
        
    def _load_nft_config(self) -> Dict:
        """Configuración de NFTs como recompensas"""
        return {
            "weapon_skins": {
                "legendary": {"probability": 0.01, "token_value": 1000},
                "epic": {"probability": 0.05, "token_value": 250},
                "rare": {"probability": 0.15, "token_value": 50},
                "common": {"probability": 0.79, "token_value": 10}
            },
            "arena_badges": {
                "champion": {"kills_required": 100, "token_value": 5000},
                "elite": {"kills_required": 50, "token_value": 1000},
                "veteran": {"kills_required": 25, "token_value": 250}
            }
        }
    
    def create_battle_royale_arena(self, name: str, max_players: int = 100) -> Arena:
        """Crea una arena estilo Population One Battle Royale"""
        arena = Arena(
            id=f"arena_{datetime.now().timestamp()}",
            name=name,
            arena_type=ArenaType.BATTLE_ROYALE,
            max_players=max_players,
            map_size=(5000, 5000, 500),  # 5km x 5km x 500m altura
            safe_zones=[
                {"center": (2500, 2500, 0), "radius": 2000, "shrink_rate": 50}
            ],
            spawn_points=self._generate_spawn_points(max_players, 5000, 5000),
            power_ups=[
                {"type": "health", "positions": [], "respawn_time": 30},
                {"type": "armor", "positions": [], "respawn_time": 45},
                {"type": "weapon_upgrade", "positions": [], "respawn_time": 60},
                {"type": "shield", "positions": [], "respawn_time": 90}
            ],
            prize_pool=max_players * 10.0  # 10 EVT tokens por jugador
        )
        
        self.active_arenas[arena.id] = arena
        return arena
    
    def _generate_spawn_points(self, count: int, width: int, height: int) -> List[tuple]:
        """Genera puntos de spawn distribuidos uniformemente"""
        import random
        spawn_points = []
        for _ in range(count):
            x = random.randint(100, width - 100)
            y = random.randint(100, height - 100)
            z = random.randint(50, 150)  # Altura inicial
            spawn_points.append((x, y, z))
        return spawn_points
    
    async def join_arena(self, arena_id: str, player: Player) -> bool:
        """Jugador se une a una arena"""
        if arena_id not in self.active_arenas:
            return False
        
        arena = self.active_arenas[arena_id]
        
        if len(arena.active_players) >= arena.max_players:
            return False
        
        # Asignar posición de spawn
        spawn_index = len(arena.active_players)
        if spawn_index < len(arena.spawn_points):
            player.position = arena.spawn_points[spawn_index]
        
        arena.active_players.append(player)
        
        # Iniciar partida si se alcanza el mínimo de jugadores
        if len(arena.active_players) >= arena.max_players * 0.75 and not arena.start_time:
            await self._start_match(arena_id)
        
        return True
    
    async def _start_match(self, arena_id: str):
        """Inicia una partida de combate"""
        arena = self.active_arenas[arena_id]
        arena.start_time = datetime.now()
        
        print(f"🎮 INICIANDO PARTIDA: {arena.name}")
        print(f"📊 Jugadores: {len(arena.active_players)}/{arena.max_players}")
        print(f"💰 Premio acumulado: {arena.prize_pool} EVT tokens")
        
        # Simular progresión de la partida
        await self._run_match_loop(arena_id)
    
    async def _run_match_loop(self, arena_id: str):
        """Loop principal de la partida"""
        arena = self.active_arenas[arena_id]
        
        while len(arena.active_players) > 1:
            # Reducir zona segura cada 60 segundos
            await asyncio.sleep(60)
            self._shrink_safe_zone(arena)
            
            # Eliminar jugadores fuera de zona
            self._check_zone_damage(arena)
            
        # Partida terminada - distribuir premios
        if arena.active_players:
            await self._distribute_rewards(arena_id, arena.active_players[0])
    
    def _shrink_safe_zone(self, arena: Arena):
        """Reduce el tamaño de la zona segura"""
        for zone in arena.safe_zones:
            zone["radius"] = max(zone["radius"] - zone["shrink_rate"], 100)
            print(f"⚠️ Zona segura reducida a {zone['radius']}m de radio")
    
    def _check_zone_damage(self, arena: Arena):
        """Aplica daño a jugadores fuera de zona segura"""
        import math
        for player in arena.active_players[:]:
            for zone in arena.safe_zones:
                distance = math.sqrt(
                    (player.position[0] - zone["center"][0]) ** 2 +
                    (player.position[1] - zone["center"][1]) ** 2
                )
                
                if distance > zone["radius"]:
                    player.health -= 10
                    if player.health <= 0:
                        self._eliminate_player(arena, player)
    
    def _eliminate_player(self, arena: Arena, player: Player):
        """Elimina un jugador de la partida"""
        if player in arena.active_players:
            arena.active_players.remove(player)
            player.deaths += 1
            print(f"💀 {player.username} eliminado - Quedan {len(arena.active_players)} jugadores")
    
    async def _distribute_rewards(self, arena_id: str, winner: Player):
        """Distribuye premios en criptomonedas y NFTs al ganador"""
        arena = self.active_arenas[arena_id]
        
        # Tokens por victoria
        winner_tokens = arena.prize_pool * 0.50  # 50% al ganador
        second_place_tokens = arena.prize_pool * 0.30  # 30% al segundo
        third_place_tokens = arena.prize_pool * 0.20  # 20% al tercero
        
        print(f"\n🏆 GANADOR: {winner.username}")
        print(f"💰 Premio: {winner_tokens} EVT tokens")
        
        # Generar NFT especial para el ganador
        nft_reward = self._generate_nft_reward(winner, "champion")
        print(f"🎁 NFT Recompensa: {nft_reward['name']} (Valor: {nft_reward['value']} EVT)")
        
        # Enviar transacción blockchain
        await self._send_blockchain_reward(winner.wallet_address, winner_tokens, nft_reward)
        
        # Actualizar estadísticas
        self._update_player_stats(winner, arena)
    
    def _generate_nft_reward(self, player: Player, tier: str) -> Dict:
        """Genera un NFT como recompensa"""
        import random
        
        nft_types = [
            {"name": "Golden Rifle Skin", "type": "weapon_skin", "rarity": "legendary"},
            {"name": "Elite Battle Badge", "type": "badge", "rarity": "epic"},
            {"name": "VR Champion Trophy", "type": "trophy", "rarity": "legendary"},
            {"name": "Combat Master Emblem", "type": "emblem", "rarity": "rare"}
        ]
        
        nft = random.choice(nft_types)
        value = self.nft_rewards_config["weapon_skins"][nft["rarity"]]["token_value"]
        
        return {
            "name": nft["name"],
            "type": nft["type"],
            "rarity": nft["rarity"],
            "value": value,
            "owner": player.wallet_address,
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "arena_type": "battle_royale",
                "kills": player.kills,
                "player_id": player.id
            }
        }
    
    async def _send_blockchain_reward(self, wallet: str, tokens: float, nft: Dict):
        """Envía recompensas a la blockchain"""
        # Simular transacción blockchain
        transaction = {
            "to": wallet,
            "token_amount": tokens,
            "nft": nft,
            "timestamp": datetime.now().isoformat(),
            "tx_hash": f"0x{''.join([str(hash(wallet))[:16]])}"
        }
        
        print(f"⛓️ Transacción blockchain enviada: {transaction['tx_hash']}")
        return transaction
    
    def _update_player_stats(self, player: Player, arena: Arena):
        """Actualiza estadísticas del jugador"""
        if player.id not in self.player_stats:
            self.player_stats[player.id] = {
                "wins": 0,
                "matches_played": 0,
                "total_kills": 0,
                "total_deaths": 0,
                "tokens_earned": 0.0,
                "nfts_collected": []
            }
        
        stats = self.player_stats[player.id]
        stats["wins"] += 1
        stats["matches_played"] += 1
        stats["total_kills"] += player.kills
        stats["total_deaths"] += player.deaths
        stats["tokens_earned"] += arena.prize_pool * 0.50
    
    def create_tournament(self, name: str, prize_pool: float, start_time: datetime) -> Dict:
        """Crea un torneo con premios en cripto"""
        tournament = {
            "id": f"tournament_{datetime.now().timestamp()}",
            "name": name,
            "prize_pool": prize_pool,
            "start_time": start_time,
            "participants": [],
            "rounds": [],
            "status": "scheduled",
            "rewards": {
                "1st": prize_pool * 0.50,
                "2nd": prize_pool * 0.30,
                "3rd": prize_pool * 0.15,
                "4th-8th": prize_pool * 0.05 / 5
            }
        }
        
        self.tournament_schedule.append(tournament)
        return tournament
    
    def get_arena_stats(self, arena_id: str) -> Dict:
        """Obtiene estadísticas de una arena"""
        if arena_id not in self.active_arenas:
            return {}
        
        arena = self.active_arenas[arena_id]
        return {
            "arena_id": arena_id,
            "name": arena.name,
            "type": arena.arena_type.value,
            "active_players": len(arena.active_players),
            "max_players": arena.max_players,
            "prize_pool": arena.prize_pool,
            "status": "active" if arena.start_time else "waiting",
            "top_players": sorted(
                arena.active_players,
                key=lambda p: p.kills,
                reverse=True
            )[:10]
        }

# Ejemplo de uso
if __name__ == "__main__":
    async def main():
        system = CombatArenaSystem()
        
        # Crear arena Battle Royale
        arena = system.create_battle_royale_arena("Population One Style Arena", max_players=50)
        print(f"✅ Arena creada: {arena.name}")
        print(f"💰 Premio acumulado: {arena.prize_pool} EVT tokens")
        
        # Simular jugadores uniéndose
        for i in range(50):
            player = Player(
                id=f"player_{i}",
                username=f"VRWarrior{i}",
                wallet_address=f"0x{''.join([str(hash(f'player_{i}'))[:40]])}",
                vr_headset="Meta Quest 3",
                position=(0, 0, 0)
            )
            await system.join_arena(arena.id, player)
        
        # Obtener estadísticas
        stats = system.get_arena_stats(arena.id)
        print(f"\n📊 Estadísticas de Arena:")
        print(f"Jugadores activos: {stats['active_players']}/{stats['max_players']}")
        print(f"Estado: {stats['status']}")
    
    asyncio.run(main())

