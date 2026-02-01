using UnityEngine;
using System.Collections.Generic;

namespace BattleArena.Maps;

/// <summary>
/// Generador de mapas procedurales para diferentes tipos de juego
/// </summary>
public class MapGenerator : MonoBehaviour
{
    [Header("Map Configuration")]
    public MapType mapType = MapType.BattleArena;
    public int mapSeed = 12345;
    public float mapSize = 5000f;
    
    [Header("Terrain Settings")]
    public int terrainResolution = 513;
    public float terrainHeight = 500f;
    public float noiseScale = 50f;
    
    [Header("Prefabs")]
    public GameObject[] buildingPrefabs;
    public GameObject[] treePrefabs;
    public GameObject[] rockPrefabs;
    public GameObject[] weaponSpawnPrefabs;
    public GameObject[] powerUpPrefabs;
    public GameObject safeZonePrefab;
    
    [Header("Spawn Points")]
    public int playerSpawnCount = 100;
    public List<Transform> spawnPoints = new List<Transform>();
    
    private Terrain terrain;
    private TerrainData terrainData;
    
    public enum MapType
    {
        BattleArena,      // Combate PvP
        OpenWorld,        // Exploración libre
        LearningZone,     // Zona educativa
        Tournament        // Torneo competitivo
    }
    
    void Start()
    {
        GenerateMap();
    }
    
    public void GenerateMap()
    {
        Random.InitState(mapSeed);
        
        Debug.Log($"🗺️ Generando mapa: {mapType}");
        
        switch (mapType)
        {
            case MapType.BattleArena:
                GenerateBattleArena();
                break;
                
            case MapType.OpenWorld:
                GenerateOpenWorld();
                break;
                
            case MapType.LearningZone:
                GenerateLearningZone();
                break;
                
            case MapType.Tournament:
                GenerateTournamentMap();
                break;
        }
        
        Debug.Log($"✅ Mapa generado con {spawnPoints.Count} spawn points");
    }
    
    #region Battle Arena Map
    void GenerateBattleArena()
    {
        // Crear terreno base
        CreateTerrain();
        
        // Generar isla central con edificios
        GenerateIslandTerrain();
        
        // Colocar edificios estratégicos
        PlaceBuildings(150);
        
        // Colocar vegetación
        PlaceVegetation(500);
        
        // Colocar armas y power-ups
        PlaceWeaponSpawns(50);
        PlacePowerUps(30);
        
        // Crear spawn points distribuidos
        CreateSpawnPoints(playerSpawnCount);
        
        // Crear zona segura visual
        CreateSafeZone();
    }
    #endregion
    
    #region Open World Map
    void GenerateOpenWorld()
    {
        // Mapa más grande para exploración
        mapSize = 10000f;
        
        CreateTerrain();
        
        // Terreno variado con montañas, valles, lagos
        GenerateVariedTerrain();
        
        // Ciudades y pueblos
        PlaceCities(5);
        
        // Bosques densos
        PlaceForests(10);
        
        // Puntos de interés educativos
        PlaceLearningStations(20);
        
        // NPCs y misiones
        PlaceNPCs(50);
        
        // Spawn points seguros
        CreateSpawnPoints(20);
    }
    #endregion
    
    #region Learning Zone Map
    void GenerateLearningZone()
    {
        // Zona educativa y tutorial
        mapSize = 2000f;
        
        CreateTerrain();
        
        // Terreno plano para fácil navegación
        GenerateFlatTerrain();
        
        // Salas de aprendizaje
        PlaceLearningRooms(15);
        
        // Zonas de práctica
        PlacePracticeZones(10);
        
        // Tutoriales interactivos
        PlaceTutorialStations(25);
        
        // Área de combate práctica
        PlacePracticeArena();
        
        // Spawn único
        CreateSpawnPoints(1);
    }
    #endregion
    
    #region Tournament Map
    void GenerateTournamentMap()
    {
        // Mapa optimizado para competición
        CreateTerrain();
        
        // Terreno balanceado
        GenerateBalancedTerrain();
        
        // Edificios simétricos
        PlaceSymmetricalBuildings();
        
        // Armas balanceadas
        PlaceBalancedWeapons();
        
        // Spawn points equitativos
        CreateEqualSpawnPoints(100);
        
        // Zona segura predecible
        CreateSafeZone();
    }
    #endregion
    
