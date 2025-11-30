using UnityEngine;
using Photon.Pun;

namespace BattleArena
{
    /// <summary>
    /// Sistema de armas para batalla VR
    /// </summary>
    public class WeaponController : MonoBehaviourPunCallbacks
    {
        [Header("Weapon Stats")]
        public WeaponType weaponType;
        public float damage = 25f;
        public float fireRate = 600f; // Disparos por minuto
        public int magazineSize = 30;
        public float reloadTime = 2.5f;
        public float range = 100f;
        public float recoil = 1f;
        
        [Header("Ammo")]
        public int currentAmmo;
        public int reserveAmmo = 120;
        
        [Header("Effects")]
        public ParticleSystem muzzleFlash;
        public GameObject impactEffect;
        public AudioClip fireSound;
        public AudioClip reloadSound;
        public AudioClip emptySound;
        
        [Header("NFT Skin")]
        public bool isNFTSkin = false;
        public string nftRarity = "Common";
        public float statBoost = 0f;
        
        private float nextFireTime = 0f;
        private bool isReloading = false;
        private AudioSource audioSource;
        private BattlePlayer owner;
        
        public enum WeaponType
        {
            AssaultRifle,
            Shotgun,
            SniperRifle,
            Pistol,
            EnergyWeapon,
            Melee
        }
        
        void Start()
        {
            currentAmmo = magazineSize;
            audioSource = GetComponent<AudioSource>();
            
            if (audioSource == null)
            {
                audioSource = gameObject.AddComponent<AudioSource>();
            }
            
            owner = GetComponentInParent<BattlePlayer>();
            
            // Aplicar boost de stats si es skin NFT
            if (isNFTSkin)
            {
                ApplyNFTBoost();
            }
        }
        
        void ApplyNFTBoost()
        {
            damage *= (1f + statBoost);
            fireRate *= (1f + statBoost * 0.5f);
            
            Debug.Log($"🎨 Skin NFT {nftRarity} aplicado: +{statBoost * 100}% stats");
        }
        
        public void Fire()
        {
            if (isReloading) return;
            if (Time.time < nextFireTime) return;
            
            if (currentAmmo > 0)
            {
                // Disparar
                PerformShot();
                
                currentAmmo--;
                nextFireTime = Time.time + (60f / fireRate);
                
                // Sincronizar con otros jugadores
                photonView.RPC("RPC_Fire", RpcTarget.All);
            }
            else
            {
                // Sin munición
                PlaySound(emptySound);
            }
        }
        
        [PunRPC]
        void RPC_Fire()
        {
            // Efectos visuales y sonoros
            if (muzzleFlash != null)
            {
                muzzleFlash.Play();
            }
            
            PlaySound(fireSound);
            
            // Aplicar retroceso
            if (photonView.IsMine && owner != null)
            {
                ApplyRecoil();
            }
        }
        
        void PerformShot()
        {
            // Raycast desde la cámara (cabeza VR)
            Ray ray = new Ray(owner.vrHead.position, owner.vrHead.forward);
            RaycastHit hit;
            
            if (Physics.Raycast(ray, out hit, range))
            {
                // Verificar si golpeamos a un jugador
                BattlePlayer targetPlayer = hit.collider.GetComponent<BattlePlayer>();
                
                if (targetPlayer != null && targetPlayer != owner)
                {
                    // Calcular daño (headshot bonus)
                    float finalDamage = damage;
                    
                    if (hit.collider.CompareTag("Head"))
                    {
                        finalDamage *= 2f; // Headshot = 2x daño
                        ShowHitMarker("HEADSHOT");
                    }
                    else
                    {
                        ShowHitMarker("HIT");
                    }
                    
                    // Aplicar daño
                    targetPlayer.photonView.RPC(
                        "TakeDamage",
                        RpcTarget.All,
                        finalDamage,
                        owner.playerName
                    );
                    
                    // Incrementar estadística de daño
                    owner.damageDealt += finalDamage;
                }
                
                // Efecto de impacto
                if (impactEffect != null)
                {
                    GameObject impact = Instantiate(
                        impactEffect,
                        hit.point,
                        Quaternion.LookRotation(hit.normal)
                    );
                    Destroy(impact, 2f);
                }
            }
        }
        
        void ApplyRecoil()
        {
            // Aplicar retroceso a la cámara VR
            if (owner.vrHead != null)
            {
                float recoilX = Random.Range(-recoil, recoil);
                float recoilY = Random.Range(recoil * 0.5f, recoil);
                
                owner.vrHead.Rotate(-recoilY, recoilX, 0f);
            }
        }
        
