using UnityEngine;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine.SceneManagement;
using System.IO;

public class AutoSetupScene : EditorWindow
{
    [MenuItem("Mundo Virtual/1. Crear Escena BattleArena Completa")]
    public static void CreateBattleArenaScene()
    {
        // Crear nueva escena
        Scene newScene = EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects, NewSceneMode.Single);
        
        Debug.Log("✅ Escena creada");

        // 1. CREAR TERRENO 5km x 5km
        GameObject terrainObj = CreateTerrain();
        Debug.Log("✅ Terreno 5000x5000 creado");

        // 2. CREAR PLAYER CON CÁMARA Y MOVIMIENTO
        GameObject player = CreatePlayer();
        Debug.Log("✅ Player con cámara y movimiento creado");

        // 3. CONFIGURAR ILUMINACIÓN
        SetupLighting();
        Debug.Log("✅ Iluminación configurada");

        // 4. GUARDAR ESCENA
        string scenePath = "Assets/Scenes/BattleArena.unity";
        
        // Crear carpeta Scenes si no existe
        if (!Directory.Exists("Assets/Scenes"))
        {
            Directory.CreateDirectory("Assets/Scenes");
            AssetDatabase.Refresh();
        }
        
        EditorSceneManager.SaveScene(newScene, scenePath);
        Debug.Log("✅ Escena guardada en: " + scenePath);

        // 5. SELECCIONAR PLAYER
        Selection.activeGameObject = player;
        SceneView.lastActiveSceneView.FrameSelected();