    #region Terrain Generation
    void CreateTerrain()
    {
        terrainData = new TerrainData();
        terrainData.heightmapResolution = terrainResolution;
        terrainData.size = new Vector3(mapSize, terrainHeight, mapSize);
        
        terrain = Terrain.CreateTerrainGameObject(terrainData).GetComponent<Terrain>();
        terrain.transform.position = new Vector3(-mapSize / 2f, 0, -mapSize / 2f);
    }
    
    void GenerateIslandTerrain()
    {
        float[,] heights = new float[terrainResolution, terrainResolution];
        
        for (int x = 0; x < terrainResolution; x++)
        {
            for (int y = 0; y < terrainResolution; y++)
            {
                // Normalizar coordenadas
                float xCoord = (float)x / terrainResolution;
                float yCoord = (float)y / terrainResolution;
                
                // Generar altura con Perlin noise
                float noise = Mathf.PerlinNoise(
                    xCoord * noiseScale,
                    yCoord * noiseScale
                );
                
                // Crear forma de isla (más bajo en los bordes)
                float distFromCenter = Vector2.Distance(
                    new Vector2(xCoord, yCoord),
                    new Vector2(0.5f, 0.5f)
                );
                
                float islandMask = 1f - Mathf.Clamp01(distFromCenter * 2f);
                
                heights[x, y] = noise * islandMask;
            }
        }
        
        terrainData.SetHeights(0, 0, heights);
    }
    
    void GenerateVariedTerrain()
    {
        float[,] heights = new float[terrainResolution, terrainResolution];
        
        for (int x = 0; x < terrainResolution; x++)
        {
            for (int y = 0; y < terrainResolution; y++)
            {
                float xCoord = (float)x / terrainResolution;
                float yCoord = (float)y / terrainResolution;
                
                // Múltiples octavas de ruido
                float height = 0f;
                height += Mathf.PerlinNoise(xCoord * 10, yCoord * 10) * 0.5f;
                height += Mathf.PerlinNoise(xCoord * 30, yCoord * 30) * 0.3f;
                height += Mathf.PerlinNoise(xCoord * 60, yCoord * 60) * 0.2f;
                
                heights[x, y] = height;
            }
        }
        
        terrainData.SetHeights(0, 0, heights);
    }
    
    void GenerateFlatTerrain()
    {
        float[,] heights = new float[terrainResolution, terrainResolution];
        
        for (int x = 0; x < terrainResolution; x++)
        {
            for (int y = 0; y < terrainResolution; y++)
            {
                heights[x, y] = 0.1f; // Ligeramente elevado
            }
        }
        
        terrainData.SetHeights(0, 0, heights);
    }
    
    void GenerateBalancedTerrain()
    {
        // Terreno simétrico para competición justa
        float[,] heights = new float[terrainResolution, terrainResolution];
        int half = terrainResolution / 2;
        
        for (int x = 0; x < half; x++)
        {
            for (int y = 0; y < terrainResolution; y++)
            {
                float xCoord = (float)x / terrainResolution;
                float yCoord = (float)y / terrainResolution;
                
                float noise = Mathf.PerlinNoise(xCoord * 20, yCoord * 20);
                
                // Aplicar simetría
                heights[x, y] = noise;
                heights[terrainResolution - 1 - x, y] = noise;
            }
        }
        
        terrainData.SetHeights(0, 0, heights);
    }
    #endregion
    
    #region Object Placement
    void PlaceBuildings(int count)
    {
        if (buildingPrefabs.Length == 0) return;
        
        for (int i = 0; i < count; i++)
        {
            Vector3 position = GetRandomTerrainPosition();
            GameObject building = buildingPrefabs[Random.Range(0, buildingPrefabs.Length)];
            
            Instantiate(building, position, Quaternion.Euler(0, Random.Range(0, 360), 0));
        }
    }
    
    void PlaceVegetation(int count)
    {
        if (treePrefabs.Length == 0) return;
        
        for (int i = 0; i < count; i++)
        {
            Vector3 position = GetRandomTerrainPosition();
            GameObject tree = treePrefabs[Random.Range(0, treePrefabs.Length)];
            
            Instantiate(tree, position, Quaternion.identity);
        }
    }
    