        void ShowHitMarker(string type)
        {
            // Mostrar marcador de golpe en HUD
            GameObject hitMarker = GameObject.Find("HitMarker");
            if (hitMarker != null)
            {
                TMPro.TextMeshProUGUI text = hitMarker.GetComponent<TMPro.TextMeshProUGUI>();
                if (text != null)
                {
                    text.text = type;
                    text.color = type == "HEADSHOT" ? Color.red : Color.white;
                    text.gameObject.SetActive(true);
                    
                    StartCoroutine(HideHitMarker(hitMarker, 0.5f));
                }
            }
        }
        
        System.Collections.IEnumerator HideHitMarker(GameObject marker, float delay)
        {
            yield return new WaitForSeconds(delay);
            marker.SetActive(false);
        }
        
        public void Reload()
        {
            if (isReloading) return;
            if (currentAmmo == magazineSize) return;
            if (reserveAmmo == 0) return;
            
            StartCoroutine(ReloadCoroutine());
        }
        
        System.Collections.IEnumerator ReloadCoroutine()
        {
            isReloading = true;
            
            PlaySound(reloadSound);
            photonView.RPC("RPC_Reload", RpcTarget.All);
            
            yield return new WaitForSeconds(reloadTime);
            
            // Calcular munición a recargar
            int ammoNeeded = magazineSize - currentAmmo;
            int ammoToReload = Mathf.Min(ammoNeeded, reserveAmmo);
            
            currentAmmo += ammoToReload;
            reserveAmmo -= ammoToReload;
            
            isReloading = false;
        }
        
        [PunRPC]
        void RPC_Reload()
        {
            // Animación de recarga
            Animator anim = GetComponent<Animator>();
            if (anim != null)
            {
                anim.SetTrigger("Reload");
            }
        }
        
        void PlaySound(AudioClip clip)
        {
            if (clip != null && audioSource != null)
            {
                audioSource.PlayOneShot(clip);
            }
        }
        
        public void AddAmmo(int amount)
        {
            reserveAmmo += amount;
        }
    }
    
    /// <summary>
    /// Power-ups que se pueden recoger en el mapa
    /// </summary>
    public class PowerUp : MonoBehaviour
    {
        public PowerUpType powerUpType;
        public float value = 50f;
        public float respawnTime = 60f;
        
        public enum PowerUpType
        {
            Health,
            Armor,
            Ammo,
            Shield,
            SpeedBoost,
            DamageBoost
        }
        
        private bool isActive = true;
        private MeshRenderer meshRenderer;
        private Collider col;
        
        void Start()
        {
            meshRenderer = GetComponent<MeshRenderer>();
            col = GetComponent<Collider>();
        }
        
        public void Collect(BattlePlayer player)
        {
            if (!isActive) return;
            
            switch (powerUpType)
            {
                case PowerUpType.Health:
                    player.Heal(value);
                    break;
                    
                case PowerUpType.Armor:
                    player.AddArmor(value);
                    break;
                    
                case PowerUpType.Ammo:
                    if (player.currentWeapon != null)
                    {
                        player.currentWeapon.AddAmmo((int)value);
                    }
                    break;
                    
                case PowerUpType.Shield:
                    StartCoroutine(ApplyShield(player));
                    break;
                    
                case PowerUpType.SpeedBoost:
                    StartCoroutine(ApplySpeedBoost(player));
                    break;
                    
                case PowerUpType.DamageBoost:
                    StartCoroutine(ApplyDamageBoost(player));
                    break;
            }
            
            // Desactivar power-up
            isActive = false;
            meshRenderer.enabled = false;
            col.enabled = false;
            
            // Respawn después de un tiempo
            if (respawnTime > 0)
            {
                Invoke("Respawn", respawnTime);
            }
        }
        
        System.Collections.IEnumerator ApplyShield(BattlePlayer player)
        {
            player.AddArmor(50f);
            yield return new WaitForSeconds(30f);
        }
        
        System.Collections.IEnumerator ApplySpeedBoost(BattlePlayer player)
        {
            // Implementar boost de velocidad
            yield return new WaitForSeconds(15f);
        }
        
        System.Collections.IEnumerator ApplyDamageBoost(BattlePlayer player)
        {
            if (player.currentWeapon != null)
            {
                float originalDamage = player.currentWeapon.damage;
                player.currentWeapon.damage *= 1.5f;
                
                yield return new WaitForSeconds(20f);
                
                player.currentWeapon.damage = originalDamage;
            }
        }
        
        void Respawn()
        {
            isActive = true;
            meshRenderer.enabled = true;
            col.enabled = true;
        }
    }
}
