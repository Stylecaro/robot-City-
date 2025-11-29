using UnityEngine;
using UnityEngine.AI;
using Photon.Pun;

namespace BattleArena.AI
{
    /// <summary>
    /// Controlador de Bot AI con diferentes comportamientos
    /// </summary>
    public class BattleBot : MonoBehaviourPunCallbacks
    {
        [Header("Bot Info")]
        public BotType botType;
        public string playerName;
        public float skillLevel = 0.5f;
        
        [Header("Combat Stats")]
        public float health = 100f;
        public float maxHealth = 100f;
        public float armor = 0f;
        public int kills = 0;
        public float damageDealt = 0f;
        
        [Header("AI Behavior")]
        public float detectionRange = 50f;
        public float attackRange = 30f;
        public float reactionTime = 0.5f;
        public float aimAccuracy = 0.7f;
        
        [Header("Movement")]
        public float moveSpeed = 5f;
        public float rotationSpeed = 120f;
        
        private NavMeshAgent navAgent;
        private BattlePlayer currentTarget;
        private WeaponController currentWeapon;
        private Vector3 patrolDestination;
        private float nextReactionCheck;
        private BotState currentState = BotState.Patrol;
        
        private enum BotState
        {
            Patrol,
            Hunt,
            Attack,
            Retreat,
            LootSearch
        }
        
        void Start()
        {
            navAgent = GetComponent<NavMeshAgent>();
            if (navAgent != null)
            {
                navAgent.speed = moveSpeed;
            }
            
            // Configurar según tipo de bot
            ConfigureBot();
            
            // Equipar arma inicial
            EquipRandomWeapon();
            
            // Iniciar patrulla
            SetRandomPatrolPoint();
        }
        
        void ConfigureBot()
        {
            switch (botType)
            {
                case BotType.HumanoidBot:
                    maxHealth = 100f;
                    moveSpeed = 5f;
                    detectionRange = 40f;
                    attackRange = 25f;
                    aimAccuracy = 0.6f + (skillLevel * 0.3f);
                    break;
                    
                case BotType.Terminator:
                    maxHealth = 200f;
                    armor = 50f;
                    moveSpeed = 4f;
                    detectionRange = 60f;
                    attackRange = 40f;
                    aimAccuracy = 0.8f + (skillLevel * 0.2f);
                    reactionTime = 0.2f;
                    break;
                    
                case BotType.CombatDrone:
                    maxHealth = 75f;
                    moveSpeed = 8f;
                    detectionRange = 70f;
                    attackRange = 50f;
                    aimAccuracy = 0.9f;
                    reactionTime = 0.1f;
                    // Drones vuelan, no usan NavMesh
                    if (navAgent != null)
                    {
                        navAgent.enabled = false;
                    }
                    break;
            }
            
            health = maxHealth;
        }
        
        void Update()
        {
            if (!photonView.IsMine) return;
            
            switch (currentState)
            {
                case BotState.Patrol:
                    Patrol();
                    break;
                    
                case BotState.Hunt:
                    Hunt();
                    break;
                    
                case BotState.Attack:
                    Attack();
                    break;
                    
                case BotState.Retreat:
                    Retreat();
                    break;
                    
                case BotState.LootSearch:
                    SearchForLoot();
                    break;
            }
            
            // Detectar enemigos
            if (Time.time >= nextReactionCheck)
            {
                DetectEnemies();
                nextReactionCheck = Time.time + reactionTime;
            }
        }
        
        void Patrol()
        {
            if (navAgent == null || !navAgent.enabled) return;
            
            // Moverse al punto de patrulla
            if (!navAgent.pathPending && navAgent.remainingDistance < 1f)
            {
                SetRandomPatrolPoint();
            }
        }
        
        void SetRandomPatrolPoint()
        {
            Vector3 randomPoint = transform.position + Random.insideUnitSphere * 50f;
            NavMeshHit hit;
            if (NavMesh.SamplePosition(randomPoint, out hit, 50f, NavMesh.AllAreas))
            {
                patrolDestination = hit.position;
                if (navAgent != null && navAgent.enabled)
                {
                    navAgent.SetDestination(patrolDestination);
                }
            }
        }
        
        void DetectEnemies()
        {
            Collider[] nearbyColliders = Physics.OverlapSphere(transform.position, detectionRange);
            
            float closestDistance = float.MaxValue;
            BattlePlayer closestEnemy = null;
            
            foreach (Collider col in nearbyColliders)
            {
                BattlePlayer player = col.GetComponent<BattlePlayer>();
                if (player != null && player.isAlive)
                {
                    float distance = Vector3.Distance(transform.position, player.transform.position);
                    if (distance < closestDistance)
                    {
                        closestDistance = distance;
                        closestEnemy = player;
                    }
                }
                
                // También detectar otros bots enemigos
                BattleBot bot = col.GetComponent<BattleBot>();
                if (bot != null && bot != this && bot.health > 0)
                {
                    float distance = Vector3.Distance(transform.position, bot.transform.position);
                    if (distance < closestDistance)
                    {
                        closestDistance = distance;
                        // Convertir bot a target (necesitaría adaptación)
                    }
                }
            }
            
            if (closestEnemy != null)
            {
                currentTarget = closestEnemy;
                
                if (closestDistance <= attackRange)
                {
                    currentState = BotState.Attack;
                }
                else
                {
                    currentState = BotState.Hunt;
                }
            }
            else
            {
                currentTarget = null;
                currentState = BotState.Patrol;
            }
        }
        
