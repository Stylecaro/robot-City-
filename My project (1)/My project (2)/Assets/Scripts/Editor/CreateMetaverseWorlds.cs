using UnityEngine;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine.SceneManagement;
using System.IO;

public class CreateMetaverseWorlds : EditorWindow
{
    [MenuItem("Metaverso/1. Crear Todos los Mundos Virtuales")]
    public static void CreateAllWorlds()
    {
        bool confirm = EditorUtility.DisplayDialog(
            "Crear Metaverso Completo 🌍",
            "Esto creará 5 mundos virtuales:\n\n" +
            "🏙️ Ciudad Central (hub principal)\n" +
            "⚔️ Arena de Batalla\n" +
            "🏝️ Isla Tropical\n" +
            "🌌 Estación Espacial\n" +
            "🎰 Casino Virtual\n\n" +
            "Con portales entre ellos.\n\n" +
            "¿Continuar?",
            "Sí, Crear Todo",
            "Cancelar"
        );

        if (!confirm) return;

        CreateCentralCity();
        CreateBattleArena();
        CreateTropicalIsland();
        CreateSpaceStation();
        CreateVirtualCasino();

        EditorUtility.DisplayDialog(
            "¡Metaverso Creado! 🎉",
            "5 mundos virtuales listos:\n\n" +
            "✅ Ciudad Central\n" +
            "✅ Arena de Batalla\n" +
            "✅ Isla Tropical\n" +
            "✅ Estación Espacial\n" +
            "✅ Casino Virtual\n\n" +
            "Cada mundo tiene portales para transportarte.\n\n" +
            "Abre: Assets/Scenes/CentralCity.unity",
            "¡Genial!"
        );
    }

    [MenuItem("Metaverso/Mundos/🏙️ Ciudad Central (Hub)")]
    public static void CreateCentralCity()
    {
        Scene scene = EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects, NewSceneMode.Single);
        
        // Terreno urbano plano
        GameObject terrain = CreateFlatTerrain(2000, "CentralCity_Ground");
        terrain.GetComponent<Terrain>().terrainData.size = new Vector3(2000, 50, 2000);
        
        // Player spawn
        GameObject player = CreatePlayerSpawn(new Vector3(1000, 5, 1000));
        
        // Edificios centrales
        CreateBuilding(new Vector3(950, 0, 1050), new Vector3(30, 60, 30), Color.gray, "Edificio_Torre_1");
        CreateBuilding(new Vector3(1050, 0, 1050), new Vector3(25, 80, 25), Color.white, "Edificio_Torre_2");
        CreateBuilding(new Vector3(1000, 0, 950), new Vector3(40, 40, 40), new Color(0.8f, 0.6f, 0.4f), "Edificio_Comercial");
        
        // Plaza central con portales
        GameObject plaza = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
        plaza.name = "Plaza_Central";
        plaza.transform.position = new Vector3(1000, 0.5f, 1000);
        plaza.transform.localScale = new Vector3(80, 1, 80);
        plaza.GetComponent<Renderer>().material.color = new Color(0.7f, 0.7f, 0.8f);
        DestroyImmediate(plaza.GetComponent<Collider>());
        
        // Portales a otros mundos
        CreatePortal(new Vector3(980, 2, 1000), "Arena de Batalla", Color.red, "BattleArena");
        CreatePortal(new Vector3(1020, 2, 1000), "Isla Tropical", Color.green, "TropicalIsland");
        CreatePortal(new Vector3(1000, 2, 980), "Estación Espacial", Color.cyan, "SpaceStation");
        CreatePortal(new Vector3(1000, 2, 1020), "Casino Virtual", Color.yellow, "VirtualCasino");
        
        // Letreros informativos
        CreateSign(new Vector3(1000, 8, 1000), "CIUDAD CENTRAL\nBienvenido al Metaverso");
        
        // Iluminación
        SetupUrbanLighting();
        
