using UnityEngine;
using UnityEngine.UI;
using Photon.Pun;
using System.Collections.Generic;

namespace BattleArena.Avatar
{
    /// <summary>
    /// Tienda de trajes de robot
    /// Los jugadores pueden comprar con EVT tokens
    /// </summary>
    public class RobotSuitShop : MonoBehaviourPunCallbacks
    {
        [Header("UI References")]
        public GameObject shopPanel;
        public Transform suitListContainer;
        public GameObject suitItemPrefab;
        public Text playerBalanceText;
        
        [Header("Shop Inventory")]
        public List<RobotSuit> availableSuits = new List<RobotSuit>();
        
        private CryptoWalletSystem walletSystem;
        private RobotSuitSystem playerSuitSystem;
        
        void Start()
        {
            walletSystem = FindObjectOfType<CryptoWalletSystem>();
            InitializeShop();
        }
        
        void InitializeShop()
        {
            // Crear catálogo de trajes
            CreateSuitCatalog();
            
            // Poblar UI
            PopulateShopUI();
        }
        
        void CreateSuitCatalog()
        {
            availableSuits.Clear();
            
            // SMALL SUITS
            availableSuits.Add(new RobotSuit
            {
                suitName = "Scout Nano",
                suitType = RobotSuitType.LightScout,
                size = RobotSuitSize.Small,
                rarity = RobotSuitRarity.Common,
                healthBonus = 0.8f,
                speedModifier = 1.4f,
                damageBonus = 0.9f,
                jumpBonus = 1.5f,
                specialAbilities = new List<string> { "double_jump", "dash" },
                priceEVT = 50f
            });
            
            availableSuits.Add(new RobotSuit
            {
                suitName = "Stealth Micro",
                suitType = RobotSuitType.StealthAssassin,
                size = RobotSuitSize.Small,
                rarity = RobotSuitRarity.Rare,
                healthBonus = 0.7f,
                speedModifier = 1.6f,
                damageBonus = 1.3f,
                jumpBonus = 1.3f,
                specialAbilities = new List<string> { "invisibility", "silent_movement" },
                priceEVT = 200f
            });
            
            // MEDIUM SUITS
            availableSuits.Add(new RobotSuit
            {
                suitName = "Combat Warrior",
                suitType = RobotSuitType.MediumWarrior,
                size = RobotSuitSize.Medium,
                rarity = RobotSuitRarity.Uncommon,
                healthBonus = 1.2f,
                armorBonus = 25f,
                speedModifier = 1.0f,
                damageBonus = 1.2f,
                jumpBonus = 1.0f,
                specialAbilities = new List<string> { "shield_boost", "melee_damage" },
                priceEVT = 100f
            });
            
            availableSuits.Add(new RobotSuit
            {
                suitName = "Speed Runner X",
                suitType = RobotSuitType.SpeedRunner,
                size = RobotSuitSize.Medium,
                rarity = RobotSuitRarity.Rare,
                healthBonus = 1.0f,
                speedModifier = 1.8f,
                damageBonus = 1.0f,
                jumpBonus = 1.2f,
                specialAbilities = new List<string> { "sprint_boost", "slide" },
                priceEVT = 250f
            });
            
            // LARGE SUITS
            availableSuits.Add(new RobotSuit
            {
                suitName = "Heavy Tank MK-II",
                suitType = RobotSuitType.HeavyTank,
                size = RobotSuitSize.Large,
                rarity = RobotSuitRarity.Epic,
                healthBonus = 2.0f,
                armorBonus = 100f,
                speedModifier = 0.7f,
                damageBonus = 1.5f,
                jumpBonus = 0.6f,
                specialAbilities = new List<string> { "damage_resistance", "ground_pound" },
                priceEVT = 500f
            });
            
            availableSuits.Add(new RobotSuit
            {
                suitName = "Assault Juggernaut",
                suitType = RobotSuitType.Juggernaut,
                size = RobotSuitSize.Large,
                rarity = RobotSuitRarity.Epic,
                healthBonus = 2.5f,
                armorBonus = 150f,
                speedModifier = 0.6f,
                damageBonus = 2.0f,
                jumpBonus = 0.5f,
                specialAbilities = new List<string> { "unstoppable", "knockback_immunity" },
                priceEVT = 750f
            });
            
            // EXTRA LARGE SUITS
            availableSuits.Add(new RobotSuit
            {
                suitName = "Mega Destroyer",
                suitType = RobotSuitType.MegaMech,
                size = RobotSuitSize.ExtraLarge,
                rarity = RobotSuitRarity.Legendary,
                healthBonus = 3.0f,
                armorBonus = 200f,
                speedModifier = 0.5f,
                damageBonus = 2.5f,
                jumpBonus = 0.4f,
                specialAbilities = new List<string> { "rocket_launcher", "missile_barrage", "emp_blast" },
                priceEVT = 1500f
            });
            
            // GIANT SUITS
            availableSuits.Add(new RobotSuit
            {
                suitName = "Titan Colossus",
                suitType = RobotSuitType.MegaMech,
                size = RobotSuitSize.Giant,
                rarity = RobotSuitRarity.Mythic,
                healthBonus = 5.0f,
                armorBonus = 500f,
                speedModifier = 0.3f,
                damageBonus = 4.0f,
                jumpBonus = 0.2f,
                specialAbilities = new List<string> { "building_crush", "earthquake", "laser_cannon", "force_field" },
                priceEVT = 5000f,
                isNFT = true
            });
            
            // SPECIAL SUITS
            availableSuits.Add(new RobotSuit
            {
                suitName = "Sky Drone Elite",
                suitType = RobotSuitType.FlyingDrone,
                size = RobotSuitSize.Medium,
                rarity = RobotSuitRarity.Legendary,
                healthBonus = 1.0f,
                armorBonus = 50f,
                speedModifier = 2.0f,
                damageBonus = 1.3f,
                jumpBonus = 3.0f,
                specialAbilities = new List<string> { "flight", "aerial_strike", "jetpack" },
                priceEVT = 2000f
            });
            
            availableSuits.Add(new RobotSuit
            {
                suitName = "Cyber Hacker",
                suitType = RobotSuitType.TechHacker,
                size = RobotSuitSize.Medium,
                rarity = RobotSuitRarity.Epic,
                healthBonus = 1.0f,
                speedModifier = 1.2f,
                damageBonus = 1.0f,
                jumpBonus = 1.0f,
                specialAbilities = new List<string> { "hack_turrets", "disable_vehicles", "scan_enemies" },
                priceEVT = 800f
            });
            
            Debug.Log($"🛒 Tienda inicializada con {availableSuits.Count} trajes");
        }
        
