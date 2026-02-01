using UnityEngine;
using Photon.Pun;

namespace BattleArena.Vehicles;

/// <summary>
/// Sistema de vehículos y maquinaria pesada
/// Incluye: Tanques, Drones, Autos de combate, Excavadoras destructoras
/// </summary>
public class VehicleManager : MonoBehaviourPunCallbacks
{
    [Header("Vehicle Prefabs")]
    public GameObject combatTankPrefab;
    public GameObject armoredCarPrefab;
    public GameObject attackDronePrefab;
    public GameObject destroyerMechPrefab;
    public GameObject excavatorPrefab;
    
    [Header("Spawn Configuration")]
    public Transform[] vehicleSpawnPoints;
    public int maxVehicles = 10;
    public float respawnTime = 60f;
    
    void Start()
    {
        if (PhotonNetwork.IsMasterClient)
        {
            SpawnInitialVehicles();
        }
    }
    
    void SpawnInitialVehicles()
    {
        foreach (Transform spawnPoint in vehicleSpawnPoints)
        {
            SpawnRandomVehicle(spawnPoint.position, spawnPoint.rotation);
        }
    }
    
    public void SpawnRandomVehicle(Vector3 position, Quaternion rotation)
    {
        VehicleType type = (VehicleType)Random.Range(0, 5);
        GameObject prefab = GetVehiclePrefab(type);
        
        if (prefab != null)
        {
            GameObject vehicle = PhotonNetwork.Instantiate(
                prefab.name,
                position,
                rotation
            );
            
            Debug.Log($"🚗 Vehículo spawneado: {type}");
        }
    }
    
    GameObject GetVehiclePrefab(VehicleType type)
    {
        switch (type)
        {
            case VehicleType.CombatTank:
                return combatTankPrefab;
            case VehicleType.ArmoredCar:
                return armoredCarPrefab;
            case VehicleType.AttackDrone:
                return attackDronePrefab;
            case VehicleType.DestroyerMech:
                return destroyerMechPrefab;
            case VehicleType.Excavator:
                return excavatorPrefab;
            default:
                return armoredCarPrefab;
        }
    }
}

public enum VehicleType
{
    CombatTank,      // Tanque de combate
    ArmoredCar,      // Auto blindado
    AttackDrone,     // Dron de ataque
    DestroyerMech,   // Mech destructor
    Excavator        // Excavadora armada
}