        SaveScene(scene, "CentralCity");
        Debug.Log("✅ Ciudad Central creada");
    }

    [MenuItem("Metaverso/Mundos/⚔️ Arena de Batalla")]
    public static void CreateBattleArena()
    {
        Scene scene = EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects, NewSceneMode.Single);
        
        // Terreno grande para combate
        GameObject terrain = CreateFlatTerrain(5000, "BattleArena_Ground");
        
        // Player spawn
        GameObject player = CreatePlayerSpawn(new Vector3(2500, 10, 2500));
        
        // Muros de la arena (círculo)
        for (int i = 0; i < 20; i++)
        {
            float angle = i * (360f / 20f);
            float x = 2500 + Mathf.Cos(angle * Mathf.Deg2Rad) * 500;
            float z = 2500 + Mathf.Sin(angle * Mathf.Deg2Rad) * 500;
            
            GameObject wall = GameObject.CreatePrimitive(PrimitiveType.Cube);
            wall.name = $"Arena_Wall_{i}";
            wall.transform.position = new Vector3(x, 15, z);
            wall.transform.localScale = new Vector3(50, 30, 10);
            wall.transform.LookAt(new Vector3(2500, 15, 2500));
            wall.GetComponent<Renderer>().material.color = new Color(0.3f, 0.3f, 0.3f);
        }
        
        // Plataformas de combate
        CreatePlatform(new Vector3(2500, 5, 2500), new Vector3(100, 2, 100), Color.gray);
        CreatePlatform(new Vector3(2400, 8, 2400), new Vector3(40, 2, 40), Color.red);
        CreatePlatform(new Vector3(2600, 8, 2600), new Vector3(40, 2, 40), Color.blue);
        
        // Obstáculos
        CreateObstacle(new Vector3(2450, 5, 2500), new Vector3(20, 20, 20));
        CreateObstacle(new Vector3(2550, 5, 2500), new Vector3(15, 25, 15));
        
        // Portal de regreso a ciudad
        CreatePortal(new Vector3(2500, 2, 2300), "Volver a Ciudad Central", Color.white, "CentralCity");
        
        // Letreros
        CreateSign(new Vector3(2500, 25, 2500), "ARENA DE BATALLA\n¡Lucha o Huye!");
        
        SetupBattleLighting();
        SaveScene(scene, "BattleArena");
        Debug.Log("✅ Arena de Batalla creada");
    }

    [MenuItem("Metaverso/Mundos/🏝️ Isla Tropical")]
    public static void CreateTropicalIsland()
    {
        Scene scene = EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects, NewSceneMode.Single);
        
        // Terreno con elevaciones (isla)
        TerrainData terrainData = new TerrainData();
        terrainData.heightmapResolution = 513;
        terrainData.size = new Vector3(1500, 200, 1500);
        
        GameObject terrainObj = Terrain.CreateTerrainGameObject(terrainData);
        terrainObj.name = "TropicalIsland_Terrain";
        terrainObj.transform.position = Vector3.zero;
        
        // Player spawn en la playa
        GameObject player = CreatePlayerSpawn(new Vector3(750, 15, 200));
        
        // Palmeras (cilindros simples)
        CreatePalmTree(new Vector3(700, 10, 250));
        CreatePalmTree(new Vector3(800, 10, 250));
        CreatePalmTree(new Vector3(720, 10, 280));
        CreatePalmTree(new Vector3(780, 10, 220));
        
        // Agua (plano azul grande)
        GameObject water = GameObject.CreatePrimitive(PrimitiveType.Plane);
        water.name = "Ocean";
        water.transform.position = new Vector3(750, 2, 750);
        water.transform.localScale = new Vector3(200, 1, 200);
        water.GetComponent<Renderer>().material.color = new Color(0.1f, 0.4f, 0.8f, 0.7f);
        
        // Cabaña
        CreateBuilding(new Vector3(750, 10, 300), new Vector3(20, 15, 25), new Color(0.6f, 0.4f, 0.2f), "Cabana_Playa");
        
        // Portal de regreso
        CreatePortal(new Vector3(750, 12, 320), "Volver a Ciudad Central", Color.white, "CentralCity");
        
        // Letrero
        CreateSign(new Vector3(750, 20, 280), "ISLA TROPICAL\nRelájate y Disfruta");
        
        SetupTropicalLighting();
        SaveScene(scene, "TropicalIsland");
        Debug.Log("✅ Isla Tropical creada");
    }

    [MenuItem("Metaverso/Mundos/🌌 Estación Espacial")]
    public static void CreateSpaceStation()
    {
        Scene scene = EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects, NewSceneMode.Single);
        
        // Sin terreno - ambiente espacial
        RenderSettings.skybox = null;
        RenderSettings.ambientLight = new Color(0.1f, 0.1f, 0.2f);
        Camera.main.backgroundColor = Color.black;
        
        // Plataforma principal de la estación
        GameObject station = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
        station.name = "SpaceStation_Main";
        station.transform.position = new Vector3(0, 0, 0);
        station.transform.localScale = new Vector3(100, 5, 100);
        station.GetComponent<Renderer>().material.color = new Color(0.7f, 0.7f, 0.8f);
        
        // Player spawn
        GameObject player = CreatePlayerSpawn(new Vector3(0, 8, 0));
        
        // Módulos de la estación
        CreateSpaceModule(new Vector3(0, 5, 60), "Modulo_Comando");
        CreateSpaceModule(new Vector3(60, 5, 0), "Modulo_Laboratorio");
        CreateSpaceModule(new Vector3(-60, 5, 0), "Modulo_Hangar");
        CreateSpaceModule(new Vector3(0, 5, -60), "Modulo_Residencial");
        
        // Ventanas con vista al espacio
        CreateWindow(new Vector3(0, 8, 45), "Ventana_Observacion");
        
        // Estrellas de fondo
        for (int i = 0; i < 100; i++)
        {
            GameObject star = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            star.name = $"Star_{i}";
            star.transform.position = Random.insideUnitSphere * 500;
            star.transform.localScale = Vector3.one * Random.Range(1f, 3f);
            star.GetComponent<Renderer>().material.color = Color.white;
            star.GetComponent<Renderer>().material.EnableKeyword("_EMISSION");
            star.GetComponent<Renderer>().material.SetColor("_EmissionColor", Color.white * 2f);
        }
        
        // Portal de regreso
        CreatePortal(new Vector3(0, 7, 0), "Volver a Ciudad Central", Color.white, "CentralCity");
        
        // Letrero
        CreateSign(new Vector3(0, 15, 0), "ESTACIÓN ESPACIAL\nOrbita Terrestre");
        
        SetupSpaceLighting();
        SaveScene(scene, "SpaceStation");
        Debug.Log("✅ Estación Espacial creada");
    }

    [MenuItem("Metaverso/Mundos/🎰 Casino Virtual")]
    public static void CreateVirtualCasino()
    {
        Scene scene = EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects, NewSceneMode.Single);
        
        // Piso del casino
        GameObject floor = GameObject.CreatePrimitive(PrimitiveType.Cube);
        floor.name = "Casino_Floor";
        floor.transform.position = new Vector3(0, -1, 0);
        floor.transform.localScale = new Vector3(200, 2, 200);
        floor.GetComponent<Renderer>().material.color = new Color(0.1f, 0.1f, 0.2f);
        
        // Player spawn
        GameObject player = CreatePlayerSpawn(new Vector3(0, 2, -80));
        
        // Mesas de juego (ruletas)
        CreateGameTable(new Vector3(-30, 0, 0), "Ruleta_1", Color.red);
        CreateGameTable(new Vector3(30, 0, 0), "Ruleta_2", Color.green);
        CreateGameTable(new Vector3(0, 0, 30), "Blackjack", Color.blue);
        
        // Máquinas tragamonedas
        for (int i = 0; i < 10; i++)
        {
            CreateSlotMachine(new Vector3(-70 + i * 15, 0, -30), $"Slot_{i}");
        }
        
        // Bar
        CreateBuilding(new Vector3(0, 0, -50), new Vector3(60, 15, 10), new Color(0.3f, 0.2f, 0.1f), "Bar");
        
        // Luces de neón
        CreateNeonLight(new Vector3(0, 20, 0), Color.magenta);
        CreateNeonLight(new Vector3(-50, 20, 0), Color.cyan);
        CreateNeonLight(new Vector3(50, 20, 0), Color.yellow);
        
        // Portal de regreso
        CreatePortal(new Vector3(0, 2, -90), "Volver a Ciudad Central", Color.white, "CentralCity");
        
        // Letrero
        CreateSign(new Vector3(0, 25, -70), "CASINO VIRTUAL\n¡Buena Suerte!");
        
        SetupCasinoLighting();
        SaveScene(scene, "VirtualCasino");
        Debug.Log("✅ Casino Virtual creado");
    }

    // ==================== FUNCIONES AUXILIARES ====================

    static GameObject CreateFlatTerrain(float size, string name)
    {
        TerrainData terrainData = new TerrainData();
        terrainData.heightmapResolution = 513;
        terrainData.size = new Vector3(size, 100, size);
        
        GameObject terrainObj = Terrain.CreateTerrainGameObject(terrainData);
        terrainObj.name = name;
        terrainObj.transform.position = Vector3.zero;
        
        return terrainObj;
    }

    static GameObject CreatePlayerSpawn(Vector3 position)
    {
        GameObject player = new GameObject("Player");
        player.transform.position = position;
        
        CharacterController controller = player.AddComponent<CharacterController>();
        controller.height = 2f;
        controller.radius = 0.5f;
        controller.center = new Vector3(0, 1, 0);
        
        GameObject camera = new GameObject("PlayerCamera");
        camera.transform.parent = player.transform;
        camera.transform.localPosition = new Vector3(0, 0.6f, 0);
        Camera cam = camera.AddComponent<Camera>();
        cam.farClipPlane = 10000f;
        camera.AddComponent<AudioListener>();
        
        GameObject model = GameObject.CreatePrimitive(PrimitiveType.Capsule);
        model.name = "PlayerModel";
        model.transform.parent = player.transform;
        model.transform.localPosition = Vector3.zero;
        DestroyImmediate(model.GetComponent<Collider>());
        
        // Intentar agregar PlayerMovement
        var movement = player.AddComponent<PlayerMovement>();
        if (movement != null)
        {
            SerializedObject so = new SerializedObject(movement);
            SerializedProperty prop = so.FindProperty("playerCamera");
            if (prop != null)
            {
                prop.objectReferenceValue = camera.transform;
                so.ApplyModifiedProperties();
            }
        }
        
        return player;
    }

    static void CreatePortal(Vector3 position, string destination, Color color, string sceneName)
    {
        GameObject portal = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
        portal.name = $"Portal_To_{sceneName}";
        portal.transform.position = position;
        portal.transform.localScale = new Vector3(5, 0.5f, 5);
        
        Renderer renderer = portal.GetComponent<Renderer>();
        renderer.material.color = color;
        renderer.material.EnableKeyword("_EMISSION");
        renderer.material.SetColor("_EmissionColor", color * 2f);
        
        // Trigger
        Collider collider = portal.GetComponent<Collider>();
        collider.isTrigger = true;
        
        // Script de transporte
        PortalTeleport teleport = portal.AddComponent<PortalTeleport>();
        teleport.destinationScene = sceneName;
        
        // Letrero arriba
        CreateFloatingText(position + Vector3.up * 4, destination);
    }

    static void CreateBuilding(Vector3 position, Vector3 scale, Color color, string name)
    {
        GameObject building = GameObject.CreatePrimitive(PrimitiveType.Cube);
        building.name = name;
        building.transform.position = position + new Vector3(0, scale.y / 2, 0);
        building.transform.localScale = scale;
        building.GetComponent<Renderer>().material.color = color;
    }

    static void CreatePlatform(Vector3 position, Vector3 scale, Color color)
    {
        GameObject platform = GameObject.CreatePrimitive(PrimitiveType.Cube);
        platform.name = "Platform";
        platform.transform.position = position;
        platform.transform.localScale = scale;
        platform.GetComponent<Renderer>().material.color = color;
    }

    static void CreateObstacle(Vector3 position, Vector3 scale)
    {
        GameObject obstacle = GameObject.CreatePrimitive(PrimitiveType.Cube);
        obstacle.name = "Obstacle";
        obstacle.transform.position = position;
        obstacle.transform.localScale = scale;
        obstacle.GetComponent<Renderer>().material.color = new Color(0.5f, 0.5f, 0.5f);
    }

    static void CreatePalmTree(Vector3 position)
    {
        // Tronco
        GameObject trunk = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
        trunk.name = "PalmTree_Trunk";
        trunk.transform.position = position + Vector3.up * 10;
        trunk.transform.localScale = new Vector3(2, 10, 2);
        trunk.GetComponent<Renderer>().material.color = new Color(0.4f, 0.3f, 0.2f);
        
        // Hojas (esfera verde arriba)
        GameObject leaves = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        leaves.name = "PalmTree_Leaves";
        leaves.transform.position = position + Vector3.up * 22;
        leaves.transform.localScale = new Vector3(8, 8, 8);
        leaves.GetComponent<Renderer>().material.color = new Color(0.2f, 0.6f, 0.2f);
        DestroyImmediate(leaves.GetComponent<Collider>());
    }

    static void CreateSpaceModule(Vector3 position, string name)
    {
        GameObject module = GameObject.CreatePrimitive(PrimitiveType.Cube);
        module.name = name;
        module.transform.position = position;
        module.transform.localScale = new Vector3(30, 20, 30);
        module.GetComponent<Renderer>().material.color = new Color(0.6f, 0.6f, 0.7f);
    }

    static void CreateWindow(Vector3 position, string name)
    {
        GameObject window = GameObject.CreatePrimitive(PrimitiveType.Plane);
        window.name = name;
        window.transform.position = position;
        window.transform.rotation = Quaternion.Euler(90, 0, 0);
        window.transform.localScale = new Vector3(3, 1, 3);
        window.GetComponent<Renderer>().material.color = new Color(0.2f, 0.4f, 0.8f, 0.5f);
    }

    static void CreateGameTable(Vector3 position, string name, Color color)
    {
        GameObject table = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
        table.name = name;
        table.transform.position = position + Vector3.up * 2;
        table.transform.localScale = new Vector3(8, 1, 8);
        table.GetComponent<Renderer>().material.color = color;
    }

    static void CreateSlotMachine(Vector3 position, string name)
    {
        GameObject slot = GameObject.CreatePrimitive(PrimitiveType.Cube);
        slot.name = name;
        slot.transform.position = position + Vector3.up * 3;
        slot.transform.localScale = new Vector3(3, 6, 2);
        slot.GetComponent<Renderer>().material.color = new Color(0.8f, 0.1f, 0.1f);
    }

    static void CreateNeonLight(Vector3 position, Color color)
    {
        GameObject light = new GameObject("NeonLight");
        light.transform.position = position;
        Light lightComp = light.AddComponent<Light>();
        lightComp.type = LightType.Point;
        lightComp.color = color;
        lightComp.intensity = 5f;
        lightComp.range = 50f;
    }

    static void CreateSign(Vector3 position, string text)
    {
        GameObject sign = GameObject.CreatePrimitive(PrimitiveType.Cube);
        sign.name = "Sign";
        sign.transform.position = position;
        sign.transform.localScale = new Vector3(20, 10, 1);
        sign.GetComponent<Renderer>().material.color = new Color(0.2f, 0.2f, 0.2f);
        
        CreateFloatingText(position, text);
    }

    static void CreateFloatingText(Vector3 position, string text)
    {
        GameObject textObj = new GameObject("FloatingText");
        textObj.transform.position = position;
        
        TextMesh textMesh = textObj.AddComponent<TextMesh>();
        textMesh.text = text;
        textMesh.fontSize = 100;
        textMesh.anchor = TextAnchor.MiddleCenter;
        textMesh.alignment = TextAlignment.Center;
        textMesh.color = Color.white;
    }

    static void SetupUrbanLighting()
    {
        RenderSettings.ambientLight = new Color(0.4f, 0.4f, 0.5f);
        RenderSettings.fog = true;
        RenderSettings.fogColor = new Color(0.6f, 0.6f, 0.7f);
        RenderSettings.fogMode = FogMode.Linear;
        RenderSettings.fogStartDistance = 500f;
        RenderSettings.fogEndDistance = 2000f;
    }

    static void SetupBattleLighting()
    {
        RenderSettings.ambientLight = new Color(0.3f, 0.3f, 0.3f);
        RenderSettings.fog = true;
        RenderSettings.fogColor = new Color(0.3f, 0.3f, 0.4f);
    }

    static void SetupTropicalLighting()
    {
        RenderSettings.ambientLight = new Color(0.7f, 0.7f, 0.6f);
        RenderSettings.fog = true;
        RenderSettings.fogColor = new Color(0.8f, 0.9f, 1f);
    }

    static void SetupSpaceLighting()
    {
        RenderSettings.ambientLight = new Color(0.05f, 0.05f, 0.1f);
        RenderSettings.fog = false;
    }

    static void SetupCasinoLighting()
    {
        RenderSettings.ambientLight = new Color(0.2f, 0.1f, 0.3f);
        RenderSettings.fog = true;
        RenderSettings.fogColor = new Color(0.3f, 0.2f, 0.4f);
    }

    static void SaveScene(Scene scene, string name)
    {
        if (!Directory.Exists("Assets/Scenes"))
        {
            Directory.CreateDirectory("Assets/Scenes");
            AssetDatabase.Refresh();
        }
        
        EditorSceneManager.SaveScene(scene, $"Assets/Scenes/{name}.unity");
    }
}

// Script de teleportación entre mundos
public class PortalTeleport : MonoBehaviour
{
    public string destinationScene;

    void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player"))
        {
            UnityEngine.SceneManagement.SceneManager.LoadScene(destinationScene);
        }
    }
}
