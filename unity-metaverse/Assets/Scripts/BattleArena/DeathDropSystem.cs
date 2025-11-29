using UnityEngine;
using Photon.Pun;
using System.Collections;
using System.Collections.Generic;

namespace BattleArena
{
    /// <summary>
    /// Sistema de Drop on Death: Cuando mueres, pierdes las criptomonedas que portabas
    /// Otros jugadores pueden recoger el botín
    /// </summary>
    public class DeathDropSystem : MonoBehaviourPunCallbacks
    {
        [Header("Drop Configuration")]
        public float dropPercentage = 1.0f;  // 100% = pierdes todo al morir
        public GameObject lootBoxPrefab;
        public float lootBoxDespawnTime = 300f; // 5 minutos
        
        [Header("Loot Settings")]
        public bool dropInventoryItems = true;
        public bool dropEquippedWeapons = true;
        public bool dropCarriedTokens = true;
        public bool dropNFTs = false; // NFTs NO se dropean por defecto
        
        private CryptoWalletSystem walletSystem;
        
        void Start()
        {
            walletSystem = FindObjectOfType<CryptoWalletSystem>();
        }
        
        /// <summary>
        /// Manejar muerte de jugador y crear loot
        /// </summary>
        public void HandlePlayerDeath(BattlePlayer victim, BattlePlayer killer)
        {
            Debug.Log($"💀 {victim.playerName} murió. Procesando drop...");
            
            // Calcular tokens a dropear
            float tokensCarried = victim.carriedTokens;
            float tokensToDrop = tokensCarried * dropPercentage;
            
            if (tokensToDrop > 0)
            {
                // Crear loot box
                CreateLootBox(victim.transform.position, tokensToDrop, victim);
                
                // Remover tokens del jugador
                victim.carriedTokens = 0;
                
                Debug.Log($"💰 {victim.playerName} dropeo {tokensToDrop} MVT");
                
                // Notificar al killer
                if (killer != null)
                {
                    photonView.RPC(
                        "RPC_NotifyLootAvailable",
                        killer.photonView.Owner,
                        tokensToDrop,
                        victim.playerName
                    );
                }
            }
            
            // Dropear items de inventario
            if (dropInventoryItems)
            {
                DropInventoryItems(victim);
            }
            
            // Transferir tokens perdidos a killer (opcional)
            if (killer != null && tokensToDrop > 0)
            {
                StartCoroutine(TransferDroppedTokens(victim, killer, tokensToDrop));
            }
        }
        
        /// <summary>
        /// Crear caja de botín en el mundo
        /// </summary>
        void CreateLootBox(Vector3 position, float tokenAmount, BattlePlayer victim)
        {
            if (lootBoxPrefab == null)
            {
                Debug.LogWarning("⚠️ Loot box prefab no asignado");
                return;
            }
            
            GameObject lootBox = PhotonNetwork.Instantiate(
                lootBoxPrefab.name,
                position + Vector3.up * 0.5f,
                Quaternion.identity
            );
            
            LootBox lootBoxComponent = lootBox.GetComponent<LootBox>();
            if (lootBoxComponent != null)
            {
                lootBoxComponent.tokenAmount = tokenAmount;
                lootBoxComponent.originalOwner = victim.playerName;
                lootBoxComponent.items = GetVictimItems(victim);
                
                // Auto-destruir después de tiempo
                Destroy(lootBox, lootBoxDespawnTime);
            }
        }
        
        /// <summary>
        /// Obtener items del jugador muerto
        /// </summary>
        List<LootItem> GetVictimItems(BattlePlayer victim)
        {
            List<LootItem> items = new List<LootItem>();
            
            // Dropear armas equipadas
            if (dropEquippedWeapons && victim.inventory != null)
            {
                foreach (WeaponController weapon in victim.inventory)
                {
                    if (weapon != null)
                    {
                        items.Add(new LootItem
                        {
                            itemType = LootItemType.Weapon,
                            itemName = weapon.weaponType.ToString(),
                            quantity = 1,
                            weaponData = new WeaponData
                            {
                                weaponType = weapon.weaponType,
                                currentAmmo = weapon.currentAmmo,
                                reserveAmmo = weapon.reserveAmmo,
                                isNFTSkin = weapon.isNFTSkin,
                                nftRarity = weapon.nftRarity
                            }
                        });
                    }
                }
            }
            
            return items;
        }
        
