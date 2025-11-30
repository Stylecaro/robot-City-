using UnityEngine;
using System.Collections.Generic;
using System.Threading.Tasks;

/// <summary>
/// RobotController - Controlador individual de robot con IA
/// Maneja movimiento, comportamiento y sincronización con backend
/// </summary>
[RequireComponent(typeof(CharacterController))]
public class RobotController : MonoBehaviour
{
    [Header("Identificación")]
    public string robotId;
    public string robotType; // manufacturing, research, security, maintenance

    [Header("Estado")]
    public string currentState = "idle";
    public float batteryLevel = 1.0f;
    public float health = 1.0f;
    public int tasksCompleted = 0;

    [Header("Movimiento")]
    public float speed = 5f;
    public float rotationSpeed = 5f;
    public List<Vector3> currentPath = new List<Vector3>();
    private int pathIndex = 0;

    [Header("Visual")]
    public Color idleColor = Color.green;
    public Color workingColor = Color.yellow;
    public Color chargingColor = Color.blue;
    public Color emergencyColor = Color.red;

    private CharacterController controller;
    private Renderer robotRenderer;
    private Vector3 targetPosition;
    private bool hasTarget = false;

    // Componentes opcionales
    private TrailRenderer trail;
    private ParticleSystem particles;

    private void Awake()
    {
        controller = GetComponent<CharacterController>();
        robotRenderer = GetComponentInChildren<Renderer>();
        trail = GetComponent<TrailRenderer>();
        particles = GetComponentInChildren<ParticleSystem>();

        // Generar ID único si no existe
        if (string.IsNullOrEmpty(robotId))
        {
            robotId = $"{robotType}_{Random.Range(1000, 9999)}";
        }
    }

    private void Start()
    {
        UpdateVisuals();
        RegisterWithCityManager();

        // Sincronizar con backend
        _ = SendStatusUpdateAsync();
    }

    private void Update()
    {
        UpdateMovement();
        UpdateBattery();
        UpdateVisuals();

        // Sincronizar cada 2 segundos
        if (Time.frameCount % 120 == 0)
        {
            _ = SendStatusUpdateAsync();
        }
    }

    /// <summary>
    /// Actualiza el movimiento del robot
    /// </summary>
    private void UpdateMovement()
    {
        if (currentPath.Count == 0 || pathIndex >= currentPath.Count)
        {
            hasTarget = false;
            return;
        }

        hasTarget = true;
        targetPosition = currentPath[pathIndex];

        // Calcular dirección
        Vector3 direction = (targetPosition - transform.position).normalized;
        direction.y = 0; // Mantener en el plano

        if (direction.magnitude > 0.1f)
        {
            // Rotar hacia el objetivo
            Quaternion targetRotation = Quaternion.LookRotation(direction);
            transform.rotation = Quaternion.Slerp(
                transform.rotation,
                targetRotation,
                rotationSpeed * Time.deltaTime
            );

            // Mover hacia el objetivo
            Vector3 movement = direction * speed * Time.deltaTime;
            controller.SimpleMove(movement);
        }

        // Verificar si llegó al waypoint
        float distance = Vector3.Distance(transform.position, targetPosition);
        if (distance < 1f)
        {
            pathIndex++;

            if (pathIndex >= currentPath.Count)
            {
                OnPathCompleted();
            }
        }
    }

    /// <summary>
    /// Actualiza el nivel de batería
    /// </summary>
    private void UpdateBattery()
    {
        if (currentState == "charging")
        {
            batteryLevel = Mathf.Min(1f, batteryLevel + 0.05f * Time.deltaTime);

            if (batteryLevel > 0.9f)
            {
                SetState("idle");
            }
        }
        else if (currentState == "working" || hasTarget)
        {
            batteryLevel = Mathf.Max(0f, batteryLevel - 0.01f * Time.deltaTime);

            if (batteryLevel < 0.2f)
            {
                SetState("charging");
                GoToChargeStation();
            }
        }
    }

    /// <summary>
    /// Actualiza visuales según el estado
    /// </summary>
    private void UpdateVisuals()
    {
        if (robotRenderer == null)
            return;

        Color targetColor = idleColor;

        switch (currentState)
        {
            case "idle":
                targetColor = idleColor;
                break;
            case "working":
            case "patrol":
                targetColor = workingColor;
                break;
            case "charging":
                targetColor = chargingColor;
                break;
            case "emergency":
                targetColor = emergencyColor;
                break;
        }

        // Aplicar color con batería como intensidad
        targetColor = Color.Lerp(Color.gray, targetColor, batteryLevel);
        robotRenderer.material.color = Color.Lerp(
            robotRenderer.material.color,
            targetColor,
            Time.deltaTime * 2f
        );

        // Activar/desactivar trail
        if (trail != null)
        {
            trail.emitting = hasTarget;
        }

        // Partículas en emergencia
        if (particles != null)
        {
            if (currentState == "emergency" && !particles.isPlaying)
            {
                particles.Play();
            }
            else if (currentState != "emergency" && particles.isPlaying)
            {
                particles.Stop();
            }
        }
    }

