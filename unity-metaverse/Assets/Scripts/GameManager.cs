using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using SocketIOClient;

namespace CiudadRobot
{
    public class GameManager : MonoBehaviour
    {
        [Header("Configuración de Conexión")]
        public string backendUrl = "http://localhost:3000";
        public string websocketUrl = "ws://localhost:3000";
        
        [Header("Managers")]
        public NetworkManager networkManager;
        public CityManager cityManager;
        public RobotManager robotManager;
        public UIManager uiManager;
        
        private SocketIOUnity socket;
        
        void Start()
        {
            InitializeGame();
            ConnectToBackend();
        }
        
        void InitializeGame()
        {
            Debug.Log("Inicializando Ciudad Robot Metaverso...");
            
            // Inicializar managers
            if (networkManager != null) networkManager.Initialize();
            if (cityManager != null) cityManager.Initialize();
            if (robotManager != null) robotManager.Initialize();
            if (uiManager != null) uiManager.Initialize();
        }
        
        void ConnectToBackend()
        {
            try
            {
                // Configurar WebSocket
                socket = new SocketIOUnity(websocketUrl);
                
                socket.OnConnected += (sender, e) =>
                {
                    Debug.Log("Conectado al backend del metaverso");
                    uiManager?.ShowConnectionStatus(true);
                };
                
                socket.OnDisconnected += (sender, e) =>
                {
                    Debug.Log("Desconectado del backend");
                    uiManager?.ShowConnectionStatus(false);
                };
                
                // Eventos del sistema
                socket.On("robot_update", OnRobotUpdate);
                socket.On("city_update", OnCityUpdate);
                socket.On("manufacturing_update", OnManufacturingUpdate);
                socket.On("research_update", OnResearchUpdate);
                
                socket.Connect();
            }
            catch (System.Exception ex)
            {
                Debug.LogError($"Error conectando al backend: {ex.Message}");
            }
        }
        
        void OnRobotUpdate(SocketIOResponse response)
        {
            Debug.Log("Actualización de robot recibida");
            // Procesar actualización de robot
            robotManager?.HandleRobotUpdate(response.GetValue<string>());
        }
        
        void OnCityUpdate(SocketIOResponse response)
        {
            Debug.Log("Actualización de ciudad recibida");
            // Procesar actualización de ciudad
            cityManager?.HandleCityUpdate(response.GetValue<string>());
        }
        
        void OnManufacturingUpdate(SocketIOResponse response)
        {
            Debug.Log("Actualización de manufacturing recibida");
            // Procesar actualización de manufacturing
        }
        
        void OnResearchUpdate(SocketIOResponse response)
        {
            Debug.Log("Actualización de investigación recibida");
            // Procesar actualización de investigación
        }
        
        void OnDestroy()
        {
            if (socket != null)
            {
                socket.Disconnect();
            }
        }
    }
}
