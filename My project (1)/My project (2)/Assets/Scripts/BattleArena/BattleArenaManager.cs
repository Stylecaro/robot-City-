using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using Photon.Pun;
using Web3Unity;
using TMPro;

namespace BattleArena;

/// <summary>
/// Sistema principal de Battle Royale para Meta Horizon y Spatial.io
/// Integra combate VR con recompensas en criptomonedas y NFTs
/// </summary>
public class BattleArenaManager : MonoBehaviourPunCallbacks
{
    [Header("Arena Configuration")]
    public ArenaType arenaType = ArenaType.BattleRoyale;
    public int maxPlayers = 100;
    public float mapSize = 5000f;
    public Transform[] spawnPoints;
    
    [Header("Safe Zone")]
    public Transform safeZoneCenter;
    public float safeZoneRadius = 2500f;
    public float safeZoneShrinkRate = 50f;
    public float zoneDamagePerSecond = 10f;
    public int shrinkIntervalSeconds = 60;
    
    [Header("Weapons & Combat")]
    public GameObject[] weaponPrefabs;
    public GameObject[] powerUpPrefabs;
    public float respawnTime = 5f;
    
    [Header("Crypto Rewards")]
    public string tokenContractAddress = "0x...";
    public string nftContractAddress = "0x...";
    public float baseRewardTokens = 1000f;
    public float killBonusTokens = 25f;
    
    [Header("UI")]
    public TextMeshProUGUI playerCountText;
    public TextMeshProUGUI safeZoneTimerText;
    public TextMeshProUGUI rewardDisplayText;
    public GameObject victoryScreen;
    
    private List<BattlePlayer> activePlayers = new List<BattlePlayer>();
    private float currentSafeZoneRadius;
    private bool matchStarted = false;
    private float nextZoneShrink;
    private CryptoRewardSystem rewardSystem;
    private BettingSystem bettingSystem;
    private DeathDropSystem deathDropSystem;
    
    public enum ArenaType
    {
        BattleRoyale,
        TeamDeathmatch,
        CaptureTheFlag,
        Survival
    }
    
    void Start()
    {
        currentSafeZoneRadius = safeZoneRadius;
        nextZoneShrink = Time.time + shrinkIntervalSeconds;
        rewardSystem = new CryptoRewardSystem(tokenContractAddress, nftContractAddress);
        bettingSystem = GetComponent<BettingSystem>();
        deathDropSystem = GetComponent<DeathDropSystem>();
        
        if (bettingSystem == null)
        {
            bettingSystem = gameObject.AddComponent<BettingSystem>();
        }
        if (deathDropSystem == null)
        {
            deathDropSystem = gameObject.AddComponent<DeathDropSystem>();
        }
        
        // Conectar a Photon para multijugador
        if (!PhotonNetwork.IsConnected)
        {
            PhotonNetwork.ConnectUsingSettings();
        }
    }
    
    void Update()
    {
        if (!matchStarted) return;
        
        // Actualizar contador de jugadores
        UpdatePlayerCount();
        
        // Actualizar zona segura
        UpdateSafeZone();
        
        // Aplicar daño a jugadores fuera de zona
        ApplyZoneDamage();
        
        // Verificar condición de victoria
        CheckVictoryCondition();
    }
    
    public override void OnConnectedToMaster()
    {
        Debug.Log("Conectado al servidor maestro");
        PhotonNetwork.JoinRandomRoom();
    }
    
    public override void OnJoinedRoom()
    {
        Debug.Log($"Unido a sala con {PhotonNetwork.CurrentRoom.PlayerCount} jugadores");
        SpawnPlayer();
        
        // Iniciar partida si hay suficientes jugadores
        if (PhotonNetwork.CurrentRoom.PlayerCount >= maxPlayers * 0.75f && !matchStarted)
        {
            photonView.RPC("StartMatch", RpcTarget.All);
        }
    }
    
    void SpawnPlayer()
    {
        // Seleccionar punto de spawn aleatorio
        int spawnIndex = Random.Range(0, spawnPoints.Length);
        Transform spawnPoint = spawnPoints[spawnIndex];
        
        // Instanciar jugador
        GameObject playerObj = PhotonNetwork.Instantiate(
            "BattlePlayer",
            spawnPoint.position,
            spawnPoint.rotation
        );
        
        BattlePlayer player = playerObj.GetComponent<BattlePlayer>();
        player.playerName = PhotonNetwork.NickName;
        player.walletAddress = PlayerPrefs.GetString("WalletAddress", "");
        
        // Cobrar entrada antes de añadir a la partida
        if (bettingSystem != null)
        {
            float entryFee = bettingSystem.GetEntryFee(arenaType);
            StartCoroutine(ChargeEntryAndAddPlayer(player, entryFee));
        }
        else
        {
            activePlayers.Add(player);
        }
    }
    
