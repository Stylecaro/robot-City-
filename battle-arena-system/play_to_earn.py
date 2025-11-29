"""
Sistema Play-to-Earn para Battle Arena
Integración completa con blockchain para recompensas en criptomonedas y NFTs
"""

from web3 import Web3
from eth_account import Account
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass
class CryptoReward:
    token_symbol: str
    amount: float
    usd_value: float
    wallet_address: str
    tx_hash: Optional[str] = None

@dataclass
class NFTReward:
    token_id: int
    name: str
    rarity: str
    attributes: Dict
    image_url: str
    contract_address: str
    value_in_tokens: float

class PlayToEarnSystem:
    """Sistema completo de Play-to-Earn con recompensas blockchain"""
    
    def __init__(self, web3_provider: str = "https://polygon-mainnet.infura.io/v3/YOUR_INFURA_KEY"):
        self.w3 = Web3(Web3.HTTPProvider(web3_provider))
        self.token_contract_address = "0x..."  # Dirección del contrato EVT Token
        self.nft_contract_address = "0x..."   # Dirección del contrato NFT
        self.reward_pools: Dict[str, float] = {
            "daily_missions": 10000.0,
            "weekly_tournaments": 50000.0,
            "monthly_championships": 200000.0,
            "battle_royale": 5000.0
        }
        self.player_earnings: Dict[str, Dict] = {}
        
    def calculate_match_reward(self, 
                              placement: int,
                              total_players: int,
                              kills: int,
                              damage_dealt: int,
                              survival_time: int) -> float:
        """Calcula recompensa basada en rendimiento en la partida"""
        
        # Recompensa base por posición
        placement_rewards = {
            1: 1000.0,  # Ganador
            2: 500.0,   # Segundo lugar
            3: 250.0,   # Tercer lugar
            4: 150.0,
            5: 100.0
        }
        
        base_reward = placement_rewards.get(placement, 50.0 if placement <= 10 else 10.0)
        
        # Bonificaciones
        kill_bonus = kills * 25.0  # 25 tokens por kill
        damage_bonus = damage_dealt * 0.1  # 0.1 token por punto de daño
        survival_bonus = survival_time * 0.5  # 0.5 tokens por segundo sobrevivido
        
        total_reward = base_reward + kill_bonus + damage_bonus + survival_bonus
        
        # Multiplicador por tamaño de partida
        size_multiplier = min(total_players / 50.0, 2.0)  # Max 2x para partidas grandes
        
        return total_reward * size_multiplier
    
    def calculate_daily_missions_reward(self, missions_completed: List[str]) -> Dict:
        """Calcula recompensas por misiones diarias completadas"""
        mission_values = {
            "win_match": 100.0,
            "10_kills": 75.0,
            "deal_5000_damage": 50.0,
            "survive_10_minutes": 40.0,
            "headshot_5_enemies": 60.0,
            "use_3_different_weapons": 30.0,
            "revive_teammates": 45.0,
            "capture_3_zones": 55.0
        }
        
        total_tokens = sum(mission_values.get(m, 0) for m in missions_completed)
        
        # Bonus por completar todas las misiones diarias
        if len(missions_completed) >= 5:
            total_tokens += 200.0
            
        return {
            "tokens_earned": total_tokens,
            "missions_completed": len(missions_completed),
            "bonus_applied": len(missions_completed) >= 5
        }
    
    def generate_nft_drop(self, player_level: int, achievement_type: str) -> Optional[NFTReward]:
        """Genera un NFT aleatorio basado en logros del jugador"""
        import random
        
        # Probabilidades basadas en nivel del jugador
        drop_chance = min(0.05 + (player_level * 0.01), 0.50)  # Max 50% de probabilidad
        
        if random.random() > drop_chance:
            return None
        
        # Tipos de NFTs disponibles
        nft_types = {
            "legendary": {
                "probability": 0.01,
                "value": 5000.0,
                "names": ["Golden Battle Crown", "Legendary Warrior Skin", "Mythic Weapon Set"]
            },
            "epic": {
                "probability": 0.05,
                "value": 1000.0,
                "names": ["Elite Combat Badge", "Epic Armor Skin", "Rare Weapon Skin"]
            },
            "rare": {
                "probability": 0.15,
                "value": 250.0,
                "names": ["Battle Veteran Badge", "Rare Emote", "Special Weapon Charm"]
            },
            "common": {
                "probability": 0.79,
                "value": 50.0,
                "names": ["Common Badge", "Basic Spray", "Standard Emote"]
            }
        }
        
        # Seleccionar rareza
        rand_val = random.random()
        cumulative_prob = 0
        selected_rarity = "common"
        
        for rarity, config in nft_types.items():
            cumulative_prob += config["probability"]
            if rand_val <= cumulative_prob:
                selected_rarity = rarity
                break
        
        selected_config = nft_types[selected_rarity]
        nft_name = random.choice(selected_config["names"])
        
        return NFTReward(
            token_id=random.randint(1000000, 9999999),
            name=nft_name,
            rarity=selected_rarity,
            attributes={
                "achievement": achievement_type,
                "player_level": player_level,
                "minted_date": datetime.now().isoformat(),
                "combat_stats_boost": random.randint(1, 10)
            },
            image_url=f"ipfs://QmExample/{selected_rarity}_{nft_name.replace(' ', '_')}.png",
            contract_address=self.nft_contract_address,
            value_in_tokens=selected_config["value"]
        )
    
    async def process_tournament_rewards(self, 
                                        tournament_id: str,
                                        final_standings: List[Dict]) -> List[CryptoReward]:
        """Procesa y distribuye recompensas de torneo"""
        rewards = []
        prize_pool = self.reward_pools["weekly_tournaments"]
        
        # Distribución de premios
        prize_distribution = {
            1: 0.40,  # 40% al primer lugar
            2: 0.25,  # 25% al segundo
            3: 0.15,  # 15% al tercero
            4: 0.08,  # 8% al cuarto
            5: 0.05,  # 5% al quinto
            6: 0.03,  # 3% al sexto
            7: 0.02,  # 2% al séptimo
            8: 0.02   # 2% al octavo
        }
        
        for standing in final_standings[:8]:
            placement = standing["placement"]
            wallet = standing["wallet_address"]
            percentage = prize_distribution.get(placement, 0)
            
            reward_amount = prize_pool * percentage
            
            # Crear transacción de recompensa
            reward = CryptoReward(
                token_symbol="EVT",
                amount=reward_amount,
                usd_value=reward_amount * 0.50,  # Asumiendo 1 EVT = $0.50
                wallet_address=wallet
            )
            
            # Enviar transacción (simulado)
            tx_hash = await self._send_token_reward(wallet, reward_amount)
            reward.tx_hash = tx_hash
            
            rewards.append(reward)
            
            # Generar NFT especial para top 3
            if placement <= 3:
                nft = self.generate_nft_drop(100, f"tournament_winner_rank_{placement}")
                if nft:
                    await self._mint_nft(wallet, nft)
        
        return rewards
    
    async def _send_token_reward(self, wallet_address: str, amount: float) -> str:
        """Envía tokens ERC20 a la wallet del jugador"""
        # Simular transacción blockchain
        # En producción, esto interactuaría con el contrato real
        tx_hash = f"0x{''.join([str(hash(wallet_address + str(amount)))[:64]])}"
        
        print(f"💰 Enviando {amount} EVT tokens a {wallet_address[:10]}...")
        print(f"📝 Transaction Hash: {tx_hash}")
        
        return tx_hash
    
    async def _mint_nft(self, wallet_address: str, nft: NFTReward) -> str:
        """Mintea un NFT ERC721 para el jugador"""
        # Simular minteo de NFT
        # En producción, esto llamaría al contrato NFT
        tx_hash = f"0x{''.join([str(hash(wallet_address + nft.name))[:64]])}"
        
        print(f"🎁 Minteando NFT '{nft.name}' para {wallet_address[:10]}...")
        print(f"🏷️ Rareza: {nft.rarity.upper()}")
        print(f"💎 Valor: {nft.value_in_tokens} EVT tokens")
        print(f"📝 Transaction Hash: {tx_hash}")
        
        return tx_hash
    
    def track_player_earnings(self, player_id: str, reward: CryptoReward):
        """Rastrea ganancias acumuladas del jugador"""
        if player_id not in self.player_earnings:
            self.player_earnings[player_id] = {
                "total_tokens": 0.0,
                "total_usd": 0.0,
                "nfts_earned": [],
                "transactions": [],
                "last_updated": datetime.now()
            }
        
        earnings = self.player_earnings[player_id]
        earnings["total_tokens"] += reward.amount
        earnings["total_usd"] += reward.usd_value
        earnings["transactions"].append({
            "amount": reward.amount,
            "timestamp": datetime.now().isoformat(),
            "tx_hash": reward.tx_hash
        })
        earnings["last_updated"] = datetime.now()
    
    def get_player_stats(self, player_id: str) -> Dict:
        """Obtiene estadísticas completas de ganancias del jugador"""
        if player_id not in self.player_earnings:
            return {
                "total_tokens": 0.0,
                "total_usd": 0.0,
                "nfts_count": 0,
                "transactions_count": 0
            }
        
        earnings = self.player_earnings[player_id]
        return {
            "total_tokens": earnings["total_tokens"],
            "total_usd": earnings["total_usd"],
            "nfts_count": len(earnings["nfts_earned"]),
            "transactions_count": len(earnings["transactions"]),
            "last_reward": earnings["last_updated"],
            "average_per_transaction": earnings["total_tokens"] / max(len(earnings["transactions"]), 1)
        }
    
    def create_staking_pool(self, nft_token_id: int, duration_days: int) -> Dict:
        """Permite a jugadores stakear NFTs para ganar tokens pasivos"""
        daily_reward_rate = 0.05  # 5% diario
        
        total_reward = nft_token_id * daily_reward_rate * duration_days
        
        return {
            "nft_token_id": nft_token_id,
            "duration_days": duration_days,
            "daily_reward": nft_token_id * daily_reward_rate,
            "total_reward": total_reward,
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(days=duration_days),
            "status": "active"
        }
    
    def calculate_season_pass_rewards(self, level: int) -> List[Dict]:
        """Calcula recompensas del pase de temporada"""
        rewards = []
        
        for lvl in range(1, level + 1):
            if lvl % 10 == 0:  # Cada 10 niveles: NFT
                rewards.append({
                    "level": lvl,
                    "type": "nft",
                    "name": f"Season {lvl} Exclusive Skin",
                    "value": 500.0
                })
            elif lvl % 5 == 0:  # Cada 5 niveles: Tokens grandes
                rewards.append({
                    "level": lvl,
                    "type": "tokens",
                    "amount": 200.0
                })
            else:  # Otros niveles: Tokens pequeños
                rewards.append({
                    "level": lvl,
                    "type": "tokens",
                    "amount": 50.0
                })
        
        return rewards