        void DropInventoryItems(BattlePlayer victim)
        {
            // Dropear items del inventario
            Debug.Log($"Dropeando items de {victim.playerName}");
        }
        
        /// <summary>
        /// Transferir tokens del muerto al killer
        /// </summary>
        IEnumerator TransferDroppedTokens(BattlePlayer victim, BattlePlayer killer, float amount)
        {
            Debug.Log($"💸 Transfiriendo {amount} MVT de {victim.playerName} a {killer.playerName}");
            
            // Opción 1: Transfer directo (el killer obtiene los tokens inmediatamente)
            killer.carriedTokens += amount;
            
            // Opción 2: Transfer a wallet (más realista pero requiere gas)
            // yield return StartCoroutine(
            //     walletSystem.TransferTokens(victim.walletAddress, killer.walletAddress, amount)
            // );
            
            yield return null;
        }
        
        [PunRPC]
        void RPC_NotifyLootAvailable(float amount, string victimName)
        {
            Debug.Log($"💰 ¡{victimName} dropeo {amount} MVT! Recógelo rápido");
            // Mostrar notificación en UI
        }
    }
    
    /// <summary>
    /// Componente de caja de botín
    /// </summary>
    public class LootBox : MonoBehaviourPunCallbacks
    {
        public float tokenAmount;
        public string originalOwner;
        public List<LootItem> items = new List<LootItem>();
        
        private bool isLooted = false;
        private ParticleSystem glowEffect;
        
        void Start()
        {
            // Añadir efecto visual
            glowEffect = GetComponent<ParticleSystem>();
            if (glowEffect != null)
            {
                glowEffect.Play();
            }
            
            // Rotación constante
            StartCoroutine(RotateLootBox());
        }
        
        IEnumerator RotateLootBox()
        {
            while (!isLooted)
            {
                transform.Rotate(Vector3.up, 50f * Time.deltaTime);
                yield return null;
            }
        }
        
        void OnTriggerEnter(Collider other)
        {
            if (isLooted) return;
            
            BattlePlayer player = other.GetComponent<BattlePlayer>();
            if (player != null && player.photonView.IsMine)
            {
                // Jugador recoge el botín
                CollectLoot(player);
            }
        }
        
        void CollectLoot(BattlePlayer player)
        {
            isLooted = true;
            
            Debug.Log($"🎁 {player.playerName} recogió {tokenAmount} MVT de {originalOwner}");
            
            // Añadir tokens al jugador
            player.carriedTokens += tokenAmount;
            
            // Añadir items
            foreach (LootItem item in items)
            {
                if (item.itemType == LootItemType.Weapon && item.weaponData != null)
                {
                    // Reconstruir arma
                    // player.AddWeaponFromData(item.weaponData);
                }
            }
            
            // Notificar
            photonView.RPC("RPC_LootCollected", RpcTarget.All, player.playerName, tokenAmount);
            
            // Destruir loot box
            PhotonNetwork.Destroy(gameObject);
        }
        
        [PunRPC]
        void RPC_LootCollected(string playerName, float amount)
        {
            Debug.Log($"📦 {playerName} recogió {amount} MVT del botín");
        }
    }
    
    /// <summary>
    /// Item de botín
    /// </summary>
    [System.Serializable]
    public class LootItem
    {
        public LootItemType itemType;
        public string itemName;
        public int quantity;
        public WeaponData weaponData;
    }
    
    public enum LootItemType
    {
        Weapon,
        Ammo,
        HealthPack,
        Armor,
        Token,
        NFT
    }
    
    /// <summary>
    /// Datos de arma para serializar
    /// </summary>
    [System.Serializable]
    public class WeaponData
    {
        public WeaponController.WeaponType weaponType;
        public int currentAmmo;
        public int reserveAmmo;
        public bool isNFTSkin;
        public string nftRarity;
    }
}