    [PunRPC]
    void StartMatch()
    {
        matchStarted = true;
        Debug.Log("🎮 ¡PARTIDA INICIADA!");
        
        // Mostrar mensaje de inicio
        ShowNotification("¡Batalla Iniciada! Sobrevive y gana criptomonedas", 5f);
    }
    
    void UpdatePlayerCount()
    {
        int aliveCount = activePlayers.FindAll(p => p.isAlive).Count;
        playerCountText.text = $"Jugadores vivos: {aliveCount}/{activePlayers.Count}";
    }
    
    void UpdateSafeZone()
    {
        if (Time.time >= nextZoneShrink)
        {
            // Reducir zona segura
            currentSafeZoneRadius = Mathf.Max(currentSafeZoneRadius - safeZoneShrinkRate, 50f);
            nextZoneShrink = Time.time + shrinkIntervalSeconds;
            
            // Actualizar visualización
            UpdateSafeZoneVisual();
            
            // Notificar a jugadores
            photonView.RPC("OnSafeZoneShrink", RpcTarget.All, currentSafeZoneRadius);
        }
        
        // Actualizar temporizador
        float timeToShrink = nextZoneShrink - Time.time;
        safeZoneTimerText.text = $"Zona reducirá en: {Mathf.CeilToInt(timeToShrink)}s";
    }
    
    [PunRPC]
    void OnSafeZoneShrink(float newRadius)
    {
        ShowNotification($"⚠️ Zona segura reducida a {newRadius}m", 3f);
    }
    
    void UpdateSafeZoneVisual()
    {
        // Actualizar shader de la zona segura
        GameObject safeZoneVisual = GameObject.FindGameObjectWithTag("SafeZone");
        if (safeZoneVisual != null)
        {
            safeZoneVisual.transform.localScale = Vector3.one * currentSafeZoneRadius * 2f;
        }
    }
    
    void ApplyZoneDamage()
    {
        foreach (BattlePlayer player in activePlayers)
        {
            if (!player.isAlive) continue;
            
            // Calcular distancia del jugador al centro de la zona
            float distance = Vector3.Distance(
                player.transform.position,
                safeZoneCenter.position
            );
            
            // Si está fuera de la zona, aplicar daño
            if (distance > currentSafeZoneRadius)
            {
                player.TakeDamage(zoneDamagePerSecond * Time.deltaTime, "Storm");
            }
        }
    }
    
    void CheckVictoryCondition()
    {
        int aliveCount = activePlayers.FindAll(p => p.isAlive).Count;
        
        if (aliveCount == 1)
        {
            // ¡Tenemos un ganador!
            BattlePlayer winner = activePlayers.Find(p => p.isAlive);
            photonView.RPC("DeclareWinner", RpcTarget.All, winner.photonView.ViewID);
        }
        else if (aliveCount == 0)
        {
            // Empate (muy raro)
            photonView.RPC("DeclareDraw", RpcTarget.All);
        }
    }
    
    [PunRPC]
    void DeclareWinner(int winnerViewID)
    {
        PhotonView winnerView = PhotonView.Find(winnerViewID);
        if (winnerView != null)
        {
            BattlePlayer winner = winnerView.GetComponent<BattlePlayer>();
            
            Debug.Log($"🏆 ¡{winner.playerName} es el GANADOR!");
            
            // Mostrar pantalla de victoria
            ShowVictoryScreen(winner);
            
            // Distribuir recompensas del pool de apuestas
            if (PhotonNetwork.IsMasterClient)
            {
                StartCoroutine(DistributeRewards(winner));
                
                // Distribuir premios del betting pool
                if (bettingSystem != null)
                {
                    BattlePlayer[] topPlayers = GetTopPlayers(8);
                    StartCoroutine(bettingSystem.DistributePrizes(topPlayers));
                }
            }
        }
    }
    
    [PunRPC]
    void DeclareDraw()
    {
        Debug.Log("Partida terminada en empate");
        ShowNotification("¡Empate! Todos fueron eliminados", 5f);
    }
    
    void ShowVictoryScreen(BattlePlayer winner)
    {
        victoryScreen.SetActive(true);
        
        TextMeshProUGUI winnerText = victoryScreen.GetComponentInChildren<TextMeshProUGUI>();
        winnerText.text = $"🏆 GANADOR: {winner.playerName}\n" +
                        $"💀 Kills: {winner.kills}\n" +
                        $"💰 Recompensa: {CalculateReward(winner)} EVT";
    }
    
    float CalculateReward(BattlePlayer player)
    {
        // Recompensa base + bonus por kills + bonus por daño
        float reward = baseRewardTokens;
        reward += player.kills * killBonusTokens;
        reward += player.damageDealt * 0.1f;
        
        // Multiplicador por tamaño de partida
        float sizeMultiplier = Mathf.Min(activePlayers.Count / 50f, 2f);
        reward *= sizeMultiplier;
        
        return reward;
    }
    
