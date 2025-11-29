using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System.Text;

namespace CiudadRobot
{
    public class NetworkManager : MonoBehaviour
    {
        [Header("Configuración API")]
        public string apiBaseUrl = "http://localhost:3000/api";
        
        public void Initialize()
        {
            Debug.Log("NetworkManager inicializado");
        }
        
        // Obtener estado de la ciudad
        public IEnumerator GetCityStatus()
        {
            string url = $"{apiBaseUrl}/city/status";
            
            using (UnityWebRequest request = UnityWebRequest.Get(url))
            {
                yield return request.SendWebRequest();
                
                if (request.result == UnityWebRequest.Result.Success)
                {
                    string jsonResponse = request.downloadHandler.text;
                    Debug.Log($"Estado de la ciudad: {jsonResponse}");
                    // Procesar respuesta
                }
                else
                {
                    Debug.LogError($"Error obteniendo estado de ciudad: {request.error}");
                }
            }
        }
        
        // Obtener robots activos
        public IEnumerator GetActiveRobots()
        {
            string url = $"{apiBaseUrl}/robots/active";
            
            using (UnityWebRequest request = UnityWebRequest.Get(url))
            {
                yield return request.SendWebRequest();
                
                if (request.result == UnityWebRequest.Result.Success)
                {
                    string jsonResponse = request.downloadHandler.text;
                    Debug.Log($"Robots activos: {jsonResponse}");
                    // Procesar respuesta
                }
                else
                {
                    Debug.LogError($"Error obteniendo robots: {request.error}");
                }
            }
        }
        
        // Enviar comando a robot
        public IEnumerator SendRobotCommand(string robotId, string command, string parameters)
        {
            string url = $"{apiBaseUrl}/robots/{robotId}/command";
            
            var commandData = new
            {
                command = command,
                parameters = parameters,
                timestamp = System.DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
            };
            
            string jsonData = JsonUtility.ToJson(commandData);
            byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonData);
            
            using (UnityWebRequest request = new UnityWebRequest(url, "POST"))
            {
                request.uploadHandler = new UploadHandlerRaw(bodyRaw);
                request.downloadHandler = new DownloadHandlerBuffer();
                request.SetRequestHeader("Content-Type", "application/json");
                
                yield return request.SendWebRequest();
                
                if (request.result == UnityWebRequest.Result.Success)
                {
                    Debug.Log($"Comando enviado exitosamente: {request.downloadHandler.text}");
                }
                else
                {
                    Debug.LogError($"Error enviando comando: {request.error}");
                }
            }
        }
    }
}
