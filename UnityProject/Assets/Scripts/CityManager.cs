using UnityEngine;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

/// <summary>
/// CityManager - Gestión central de la Ciudad Robot
/// Coordina edificios, robots, recursos y sincronización con IA
/// </summary>
public class CityManager : MonoBehaviour
{
    [Header("Referencias")]
    public Transform buildingsParent;
    public Transform robotsParent;
    public GameObject robotPrefab;

    [Header("Configuración de Ciudad")]
    public int maxRobots = 200;
    public float citySize = 200f;
    public bool autoSpawnRobots = true;
    public float spawnInterval = 5f;

    [Header("Métricas en Tiempo Real")]
    public int totalRobots = 0;
    public int activeRobots = 0;
    public float manufacturingEfficiency = 0f;
    public float researchProgress = 0f;
    public float securityLevel = 0f;
    public float energyConsumption = 0f;

    // Gestión de robots
    [Header("Núcleo Cuántico")]
    public bool showQuantumOverlay = true;
    public string centralQuantumNodeId = "";
    public string lastQuantumChannelId = "";
    public string lastQuantumMessage = "";
    public float lastQuantumBitErrorRate = 0f;
    public float lastQuantumFidelity = 0f;
    public string lastQuantumTarget = "";
    private Dictionary<string, RobotController> robots = new Dictionary<string, RobotController>();
    private List<GameObject> buildings = new List<GameObject>();
    private float lastSpawnTime = 0f;