    IEnumerator DistributeRewards(BattlePlayer winner)
    {
        float rewardAmount = CalculateReward(winner);
        
        // Enviar tokens ERC20
        yield return StartCoroutine(
            rewardSystem.SendTokenReward(winner.walletAddress, rewardAmount)
        );
        
        // Generar NFT con probabilidad basada en rendimiento
        float nftChance = 0.10f + (winner.kills * 0.05f); // 10% base + 5% por kill
        
        if (Random.value < nftChance)
        {
            yield return StartCoroutine(
                rewardSystem.MintNFT(winner.walletAddress, "Victory NFT", "Legendary")
            );
        }
        
        // Actualizar UI
        ShowRewardNotification(winner.playerName, rewardAmount);
    }
    
    void ShowRewardNotification(string playerName, float amount)
    {
        rewardDisplayText.text = $"💰 {playerName} ganó {amount} EVT tokens!";
        rewardDisplayText.gameObject.SetActive(true);
        StartCoroutine(HideRewardAfterDelay(5f));
    }
    
    IEnumerator HideRewardAfterDelay(float delay)
    {
        yield return new WaitForSeconds(delay);
        rewardDisplayText.gameObject.SetActive(false);
    }
    
    void ShowNotification(string message, float duration)
    {
        // Implementar sistema de notificaciones
        Debug.Log($"📢 {message}");
    }
    
    IEnumerator ChargeEntryAndAddPlayer(BattlePlayer player, float entryFee)
    {
        bool paymentSuccess = yield return StartCoroutine(
            bettingSystem.ChargeEntryFee(player, entryFee)
        );
        
        if (paymentSuccess)
        {
            activePlayers.Add(player);
            Debug.Log($"✅ {player.playerName} unido a la partida (entrada: {entryFee} EVT)");
        }
        else
        {
            Debug.LogWarning($"❌ {player.playerName} no pudo unirse (fondos insuficientes)");
            PhotonNetwork.Destroy(player.gameObject);
        }
    }
    
    BattlePlayer[] GetTopPlayers(int count)
    {
        // Ordenar jugadores por kills, luego por damage
        List<BattlePlayer> sortedPlayers = new List<BattlePlayer>(activePlayers);
        sortedPlayers.Sort((a, b) =>
        {
            if (a.kills != b.kills)
                return b.kills.CompareTo(a.kills);
            return b.damageDealt.CompareTo(a.damageDealt);
        });
        
        int topCount = Mathf.Min(count, sortedPlayers.Count);
        BattlePlayer[] topPlayers = new BattlePlayer[topCount];
        
        for (int i = 0; i < topCount; i++)
        {
            topPlayers[i] = sortedPlayers[i];
        }
        
        return topPlayers;
    }
    
    public void OnPlayerEliminated(BattlePlayer player, BattlePlayer killer)
    {
        player.isAlive = false;
        
        // Otorgar kill al eliminador
        if (killer != null)
        {
            killer.kills++;
            
            // Pequeña recompensa por kill
            if (PhotonNetwork.IsMasterClient)
            {
                StartCoroutine(
                    rewardSystem.SendTokenReward(killer.walletAddress, killBonusTokens)
                );
            }
        }
        
        // Notificar eliminación
        photonView.RPC(
            "BroadcastElimination",
            RpcTarget.All,
            player.playerName,
            killer != null ? killer.playerName : "Storm"
        );
    }
    
    [PunRPC]
    void BroadcastElimination(string victimName, string killerName)
    {
        ShowNotification($"💀 {victimName} eliminado por {killerName}", 3f);
    }
}

/// <summary>
/// Sistema de recompensas en criptomonedas
/// </summary>
public class CryptoRewardSystem
{
    private string tokenContract;
    private string nftContract;
    
    public CryptoRewardSystem(string tokenAddr, string nftAddr)
    {
        tokenContract = tokenAddr;
        nftContract = nftAddr;
    }
    
    public IEnumerator SendTokenReward(string walletAddress, float amount)
    {
        Debug.Log($"💰 Enviando {amount} tokens a {walletAddress}");
        
        // Aquí iría la integración real con Web3Unity
        // Por ahora simulamos la transacción
        yield return new WaitForSeconds(2f);
        
        string txHash = $"0x{Random.Range(1000000, 9999999)}";
        Debug.Log($"✅ Transacción completada: {txHash}");
    }
    
    public IEnumerator MintNFT(string walletAddress, string nftName, string rarity)
    {
        Debug.Log($"🎁 Minteando NFT '{nftName}' ({rarity}) para {walletAddress}");
        
        yield return new WaitForSeconds(3f);
        
        string txHash = $"0x{Random.Range(1000000, 9999999)}";
        Debug.Log($"✅ NFT minteado: {txHash}");
    }
}

