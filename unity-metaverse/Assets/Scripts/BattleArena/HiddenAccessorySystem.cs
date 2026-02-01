using UnityEngine;
using Photon.Pun;
using System.Collections.Generic;

namespace BattleArena.Avatar;

/// <summary>
/// Sistema de accesorios ocultos en el mundo virtual
/// Los jugadores pueden encontrar items secretos explorando
/// </summary>
public class HiddenAccessorySystem : MonoBehaviourPunCallbacks
{
    [Header("Spawn Configuration")]
    public int maxHiddenAccessories = 50;
    public float respawnTime = 300f; // 5 minutos
    
    [Header("Accessory Types")]
    public GameObject[] accessoryPrefabs;
    
    private List<HiddenAccessory> spawnedAccessories = new List<HiddenAccessory>();
    private List<Vector3> hiddenLocations = new List<Vector3>();
    
    void Start()
    {
        if (PhotonNetwork.IsMasterClient)
        {
            GenerateHiddenLocations();
            SpawnAllAccessories();
        }
    }
    
    void GenerateHiddenLocations()
    {
        hiddenLocations.Clear();
        
        // Generar ubicaciones secretas
        for (int i = 0; i < maxHiddenAccessories; i++)
        {
            Vector3 location = GenerateRandomHiddenLocation();
            hiddenLocations.Add(location);
        }
        
        Debug.Log($"🔍 {maxHiddenAccessories} ubicaciones secretas generadas");
    }
    
    Vector3 GenerateRandomHiddenLocation()
    {
        // Tipos de ubicaciones secretas
        int locationType = Random.Range(0, 5);
        
        switch (locationType)
        {
            case 0: // Cueva subterránea
                return new Vector3(
                    Random.Range(-2500f, 2500f),
                    Random.Range(-50f, -10f), // Bajo tierra
                    Random.Range(-2500f, 2500f)
                );
                
            case 1: // Torre alta
                return new Vector3(
                    Random.Range(-2000f, 2000f),
                    Random.Range(50f, 150f), // Alto
                    Random.Range(-2000f, 2000f)
                );
                
            case 2: // Bajo el agua
                return new Vector3(
                    Random.Range(-1500f, 1500f),
                    Random.Range(-20f, -5f),
                    Random.Range(-1500f, 1500f)
                );
                
            case 3: // Edificio oculto
                return new Vector3(
                    Random.Range(-2000f, 2000f),
                    Random.Range(10f, 30f),
                    Random.Range(-2000f, 2000f)
                );
                
            case 4: // Zona remota
                return new Vector3(
                    Random.Range(-4000f, 4000f),
                    Random.Range(0f, 20f),
                    Random.Range(-4000f, 4000f)
                );
                
            default:
                return Vector3.zero;
        }
    }
    
    void SpawnAllAccessories()
    {
        for (int i = 0; i < hiddenLocations.Count; i++)
        {
            SpawnAccessoryAtLocation(hiddenLocations[i], i);
        }
    }
    
    void SpawnAccessoryAtLocation(Vector3 location, int index)
    {
        AccessoryType type = (AccessoryType)Random.Range(0, System.Enum.GetValues(typeof(AccessoryType)).Length);
        AccessoryRarity rarity = DetermineRarity();
        
        GameObject accessoryObj = PhotonNetwork.Instantiate(
            "HiddenAccessory",
            location,
            Quaternion.Euler(0, Random.Range(0, 360), 0)
        );
        
        HiddenAccessory accessory = accessoryObj.GetComponent<HiddenAccessory>();
        if (accessory != null)
        {
            accessory.accessoryType = type;
            accessory.rarity = rarity;
            accessory.accessoryName = GenerateAccessoryName(type, rarity);
            accessory.statBonus = GenerateStatBonus(rarity);
            accessory.locationIndex = index;
            
            spawnedAccessories.Add(accessory);
        }
        
        Debug.Log($"🎁 Accesorio oculto spawneado: {accessory.accessoryName} en {location}");
    }
    
    AccessoryRarity DetermineRarity()
    {
        float roll = Random.value;
        
        if (roll < 0.50f) return AccessoryRarity.Common;
        if (roll < 0.75f) return AccessoryRarity.Uncommon;
        if (roll < 0.90f) return AccessoryRarity.Rare;
        if (roll < 0.97f) return AccessoryRarity.Epic;
        if (roll < 0.995f) return AccessoryRarity.Legendary;
        return AccessoryRarity.Mythic;
    }
    
    string GenerateAccessoryName(AccessoryType type, AccessoryRarity rarity)
    {
        string rarityPrefix = rarity.ToString();
        
        switch (type)
        {
            case AccessoryType.Helmet:
                return $"{rarityPrefix} Casco {Random.Range(1, 100)}";
            case AccessoryType.Visor:
                return $"{rarityPrefix} Visor Táctico";
            case AccessoryType.Shoulder:
                return $"{rarityPrefix} Hombrera Blindada";
            case AccessoryType.Chest:
                return $"{rarityPrefix} Pechera de Combate";
            case AccessoryType.Arms:
                return $"{rarityPrefix} Brazaletes de Poder";
            case AccessoryType.Legs:
                return $"{rarityPrefix} Piernas Mejoradas";
            case AccessoryType.Back:
                return $"{rarityPrefix} Jetpack";
            case AccessoryType.Weapon:
                return $"{rarityPrefix} Arma Legendaria";
            case AccessoryType.Shield:
                return $"{rarityPrefix} Escudo de Energía";
            case AccessoryType.Wings:
                return $"{rarityPrefix} Alas Mecánicas";
            default:
                return "Accesorio Misterioso";
        }
    }
    