        void Hunt()
        {
            if (currentTarget == null || !currentTarget.isAlive)
            {
                currentState = BotState.Patrol;
                return;
            }
            
            // Perseguir al enemigo
            if (navAgent != null && navAgent.enabled)
            {
                navAgent.SetDestination(currentTarget.transform.position);
            }
            
            float distance = Vector3.Distance(transform.position, currentTarget.transform.position);
            
            if (distance <= attackRange)
            {
                currentState = BotState.Attack;
            }
            else if (distance > detectionRange)
            {
                currentState = BotState.Patrol;
            }
        }
        
        void Attack()
        {
            if (currentTarget == null || !currentTarget.isAlive)
            {
                currentState = BotState.Patrol;
                return;
            }
            
            // Detenerse para disparar
            if (navAgent != null && navAgent.enabled)
            {
                navAgent.isStopped = true;
            }
            
            // Apuntar al objetivo
            Vector3 direction = (currentTarget.transform.position - transform.position).normalized;
            Quaternion lookRotation = Quaternion.LookRotation(direction);
            transform.rotation = Quaternion.Slerp(transform.rotation, lookRotation, Time.deltaTime * rotationSpeed);
            
            // Disparar con precisión ajustada
            if (currentWeapon != null)
            {
                // Añadir imprecisión basada en skillLevel
                float spread = (1f - aimAccuracy) * 10f;
                Vector3 targetPos = currentTarget.transform.position;
                targetPos += new Vector3(
                    Random.Range(-spread, spread),
                    Random.Range(-spread, spread),
                    Random.Range(-spread, spread)
                );
                
                // Simular disparo
                if (Random.value < 0.3f) // 30% de probabilidad de disparar cada frame
                {
                    currentWeapon.Fire();
                }
            }
            
            // Verificar si debe retirarse (poca vida)
            if (health < maxHealth * 0.3f)
            {
                currentState = BotState.Retreat;
            }
            
            float distance = Vector3.Distance(transform.position, currentTarget.transform.position);
            if (distance > attackRange)
            {
                if (navAgent != null && navAgent.enabled)
                {
                    navAgent.isStopped = false;
                }
                currentState = BotState.Hunt;
            }
        }
        
        void Retreat()
        {
            // Huir en dirección opuesta al enemigo
            if (currentTarget != null)
            {
                Vector3 fleeDirection = (transform.position - currentTarget.transform.position).normalized;
                Vector3 fleeDestination = transform.position + fleeDirection * 30f;
                
                NavMeshHit hit;
                if (NavMesh.SamplePosition(fleeDestination, out hit, 30f, NavMesh.AllAreas))
                {
                    if (navAgent != null && navAgent.enabled)
                    {
                        navAgent.SetDestination(hit.position);
                    }
                }
            }
            
            // Buscar health packs
            SearchForHealthPack();
            
            // Volver a patrullar si recuperó vida
            if (health > maxHealth * 0.6f)
            {
                currentState = BotState.Patrol;
            }
        }
        
        void SearchForLoot()
        {
            // Buscar loot boxes cercanas
            Collider[] lootBoxes = Physics.OverlapSphere(transform.position, 30f);
            
            foreach (Collider col in lootBoxes)
            {
                if (col.CompareTag("LootBox"))
                {
                    if (navAgent != null && navAgent.enabled)
                    {
                        navAgent.SetDestination(col.transform.position);
                    }
                    return;
                }
            }
            
            currentState = BotState.Patrol;
        }
        
        void SearchForHealthPack()
        {
            // Buscar power-ups de salud
            Collider[] powerUps = Physics.OverlapSphere(transform.position, 40f);
            
            foreach (Collider col in powerUps)
            {
                PowerUp powerUp = col.GetComponent<PowerUp>();
                if (powerUp != null && powerUp.powerUpType == PowerUp.PowerUpType.Health)
                {
                    if (navAgent != null && navAgent.enabled)
                    {
                        navAgent.SetDestination(col.transform.position);
                    }
                    return;
                }
            }
        }
        
        void EquipRandomWeapon()
        {
            // Equipar arma según tipo de bot
            // Implementar según disponibilidad de armas
        }
        
        public void TakeDamage(float damage, string attackerName)
        {
            health -= damage;
            
            if (health <= 0)
            {
                Die(attackerName);
            }
        }
        
        void Die(string killerName)
        {
            Debug.Log($"🤖💀 Bot {playerName} eliminado por {killerName}");
            
            // Drop loot
            DeathDropSystem dropSystem = FindObjectOfType<DeathDropSystem>();
            if (dropSystem != null)
            {
                // Bots también dropean tokens (menos que jugadores)
                float botTokens = Random.Range(10f, 50f);
                // Crear loot box simplificado
            }
            
            // Destruir bot
            if (PhotonNetwork.IsMasterClient)
            {
                PhotonNetwork.Destroy(gameObject);
            }
        }
        
        void OnDrawGizmosSelected()
        {
            // Visualizar rangos
            Gizmos.color = Color.yellow;
            Gizmos.DrawWireSphere(transform.position, detectionRange);
            
            Gizmos.color = Color.red;
            Gizmos.DrawWireSphere(transform.position, attackRange);
        }
    }
}
