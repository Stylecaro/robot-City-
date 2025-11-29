// Spatial.io TypeScript Script para Battle Arena
// Compatible con Spatial SDK

import { SpatialComponentSystem } from '@spatial/spatial-scripting';

// Configuración del Arena
export const ArenaConfig = {
  maxPlayers: 50,
  mapSize: 3000,
  safeZoneRadius: 1500,
  shrinkInterval: 45,
  damagePerSecond: 10,
  tokenContract: '0x...', // Dirección del contrato MVT
  nftContract: '0x...'   // Dirección del contrato NFT
};

// Sistema de combate para Spatial.io
export class BattleArenaSystem extends SpatialComponentSystem {
  private activePlayers: Map<string, PlayerData> = new Map();
  private currentSafeZoneRadius: number = ArenaConfig.safeZoneRadius;
  private matchStarted: boolean = false;
  private nextZoneShrink: number = 0;
  
  init() {
    console.log('🎮 Battle Arena System inicializado');
    this.setupEventListeners();
  }
  
  setupEventListeners() {
    // Evento cuando un jugador se une
    this.onPlayerJoined((player) => {
      this.addPlayer(player);
    });
    
    // Evento cuando un jugador se va
    this.onPlayerLeft((player) => {
      this.removePlayer(player.id);
    });
    
    // Evento de disparo
    this.onPlayerShoot((player, target, damage) => {
      this.handleDamage(target, damage, player);
    });
  }
  
  update(deltaTime: number) {
    if (!this.matchStarted) {
      this.checkMatchStart();
      return;
    }
    
    // Actualizar zona segura
    this.updateSafeZone(deltaTime);
    
    // Aplicar daño de zona
    this.applyZoneDamage();
    
    // Verificar victoria
    this.checkVictory();
  }
  
  addPlayer(player: any) {
    const playerData: PlayerData = {
      id: player.id,
      name: player.name,
      walletAddress: player.customData?.wallet || '',
      health: 100,
      armor: 0,
      kills: 0,
      deaths: 0,
      damageDealt: 0,
      isAlive: true,
      position: player.position,
      team: null
    };
    
    this.activePlayers.set(player.id, playerData);
    
    console.log(`✅ Jugador ${player.name} se unió. Total: ${this.activePlayers.size}`);
    
    // Spawnar jugador en posición aleatoria
    this.spawnPlayer(player);
  }
  
  removePlayer(playerId: string) {
    this.activePlayers.delete(playerId);
    console.log(`❌ Jugador salió. Quedan: ${this.activePlayers.size}`);
  }
  
  spawnPlayer(player: any) {
    // Generar posición de spawn aleatoria dentro del mapa
    const spawnPos = this.getRandomSpawnPosition();
    player.teleport(spawnPos);
    
    // Equipar arma inicial
    this.giveStarterWeapon(player);
  }
  
  getRandomSpawnPosition(): { x: number, y: number, z: number } {
    const angle = Math.random() * Math.PI * 2;
    const distance = Math.random() * ArenaConfig.mapSize * 0.8;
    
    return {
      x: Math.cos(angle) * distance,
      y: 50, // Altura de spawn
      z: Math.sin(angle) * distance
    };
  }
  
  giveStarterWeapon(player: any) {
    // Dar pistola básica al inicio
    player.inventory.add({
      type: 'weapon',
      id: 'starter_pistol',
      damage: 15,
      fireRate: 300,
      ammo: 50
    });
  }
  
  checkMatchStart() {
    const playerCount = this.activePlayers.size;
    
    if (playerCount >= ArenaConfig.maxPlayers * 0.5 && !this.matchStarted) {
      this.startMatch();
    }
  }
  
  startMatch() {
    this.matchStarted = true;
    this.nextZoneShrink = Date.now() + (ArenaConfig.shrinkInterval * 1000);
    
    console.log('🎮 ¡BATALLA INICIADA!');
    
    // Notificar a todos los jugadores
    this.broadcastMessage('¡La batalla ha comenzado! Sobrevive y gana criptomonedas', 'success');
  }
  
  updateSafeZone(deltaTime: number) {
    const now = Date.now();
    
    if (now >= this.nextZoneShrink && this.currentSafeZoneRadius > 50) {
      // Reducir zona
      this.currentSafeZoneRadius -= 50;
      this.nextZoneShrink = now + (ArenaConfig.shrinkInterval * 1000);
      
      // Actualizar visual de la zona
      this.updateSafeZoneVisual();
      
      // Notificar
      this.broadcastMessage(
        `⚠️ Zona segura reducida a ${this.currentSafeZoneRadius}m`,
        'warning'
      );
    }
  }
  
