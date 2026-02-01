using UnityEngine;
using Photon.Pun;

namespace BattleArena.Vehicles;

/// <summary>
/// Controlador de vehículo pilotable
/// </summary>
public class VehicleController : MonoBehaviourPunCallbacks
{
    [Header("Vehicle Info")]
    public VehicleType vehicleType;
    public string vehicleName;
    
    [Header("Vehicle Stats")]
    public float maxHealth = 500f;
    public float currentHealth;
    public float maxSpeed = 20f;
    public float acceleration = 10f;
    public float turnSpeed = 50f;
    
    [Header("Combat")]
    public GameObject[] weaponMounts;
    public float weaponDamage = 50f;
    public float fireRate = 2f;
    public int maxAmmo = 100;
    public int currentAmmo;
    
    [Header("Capacity")]
    public int maxPassengers = 4;
    public Transform[] passengerSeats;
    
    private BattlePlayer driver;
    private List<BattlePlayer> passengers = new List<BattlePlayer>();
    private Rigidbody rb;
    private float nextFireTime;
    private bool isDestroyed = false;
    
    void Start()
    {
        rb = GetComponent<Rigidbody>();
        currentHealth = maxHealth;
        currentAmmo = maxAmmo;
        
        ConfigureVehicle();
    }
    
    void ConfigureVehicle()
    {
        switch (vehicleType)
        {
            case VehicleType.CombatTank:
                vehicleName = "Tanque de Combate";
                maxHealth = 1000f;
                maxSpeed = 15f;
                weaponDamage = 100f;
                fireRate = 1f;
                maxPassengers = 2;
                break;
                
            case VehicleType.ArmoredCar:
                vehicleName = "Auto Blindado";
                maxHealth = 300f;
                maxSpeed = 40f;
                weaponDamage = 30f;
                fireRate = 5f;
                maxPassengers = 4;
                break;
                
            case VehicleType.AttackDrone:
                vehicleName = "Dron de Ataque";
                maxHealth = 200f;
                maxSpeed = 50f;
                weaponDamage = 25f;
                fireRate = 10f;
                maxPassengers = 1;
                break;
                
            case VehicleType.DestroyerMech:
                vehicleName = "Mech Destructor";
                maxHealth = 1500f;
                maxSpeed = 10f;
                weaponDamage = 150f;
                fireRate = 0.5f;
                maxPassengers = 1;
                break;
                
            case VehicleType.Excavator:
                vehicleName = "Excavadora Armada";
                maxHealth = 800f;
                maxSpeed = 8f;
                weaponDamage = 200f; // Daño cuerpo a cuerpo
                fireRate = 2f;
                maxPassengers = 1;
                break;
        }
        
        currentHealth = maxHealth;
    }
    
    void Update()
    {
        if (isDestroyed) return;
        
        if (driver != null && photonView.IsMine)
        {
            HandleInput();
        }
    }
    
    void HandleInput()
    {
        // Movimiento
        float moveInput = Input.GetAxis("Vertical");
        float turnInput = Input.GetAxis("Horizontal");
        
        // Acelerar/retroceder
        Vector3 movement = transform.forward * moveInput * acceleration * Time.deltaTime;
        rb.AddForce(movement, ForceMode.VelocityChange);
        
        // Limitar velocidad
        if (rb.velocity.magnitude > maxSpeed)
        {
            rb.velocity = rb.velocity.normalized * maxSpeed;
        }
        
        // Girar
        transform.Rotate(0, turnInput * turnSpeed * Time.deltaTime, 0);
        
        // Disparar
        if (Input.GetButton("Fire1") && Time.time >= nextFireTime && currentAmmo > 0)
        {
            Fire();
            nextFireTime = Time.time + (1f / fireRate);
        }
        
        // Salir del vehículo
        if (Input.GetKeyDown(KeyCode.F))
        {
            ExitVehicle();
        }
    }
    
    public void EnterVehicle(BattlePlayer player)
    {
        if (driver == null)
        {
            driver = player;
            player.transform.SetParent(transform);
            player.transform.localPosition = Vector3.zero;
            player.GetComponent<CharacterController>().enabled = false;
            
            photonView.RPC("RPC_EnterVehicle", RpcTarget.All, player.photonView.ViewID);
            
            Debug.Log($"🚗 {player.playerName} subió al {vehicleName}");
        }
        else if (passengers.Count < maxPassengers)
        {
            passengers.Add(player);
            player.transform.SetParent(passengerSeats[passengers.Count - 1]);
            player.transform.localPosition = Vector3.zero;
            player.GetComponent<CharacterController>().enabled = false;
        }
    }
    