# Ejemplo de uso
if __name__ == "__main__":
    import asyncio
    
    async def demo():
        p2e = PlayToEarnSystem()
        
        # Calcular recompensa de partida
        match_reward = p2e.calculate_match_reward(
            placement=1,
            total_players=100,
            kills=12,
            damage_dealt=2500,
            survival_time=900
        )
        print(f"💰 Recompensa de partida: {match_reward} EVT tokens")
        
        # Generar NFT drop
        nft = p2e.generate_nft_drop(player_level=25, achievement_type="victory_royale")
        if nft:
            print(f"\n🎁 ¡NFT Drop!")
            print(f"Nombre: {nft.name}")
            print(f"Rareza: {nft.rarity}")
            print(f"Valor: {nft.value_in_tokens} EVT")
        
        # Simular torneo
        standings = [
            {"placement": 1, "wallet_address": "0xPlayer1", "username": "ProGamer1"},
            {"placement": 2, "wallet_address": "0xPlayer2", "username": "ElitePlayer2"},
            {"placement": 3, "wallet_address": "0xPlayer3", "username": "Champion3"}
        ]
        
        print("\n🏆 Distribuyendo premios de torneo...")
        rewards = await p2e.process_tournament_rewards("tournament_001", standings)
        
        for reward in rewards:
            print(f"✅ {reward.amount} EVT enviados a {reward.wallet_address[:10]}...")
    
    asyncio.run(demo())

