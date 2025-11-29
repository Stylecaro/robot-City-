using UnityEngine;
using Photon.Pun;

namespace BattleArena
{
    /// <summary>
    /// Representa un jugador en la arena de batalla
    /// </summary>
    public class BattlePlayer : MonoBehaviourPunCallbacks
    {
        [Header("Player Info")]
        public string playerName;
        public string walletAddress;
        public int playerLevel = 1;
        
        [Header("Combat Stats")]
        public float health = 100f;
        public float maxHealth = 100f;
        public float armor = 0f;
        public float maxArmor = 100f;
        public int kills = 0;
        public int deaths = 0;
        public float damageDealt = 0f;
        public float survivalTime = 0f;
        
        [Header("Crypto & Betting")]
        public float entryFeePaid = 0f;      // Entrada pagada para esta partida
        public float carriedTokens = 0f;     // Tokens que porta el jugador (se pierden al morir)
        public bool hasInsurance = false;    // Seguro para proteger tokens
        
        [Header("VR Setup")]
        public Transform vrHead;
        public Transform vrLeftHand;
        public Transform vrRightHand;
        public string vrHeadset = "Meta Quest 3";
        
        [Header("Weapons")]
        public WeaponController currentWeapon;
        public WeaponController[] inventory = new WeaponController[3];
        public int currentWeaponSlot = 0;
        
        public bool isAlive = true;
        private float spawnTime;
        private BattleArenaManager arenaManager;
        
        void Start()
        {
            spawnTime = Time.time;
            arenaManager = FindObjectOfType<BattleArenaManager>();
            
            if (photonView.IsMine)
            {
                // Configurar cámara VR para este jugador
                SetupVRCamera();
                
                // Obtener dirección de wallet del jugador
                walletAddress = PlayerPrefs.GetString("WalletAddress", "");
                playerLevel = PlayerPrefs.GetInt("PlayerLevel", 1);
            }
        }
        
        void Update()
        {
            if (!isAlive) return;
            
            // Actualizar tiempo de supervivencia
            survivalTime = Time.time - spawnTime;
            
            // Solo el dueño del jugador puede controlarlo
            if (photonView.IsMine)
            {
                HandleInput();
            }
        }
        
        void SetupVRCamera()
        {
            // Configurar cámara XR para VR
            GameObject xrRig = GameObject.Find("XR Origin");
            if (xrRig != null)
            {
                transform.SetParent(xrRig.transform);
            }
        }
        
        void HandleInput()
        {
            // Cambiar arma (botones d-pad o teclas numéricas)
            if (Input.GetKeyDown(KeyCode.Alpha1)) SwitchWeapon(0);
            if (Input.GetKeyDown(KeyCode.Alpha2)) SwitchWeapon(1);
            if (Input.GetKeyDown(KeyCode.Alpha3)) SwitchWeapon(2);
            
            // Disparar (gatillo VR o botón izquierdo del mouse)
            if (Input.GetButton("Fire1") && currentWeapon != null)
            {
                currentWeapon.Fire();
            }
            
            // Recargar (botón B/Y en VR o tecla R)
            if (Input.GetKeyDown(KeyCode.R) && currentWeapon != null)
            {
                currentWeapon.Reload();
            }
        }
        
        void SwitchWeapon(int slot)
        {
            if (slot < 0 || slot >= inventory.Length) return;
            
            if (inventory[slot] != null)
            {
                // Desactivar arma actual
                if (currentWeapon != null)
                {
                    currentWeapon.gameObject.SetActive(false);
                }
                
                // Activar nueva arma
                currentWeaponSlot = slot;
                currentWeapon = inventory[slot];
                currentWeapon.gameObject.SetActive(true);
                
                photonView.RPC("RPC_SwitchWeapon", RpcTarget.All, slot);
            }
        }
        
        [PunRPC]
        void RPC_SwitchWeapon(int slot)
        {
            if (!photonView.IsMine)
            {
                // Sincronizar arma visual para otros jugadores
                currentWeaponSlot = slot;
                currentWeapon = inventory[slot];
            }
        }
        
        public void TakeDamage(float damage, string source)
        {
            if (!isAlive) return;
            
            // Aplicar daño a armadura primero
            if (armor > 0)
            {
                float armorDamage = Mathf.Min(damage, armor);
                armor -= armorDamage;
                damage -= armorDamage;
            }
            
            // Aplicar daño restante a salud
            health -= damage;
            
            // Sincronizar con otros jugadores
            photonView.RPC("RPC_TakeDamage", RpcTarget.All, health, armor);
            
            // Verificar muerte
            if (health <= 0 && isAlive)
            {
                Die(source);
            }
        }
        
        [PunRPC]
        void RPC_TakeDamage(float newHealth, float newArmor)
        {
            health = newHealth;
            armor = newArmor;
            
            // Actualizar UI de salud
            UpdateHealthUI();
        }
        
