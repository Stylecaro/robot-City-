using UnityEngine;
using Photon.Pun;
using System.Collections.Generic;

namespace BattleArena.AI
{
    /// <summary>
    /// Sistema de Bots AI para llenar partidas y dar oportunidades de práctica
    /// </summary>
    public class BotManager : MonoBehaviourPunCallbacks
    {
        [Header("Bot Configuration")]
        public int maxBots = 50;
        public bool autoFillWithBots = true;
        public float botSkillLevel = 0.5f; // 0-1 (0 = fácil, 1 = experto)
        
        [Header("Bot Prefabs")]
        public GameObject humanoidBotPrefab;
        public GameObject terminatorBotPrefab;
        public GameObject combatDronePrefab;
        
        [Header("Bot AI Settings")]
        public float reactionTime = 0.5f;
        public float aimAccuracy = 0.7f;
        public float aggressiveness = 0.6f;
        
        private List<BattleBot> activeBots = new List<BattleBot>();
        private BattleArenaManager arenaManager;
        
        void Start()
        {
            arenaManager = GetComponent<BattleArenaManager>();
        }
        
        public void SpawnBots(int count)
        {
            if (!PhotonNetwork.IsMasterClient) return;
            
            for (int i = 0; i < count; i++)
            {
                SpawnRandomBot();
            }
            
            Debug.Log($"🤖 {count} bots spawneados");
        }
        
        void SpawnRandomBot()
        {
            // Seleccionar tipo aleatorio
            BotType botType = (BotType)Random.Range(0, 3);
            GameObject prefab = GetBotPrefab(botType);
            
            if (prefab == null) return;
            
            // Spawn en punto aleatorio
            Transform spawnPoint = arenaManager.spawnPoints[Random.Range(0, arenaManager.spawnPoints.Length)];
            GameObject botObj = PhotonNetwork.Instantiate(
                prefab.name,
                spawnPoint.position,
                spawnPoint.rotation
            );
            
            BattleBot bot = botObj.GetComponent<BattleBot>();
            if (bot != null)
            {
                bot.botType = botType;
                bot.skillLevel = botSkillLevel;
                bot.playerName = GenerateBotName(botType);
                activeBots.Add(bot);
            }
        }
        
        GameObject GetBotPrefab(BotType type)
        {
            switch (type)
            {
                case BotType.HumanoidBot:
                    return humanoidBotPrefab;
                case BotType.Terminator:
                    return terminatorBotPrefab;
                case BotType.CombatDrone:
                    return combatDronePrefab;
                default:
                    return humanoidBotPrefab;
            }
        }
        
        string GenerateBotName(BotType type)
        {
            string[] humanoidNames = { "Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot" };
            string[] terminatorNames = { "T-800", "T-1000", "T-X", "Rev-9", "T-3000" };
            string[] droneNames = { "Drone-01", "Drone-02", "Drone-03", "Reaper-1", "Predator-1" };
            
            switch (type)
            {
                case BotType.HumanoidBot:
                    return "Bot-" + humanoidNames[Random.Range(0, humanoidNames.Length)];
                case BotType.Terminator:
                    return terminatorNames[Random.Range(0, terminatorNames.Length)];
                case BotType.CombatDrone:
                    return droneNames[Random.Range(0, droneNames.Length)];
                default:
                    return "Bot-" + Random.Range(1000, 9999);
            }
        }
        
        public void RemoveBot(BattleBot bot)
        {
            activeBots.Remove(bot);
            PhotonNetwork.Destroy(bot.gameObject);
        }
        
        public void RemoveAllBots()
        {
            foreach (BattleBot bot in activeBots.ToArray())
            {
                PhotonNetwork.Destroy(bot.gameObject);
            }
            activeBots.Clear();
        }
    }
    
    public enum BotType
    {
        HumanoidBot,    // Bot humanoide básico
        Terminator,     // Robot de combate avanzado
        CombatDrone     // Dron volador
    }
}
