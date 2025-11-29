using UnityEngine;
using System.Collections;
using Web3Unity;

namespace BattleArena
{
    /// <summary>
    /// Sistema de wallet para manejar criptomonedas en el juego
    /// </summary>
    public class CryptoWalletSystem : MonoBehaviour
    {
        [Header("Contract Addresses")]
        public string tokenContractAddress = "0x..."; // EVT Token
        public string nftContractAddress = "0x...";   // Battle NFT
        
        [Header("Network")]
        public string rpcUrl = "https://polygon-rpc.com/";
        public int chainId = 137; // Polygon Mainnet
        
        private string playerWalletAddress;
        
        void Start()
        {
            // Conectar wallet del jugador
            ConnectWallet();
        }
        
        /// <summary>
        /// Conectar wallet del jugador (MetaMask)
        /// </summary>
        public void ConnectWallet()
        {
            #if UNITY_WEBGL
            // En WebGL, usar MetaMask
            playerWalletAddress = Web3GL.Account();
            Debug.Log($"💼 Wallet conectada: {playerWalletAddress}");
            #else
            // En standalone, cargar de PlayerPrefs
            playerWalletAddress = PlayerPrefs.GetString("WalletAddress", "");
            
            if (string.IsNullOrEmpty(playerWalletAddress))
            {
                Debug.LogWarning("⚠️ No hay wallet conectada. Usando modo demo.");
                playerWalletAddress = "0xDEMO" + Random.Range(1000, 9999);
            }
            #endif
        }
        
        /// <summary>
        /// Obtener balance de tokens del jugador
        /// </summary>
        public IEnumerator GetBalance(string walletAddress)
        {
            Debug.Log($"💰 Consultando balance de {walletAddress}");
            
            #if UNITY_WEBGL && !UNITY_EDITOR
            // Llamada real al smart contract
            string method = "balanceOf";
            string abi = "[{\"inputs\":[{\"internalType\":\"address\",\"name\":\"account\",\"type\":\"address\"}],\"name\":\"balanceOf\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"}]";
            string args = $"[\"{walletAddress}\"]";
            
            string response = yield return Web3GL.Call(
                method,
                abi,
                tokenContractAddress,
                args,
                "0", // No enviar ETH
                "" // Sin gas limit
            );
            
            float balance = float.Parse(response) / 1e18f; // Convertir de wei
            yield return balance;
            #else
            // Modo demo/editor
            yield return 1000f; // Balance demo
            #endif
        }
        
        /// <summary>
        /// Deducir tokens del wallet (para pagar entrada)
        /// </summary>
        public IEnumerator DeductTokens(string walletAddress, float amount)
        {
            Debug.Log($"💸 Deduciendo {amount} EVT de {walletAddress}");
            
            #if UNITY_WEBGL && !UNITY_EDITOR
            // Transfer tokens al contrato del juego
            string method = "transfer";
            string abi = "[{\"inputs\":[{\"internalType\":\"address\",\"name\":\"to\",\"type\":\"address\"},{\"internalType\":\"uint256\",\"name\":\"amount\",\"type\":\"uint256\"}],\"name\":\"transfer\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"}]";
            
            string gameWallet = "0xGAME_TREASURY_ADDRESS"; // Wallet del juego
            string amountWei = (amount * 1e18).ToString("F0");
            string args = $"[\"{gameWallet}\",\"{amountWei}\"]";
            
            string response = yield return Web3GL.SendContract(
                method,
                abi,
                tokenContractAddress,
                args,
                "0", // No enviar ETH
                "" // Gas limit automático
            );
            
            yield return !string.IsNullOrEmpty(response);
            #else
            // Modo demo
            yield return true;
            #endif
        }
        
        /// <summary>
        /// Enviar tokens al jugador (premios)
        /// </summary>
        public IEnumerator SendTokens(string walletAddress, float amount)
        {
            Debug.Log($"💰 Enviando {amount} EVT a {walletAddress}");
            
            #if UNITY_WEBGL && !UNITY_EDITOR
            // Esta operación se hace desde el backend (servidor tiene permisos de minter)
            // Aquí solo simulamos para el cliente
            yield return true;
            #else
            // Modo demo
            Debug.Log($"✅ {amount} EVT enviados a {walletAddress}");
            yield return true;
            #endif
        }
        
        /// <summary>
        /// Transferir tokens entre jugadores
        /// </summary>
        public IEnumerator TransferTokens(string from, string to, float amount)
        {
            Debug.Log($"💸 Transfiriendo {amount} EVT de {from} a {to}");
            
            // Esta operación requiere firma del remitente
            // En el juego, usamos el sistema de "carried tokens" en memoria
            // Solo se escribe a blockchain al final de la partida
            
            yield return true;
        }
        
        /// <summary>
        /// Mintear NFT para jugador
        /// </summary>
        public IEnumerator MintNFT(string walletAddress, string metadata)
        {
            Debug.Log($"🎁 Minteando NFT para {walletAddress}");
            
            #if UNITY_WEBGL && !UNITY_EDITOR
            // Llamar al backend que tiene permisos de minter
            string url = "https://api.battlearena.com/mint-nft";
            WWWForm form = new WWWForm();
            form.AddField("wallet", walletAddress);
            form.AddField("metadata", metadata);
            
            UnityWebRequest www = UnityWebRequest.Post(url, form);
            yield return www.SendWebRequest();
            
            if (www.result == UnityWebRequest.Result.Success)
            {
                Debug.Log($"✅ NFT minteado: {www.downloadHandler.text}");
                yield return true;
            }
            else
            {
                Debug.LogError($"❌ Error minteando NFT: {www.error}");
                yield return false;
            }
            #else
            // Modo demo
            Debug.Log($"✅ NFT demo minteado para {walletAddress}");
            yield return true;
            #endif
        }
        
        /// <summary>
        /// Verificar si jugador tiene NFT específico
        /// </summary>
        public IEnumerator HasNFT(string walletAddress, int tokenId)
        {
            Debug.Log($"🔍 Verificando NFT #{tokenId} para {walletAddress}");
            
            #if UNITY_WEBGL && !UNITY_EDITOR
            string method = "ownerOf";
            string abi = "[{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"tokenId\",\"type\":\"uint256\"}],\"name\":\"ownerOf\",\"outputs\":[{\"internalType\":\"address\",\"name\":\"\",\"type\":\"address\"}],\"stateMutability\":\"view\",\"type\":\"function\"}]";
            string args = $"[\"{tokenId}\"]";
            
            string owner = yield return Web3GL.Call(
                method,
                abi,
                nftContractAddress,
                args,
                "0",
                ""
            );
            
            yield return owner.ToLower() == walletAddress.ToLower();
            #else
            yield return false;
            #endif
        }
        
        public string GetPlayerWallet()
        {
            return playerWalletAddress;
        }
    }
}

