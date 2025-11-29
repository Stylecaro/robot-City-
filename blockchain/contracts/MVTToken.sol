// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

/**
 * @title MVTToken
 * @dev Token ERC20 para recompensas de Battle Arena
 * MetaversoToken (MVT) - Token de utilidad del ecosistema
 */
contract MVTToken is ERC20, Ownable, Pausable {
    
    // Direcciones autorizadas para mintear (servidores del juego)
    mapping(address => bool) public authorizedMinters;
    
    // Límite de minteo diario por jugador
    mapping(address => uint256) public dailyMintedAmount;
    mapping(address => uint256) public lastMintDay;
    
    uint256 public constant DAILY_MINT_LIMIT = 10000 * 10**18; // 10,000 MVT por día
    uint256 public constant MAX_SUPPLY = 1000000000 * 10**18; // 1 billón total
    
    // Eventos
    event MinterAdded(address indexed minter);
    event MinterRemoved(address indexed minter);
    event RewardMinted(address indexed player, uint256 amount, string reason);
    
    constructor() ERC20("MetaversoToken", "MVT") {
        // Mintear suministro inicial al creador
        _mint(msg.sender, 100000000 * 10**18); // 100 millones iniciales
        
        // Autorizar owner como minter
        authorizedMinters[msg.sender] = true;
    }
    
    /**
     * @dev Modificador para verificar que el caller es un minter autorizado
     */
    modifier onlyMinter() {
        require(authorizedMinters[msg.sender], "No autorizado para mintear");
        _;
    }
    
    /**
     * @dev Añadir minter autorizado (servidor del juego)
     */
    function addMinter(address minter) external onlyOwner {
        authorizedMinters[minter] = true;
        emit MinterAdded(minter);
    }
    
    /**
     * @dev Remover minter autorizado
     */
    function removeMinter(address minter) external onlyOwner {
        authorizedMinters[minter] = false;
        emit MinterRemoved(minter);
    }
    
    /**
     * @dev Mintear recompensas para jugador
     * @param player Dirección del jugador
     * @param amount Cantidad de tokens
     * @param reason Razón de la recompensa (victoria, kill, etc)
     */
    function mintReward(
        address player,
        uint256 amount,
        string memory reason
    ) external onlyMinter whenNotPaused {
        require(player != address(0), "Direccion invalida");
        require(amount > 0, "Cantidad debe ser mayor a 0");
        require(totalSupply() + amount <= MAX_SUPPLY, "Excede suministro maximo");
        
        // Verificar límite diario
        uint256 currentDay = block.timestamp / 1 days;
        
        if (lastMintDay[player] < currentDay) {
            // Nuevo día, resetear contador
            dailyMintedAmount[player] = 0;
            lastMintDay[player] = currentDay;
        }
        
        require(
            dailyMintedAmount[player] + amount <= DAILY_MINT_LIMIT,
            "Excede limite diario"
        );
        
        dailyMintedAmount[player] += amount;
        
        _mint(player, amount);
        emit RewardMinted(player, amount, reason);
    }
    
    /**
     * @dev Batch mintear recompensas para múltiples jugadores
     */
    function mintBatchRewards(
        address[] memory players,
        uint256[] memory amounts,
        string[] memory reasons
    ) external onlyMinter whenNotPaused {
        require(
            players.length == amounts.length && amounts.length == reasons.length,
            "Arrays deben tener misma longitud"
        );
        
        for (uint256 i = 0; i < players.length; i++) {
            mintReward(players[i], amounts[i], reasons[i]);
        }
    }
    
    /**
     * @dev Pausar transferencias (emergencia)
     */
    function pause() external onlyOwner {
        _pause();
    }
    
    /**
     * @dev Reanudar transferencias
     */
    function unpause() external onlyOwner {
        _unpause();
    }
    
    /**
     * @dev Override transfer para pausable
     */
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal override whenNotPaused {
        super._beforeTokenTransfer(from, to, amount);
    }
}
