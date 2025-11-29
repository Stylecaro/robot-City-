using System;
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using System.Text;

public class WebSocketManager : MonoBehaviour 
{
    [Header("Conexión Web")]
    public string webSocketUrl = "ws://localhost:8000/ws";
    public string dashboardUrl = "http://localhost:8000";
    
    [Header("Estado de Conexión")]
    public bool isConnected = false;
    public string connectionStatus = "Desconectado";
    
    [Header("Datos del Metaverso")]
    public MetaversoData metaversoData = new MetaversoData();
    
    private GameManager gameManager;
    
    void Start()
    {
        gameManager = GetComponent<GameManager>();
        StartCoroutine(ConnectToBackend());
        
        // Actualizar datos cada 5 segundos
        InvokeRepeating("UpdateMetaversoData", 1f, 5f);
    }
    
    IEnumerator ConnectToBackend()
    {
        Debug.Log("🔗 Conectando con backend web...");
        connectionStatus = "Conectando...";
        
        // Verificar si el servidor web está disponible
        UnityWebRequest request = UnityWebRequest.Get(dashboardUrl);
        yield return request.SendWebRequest();
        
        if (request.result == UnityWebRequest.Result.Success)
        {
            isConnected = true;
            connectionStatus = "Conectado ✅";
            Debug.Log("✅ Conexión establecida con dashboard web");
            
            // Enviar datos iniciales
            StartCoroutine(SendMetaversoState());
        }
        else
        {
            isConnected = false;  
            connectionStatus = "Error de conexión ❌";
            Debug.LogWarning("⚠️ No se pudo conectar al dashboard web");
            
            // Reintentar conexión en 10 segundos
            yield return new WaitForSeconds(10f);
            StartCoroutine(ConnectToBackend());
        }
    }
    
    void UpdateMetaversoData()
    {
        if (!isConnected) return;
        
        // Actualizar datos del metaverso
        metaversoData.timestamp = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
        metaversoData.activeRobots = UnityEngine.Random.Range(15, 25);
        metaversoData.manufacturingRate = UnityEngine.Random.Range(80, 100);
        metaversoData.researchProgress = UnityEngine.Random.Range(60, 85);
        metaversoData.securityLevel = UnityEngine.Random.Range(90, 100);
        metaversoData.aiProcessing = UnityEngine.Random.Range(70, 95);
        
        // Enviar al dashboard web
        StartCoroutine(SendMetaversoState());
    }
    
    IEnumerator SendMetaversoState()
    {
        string jsonData = JsonUtility.ToJson(metaversoData);
        byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonData);
        
        UnityWebRequest request = new UnityWebRequest(dashboardUrl + "/api/unity-data", "POST");
        request.uploadHandler = new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");
        
        yield return request.SendWebRequest();
        
        if (request.result == UnityWebRequest.Result.Success)
        {
            Debug.Log("📊 Datos enviados al dashboard web");
        }
        else
        {
            Debug.LogWarning("⚠️ Error enviando datos: " + request.error);
        }
    }
    
    // Método llamado desde el dashboard web
    public void ReceiveWebCommand(string command)
    {
        Debug.Log("🌐 Comando recibido del web: " + command);
        
        switch (command)
        {
            case "reset_camera":
                ResetCameraPosition();
                break;
                
            case "show_robots":
                ShowAllRobots();
                break;
                
            case "manufacturing_focus":
                FocusOnBuilding("Manufacturing");
                break;
                
            case "research_focus":
                FocusOnBuilding("Research");
                break;
                
            case "security_focus":
                FocusOnBuilding("Security");
                break;
                
            case "ai_focus":
                FocusOnBuilding("AI");
                break;
        }
    }
    
    void ResetCameraPosition()
    {
        Camera.main.transform.position = new Vector3(0, 15, -20);
        Camera.main.transform.LookAt(Vector3.zero);
        Debug.log("📷 Cámara restablecida");
    }
    
    void ShowAllRobots()
    {
        // Mostrar todos los robots activos
        GameObject[] robots = GameObject.FindGameObjectsWithTag("Robot");
        foreach (GameObject robot in robots)
        {
            robot.GetComponent<Renderer>().enabled = true;
        }
        Debug.Log("🤖 Mostrando todos los robots");
    }
    
    void FocusOnBuilding(string buildingName)
    {
        GameObject building = GameObject.Find(buildingName + " Center");
        if (building != null)
        {
            Camera.main.transform.position = building.transform.position + Vector3.up * 10 + Vector3.back * 15;
            Camera.main.transform.LookAt(building.transform);
            Debug.Log("🏢 Enfocando en " + buildingName);
        }
    }
    
    void OnGUI()
    {
        GUI.Box(new Rect(10, 10, 300, 120), "🔗 Conexión Web Dashboard");
        GUI.Label(new Rect(20, 35), "Estado: " + connectionStatus);
        GUI.Label(new Rect(20, 55), "URL: " + dashboardUrl);
        GUI.Label(new Rect(20, 75), "Robots Activos: " + metaversoData.activeRobots);
        GUI.Label(new Rect(20, 95), "Manufacturing: " + metaversoData.manufacturingRate + "%");
        
        if (GUI.Button(new Rect(20, 140, 100, 25), "Reconectar"))
        {
            StartCoroutine(ConnectToBackend());
        }
        
        if (GUI.Button(new Rect(130, 140, 100, 25), "Abrir Web"))
        {
            Application.OpenURL(dashboardUrl);
        }
    }
}

[System.Serializable]
public class MetaversoData
{
    public string timestamp;
    public int activeRobots;
    public int manufacturingRate;
    public int researchProgress;
    public int securityLevel;
    public int aiProcessing;
    public Vector3 cameraPosition;
    public string currentFocus;
}