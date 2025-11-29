using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace CiudadRobot
{
    public class CityManager : MonoBehaviour
    {
        [Header("Edificios y Estructuras")]
        public GameObject[] buildingPrefabs;
        public GameObject[] factoryPrefabs;
        public GameObject[] labPrefabs;
        
        [Header("Configuración de Ciudad")]
        public Vector3 cityCenter = Vector3.zero;
        public float cityRadius = 1000f;
        public int maxBuildings = 100;
        
        private Dictionary<string, GameObject> instantiatedBuildings;
        
        public void Initialize()
        {
            Debug.Log("CityManager inicializado");
            instantiatedBuildings = new Dictionary<string, GameObject>();
            GenerateInitialCity();
        }
        
        void GenerateInitialCity()
        {
            // Generar ciudad inicial
            CreateCentralHub();
            CreateManufacturingDistrict();
            CreateResearchDistrict();
            CreateSecurityPerimeter();
        }
        
        void CreateCentralHub()
        {
            // Crear hub central de IA
            Vector3 hubPosition = cityCenter;
            GameObject hub = CreateBuilding("central_hub", hubPosition, "AI_Hub");
            
            if (hub != null)
            {
                // Añadir efectos especiales al hub central
                AddSpecialEffects(hub, "ai_core");
            }
        }
        
        void CreateManufacturingDistrict()
        {
            // Crear distrito de manufacturing
            for (int i = 0; i < 5; i++)
            {
                Vector3 position = cityCenter + new Vector3(
                    Random.Range(-200f, 200f),
                    0f,
                    Random.Range(-200f, 200f)
                );
                
                CreateBuilding($"factory_{i}", position, "Robot_Factory");
            }
        }
        
        void CreateResearchDistrict()
        {
            // Crear distrito de investigación
            for (int i = 0; i < 3; i++)
            {
                Vector3 position = cityCenter + new Vector3(
                    Random.Range(-300f, 300f),
                    0f,
                    Random.Range(-300f, 300f)
                );
                
                CreateBuilding($"lab_{i}", position, "Research_Lab");
            }
        }
        
        void CreateSecurityPerimeter()
        {
            // Crear perímetro de seguridad
            int numTowers = 8;
            for (int i = 0; i < numTowers; i++)
            {
                float angle = (360f / numTowers) * i * Mathf.Deg2Rad;
                Vector3 position = cityCenter + new Vector3(
                    Mathf.Cos(angle) * cityRadius * 0.8f,
                    0f,
                    Mathf.Sin(angle) * cityRadius * 0.8f
                );
                
                CreateBuilding($"security_tower_{i}", position, "Security_Tower");
            }
        }
        
        GameObject CreateBuilding(string buildingId, Vector3 position, string buildingType)
        {
            GameObject prefab = GetBuildingPrefab(buildingType);
            if (prefab == null)
            {
                Debug.LogWarning($"Prefab no encontrado para tipo: {buildingType}");
                return null;
            }
            
            GameObject building = Instantiate(prefab, position, Quaternion.identity);
            building.name = $"{buildingType}_{buildingId}";
            
            instantiatedBuildings[buildingId] = building;
            
            Debug.Log($"Edificio creado: {buildingId} en posición {position}");
            return building;
        }
        
        GameObject GetBuildingPrefab(string buildingType)
        {
            // Retornar prefab apropiado basado en el tipo
            // Por ahora retornamos un cubo básico
            GameObject cube = GameObject.CreatePrimitive(PrimitiveType.Cube);
            cube.transform.localScale = new Vector3(10f, 5f, 10f);
            
            // Asignar color basado en tipo
            Renderer renderer = cube.GetComponent<Renderer>();
            switch (buildingType)
            {
                case "AI_Hub":
                    renderer.material.color = Color.cyan;
                    break;
                case "Robot_Factory":
                    renderer.material.color = Color.yellow;
                    break;
                case "Research_Lab":
                    renderer.material.color = Color.green;
                    break;
                case "Security_Tower":
                    renderer.material.color = Color.red;
                    break;
                default:
                    renderer.material.color = Color.gray;
                    break;
            }
            
            return cube;
        }
        
        void AddSpecialEffects(GameObject building, string effectType)
        {
            // Añadir efectos especiales como partículas, luces, etc.
            Light buildingLight = building.AddComponent<Light>();
            buildingLight.color = Color.cyan;
            buildingLight.intensity = 2f;
            buildingLight.range = 50f;
        }
        
        public void HandleCityUpdate(string updateData)
        {
            Debug.Log($"Procesando actualización de ciudad: {updateData}");
            // Procesar actualizaciones en tiempo real
        }
    }
}