        void UpdateHealthUI()
        {
            // Actualizar barras de salud y armadura
            // (implementar con sistema UI específico)
        }
        
        void Die(string killerSource)
        {
            isAlive = false;
            deaths++;
            
            Debug.Log($"💀 {playerName} fue eliminado por {killerSource}");
            
            // Notificar al arena manager
            BattlePlayer killer = FindPlayerByName(killerSource);
            arenaManager.OnPlayerEliminated(this, killer);
            
            // DEATH DROP: Perder tokens portados
            if (!hasInsurance && carriedTokens > 0)
            {
                DeathDropSystem dropSystem = FindObjectOfType<DeathDropSystem>();
                if (dropSystem != null)
                {
                    dropSystem.HandlePlayerDeath(this, killer);
                }
            }
            
            // Desactivar controles
            GetComponent<CharacterController>().enabled = false;
            
            // Mostrar pantalla de muerte
            if (photonView.IsMine)
            {
                ShowDeathScreen();
            }
            
            // Reproducir animación de muerte
            photonView.RPC("RPC_PlayDeathAnimation", RpcTarget.All);
        }
        
        [PunRPC]
        void RPC_PlayDeathAnimation()
        {
            // Reproducir animación de muerte
            Animator anim = GetComponent<Animator>();
            if (anim != null)
            {
                anim.SetTrigger("Death");
            }
            
            // Activar ragdoll
            ActivateRagdoll();
        }
        
        void ActivateRagdoll()
        {
            // Desactivar animator
            Animator anim = GetComponent<Animator>();
            if (anim != null)
            {
                anim.enabled = false;
            }
            
            // Activar física en todas las partes del cuerpo
            Rigidbody[] rigidbodies = GetComponentsInChildren<Rigidbody>();
            foreach (Rigidbody rb in rigidbodies)
            {
                rb.isKinematic = false;
            }
        }
        
        void ShowDeathScreen()
        {
            GameObject deathScreen = GameObject.Find("DeathScreen");
            if (deathScreen != null)
            {
                deathScreen.SetActive(true);
                
                // Mostrar estadísticas de la partida
                TMPro.TextMeshProUGUI statsText = deathScreen.GetComponentInChildren<TMPro.TextMeshProUGUI>();
                if (statsText != null)
                {
                    statsText.text = $"💀 ELIMINADO\n\n" +
                                   $"Kills: {kills}\n" +
                                   $"Daño infligido: {damageDealt:F0}\n" +
                                   $"Tiempo de supervivencia: {FormatTime(survivalTime)}\n" +
                                   $"Tokens ganados: {CalculateTokenReward():F0} MVT";
                }
            }
        }
        
        float CalculateTokenReward()
        {
            // Recompensa parcial por participación
            float reward = 50f; // Base participation
            reward += kills * 25f;
            reward += damageDealt * 0.05f;
            reward += survivalTime * 0.5f;
            
            return reward;
        }
        
        string FormatTime(float seconds)
        {
            int minutes = Mathf.FloorToInt(seconds / 60f);
            int secs = Mathf.FloorToInt(seconds % 60f);
            return $"{minutes:00}:{secs:00}";
        }
        
        BattlePlayer FindPlayerByName(string name)
        {
            BattlePlayer[] players = FindObjectsOfType<BattlePlayer>();
            foreach (BattlePlayer player in players)
            {
                if (player.playerName == name)
                {
                    return player;
                }
            }
            return null;
        }
        
        public void AddWeapon(WeaponController weapon)
        {
            // Buscar slot vacío
            for (int i = 0; i < inventory.Length; i++)
            {
                if (inventory[i] == null)
                {
                    inventory[i] = weapon;
                    weapon.transform.SetParent(vrRightHand);
                    weapon.transform.localPosition = Vector3.zero;
                    weapon.transform.localRotation = Quaternion.identity;
                    
                    if (currentWeapon == null)
                    {
                        SwitchWeapon(i);
                    }
                    
                    break;
                }
            }
        }
        
        public void Heal(float amount)
        {
            health = Mathf.Min(health + amount, maxHealth);
            photonView.RPC("RPC_TakeDamage", RpcTarget.All, health, armor);
        }
        
        public void AddArmor(float amount)
        {
            armor = Mathf.Min(armor + amount, maxArmor);
            photonView.RPC("RPC_TakeDamage", RpcTarget.All, health, armor);
        }
        
        void OnCollisionEnter(Collision collision)
        {
            // Detectar colisión con power-ups
            if (collision.gameObject.CompareTag("PowerUp"))
            {
                PowerUp powerUp = collision.gameObject.GetComponent<PowerUp>();
                if (powerUp != null)
                {
                    powerUp.Collect(this);
                }
            }
        }
    }
}
