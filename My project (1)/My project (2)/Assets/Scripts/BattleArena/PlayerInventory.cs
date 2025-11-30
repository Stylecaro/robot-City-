using UnityEngine;
using System.Collections.Generic;
using System.Linq;

namespace BattleArena.Avatar
{
    /// <summary>
    /// Inventario del jugador para trajes y accesorios
    /// </summary>
    public class PlayerInventory : MonoBehaviour
    {
        [Header("Inventories")]
        public List<RobotSuit> ownedSuits = new List<RobotSuit>();
        public List<HiddenAccessory> ownedAccessories = new List<HiddenAccessory>();
        
        [Header("Equipped")]
        public RobotSuit equippedSuit;
        public List<HiddenAccessory> equippedAccessories = new List<HiddenAccessory>();
        public int maxEquippedAccessories = 10;
        
        [Header("Stats")]
        public float totalHealthBonus = 0f;
        public float totalArmorBonus = 0f;
        public float totalDamageBonus = 0f;
        public float totalSpeedBonus = 0f;
        
        public void AddRobotSuit(RobotSuit suit)
        {
            ownedSuits.Add(suit);
            Debug.Log($"🎒 Traje añadido al inventario: {suit.suitName}");
            
            // Guardar en persistencia
            SaveInventory();
        }
        
        public void AddAccessory(HiddenAccessory accessory)
        {
            ownedAccessories.Add(accessory);
            Debug.Log($"🎒 Accesorio añadido: {accessory.accessoryName}");
            
            // Auto-equipar si hay espacio
            if (equippedAccessories.Count < maxEquippedAccessories)
            {
                EquipAccessory(accessory);
            }
            
            SaveInventory();
        }
        
        public void EquipAccessory(HiddenAccessory accessory)
        {
            if (equippedAccessories.Count >= maxEquippedAccessories)
            {
                Debug.Log("❌ No hay espacio para más accesorios");
                return;
            }
            
            equippedAccessories.Add(accessory);
            
            // Aplicar stats
            totalHealthBonus += accessory.statBonus.healthBonus;
            totalArmorBonus += accessory.statBonus.armorBonus;
            totalDamageBonus += accessory.statBonus.damageBonus;
            totalSpeedBonus += accessory.statBonus.speedBonus;
            
            Debug.Log($"✅ Accesorio equipado: {accessory.accessoryName}");
            UpdatePlayerStats();
        }
        
        public void UnequipAccessory(HiddenAccessory accessory)
        {
            if (equippedAccessories.Remove(accessory))
            {
                // Revertir stats
                totalHealthBonus -= accessory.statBonus.healthBonus;
                totalArmorBonus -= accessory.statBonus.armorBonus;
                totalDamageBonus -= accessory.statBonus.damageBonus;
                totalSpeedBonus -= accessory.statBonus.speedBonus;
                
                UpdatePlayerStats();
            }
        }
        
        void UpdatePlayerStats()
        {
            BattlePlayer player = GetComponent<BattlePlayer>();
            if (player != null)
            {
                // Aplicar bonos acumulados
                player.maxHealth = 100 + totalHealthBonus;
                player.armor = totalArmorBonus;
            }
        }
        
        public void SaveInventory()
        {
            // Guardar en PlayerPrefs o base de datos
            PlayerPrefs.SetInt("OwnedSuitsCount", ownedSuits.Count);
            PlayerPrefs.SetInt("OwnedAccessoriesCount", ownedAccessories.Count);
            PlayerPrefs.Save();
            
            Debug.Log("💾 Inventario guardado");
        }
        
        public void LoadInventory()
        {
            // Cargar desde PlayerPrefs o base de datos
            int suitsCount = PlayerPrefs.GetInt("OwnedSuitsCount", 0);
            int accessoriesCount = PlayerPrefs.GetInt("OwnedAccessoriesCount", 0);
            
            Debug.Log($"📂 Inventario cargado: {suitsCount} trajes, {accessoriesCount} accesorios");
        }
        
        public string GetInventorySummary()
        {
            int common = ownedAccessories.Count(a => a.rarity == AccessoryRarity.Common);
            int uncommon = ownedAccessories.Count(a => a.rarity == AccessoryRarity.Uncommon);
            int rare = ownedAccessories.Count(a => a.rarity == AccessoryRarity.Rare);
            int epic = ownedAccessories.Count(a => a.rarity == AccessoryRarity.Epic);
            int legendary = ownedAccessories.Count(a => a.rarity == AccessoryRarity.Legendary);
            int mythic = ownedAccessories.Count(a => a.rarity == AccessoryRarity.Mythic);
            
            return $@"
🎒 INVENTARIO
Trajes: {ownedSuits.Count}
Accesorios: {ownedAccessories.Count}
  - Comunes: {common}
  - Poco comunes: {uncommon}
  - Raros: {rare}
  - Épicos: {epic}
  - Legendarios: {legendary}
  - Míticos: {mythic}

📊 STATS TOTALES
HP: +{totalHealthBonus}
Armor: +{totalArmorBonus}
Daño: +{totalDamageBonus * 100}%
Velocidad: +{totalSpeedBonus * 100}%
            ";
        }
    }
}