    /// <summary>
    /// Cambia el estado del robot
    /// </summary>
    public void SetState(string newState)
    {
        if (currentState != newState)
        {
            Debug.Log($"🤖 {robotId}: {currentState} → {newState}");
            currentState = newState;
            _ = SendStatusUpdateAsync();
        }
    }

    /// <summary>
    /// Asigna un nuevo camino al robot
    /// </summary>
    public void SetPath(List<Vector3> path)
    {
        currentPath = path;
        pathIndex = 0;

        if (path.Count > 0)
        {
            SetState("patrol");
        }
    }

    /// <summary>
    /// Va a posición específica
    /// </summary>
    public void GoToPosition(Vector3 position)
    {
        currentPath = new List<Vector3> { position };
        pathIndex = 0;
        SetState("working");
    }

    /// <summary>
    /// Va a la estación de carga
    /// </summary>
    public void GoToChargeStation()
    {
        // Buscar estación de carga más cercana
        GameObject[] chargeStations = GameObject.FindGameObjectsWithTag("ChargeStation");

        if (chargeStations.Length > 0)
        {
            GameObject nearest = chargeStations[0];
            float minDistance = Vector3.Distance(transform.position, nearest.transform.position);

            foreach (GameObject station in chargeStations)
            {
                float distance = Vector3.Distance(transform.position, station.transform.position);
                if (distance < minDistance)
                {
                    minDistance = distance;
                    nearest = station;
                }
            }

            GoToPosition(nearest.transform.position);
            SetState("charging");
        }
        else
        {
            // Ir al origen como fallback
            GoToPosition(Vector3.zero);
            SetState("charging");
        }
    }

    /// <summary>
    /// Callback cuando completa un camino
    /// </summary>
    private void OnPathCompleted()
    {
        Debug.Log($"✅ {robotId}: Camino completado");
        currentPath.Clear();
        pathIndex = 0;

        if (currentState == "working")
        {
            tasksCompleted++;
        }

        SetState("idle");
    }

    /// <summary>
    /// Registra el robot con CityManager
    /// </summary>
    private void RegisterWithCityManager()
    {
        if (CityManager.Instance != null)
        {
            CityManager.Instance.RegisterRobot(this);
        }
    }

    /// <summary>
    /// Envía actualización de estado al servidor
    /// </summary>
    private async Task SendStatusUpdateAsync()
    {
        if (NetworkManager.Instance == null || !NetworkManager.Instance.isConnected)
            return;

        var status = new
        {
            type = "robot_update",
            robot_id = robotId,
            robot_type = robotType,
            position = new float[] { transform.position.x, transform.position.y, transform.position.z },
            state = currentState,
            battery_level = batteryLevel,
            health = health,
            tasks_completed = tasksCompleted
        };

        await NetworkManager.Instance.SendJsonAsync(status);
    }

    /// <summary>
    /// Actualiza desde datos del servidor
    /// </summary>
    public void UpdateFromServer(Dictionary<string, object> data)
    {
        if (data.ContainsKey("state"))
        {
            SetState(data["state"].ToString());
        }

        if (data.ContainsKey("battery_level"))
        {
            batteryLevel = float.Parse(data["battery_level"].ToString());
        }

        if (data.ContainsKey("target_position"))
        {
            var pos = data["target_position"] as List<object>;
            if (pos != null && pos.Count == 3)
            {
                Vector3 target = new Vector3(
                    float.Parse(pos[0].ToString()),
                    float.Parse(pos[1].ToString()),
                    float.Parse(pos[2].ToString())
                );
                GoToPosition(target);
            }
        }
    }

    /// <summary>
    /// Obtiene estado como diccionario
    /// </summary>
    public Dictionary<string, object> GetStatus()
    {
        return new Dictionary<string, object>
        {
            { "robot_id", robotId },
            { "robot_type", robotType },
            { "position", new float[] { transform.position.x, transform.position.y, transform.position.z } },
            { "state", currentState },
            { "battery_level", batteryLevel },
            { "health", health },
            { "tasks_completed", tasksCompleted },
            { "has_target", hasTarget }
        };
    }

    private void OnDrawGizmos()
    {
        // Dibujar camino en el editor
        if (currentPath.Count > 0)
        {
            Gizmos.color = Color.cyan;

            for (int i = 0; i < currentPath.Count - 1; i++)
            {
                Gizmos.DrawLine(currentPath[i], currentPath[i + 1]);
            }

            // Dibujar target actual
            if (pathIndex < currentPath.Count)
            {
                Gizmos.color = Color.green;
                Gizmos.DrawWireSphere(currentPath[pathIndex], 0.5f);
            }
        }

        // Dibujar rango de batería
        Gizmos.color = Color.Lerp(Color.red, Color.green, batteryLevel);
        Gizmos.DrawWireSphere(transform.position, 1f);
    }
}