        void PopulateShopUI()
        {
            // Limpiar lista
            foreach (Transform child in suitListContainer)
            {
                Destroy(child.gameObject);
            }
            
            // Crear items
            foreach (RobotSuit suit in availableSuits)
            {
                GameObject item = Instantiate(suitItemPrefab, suitListContainer);
                
                // Configurar UI del item
                Text nameText = item.transform.Find("Name").GetComponent<Text>();
                Text priceText = item.transform.Find("Price").GetComponent<Text>();
                Text statsText = item.transform.Find("Stats").GetComponent<Text>();
                Button buyButton = item.transform.Find("BuyButton").GetComponent<Button>();
                
                nameText.text = $"{suit.suitName} ({suit.size})";
                priceText.text = $"{suit.priceEVT} EVT";
                statsText.text = $"HP: +{(suit.healthBonus - 1) * 100}% | DMG: +{(suit.damageBonus - 1) * 100}% | SPD: {suit.speedModifier}x";
                
                // Color según rareza
                nameText.color = GetRarityColor(suit.rarity);
                
                // Listener del botón
                buyButton.onClick.AddListener(() => PurchaseSuit(suit));
            }
        }
        
        Color GetRarityColor(RobotSuitRarity rarity)
        {
            switch (rarity)
            {
                case RobotSuitRarity.Common:
                    return Color.gray;
                case RobotSuitRarity.Uncommon:
                    return Color.green;
                case RobotSuitRarity.Rare:
                    return Color.blue;
                case RobotSuitRarity.Epic:
                    return new Color(0.6f, 0, 1); // Púrpura
                case RobotSuitRarity.Legendary:
                    return new Color(1, 0.5f, 0); // Naranja
                case RobotSuitRarity.Mythic:
                    return new Color(1, 0, 0); // Rojo
                default:
                    return Color.white;
            }
        }
        
        public void PurchaseSuit(RobotSuit suit)
        {
            // Verificar balance
            if (walletSystem == null)
            {
                Debug.LogError("❌ Sistema de wallet no encontrado");
                return;
            }
            
            float playerBalance = walletSystem.GetBalance();
            
            if (playerBalance < suit.priceEVT)
            {
                Debug.Log($"❌ Balance insuficiente. Necesitas {suit.priceEVT} EVT (Tienes: {playerBalance})");
                ShowMessage($"Balance insuficiente. Necesitas {suit.priceEVT} EVT");
                return;
            }
            
            // Deducir tokens
            bool success = walletSystem.DeductTokens(suit.priceEVT);
            
            if (success)
            {
                // Añadir traje al inventario del jugador
                AddSuitToInventory(suit);
                
                Debug.Log($"✅ Traje comprado: {suit.suitName} por {suit.priceEVT} EVT");
                ShowMessage($"¡Compra exitosa! {suit.suitName}");
                
                // Equipar automáticamente si no tiene uno
                BattlePlayer player = FindObjectOfType<BattlePlayer>();
                if (player != null)
                {
                    RobotSuitSystem suitSystem = player.GetComponent<RobotSuitSystem>();
                    if (suitSystem != null && !suitSystem.isWearingSuit)
                    {
                        suitSystem.EquipSuit(suit);
                    }
                }
            }
        }
        
        void AddSuitToInventory(RobotSuit suit)
        {
            // Guardar en inventario del jugador
            PlayerInventory inventory = FindObjectOfType<PlayerInventory>();
            if (inventory != null)
            {
                inventory.AddRobotSuit(suit);
            }
        }
        
        void ShowMessage(string message)
        {
            // Mostrar mensaje temporal
            Debug.Log($"📢 {message}");
        }
        
        public void OpenShop()
        {
            shopPanel.SetActive(true);
            UpdateBalanceDisplay();
        }
        
        public void CloseShop()
        {
            shopPanel.SetActive(false);
        }
        
        void UpdateBalanceDisplay()
        {
            if (walletSystem != null && playerBalanceText != null)
            {
                float balance = walletSystem.GetBalance();
                playerBalanceText.text = $"Balance: {balance} EVT";
            }
        }
    }
}