  updateSafeZoneVisual() {
    // Actualizar shader/mesh de la zona segura
    const safeZone = this.getObjectByName('SafeZone');
    if (safeZone) {
      safeZone.scale.set(
        this.currentSafeZoneRadius * 2,
        500,
        this.currentSafeZoneRadius * 2
      );
    }
  }
  
  applyZoneDamage() {
    this.activePlayers.forEach((playerData, playerId) => {
      if (!playerData.isAlive) return;
      
      const player = this.getPlayerById(playerId);
      if (!player) return;
      
      // Calcular distancia al centro
      const distance = this.getDistanceToCenter(player.position);
      
      // Si está fuera de la zona, aplicar daño
      if (distance > this.currentSafeZoneRadius) {
        this.damagePlayer(playerData, ArenaConfig.damagePerSecond * 0.016, 'Storm');
      }
    });
  }
  
  getDistanceToCenter(position: any): number {
    return Math.sqrt(position.x ** 2 + position.z ** 2);
  }
  
  handleDamage(targetId: string, damage: number, attackerId: string) {
    const targetData = this.activePlayers.get(targetId);
    const attackerData = this.activePlayers.get(attackerId);
    
    if (!targetData || !attackerData) return;
    
    this.damagePlayer(targetData, damage, attackerData.name);
    
    // Registrar daño del atacante
    attackerData.damageDealt += damage;
    
    // Verificar muerte
    if (targetData.health <= 0 && targetData.isAlive) {
      this.eliminatePlayer(targetData, attackerData);
    }
  }
  
  damagePlayer(playerData: PlayerData, damage: number, source: string) {
    // Aplicar daño a armadura primero
    if (playerData.armor > 0) {
      const armorDamage = Math.min(damage, playerData.armor);
      playerData.armor -= armorDamage;
      damage -= armorDamage;
    }
    
    // Aplicar daño a salud
    playerData.health -= damage;
    
    // Actualizar UI
    this.updatePlayerHealthUI(playerData);
  }
  
  updatePlayerHealthUI(playerData: PlayerData) {
    const player = this.getPlayerById(playerData.id);
    if (player) {
      player.setCustomData('health', playerData.health);
      player.setCustomData('armor', playerData.armor);
    }
  }
  
  eliminatePlayer(victim: PlayerData, killer: PlayerData) {
    victim.isAlive = false;
    victim.deaths++;
    killer.kills++;
    
    console.log(`💀 ${victim.name} eliminado por ${killer.name}`);
    
    // Notificar eliminación
    this.broadcastMessage(
      `💀 ${victim.name} eliminado por ${killer.name}`,
      'info'
    );
    
    // Recompensa por kill
    this.rewardKill(killer);
    
    // Teleport a área de espectadores
    const victimPlayer = this.getPlayerById(victim.id);
    if (victimPlayer) {
      victimPlayer.teleport({ x: 0, y: 1000, z: 0 });
    }
  }
  
  async rewardKill(killer: PlayerData) {
    const killReward = 25; // MVT tokens por kill
    
    if (killer.walletAddress) {
      try {
        // Enviar recompensa (integración con blockchain)
        await this.sendTokenReward(killer.walletAddress, killReward);
        
        console.log(`💰 ${killer.name} ganó ${killReward} MVT por el kill`);
      } catch (error) {
        console.error('Error enviando recompensa:', error);
      }
    }
  }
  
  checkVictory() {
    const alivePlayers = Array.from(this.activePlayers.values())
      .filter(p => p.isAlive);
    
    if (alivePlayers.length === 1) {
      // ¡Tenemos un ganador!
      const winner = alivePlayers[0];
      this.declareWinner(winner);
    } else if (alivePlayers.length === 0) {
      this.declareDraw();
    }
  }
  
  async declareWinner(winner: PlayerData) {
    console.log(`🏆 ¡${winner.name} ES EL GANADOR!`);
    
    // Calcular recompensa
    const reward = this.calculateReward(winner);
    
    // Mostrar pantalla de victoria
    this.showVictoryScreen(winner, reward);
    
    // Distribuir recompensas
    if (winner.walletAddress) {
      await this.distributeRewards(winner, reward);
    }
    
    // Reiniciar partida después de 30 segundos
    setTimeout(() => this.resetMatch(), 30000);
  }
  
