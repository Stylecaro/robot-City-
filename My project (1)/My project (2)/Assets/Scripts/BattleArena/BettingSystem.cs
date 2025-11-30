using UnityEngine;
using Photon.Pun;
using System.Collections;

namespace BattleArena
{
    /// <summary>
    /// Sistema de apuestas: jugadores deben depositar cripto para participar
    /// El pool se usa para gastos operativos y premios
    /// </summary>
    public class BettingSystem : MonoBehaviourPunCallbacks
    {
        [Header("Entry Fees")]
        public float casualMatchFee = 0f;      // Gratis
        public float rankedMatchFee = 10f;     // 10 EVT
        public float tournamentFee = 50f;      // 50 EVT
        public float highStakesFee = 100f;     // 100 EVT
        
        [Header("Prize Pool Distribution")]
        [Range(0f, 1f)] public float prizePoolPercentage = 0.70f;    // 70% para premios
        [Range(0f, 1f)] public float operatingCostPercentage = 0.25f; // 25% gastos
        [Range(0f, 1f)] public float platformFeePercentage = 0.05f;   // 5% comisión
        
        [Header("Current Match Pool")]
        public float currentPrizePool = 0f;
        public float operatingFunds = 0f;
        public float platformFees = 0f;
        
        private BattleArenaManager arenaManager;
        private CryptoWalletSystem walletSystem;
        
        void Start()
        {
            arenaManager = GetComponent<BattleArenaManager>();
            walletSystem = FindObjectOfType<CryptoWalletSystem>();
        }
        
        /// <summary>
        /// Cobrar entrada a jugador antes de unirse a partida
        /// </summary>
        public IEnumerator ChargeEntryFee(BattlePlayer player, float entryFee)
        {
            if (entryFee == 0f)
            {
                // Partida gratis, permitir entrada
                yield return true;
            }
            
            Debug.Log($"💰 Cobrando {entryFee} EVT a {player.playerName}");
            
            // Verificar que el jugador tenga suficientes fondos
            float playerBalance = yield return StartCoroutine(
                walletSystem.GetBalance(player.walletAddress)
            );
            
            if (playerBalance < entryFee)
            {
                Debug.LogWarning($"❌ {player.playerName} no tiene fondos suficientes");
                ShowInsufficientFundsMessage(player);
                yield return false;
            }
            
            // Cobrar entrada
            bool success = yield return StartCoroutine(
                walletSystem.DeductTokens(player.walletAddress, entryFee)
            );
            
            if (success)
            {
                // Distribuir fondos
                float prizeAmount = entryFee * prizePoolPercentage;
                float operatingAmount = entryFee * operatingCostPercentage;
                float feeAmount = entryFee * platformFeePercentage;
                
                currentPrizePool += prizeAmount;
                operatingFunds += operatingAmount;
                platformFees += feeAmount;
                
                Debug.Log($"✅ Entrada pagada. Pool actual: {currentPrizePool} EVT");
                
                // Registrar apuesta del jugador
                player.entryFeePaid = entryFee;
                
                yield return true;
            }
            else
            {
                Debug.LogError($"❌ Error al cobrar entrada a {player.playerName}");
                yield return false;
            }
        }
        
        /// <summary>
        /// Distribuir premios al finalizar partida
        /// </summary>
        public IEnumerator DistributePrizes(BattlePlayer[] topPlayers)
        {
            Debug.Log($"🏆 Distribuyendo {currentPrizePool} EVT entre {topPlayers.Length} ganadores");
            
            // Distribución de premios (estilo battle royale)
            float[] distribution = new float[]
            {
                0.40f,  // 1er lugar: 40%
                0.25f,  // 2do lugar: 25%
                0.15f,  // 3er lugar: 15%
                0.08f,  // 4to lugar: 8%
                0.05f,  // 5to lugar: 5%
                0.03f,  // 6to lugar: 3%
                0.02f,  // 7mo lugar: 2%
                0.02f   // 8vo lugar: 2%
            };
            
            for (int i = 0; i < topPlayers.Length && i < distribution.Length; i++)
            {
                BattlePlayer player = topPlayers[i];
                float prize = currentPrizePool * distribution[i];
                
                // Enviar premio
                yield return StartCoroutine(
                    walletSystem.SendTokens(player.walletAddress, prize)
                );
                
                Debug.Log($"💰 {player.playerName} ganó {prize} EVT (puesto #{i + 1})");
                
                // Notificar al jugador
                photonView.RPC("RPC_NotifyPrize", player.photonView.Owner, prize, i + 1);
            }
            
            // Resetear pool
            currentPrizePool = 0f;
        }
        
        [PunRPC]
        void RPC_NotifyPrize(float amount, int placement)
        {
            Debug.Log($"🎉 ¡Ganaste {amount} EVT! (Puesto #{placement})");
            // Mostrar UI de premio
        }
        
        void ShowInsufficientFundsMessage(BattlePlayer player)
        {
            if (photonView.IsMine)
            {
                // Mostrar mensaje de error
                Debug.LogWarning("⚠️ Fondos insuficientes para unirse a esta partida");
                // TODO: Mostrar UI con opción de comprar tokens
            }
        }
        
        /// <summary>
        /// Obtener fee según tipo de partida
        /// </summary>
        public float GetEntryFee(BattleArenaManager.ArenaType arenaType)
        {
            switch (arenaType)
            {
                case BattleArenaManager.ArenaType.BattleRoyale:
                    return rankedMatchFee;
                    
                case BattleArenaManager.ArenaType.TeamDeathmatch:
                    return casualMatchFee;
                    
                case BattleArenaManager.ArenaType.CaptureTheFlag:
                    return casualMatchFee;
                    
                case BattleArenaManager.ArenaType.Survival:
                    return highStakesFee;
                    
                default:
                    return casualMatchFee;
            }
        }
    }
}

