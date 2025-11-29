using UnityEngine;
using Photon.Pun;
using System.Collections.Generic;

namespace BattleArena.Avatar
{
    /// <summary>
    /// Sistema de trajes de robot comprables para avatares
    /// Diferentes tamaños y habilidades
    /// </summary>
    public class RobotSuitSystem : MonoBehaviourPunCallbacks
    {
        [Header("Player Reference")]
        public BattlePlayer player;
        
        [Header("Current Suit")]
        public RobotSuit currentSuit;
        public bool isWearingSuit = false;
        
        [Header("Suit Stats Multipliers")]
        private float healthMultiplier = 1f;
        private float speedMultiplier = 1f;
        private float damageMultiplier = 1f;
        private float jumpMultiplier = 1f;
        
        private GameObject suitModel;
        private RobotSuitType equippedSuitType;
        
        void Start()
        {
            player = GetComponent<BattlePlayer>();
        }
        
        public void EquipSuit(RobotSuit suit)
        {
            if (suit == null || isWearingSuit) return;
            
            currentSuit = suit;
            equippedSuitType = suit.suitType;
            isWearingSuit = true;
            
            // Aplicar stats del traje
            ApplySuitStats(suit);
            
            // Instanciar modelo visual
            SpawnSuitModel(suit);
            
            photonView.RPC("RPC_EquipSuit", RpcTarget.All, (int)suit.suitType);
            
            Debug.Log($"🤖 Traje equipado: {suit.suitName} (Tamaño: {suit.size})");
        }
        
        void ApplySuitStats(RobotSuit suit)
        {
            // Multiplicadores según el traje
            healthMultiplier = suit.healthBonus;
            speedMultiplier = suit.speedModifier;
            damageMultiplier = suit.damageBonus;
            jumpMultiplier = suit.jumpBonus;
            
            // Aplicar al jugador
            if (player != null)
            {
                player.maxHealth *= healthMultiplier;
                player.health = player.maxHealth;
                player.armor += suit.armorBonus;
            }
        }
        
        void SpawnSuitModel(RobotSuit suit)
        {
            // Cargar prefab del traje
            string prefabPath = $"RobotSuits/{suit.suitType}";
            GameObject suitPrefab = Resources.Load<GameObject>(prefabPath);
            
            if (suitPrefab != null)
            {
                suitModel = Instantiate(suitPrefab, transform);
                suitModel.transform.localPosition = Vector3.zero;
                suitModel.transform.localScale = GetSuitScale(suit.size);
            }
        }
        
        Vector3 GetSuitScale(RobotSuitSize size)
        {
            switch (size)
            {
                case RobotSuitSize.Small:
                    return Vector3.one * 0.8f;
                case RobotSuitSize.Medium:
                    return Vector3.one * 1.0f;
                case RobotSuitSize.Large:
                    return Vector3.one * 1.5f;
                case RobotSuitSize.ExtraLarge:
                    return Vector3.one * 2.0f;
                case RobotSuitSize.Giant:
                    return Vector3.one * 3.0f;
                default:
                    return Vector3.one;
            }
        }
        
        public void RemoveSuit()
        {
            if (!isWearingSuit) return;
            
            // Revertir stats
            if (player != null)
            {
                player.maxHealth /= healthMultiplier;
                player.health = Mathf.Min(player.health, player.maxHealth);
                player.armor -= currentSuit.armorBonus;
            }
            
            // Destruir modelo
            if (suitModel != null)
            {
                Destroy(suitModel);
            }
            
            isWearingSuit = false;
            currentSuit = null;
            
            photonView.RPC("RPC_RemoveSuit", RpcTarget.All);
            
            Debug.Log("🤖 Traje removido");
        }
        
        [PunRPC]
        void RPC_EquipSuit(int suitTypeInt)
        {
            // Sincronizar visual para otros jugadores
            RobotSuitType suitType = (RobotSuitType)suitTypeInt;
            // Actualizar visual
        }
        
        [PunRPC]
        void RPC_RemoveSuit()
        {
            // Sincronizar remoción
        }
        
        public float GetDamageMultiplier()
        {
            return isWearingSuit ? damageMultiplier : 1f;
        }
        
        public float GetSpeedMultiplier()
        {
            return isWearingSuit ? speedMultiplier : 1f;
        }
        
        public bool HasSpecialAbility(string abilityName)
        {
            if (!isWearingSuit || currentSuit == null) return false;
            return currentSuit.specialAbilities.Contains(abilityName);
        }
    }
    
    [System.Serializable]
    public class RobotSuit
    {
        public string suitName;
        public RobotSuitType suitType;
        public RobotSuitSize size;
        public RobotSuitRarity rarity;
        
        [Header("Stats")]
        public float healthBonus = 1.0f;
        public float armorBonus = 0f;
        public float speedModifier = 1.0f;
        public float damageBonus = 1.0f;
        public float jumpBonus = 1.0f;
        
        [Header("Special Abilities")]
        public List<string> specialAbilities = new List<string>();
        
        [Header("Economy")]
        public float priceEVT = 100f;
        public bool isNFT = false;
        public string nftTokenId = "";
    }
    
    public enum RobotSuitType
    {
        LightScout,          // Scout ligero
        MediumWarrior,       // Guerrero medio
        HeavyTank,           // Tanque pesado
        StealthAssassin,     // Asesino sigiloso
        FlyingDrone,         // Dron volador
        MegaMech,            // Mech gigante
        SpeedRunner,         // Corredor veloz
        Juggernaut,          // Imparable
        TechHacker,          // Hacker tecnológico
        ElementalMage        // Mago elemental (futuro)
    }
    
    public enum RobotSuitSize
    {
        Small,       // 0.8x - Pequeño, ágil
        Medium,      // 1.0x - Tamaño normal
        Large,       // 1.5x - Grande, resistente
        ExtraLarge,  // 2.0x - Extra grande
        Giant        // 3.0x - Gigante
    }
    
    public enum RobotSuitRarity
    {
        Common,      // Común - Fácil de encontrar
        Uncommon,    // Poco común
        Rare,        // Raro
        Epic,        // Épico
        Legendary,   // Legendario
        Mythic       // Mítico - Extremadamente raro
    }
}