  calculateReward(player: PlayerData): number {
    let reward = 1000; // Recompensa base por victoria
    reward += player.kills * 25;
    reward += player.damageDealt * 0.1;
    
    // Multiplicador por tamaño de partida
    const sizeMultiplier = Math.min(this.activePlayers.size / 25, 2);
    reward *= sizeMultiplier;
    
    return Math.floor(reward);
  }
  
  showVictoryScreen(winner: PlayerData, reward: number) {
    this.broadcastMessage(
      `🏆 ¡${winner.name} GANÓ!\n💰 Recompensa: ${reward} MVT\n💀 Kills: ${winner.kills}`,
      'success'
    );
  }
  
  async distributeRewards(winner: PlayerData, amount: number) {
    try {
      // Enviar tokens ERC20
      await this.sendTokenReward(winner.walletAddress, amount);
      
      // Posibilidad de NFT (10% + 5% por kill)
      const nftChance = 0.10 + (winner.kills * 0.05);
      
      if (Math.random() < nftChance) {
        await this.mintNFT(winner.walletAddress, {
          name: 'Victory Badge',
          rarity: this.getNFTRarity(winner.kills),
          kills: winner.kills,
          damage: winner.damageDealt
        });
      }
    } catch (error) {
      console.error('Error distribuyendo recompensas:', error);
    }
  }
  
  getNFTRarity(kills: number): string {
    if (kills >= 100) return 'Legendary';
    if (kills >= 50) return 'Epic';
    if (kills >= 25) return 'Rare';
    return 'Common';
  }
  
  async sendTokenReward(wallet: string, amount: number) {
    // Integración con Web3
    console.log(`💰 Enviando ${amount} MVT a ${wallet}`);
    
    // Aquí iría la llamada real al smart contract
    // await tokenContract.transfer(wallet, amount);
  }
  
  async mintNFT(wallet: string, metadata: any) {
    console.log(`🎁 Minteando NFT para ${wallet}:`, metadata);
    
    // Aquí iría la llamada real al contrato NFT
    // await nftContract.mint(wallet, metadata);
  }
  
  declareDraw() {
    console.log('Partida terminada en empate');
    this.broadcastMessage('¡Empate! Todos fueron eliminados', 'info');
    setTimeout(() => this.resetMatch(), 30000);
  }
  
  resetMatch() {
    console.log('♻️ Reiniciando partida...');
    
    this.matchStarted = false;
    this.currentSafeZoneRadius = ArenaConfig.safeZoneRadius;
    
    // Resetear jugadores
    this.activePlayers.forEach((player, id) => {
      player.health = 100;
      player.armor = 0;
      player.kills = 0;
      player.deaths = 0;
      player.damageDealt = 0;
      player.isAlive = true;
      
      // Re-spawnar
      const playerObj = this.getPlayerById(id);
      if (playerObj) {
        this.spawnPlayer(playerObj);
      }
    });
    
    this.broadcastMessage('Nueva partida comenzando...', 'info');
  }
  
  broadcastMessage(message: string, type: string) {
    // Enviar mensaje a todos los jugadores
    this.sendGlobalMessage({
      text: message,
      type: type,
      duration: 5000
    });
  }
  
  // Métodos auxiliares (implementación depende del SDK de Spatial)
  getPlayerById(id: string): any {
    // Implementar según Spatial SDK
    return null;
  }
  
  getObjectByName(name: string): any {
    // Implementar según Spatial SDK
    return null;
  }
  
  onPlayerJoined(callback: (player: any) => void) {
    // Implementar según Spatial SDK
  }
  
  onPlayerLeft(callback: (player: any) => void) {
    // Implementar según Spatial SDK
  }
  
  onPlayerShoot(callback: (player: any, target: string, damage: number) => void) {
    // Implementar según Spatial SDK
  }
  
  sendGlobalMessage(message: any) {
    // Implementar según Spatial SDK
  }
}

// Tipos de datos
interface PlayerData {
  id: string;
  name: string;
  walletAddress: string;
  health: number;
  armor: number;
  kills: number;
  deaths: number;
  damageDealt: number;
  isAlive: boolean;
  position: { x: number, y: number, z: number };
  team: string | null;
}

// Exportar sistema
export default BattleArenaSystem;