    // Singleton
    public static CityManager Instance { get; private set; }

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
        }
        else
        {
            Destroy(gameObject);
        }
    }

    private void Start()
    {
        SetupCity();
        
        if (autoSpawnRobots)
        {
            SpawnInitialRobots();
        }

        // Sincronizar con IA cada 5 segundos
        InvokeRepeating(nameof(SyncWithAI), 1f, 5f);
    }

    private void Update()
    {
        UpdateMetrics();

        // Auto-spawn de robots
        if (autoSpawnRobots && Time.time - lastSpawnTime > spawnInterval)
        {
            if (totalRobots < maxRobots)
            {
                SpawnRobot(GetRandomRobotType());
                lastSpawnTime = Time.time;
            }
        }
        UpdateQuantumVisuals();
    }

    /// <summary>
    /// Configura la ciudad inicial
    /// </summary>
    private void SetupCity()
    {
        Debug.Log("🏙️ Configurando Ciudad Robot...");

        // Crear padres si no existen
        if (buildingsParent == null)
        {
            buildingsParent = new GameObject("Buildings").transform;
        }

        if (robotsParent == null)
        {
            robotsParent = new GameObject("Robots").transform;
        }

        // Crear edificios principales
        CreateBuilding("Manufacturing Center", new Vector3(-40, 0, -40), Color.blue, 30f, 60f);
        CreateBuilding("Research Lab", new Vector3(40, 0, -40), Color.green, 25f, 80f);
        CreateBuilding("Security HQ", new Vector3(-40, 0, 40), Color.red, 35f, 50f);
        CreateBuilding("AI Core", new Vector3(40, 0, 40), Color.yellow, 40f, 100f);
        CreateQuantumCore(new Vector3(0, 0, 0));

        // Crear estaciones de carga
        for (int i = 0; i < 4; i++)
        {
            float angle = i * 90f * Mathf.Deg2Rad;
            Vector3 pos = new Vector3(Mathf.Cos(angle) * 60f, 0, Mathf.Sin(angle) * 60f);
            CreateChargeStation(pos);
        }

        // Crear terreno/plaza central
        CreateCentralPlaza();

        Debug.Log($"✅ Ciudad creada con {buildings.Count} edificios");
    }

    /// <summary>
    /// Crea un edificio
    /// </summary>
    private void CreateBuilding(string name, Vector3 position, Color color, float width, float height)
    {
        GameObject building = GameObject.CreatePrimitive(PrimitiveType.Cube);
        building.name = name;
        building.transform.parent = buildingsParent;
        building.transform.position = position + Vector3.up * (height / 2f);
        building.transform.localScale = new Vector3(width, height, width);

        // Material y color
        Renderer renderer = building.GetComponent<Renderer>();
        renderer.material = new Material(Shader.Find("Standard"));
        renderer.material.color = color;
        renderer.material.SetFloat("_Metallic", 0.5f);
        renderer.material.SetFloat("_Glossiness", 0.8f);

        // Añadir emisión para efecto neón
        renderer.material.EnableKeyword("_EMISSION");
        renderer.material.SetColor("_EmissionColor", color * 0.3f);

        buildings.Add(building);

        // Crear letrero
        CreateBuildingSign(building, name);
    }

    /// <summary>
    /// Crea letrero flotante para edificio
    /// </summary>
    private void CreateBuildingSign(GameObject building, string text)
    {
        GameObject sign = new GameObject($"{text}_Sign");
        sign.transform.parent = building.transform;
        sign.transform.localPosition = Vector3.up * (building.transform.localScale.y / 2f + 5f);
        sign.transform.localRotation = Quaternion.identity;

        TextMesh textMesh = sign.AddComponent<TextMesh>();
        textMesh.text = text;
        textMesh.fontSize = 50;
        textMesh.alignment = TextAlignment.Center;
        textMesh.anchor = TextAnchor.MiddleCenter;
        textMesh.color = Color.white;
    }

    /// <summary>
    /// Crea estación de carga
    /// </summary>
    private void CreateChargeStation(Vector3 position)
    {
        GameObject station = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
        station.name = "ChargeStation";
        station.tag = "ChargeStation";
        station.transform.parent = buildingsParent;
        station.transform.position = position + Vector3.up * 2.5f;
        station.transform.localScale = new Vector3(5f, 5f, 5f);

        Renderer renderer = station.GetComponent<Renderer>();
        renderer.material.color = Color.cyan;
        renderer.material.EnableKeyword("_EMISSION");
        renderer.material.SetColor("_EmissionColor", Color.cyan * 0.5f);

        // Añadir luz
        Light light = station.AddComponent<Light>();
        light.color = Color.cyan;
        light.intensity = 2f;
        light.range = 15f;
    }

    /// <summary>
    /// Crea plaza central
    /// </summary>
    private void CreateCentralPlaza()
    {
        GameObject plaza = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
        plaza.name = "Central Plaza";
        plaza.transform.parent = buildingsParent;
        plaza.transform.position = Vector3.up * 0.1f;
        plaza.transform.localScale = new Vector3(80f, 0.2f, 80f);

        Renderer renderer = plaza.GetComponent<Renderer>();
        renderer.material.color = new Color(0.3f, 0.3f, 0.3f);
    }

    /// <summary>
    /// Genera robots iniciales
    /// </summary>
    private void SpawnInitialRobots()
    {
        string[] types = { "manufacturing", "research", "security", "maintenance" };

        for (int i = 0; i < 20; i++)
        {
            string type = types[Random.Range(0, types.Length)];
            SpawnRobot(type);
        }

        Debug.Log($"🤖 {totalRobots} robots iniciales generados");
    }

    /// <summary>
    /// Genera un nuevo robot
    /// </summary>
    public GameObject SpawnRobot(string robotType)
    {
        if (totalRobots >= maxRobots)
        {
            Debug.LogWarning("⚠️ Límite de robots alcanzado");
            return null;
        }

        // Crear prefab o primitivo
        GameObject robot;

        if (robotPrefab != null)
        {
            robot = Instantiate(robotPrefab, robotsParent);
        }
        else
        {
            robot = CreateDefaultRobotMesh(robotType);
        }

        // Posición aleatoria
        Vector3 spawnPos = new Vector3(
            Random.Range(-citySize / 2, citySize / 2),
            1f,
            Random.Range(-citySize / 2, citySize / 2)
        );
        robot.transform.position = spawnPos;

        // Configurar controller
        RobotController controller = robot.GetComponent<RobotController>();
        if (controller == null)
        {
            controller = robot.AddComponent<RobotController>();
        }

        controller.robotType = robotType;
        controller.robotId = $"{robotType}_{totalRobots}_{Random.Range(100, 999)}";

        // Registrar
        RegisterRobot(controller);

        Debug.Log($"🤖 Robot creado: {controller.robotId} ({robotType})");

        return robot;
    }

    /// <summary>
    /// Crea mesh por defecto para robot
    /// </summary>
    private GameObject CreateDefaultRobotMesh(string robotType)
    {
        GameObject robot = new GameObject($"Robot_{robotType}");
        robot.transform.parent = robotsParent;

        // Cuerpo
        GameObject body = GameObject.CreatePrimitive(PrimitiveType.Capsule);
        body.transform.parent = robot.transform;
        body.transform.localPosition = Vector3.up * 1f;
        body.transform.localScale = new Vector3(1f, 1.5f, 1f);

        // Cabeza
        GameObject head = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        head.transform.parent = robot.transform;
        head.transform.localPosition = Vector3.up * 2.5f;
        head.transform.localScale = Vector3.one * 0.8f;

        // Color según tipo
        Color robotColor = GetColorForType(robotType);
        body.GetComponent<Renderer>().material.color = robotColor;
        head.GetComponent<Renderer>().material.color = robotColor;

        // Añadir componentes
        CharacterController cc = robot.AddComponent<CharacterController>();
        cc.radius = 0.5f;
        cc.height = 3f;
        cc.center = Vector3.up * 1.5f;

        // Trail opcional
        TrailRenderer trail = robot.AddComponent<TrailRenderer>();
        trail.time = 1f;
        trail.startWidth = 0.3f;
        trail.endWidth = 0.05f;
        trail.material = new Material(Shader.Find("Sprites/Default"));
        trail.startColor = robotColor;
        trail.endColor = new Color(robotColor.r, robotColor.g, robotColor.b, 0f);

        return robot;
    }

    /// <summary>
    /// Obtiene color según tipo de robot
    /// </summary>
    private Color GetColorForType(string type)
    {
        switch (type)
        {
            case "manufacturing": return Color.blue;
            case "research": return Color.green;
            case "security": return Color.red;
            case "maintenance": return Color.yellow;
            default: return Color.white;
        }
    }

    /// <summary>
    /// Tipo de robot aleatorio
    /// </summary>
    private string GetRandomRobotType()
    {
        string[] types = { "manufacturing", "research", "security", "maintenance" };
        return types[Random.Range(0, types.Length)];
    }

    /// <summary>
    /// Registra un robot
    /// </summary>
    public void RegisterRobot(RobotController robot)
    {
        if (!robots.ContainsKey(robot.robotId))
        {
            robots[robot.robotId] = robot;
            totalRobots = robots.Count;
        }
    }

    /// <summary>
    /// Elimina un robot
    /// </summary>
    public void RemoveRobot(string robotId)
    {
        if (robots.ContainsKey(robotId))
        {
            Destroy(robots[robotId].gameObject);
            robots.Remove(robotId);
            totalRobots = robots.Count;
        }
    }

    /// <summary>
    /// Actualiza métricas de la ciudad
    /// </summary>
    private void UpdateMetrics()
    {
        totalRobots = robots.Count;
        activeRobots = robots.Values.Count(r => r.currentState == "working" || r.currentState == "patrol");

        // Calcular eficiencias
        if (totalRobots > 0)
        {
            manufacturingEfficiency = robots.Values
                .Where(r => r.robotType == "manufacturing")
                .Average(r => r.batteryLevel);

            researchProgress = robots.Values
                .Where(r => r.robotType == "research")
                .Average(r => r.health);

            securityLevel = robots.Values
                .Where(r => r.robotType == "security")
                .Count() / (float)totalRobots;

            energyConsumption = 1f - robots.Values.Average(r => r.batteryLevel);
        }
    }

    /// <summary>
    /// Actualiza robot desde servidor
    /// </summary>
    public void UpdateRobotFromServer(Dictionary<string, object> data)
    {
        if (!data.ContainsKey("robot_id"))
            return;

        string robotId = data["robot_id"].ToString();

        if (robots.ContainsKey(robotId))
        {
            robots[robotId].UpdateFromServer(data);
        }
    }

    /// <summary>
    /// Actualiza métricas desde servidor
    /// </summary>
    public void UpdateMetrics(Dictionary<string, object> data)
    {
        if (data.ContainsKey("manufacturing_efficiency"))
            manufacturingEfficiency = float.Parse(data["manufacturing_efficiency"].ToString());

        if (data.ContainsKey("research_progress"))
            researchProgress = float.Parse(data["research_progress"].ToString());

        if (data.ContainsKey("security_level"))
            securityLevel = float.Parse(data["security_level"].ToString());

        if (data.ContainsKey("energy_consumption"))
            energyConsumption = float.Parse(data["energy_consumption"].ToString());
    }

    public void HandleQuantumEntangleResult(Dictionary<string, object> data)
    {
        if (data == null)
            return;

        if (data.ContainsKey("channel_id"))
            lastQuantumChannelId = data["channel_id"].ToString();

        if (data.ContainsKey("fidelity"))
            lastQuantumFidelity = float.Parse(data["fidelity"].ToString());
    }

    public void HandleQuantumMessageResult(Dictionary<string, object> data)
    {
        if (data == null)
            return;

        if (data.ContainsKey("channel_id"))
            lastQuantumChannelId = data["channel_id"].ToString();

        if (data.ContainsKey("received"))
            lastQuantumMessage = data["received"].ToString();

        if (data.ContainsKey("bit_error_rate"))
            lastQuantumBitErrorRate = float.Parse(data["bit_error_rate"].ToString());

        if (data.ContainsKey("fidelity"))
            lastQuantumFidelity = float.Parse(data["fidelity"].ToString());

        if (data.ContainsKey("target"))
            lastQuantumTarget = data["target"].ToString();
    }

    /// <summary>
    /// Sincroniza con sistema de IA
    /// </summary>
    private async void SyncWithAI()
    {
        if (NetworkManager.Instance == null || !NetworkManager.Instance.isConnected)
            return;

        var cityData = new
        {
            type = "city_status",
            total_robots = totalRobots,
            active_robots = activeRobots,
            manufacturing_efficiency = manufacturingEfficiency,
            research_progress = researchProgress,
            security_level = securityLevel,
            energy_consumption = energyConsumption,
            robots = robots.Values.Select(r => r.GetStatus()).ToList()
        };

        await NetworkManager.Instance.SendJsonAsync(cityData);
    }

    /// <summary>
    /// Obtiene robot por ID
    /// </summary>
    public RobotController GetRobot(string robotId)
    {
        return robots.ContainsKey(robotId) ? robots[robotId] : null;
    }

    /// <summary>
    /// Obtiene todos los robots
    /// </summary>
    public List<RobotController> GetAllRobots()
    {
        return robots.Values.ToList();
    }

    /// <summary>
    /// Obtiene robots por tipo
    /// </summary>
    public List<RobotController> GetRobotsByType(string robotType)
    {
        return robots.Values.Where(r => r.robotType == robotType).ToList();
    }

    private void OnDrawGizmos()
    {
        // Dibujar límites de la ciudad
        Gizmos.color = Color.cyan;
        Gizmos.DrawWireCube(Vector3.zero, new Vector3(citySize, 10f, citySize));

        // Dibujar info de robots
        if (robots != null)
        {
            Gizmos.color = Color.green;
            foreach (var robot in robots.Values)
            {
                if (robot != null)
                {
                    Gizmos.DrawLine(robot.transform.position, robot.transform.position + Vector3.up * 5f);
                }
            }
        }
    }

    private void OnGUI()
    {
        if (!showQuantumOverlay)
            return;

        GUI.color = Color.white;
        GUILayout.BeginArea(new Rect(20, 20, 360, 160), "", "box");
        GUILayout.Label("⚛️ Núcleo Cuántico");
        GUILayout.Label($"Canal: {(string.IsNullOrEmpty(lastQuantumChannelId) ? "-" : lastQuantumChannelId)}");
        GUILayout.Label($"Fidelidad: {lastQuantumFidelity:0.000}");
        GUILayout.Label($"BER: {lastQuantumBitErrorRate:0.000000}");
        GUILayout.Label($"Destino: {(string.IsNullOrEmpty(lastQuantumTarget) ? "central_city" : lastQuantumTarget)}");
        GUILayout.Label($"Mensaje: {(string.IsNullOrEmpty(lastQuantumMessage) ? "-" : lastQuantumMessage)}");
        GUILayout.EndArea();
    }

    private GameObject quantumCoreObject;

    private void CreateQuantumCore(Vector3 position)
    {
        quantumCoreObject = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        quantumCoreObject.name = "Quantum Core";
        quantumCoreObject.transform.parent = buildingsParent;
        quantumCoreObject.transform.position = position + Vector3.up * 6f;
        quantumCoreObject.transform.localScale = new Vector3(12f, 12f, 12f);

        Renderer renderer = quantumCoreObject.GetComponent<Renderer>();
        renderer.material = new Material(Shader.Find("Standard"));
        renderer.material.color = new Color(0.35f, 0.0f, 0.9f);
        renderer.material.EnableKeyword("_EMISSION");
        renderer.material.SetColor("_EmissionColor", new Color(0.4f, 0.2f, 1f));

        Light light = quantumCoreObject.AddComponent<Light>();
        light.color = new Color(0.6f, 0.4f, 1f);
        light.intensity = 3f;
        light.range = 25f;
    }

    private void UpdateQuantumVisuals()
    {
        if (quantumCoreObject == null)
            return;

        float pulse = 1.5f + Mathf.Sin(Time.time * 2f) * 0.5f;
        quantumCoreObject.transform.localScale = new Vector3(12f, 12f, 12f) * pulse;

        Renderer renderer = quantumCoreObject.GetComponent<Renderer>();
        if (renderer != null)
        {
            float intensity = Mathf.Clamp01(lastQuantumFidelity > 0 ? lastQuantumFidelity : 0.5f);
            Color glow = Color.Lerp(new Color(0.4f, 0.2f, 1f), new Color(0.2f, 1f, 1f), intensity);
            renderer.material.SetColor("_EmissionColor", glow * (0.7f + intensity));
        }
    }
}
