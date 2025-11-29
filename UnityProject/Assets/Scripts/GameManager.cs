using UnityEngine;

public class GameManager : MonoBehaviour
{
    [Header("Integración Web")]
    public WebSocketManager webSocketManager;
    
    void Start()
    {
        Debug.Log("🤖 ¡Bienvenido a Ciudad Robot Metaverso!");
        CreateBasicWorld();
        
        // Configurar WebSocket Manager si existe
        if (webSocketManager == null)
        {
            webSocketManager = gameObject.AddComponent<WebSocketManager>();
        }
    }
    
    void CreateBasicWorld()
    {
        // Crear terreno
        GameObject ground = GameObject.CreatePrimitive(PrimitiveType.Plane);
        ground.name = "Ground";
        ground.transform.localScale = new Vector3(10, 1, 10);
        
        // Edificios de la ciudad
        CreateBuilding(new Vector3(-5, 1, 0), Color.blue, "Manufacturing");
        CreateBuilding(new Vector3(5, 1, 0), Color.green, "Research Lab");
        CreateBuilding(new Vector3(0, 1, -5), Color.red, "Security HQ");
        CreateBuilding(new Vector3(0, 1, 5), Color.yellow, "AI Center");
        
        // Configurar cámara
        Camera.main.transform.position = new Vector3(0, 8, -12);
        Camera.main.transform.LookAt(Vector3.zero);
        
        Debug.Log("✅ Mundo básico creado - ¡Explora la ciudad!");
    }
    
    GameObject CreateBuilding(Vector3 pos, Color color, string name)
    {
        GameObject building = GameObject.CreatePrimitive(PrimitiveType.Cube);
        building.name = name;
        building.transform.position = pos;
        building.transform.localScale = new Vector3(2, 3, 2);
        building.GetComponent<Renderer>().material.color = color;
        return building;
    }
}