    void PlaceWeaponSpawns(int count)
    {
        if (weaponSpawnPrefabs.Length == 0) return;
        
        for (int i = 0; i < count; i++)
        {
            Vector3 position = GetRandomTerrainPosition();
            GameObject weaponSpawn = weaponSpawnPrefabs[Random.Range(0, weaponSpawnPrefabs.Length)];
            
            Instantiate(weaponSpawn, position + Vector3.up * 0.5f, Quaternion.identity);
        }
    }
    
    void PlacePowerUps(int count)
    {
        if (powerUpPrefabs.Length == 0) return;
        
        for (int i = 0; i < count; i++)
        {
            Vector3 position = GetRandomTerrainPosition();
            GameObject powerUp = powerUpPrefabs[Random.Range(0, powerUpPrefabs.Length)];
            
            Instantiate(powerUp, position + Vector3.up * 0.5f, Quaternion.identity);
        }
    }
    
    void PlaceCities(int count)
    {
        // Implementar ciudades para Open World
        Debug.Log($"Colocando {count} ciudades");
    }
    
    void PlaceForests(int count)
    {
        // Implementar bosques densos
        Debug.Log($"Colocando {count} bosques");
    }
    
    void PlaceLearningStations(int count)
    {
        // Estaciones educativas
        Debug.Log($"Colocando {count} estaciones de aprendizaje");
    }
    
    void PlaceNPCs(int count)
    {
        // NPCs para misiones
        Debug.Log($"Colocando {count} NPCs");
    }
    
    void PlaceLearningRooms(int count)
    {
        // Salas de clase virtuales
        Debug.Log($"Colocando {count} salas de aprendizaje");
    }
    
    void PlacePracticeZones(int count)
    {
        // Zonas de práctica
        Debug.Log($"Colocando {count} zonas de práctica");
    }
    
    void PlaceTutorialStations(int count)
    {
        // Tutoriales interactivos
        Debug.Log($"Colocando {count} tutoriales");
    }
    
    void PlacePracticeArena()
    {
        // Arena de práctica
        Debug.Log("Creando arena de práctica");
    }
    
    void PlaceSymmetricalBuildings()
    {
        // Edificios simétricos para torneos
        Debug.Log("Colocando edificios simétricos");
    }
    
    void PlaceBalancedWeapons()
    {
        // Armas balanceadas para competición
        Debug.Log("Colocando armas balanceadas");
    }
    #endregion
    
    #region Spawn Points
    void CreateSpawnPoints(int count)
    {
        spawnPoints.Clear();
        
        for (int i = 0; i < count; i++)
        {
            GameObject spawnPoint = new GameObject($"SpawnPoint_{i}");
            spawnPoint.transform.position = GetRandomTerrainPosition() + Vector3.up * 2f;
            spawnPoint.transform.SetParent(transform);
            
            spawnPoints.Add(spawnPoint.transform);
        }
    }
    
    void CreateEqualSpawnPoints(int count)
    {
        // Spawn points distribuidos equitativamente
        spawnPoints.Clear();
        
        float angleStep = 360f / count;
        float radius = mapSize * 0.4f;
        
        for (int i = 0; i < count; i++)
        {
            float angle = i * angleStep * Mathf.Deg2Rad;
            Vector3 position = new Vector3(
                Mathf.Cos(angle) * radius,
                0,
                Mathf.Sin(angle) * radius
            );
            
            position.y = terrain.SampleHeight(position) + 2f;
            
            GameObject spawnPoint = new GameObject($"SpawnPoint_{i}");
            spawnPoint.transform.position = position;
            spawnPoint.transform.SetParent(transform);
            
            spawnPoints.Add(spawnPoint.transform);
        }
    }
    #endregion
    
    #region Safe Zone
    void CreateSafeZone()
    {
        if (safeZonePrefab != null)
        {
            GameObject safeZone = Instantiate(safeZonePrefab, Vector3.zero, Quaternion.identity);
            safeZone.name = "SafeZone";
            safeZone.transform.localScale = Vector3.one * 5000f;
        }
    }
    #endregion
    
    #region Utilities
    Vector3 GetRandomTerrainPosition()
    {
        float x = Random.Range(-mapSize / 2f, mapSize / 2f);
        float z = Random.Range(-mapSize / 2f, mapSize / 2f);
        float y = terrain.SampleHeight(new Vector3(x, 0, z));
        
        return new Vector3(x, y, z);
    }
    #endregion
}