        EditorUtility.DisplayDialog(
            "¡Escena Creada Exitosamente! 🎉",
            "BattleArena está lista:\n\n" +
            "✅ Terreno 5000x5000 metros\n" +
            "✅ Player con movimiento WASD\n" +
            "✅ Cámara primera persona\n" +
            "✅ Iluminación configurada\n\n" +
            "¡Presiona PLAY (▶️) para probar!\n\n" +
            "Controles:\n" +
            "WASD - Mover\n" +
            "Mouse - Mirar\n" +
            "Espacio - Saltar",
            "¡Entendido!"
        );
    }

    static GameObject CreateTerrain()
    {
        // Crear terreno
        TerrainData terrainData = new TerrainData();
        terrainData.heightmapResolution = 513;
        terrainData.size = new Vector3(5000, 600, 5000);
        terrainData.baseMapResolution = 1024;
        terrainData.SetDetailResolution(1024, 16);

        GameObject terrainObj = Terrain.CreateTerrainGameObject(terrainData);
        terrainObj.name = "BattleArena_Terrain";
        
        // Posicionar en 0,0,0
        terrainObj.transform.position = Vector3.zero;

        // Crear asset del terrainData
        if (!Directory.Exists("Assets/Terrains"))
        {
            Directory.CreateDirectory("Assets/Terrains");
            AssetDatabase.Refresh();
        }
        
        AssetDatabase.CreateAsset(terrainData, "Assets/Terrains/BattleArena_TerrainData.asset");

        return terrainObj;
    }

    static GameObject CreatePlayer()
    {
        // Crear Player vacío
        GameObject player = new GameObject("Player");
        player.transform.position = new Vector3(2500, 10, 2500); // Centro del mapa

        // Agregar CharacterController
        CharacterController controller = player.AddComponent<CharacterController>();
        controller.height = 2f;
        controller.radius = 0.5f;
        controller.center = new Vector3(0, 1, 0);

        // Agregar PlayerMovement script (si existe)
        var playerMovement = player.AddComponent<PlayerMovement>();

        // Crear modelo visual temporal (Capsule)
        GameObject playerModel = GameObject.CreatePrimitive(PrimitiveType.Capsule);
        playerModel.name = "PlayerModel";
        playerModel.transform.parent = player.transform;
        playerModel.transform.localPosition = Vector3.zero;
        playerModel.transform.localRotation = Quaternion.identity;
        
        // Remover el collider del modelo (usamos el CharacterController)
        DestroyImmediate(playerModel.GetComponent<Collider>());

        // Crear cámara
        GameObject cameraObj = new GameObject("PlayerCamera");
        cameraObj.transform.parent = player.transform;
        cameraObj.transform.localPosition = new Vector3(0, 0.6f, 0);
        cameraObj.transform.localRotation = Quaternion.identity;

        Camera cam = cameraObj.AddComponent<Camera>();
        cam.fieldOfView = 60f;
        cam.nearClipPlane = 0.1f;
        cam.farClipPlane = 6000f; // Ver todo el mapa 5km

        // Asignar cámara al PlayerMovement
        if (playerMovement != null)
        {
            SerializedObject serializedPlayer = new SerializedObject(playerMovement);
            SerializedProperty cameraProperty = serializedPlayer.FindProperty("playerCamera");
            if (cameraProperty != null)
            {
                cameraProperty.objectReferenceValue = cameraObj.transform;
                serializedPlayer.ApplyModifiedProperties();
            }
        }

        // Agregar AudioListener
        cameraObj.AddComponent<AudioListener>();

        return player;
    }

    static void SetupLighting()
    {
        // Buscar o crear Directional Light
        Light[] lights = Object.FindObjectsOfType<Light>();
        Light dirLight = null;

        foreach (Light light in lights)
        {
            if (light.type == LightType.Directional)
            {
                dirLight = light;
                break;
            }
        }

        if (dirLight == null)
        {
            GameObject lightObj = new GameObject("Directional Light");
            dirLight = lightObj.AddComponent<Light>();
            dirLight.type = LightType.Directional;
        }

        // Configurar luz
        dirLight.transform.rotation = Quaternion.Euler(50, -30, 0);
        dirLight.intensity = 1.5f;
        dirLight.color = new Color(1f, 0.96f, 0.84f); // Luz cálida

        // Configurar ambiente
        RenderSettings.ambientMode = UnityEngine.Rendering.AmbientMode.Skybox;
        RenderSettings.ambientIntensity = 1f;
        RenderSettings.fog = true;
        RenderSettings.fogColor = new Color(0.5f, 0.6f, 0.7f);
        RenderSettings.fogMode = FogMode.Linear;
        RenderSettings.fogStartDistance = 1000f;
        RenderSettings.fogEndDistance = 5000f;
    }

    [MenuItem("Mundo Virtual/2. Agregar Bots AI al Mapa")]
    public static void AddBotsToScene()
    {
        // Buscar BotManager o crearlo
        BotManager botManager = Object.FindObjectOfType<BotManager>();
        
        if (botManager == null)
        {
            GameObject botManagerObj = new GameObject("BotManager");
            botManager = botManagerObj.AddComponent<BotManager>();
            
            Debug.Log("✅ BotManager creado");
        }

        // Crear prefabs de bots básicos
        for (int i = 0; i < 3; i++)
        {
            GameObject bot = GameObject.CreatePrimitive(PrimitiveType.Cube);
            bot.name = $"Bot_{i + 1}";
            bot.transform.position = new Vector3(
                Random.Range(2400, 2600),
                10,
                Random.Range(2400, 2600)
            );
            bot.transform.localScale = new Vector3(0.8f, 1.8f, 0.8f);
            
            // Color diferente por bot
            Renderer renderer = bot.GetComponent<Renderer>();
            renderer.material.color = new Color(
                Random.Range(0.5f, 1f),
                Random.Range(0.5f, 1f),
                Random.Range(0.5f, 1f)
            );
        }

        EditorUtility.DisplayDialog(
            "Bots Agregados ✅",
            "Se agregaron 3 bots de ejemplo al mapa.\n\n" +
            "Nota: Son cubos temporales.\n" +
            "Después puedes reemplazarlos con modelos 3D reales.",
            "OK"
        );
    }

    [MenuItem("Mundo Virtual/3. Agregar Vehículo de Prueba")]
    public static void AddVehicleToScene()
    {
        // Crear vehículo básico (caja con ruedas)
        GameObject vehicle = new GameObject("Vehicle_Test");
        vehicle.transform.position = new Vector3(2520, 5, 2520);

        // Cuerpo del vehículo
        GameObject body = GameObject.CreatePrimitive(PrimitiveType.Cube);
        body.name = "VehicleBody";
        body.transform.parent = vehicle.transform;
        body.transform.localPosition = new Vector3(0, 1, 0);
        body.transform.localScale = new Vector3(2, 1, 4);
        body.GetComponent<Renderer>().material.color = new Color(0.3f, 0.3f, 0.3f);

        // Ruedas
        for (int i = 0; i < 4; i++)
        {
            GameObject wheel = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
            wheel.name = $"Wheel_{i + 1}";
            wheel.transform.parent = vehicle.transform;
            wheel.transform.localScale = new Vector3(0.5f, 0.2f, 0.5f);
            wheel.transform.localRotation = Quaternion.Euler(0, 0, 90);
            
            float x = (i % 2 == 0) ? -1.2f : 1.2f;
            float z = (i < 2) ? 1.5f : -1.5f;
            wheel.transform.localPosition = new Vector3(x, 0.3f, z);
            
            wheel.GetComponent<Renderer>().material.color = Color.black;
        }

        EditorUtility.DisplayDialog(
            "Vehículo Agregado ✅",
            "Se agregó un vehículo de prueba cerca del jugador.\n\n" +
            "Es un modelo temporal de cubos.\n" +
            "Después puedes reemplazarlo con un modelo 3D real.",
            "OK"
        );

        Selection.activeGameObject = vehicle;
        SceneView.lastActiveSceneView.FrameSelected();
    }

    [MenuItem("Mundo Virtual/4. Configurar UI HUD Básico")]
    public static void CreateBasicHUD()
    {
        // Crear Canvas
        GameObject canvasObj = new GameObject("HUD_Canvas");
        Canvas canvas = canvasObj.AddComponent<Canvas>();
        canvas.renderMode = RenderMode.ScreenSpaceOverlay;
        canvasObj.AddComponent<UnityEngine.UI.CanvasScaler>();
        canvasObj.AddComponent<UnityEngine.UI.GraphicRaycaster>();

        // Crear texto de salud
        GameObject healthTextObj = new GameObject("HealthText");
        healthTextObj.transform.parent = canvasObj.transform;
        
        UnityEngine.UI.Text healthText = healthTextObj.AddComponent<UnityEngine.UI.Text>();
        healthText.text = "Health: 100";
        healthText.font = Resources.GetBuiltinResource<Font>("Arial.ttf");
        healthText.fontSize = 24;
        healthText.color = Color.white;
        healthText.alignment = TextAnchor.UpperLeft;

        RectTransform healthRect = healthTextObj.GetComponent<RectTransform>();
        healthRect.anchorMin = new Vector2(0, 1);
        healthRect.anchorMax = new Vector2(0, 1);
        healthRect.pivot = new Vector2(0, 1);
        healthRect.anchoredPosition = new Vector2(20, -20);
        healthRect.sizeDelta = new Vector2(200, 30);

        // Crear texto de munición
        GameObject ammoTextObj = new GameObject("AmmoText");
        ammoTextObj.transform.parent = canvasObj.transform;
        
        UnityEngine.UI.Text ammoText = ammoTextObj.AddComponent<UnityEngine.UI.Text>();
        ammoText.text = "Ammo: 30/120";
        ammoText.font = Resources.GetBuiltinResource<Font>("Arial.ttf");
        ammoText.fontSize = 24;
        ammoText.color = Color.white;
        ammoText.alignment = TextAnchor.LowerRight;

        RectTransform ammoRect = ammoTextObj.GetComponent<RectTransform>();
        ammoRect.anchorMin = new Vector2(1, 0);
        ammoRect.anchorMax = new Vector2(1, 0);
        ammoRect.pivot = new Vector2(1, 0);
        ammoRect.anchoredPosition = new Vector2(-20, 20);
        ammoRect.sizeDelta = new Vector2(200, 30);

        // Crear crosshair
        GameObject crosshairObj = new GameObject("Crosshair");
        crosshairObj.transform.parent = canvasObj.transform;
        
        UnityEngine.UI.Image crosshair = crosshairObj.AddComponent<UnityEngine.UI.Image>();
        crosshair.color = new Color(1, 1, 1, 0.8f);

        RectTransform crosshairRect = crosshairObj.GetComponent<RectTransform>();
        crosshairRect.anchorMin = new Vector2(0.5f, 0.5f);
        crosshairRect.anchorMax = new Vector2(0.5f, 0.5f);
        crosshairRect.pivot = new Vector2(0.5f, 0.5f);
        crosshairRect.anchoredPosition = Vector2.zero;
        crosshairRect.sizeDelta = new Vector2(20, 20);

        EditorUtility.DisplayDialog(
            "HUD Creado ✅",
            "Se creó un HUD básico con:\n\n" +
            "✅ Texto de salud (arriba izquierda)\n" +
            "✅ Texto de munición (abajo derecha)\n" +
            "✅ Crosshair (centro)\n\n" +
            "Puedes personalizar estos elementos en el Inspector.",
            "OK"
        );
    }

    [MenuItem("Mundo Virtual/5. Probar Escena (Play Mode)")]
    public static void PlayScene()
    {
        if (!EditorApplication.isPlaying)
        {
            EditorApplication.isPlaying = true;
            Debug.Log("▶️ Entrando en Play Mode - Prueba tu escena!");
        }
        else
        {
            EditorApplication.isPlaying = false;
            Debug.Log("⏹️ Saliendo de Play Mode");
        }
    }

    [MenuItem("Mundo Virtual/📚 Ayuda - Guía Rápida")]
    public static void ShowHelp()
    {
        EditorUtility.DisplayDialog(
            "Guía Rápida - Mundo Virtual 🎮",
            "MENÚ MUNDO VIRTUAL:\n\n" +
            "1️⃣ Crear Escena BattleArena Completa\n" +
            "   → Crea terreno 5km, player y todo listo\n\n" +
            "2️⃣ Agregar Bots AI al Mapa\n" +
            "   → Añade 3 bots de prueba\n\n" +
            "3️⃣ Agregar Vehículo de Prueba\n" +
            "   → Añade un vehículo básico\n\n" +
            "4️⃣ Configurar UI HUD Básico\n" +
            "   → Crea HUD con salud/munición\n\n" +
            "5️⃣ Probar Escena (Play Mode)\n" +
            "   → Presiona Play automáticamente\n\n" +
            "CONTROLES:\n" +
            "WASD - Mover\n" +
            "Mouse - Mirar\n" +
            "Espacio - Saltar\n\n" +
            "¡Empieza con la opción 1!",
            "Entendido"
        );
    }
}