    AccessoryStats GenerateStatBonus(AccessoryRarity rarity)
    {
        float multiplier = 1f;
        
        switch (rarity)
        {
            case AccessoryRarity.Common:
                multiplier = 1.05f;
                break;
            case AccessoryRarity.Uncommon:
                multiplier = 1.15f;
                break;
            case AccessoryRarity.Rare:
                multiplier = 1.30f;
                break;
            case AccessoryRarity.Epic:
                multiplier = 1.50f;
                break;
            case AccessoryRarity.Legendary:
                multiplier = 2.00f;
                break;
            case AccessoryRarity.Mythic:
                multiplier = 3.00f;
                break;
        }
        
        return new AccessoryStats
        {
            healthBonus = Random.Range(0, 100) * multiplier,
            armorBonus = Random.Range(0, 50) * multiplier,
            damageBonus = Random.Range(0f, 0.5f) * multiplier,
            speedBonus = Random.Range(0f, 0.3f) * multiplier,
            specialAbility = rarity >= AccessoryRarity.Epic ? "special_power" : ""
        };
    }
    
    public void OnAccessoryCollected(int locationIndex)
    {
        // Respawnear después de un tiempo
        Invoke("RespawnAccessory", respawnTime);
    }
    
    void RespawnAccessory()
    {
        if (PhotonNetwork.IsMasterClient)
        {
            int randomIndex = Random.Range(0, hiddenLocations.Count);
            SpawnAccessoryAtLocation(hiddenLocations[randomIndex], randomIndex);
        }
    }
}

[System.Serializable]
public class HiddenAccessory : MonoBehaviourPunCallbacks
{
    public string accessoryName;
    public AccessoryType accessoryType;
    public AccessoryRarity rarity;
    public AccessoryStats statBonus;
    public int locationIndex;
    public bool isCollected = false;
    
    [Header("Visual Effects")]
    public ParticleSystem glowEffect;
    public Light spotLight;
    
    void Start()
    {
        // Efecto visual según rareza
        SetupVisuals();
    }
    
    void SetupVisuals()
    {
        Color rarityColor = GetRarityColor();
        
        if (glowEffect != null)
        {
            var main = glowEffect.main;
            main.startColor = rarityColor;
        }
        
        if (spotLight != null)
        {
            spotLight.color = rarityColor;
        }
    }
    
    Color GetRarityColor()
    {
        switch (rarity)
        {
            case AccessoryRarity.Common:
                return Color.gray;
            case AccessoryRarity.Uncommon:
                return Color.green;
            case AccessoryRarity.Rare:
                return Color.blue;
            case AccessoryRarity.Epic:
                return new Color(0.6f, 0, 1);
            case AccessoryRarity.Legendary:
                return new Color(1, 0.5f, 0);
            case AccessoryRarity.Mythic:
                return Color.red;
            default:
                return Color.white;
        }
    }
    
    void OnTriggerEnter(Collider other)
    {
        if (isCollected) return;
        
        BattlePlayer player = other.GetComponent<BattlePlayer>();
        if (player != null && player.photonView.IsMine)
        {
            CollectAccessory(player);
        }
    }
    
    void CollectAccessory(BattlePlayer player)
    {
        isCollected = true;
        
        // Añadir al inventario
        PlayerInventory inventory = player.GetComponent<PlayerInventory>();
        if (inventory != null)
        {
            inventory.AddAccessory(this);
        }
        
        // Aplicar stats inmediatamente
        ApplyStatsToPlayer(player);
        
        Debug.Log($"✨ {player.playerName} encontró: {accessoryName}!");
        
        // Notificar al sistema
        HiddenAccessorySystem system = FindObjectOfType<HiddenAccessorySystem>();
        if (system != null)
        {
            system.OnAccessoryCollected(locationIndex);
        }
        
        // Destruir objeto
        photonView.RPC("RPC_DestroyAccessory", RpcTarget.All);
    }
    
    void ApplyStatsToPlayer(BattlePlayer player)
    {
        player.maxHealth += statBonus.healthBonus;
        player.health = player.maxHealth;
        player.armor += statBonus.armorBonus;
    }
    
    [PunRPC]
    void RPC_DestroyAccessory()
    {
        Destroy(gameObject);
    }
}

[System.Serializable]
public struct AccessoryStats
{
    public float healthBonus;
    public float armorBonus;
    public float damageBonus;
    public float speedBonus;
    public string specialAbility;
}

public enum AccessoryType
{
    Helmet,      // Casco
    Visor,       // Visor
    Shoulder,    // Hombreras
    Chest,       // Pechera
    Arms,        // Brazos
    Legs,        // Piernas
    Back,        // Espalda (jetpack, alas)
    Weapon,      // Arma adicional
    Shield,      // Escudo
    Wings        // Alas
}

public enum AccessoryRarity
{
    Common,      // 50% - Gris
    Uncommon,    // 25% - Verde
    Rare,        // 15% - Azul
    Epic,        // 7% - Púrpura
    Legendary,   // 2.5% - Naranja
    Mythic       // 0.5% - Rojo
}