    [PunRPC]
    void RPC_EnterVehicle(int playerViewID)
    {
        PhotonView playerView = PhotonView.Find(playerViewID);
        if (playerView != null)
        {
            BattlePlayer player = playerView.GetComponent<BattlePlayer>();
            // Sincronizar visualmente
        }
    }
    
    public void ExitVehicle()
    {
        if (driver != null)
        {
            driver.transform.SetParent(null);
            driver.transform.position = transform.position + transform.right * 3f;
            driver.GetComponent<CharacterController>().enabled = true;
            
            photonView.RPC("RPC_ExitVehicle", RpcTarget.All, driver.photonView.ViewID);
            
            driver = null;
        }
    }
    
    [PunRPC]
    void RPC_ExitVehicle(int playerViewID)
    {
        // Sincronizar salida
    }
    
    void Fire()
    {
        if (weaponMounts.Length == 0) return;
        
        foreach (GameObject mount in weaponMounts)
        {
            // Raycast desde el arma
            Ray ray = new Ray(mount.transform.position, mount.transform.forward);
            RaycastHit hit;
            
            if (Physics.Raycast(ray, out hit, 100f))
            {
                // Aplicar daño
                BattlePlayer player = hit.collider.GetComponent<BattlePlayer>();
                if (player != null)
                {
                    player.TakeDamage(weaponDamage, vehicleName);
                }
                
                VehicleController vehicle = hit.collider.GetComponent<VehicleController>();
                if (vehicle != null)
                {
                    vehicle.TakeDamage(weaponDamage);
                }
                
                // Efecto de impacto
                CreateImpactEffect(hit.point, hit.normal);
            }
        }
        
        currentAmmo--;
        
        photonView.RPC("RPC_Fire", RpcTarget.All);
    }
    
    [PunRPC]
    void RPC_Fire()
    {
        // Efectos visuales y sonoros
    }
    
    public void TakeDamage(float damage)
    {
        currentHealth -= damage;
        
        photonView.RPC("RPC_UpdateHealth", RpcTarget.All, currentHealth);
        
        if (currentHealth <= 0)
        {
            Destroy();
        }
    }
    
    [PunRPC]
    void RPC_UpdateHealth(float newHealth)
    {
        currentHealth = newHealth;
        // Actualizar UI de salud del vehículo
    }
    
    void Destroy()
    {
        isDestroyed = true;
        
        Debug.Log($"💥 {vehicleName} destruido!");
        
        // Expulsar pasajeros
        if (driver != null)
        {
            ExitVehicle();
        }
        
        foreach (BattlePlayer passenger in passengers)
        {
            passenger.transform.SetParent(null);
            passenger.GetComponent<CharacterController>().enabled = true;
        }
        
        // Explosión
        CreateExplosion();
        
        // Destruir después de animación
        Invoke("DestroyVehicle", 2f);
    }
    
    void CreateExplosion()
    {
        // Crear efecto de explosión
        // Dañar jugadores cercanos
        Collider[] nearbyObjects = Physics.OverlapSphere(transform.position, 10f);
        
        foreach (Collider col in nearbyObjects)
        {
            BattlePlayer player = col.GetComponent<BattlePlayer>();
            if (player != null)
            {
                float distance = Vector3.Distance(transform.position, player.transform.position);
                float damage = Mathf.Lerp(100f, 0f, distance / 10f);
                player.TakeDamage(damage, "Explosión de " + vehicleName);
            }
        }
    }
    
    void CreateImpactEffect(Vector3 position, Vector3 normal)
    {
        // Crear efecto de impacto
    }
    
    void DestroyVehicle()
    {
        if (PhotonNetwork.IsMasterClient)
        {
            PhotonNetwork.Destroy(gameObject);
        }
    }
    
    void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player"))
        {
            BattlePlayer player = other.GetComponent<BattlePlayer>();
            if (player != null && Input.GetKey(KeyCode.F))
            {
                EnterVehicle(player);
            }
        }
    }
}
