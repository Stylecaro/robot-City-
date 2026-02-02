using UnityEngine;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using Newtonsoft.Json;

/// <summary>
/// NetworkManager - Gestor de comunicación en tiempo real con backend Python
/// Sincroniza Unity con el sistema de IA y servidor
/// </summary>
public class NetworkManager : MonoBehaviour
{
    [Header("Configuración de Conexión")]
    public string serverUrl = "ws://localhost:8765/ws/unity";
    public float reconnectDelay = 5f;
    public bool autoConnect = true;

    [Header("Estado")]
    public bool isConnected = false;
    public int reconnectAttempts = 0;
    public float lastPingTime = 0f;

    // WebSocket
    private ClientWebSocket webSocket;
    private CancellationTokenSource cancellationToken;
    private Queue<string> messageQueue = new Queue<string>();

    // Singleton
    public static NetworkManager Instance { get; private set; }

    // Eventos
    public event Action OnConnected;
    public event Action OnDisconnected;
    public event Action<string> OnMessageReceived;

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }

    private void Start()
    {
        if (autoConnect)
        {
            _ = ConnectAsync();
        }
    }

    private void Update()
    {
        // Procesar mensajes en el hilo principal
        while (messageQueue.Count > 0)
        {
            string message = messageQueue.Dequeue();
            ProcessMessage(message);
        }
    }

    /// <summary>
    /// Conecta al servidor WebSocket
    /// </summary>
    public async Task ConnectAsync()
    {
        if (isConnected)
        {
            Debug.LogWarning("Ya está conectado al servidor");
            return;
        }

        try
        {
            Debug.Log($"🌐 Conectando a {serverUrl}...");

            webSocket = new ClientWebSocket();
            cancellationToken = new CancellationTokenSource();

            await webSocket.ConnectAsync(new Uri(serverUrl), cancellationToken.Token);

            isConnected = true;
            reconnectAttempts = 0;
            Debug.Log("✅ Conectado al servidor");

            OnConnected?.Invoke();

            // Iniciar recepción de mensajes
            _ = ReceiveMessagesAsync();
        }
        catch (Exception ex)
        {
            Debug.LogError($"❌ Error al conectar: {ex.Message}");
            isConnected = false;

            // Intentar reconexión
            reconnectAttempts++;
            await Task.Delay((int)(reconnectDelay * 1000));
            _ = ConnectAsync();
        }
    }

    /// <summary>
    /// Desconecta del servidor
    /// </summary>
    public async Task DisconnectAsync()
    {
        if (!isConnected)
            return;

        try
        {
            cancellationToken?.Cancel();
            await webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Cierre normal", CancellationToken.None);
            isConnected = false;

            Debug.Log("🔌 Desconectado del servidor");
            OnDisconnected?.Invoke();
        }
        catch (Exception ex)
        {
            Debug.LogError($"Error al desconectar: {ex.Message}");
        }
    }

    /// <summary>
    /// Envía mensaje al servidor
    /// </summary>
    public async Task SendMessageAsync(string message)
    {
        if (!isConnected)
        {
            Debug.LogWarning("No conectado al servidor");
            return;
        }

        try
        {
            byte[] buffer = Encoding.UTF8.GetBytes(message);
            await webSocket.SendAsync(
                new ArraySegment<byte>(buffer),
                WebSocketMessageType.Text,
                true,
                cancellationToken.Token
            );
        }
        catch (Exception ex)
        {
            Debug.LogError($"Error al enviar mensaje: {ex.Message}");
            isConnected = false;
            _ = ConnectAsync();
        }
    }

    /// <summary>
    /// Envía datos en formato JSON
    /// </summary>
    public async Task SendJsonAsync(object data)
    {
        string json = JsonConvert.SerializeObject(data);
        await SendMessageAsync(json);
    }

    /// <summary>
    /// Recibe mensajes del servidor
    /// </summary>
    private async Task ReceiveMessagesAsync()
    {
        byte[] buffer = new byte[8192];

        try
        {
            while (isConnected && webSocket.State == WebSocketState.Open)
            {
                WebSocketReceiveResult result = await webSocket.ReceiveAsync(
                    new ArraySegment<byte>(buffer),
                    cancellationToken.Token
                );

                if (result.MessageType == WebSocketMessageType.Close)
                {
                    isConnected = false;
                    OnDisconnected?.Invoke();
                    _ = ConnectAsync(); // Reconectar
                    break;
                }

                string message = Encoding.UTF8.GetString(buffer, 0, result.Count);
                
                // Agregar a cola para procesar en Update()
                messageQueue.Enqueue(message);
            }
        }
        catch (Exception ex)
        {
            Debug.LogError($"Error al recibir mensajes: {ex.Message}");
            isConnected = false;
            _ = ConnectAsync();
        }
    }

    /// <summary>
    /// Procesa mensaje recibido
    /// </summary>
    private void ProcessMessage(string message)
    {
        try
        {
            OnMessageReceived?.Invoke(message);

            // Parsear JSON
            var data = JsonConvert.DeserializeObject<Dictionary<string, object>>(message);

            if (data.ContainsKey("type"))
            {
                string messageType = data["type"].ToString();
                Dictionary<string, object> payload = ExtractPayload(data);

                switch (messageType)
                {
                    case "robot_update":
                        HandleRobotUpdate(data);
                        break;
                    case "city_metrics":
                        HandleCityMetrics(data);
                        break;
                    case "ai_command":
                        HandleAICommand(data);
                        break;
                    case "quantum_entangle_result":
                        HandleQuantumEntangleResult(payload);
                        break;
                    case "quantum_message_result":
                        HandleQuantumMessageResult(payload);
                        break;
                    case "ping":
                        HandlePing();
                        break;
                    default:
                        Debug.LogWarning($"Tipo de mensaje desconocido: {messageType}");
                        break;
                }
            }
        }
        catch (Exception ex)
        {
            Debug.LogError($"Error al procesar mensaje: {ex.Message}");
        }
    }

    private void HandleRobotUpdate(Dictionary<string, object> data)
    {
        // Actualizar robot en Unity
        if (CityManager.Instance != null)
        {
            CityManager.Instance.UpdateRobotFromServer(data);
        }
    }

    private void HandleCityMetrics(Dictionary<string, object> data)
    {
        // Actualizar métricas de la ciudad
        if (CityManager.Instance != null)
        {
            CityManager.Instance.UpdateMetrics(data);
        }
    }

    private void HandleAICommand(Dictionary<string, object> data)
    {
        // Ejecutar comando de IA
        Debug.Log($"🤖 Comando IA: {data["command"]}");
    }

    private void HandleQuantumEntangleResult(Dictionary<string, object> data)
    {
        if (CityManager.Instance != null)
        {
            CityManager.Instance.HandleQuantumEntangleResult(data);
        }
    }

    private void HandleQuantumMessageResult(Dictionary<string, object> data)
    {
        if (CityManager.Instance != null)
        {
            CityManager.Instance.HandleQuantumMessageResult(data);
        }
    }

    private async void HandlePing()
    {
        lastPingTime = Time.time;
        await SendJsonAsync(new { type = "pong", timestamp = DateTime.Now.ToString("o") });
    }

    private Dictionary<string, object> ExtractPayload(Dictionary<string, object> data)
    {
        if (data == null || !data.ContainsKey("data") || data["data"] == null)
        {
            return new Dictionary<string, object>();
        }

        try
        {
            return JsonConvert.DeserializeObject<Dictionary<string, object>>(data["data"].ToString());
        }
        catch
        {
            return new Dictionary<string, object>();
        }
    }

    public async Task CreateQuantumChannel(string nodeA, string nodeB, float fidelity = 0.98f)
    {
        await SendJsonAsync(new
        {
            type = "quantum_entangle",
            node_a = nodeA,
            node_b = nodeB,
            fidelity = fidelity
        });
    }

    public async Task SendQuantumMessage(string channelId, string message, float noise = 0.01f)
    {
        await SendJsonAsync(new
        {
            type = "quantum_message",
            channel_id = channelId,
            message = message,
            noise = noise
        });
    }

    private void OnDestroy()
    {
        _ = DisconnectAsync();
    }

    private void OnApplicationQuit()
    {
        _ = DisconnectAsync();
    }
}
