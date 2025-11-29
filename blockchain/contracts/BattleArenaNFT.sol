// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

/**
 * @title BattleArenaNFT
 * @dev NFTs coleccionables por victorias y logros en Battle Arena
 */
contract BattleArenaNFT is ERC721, ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;
    
    // Metadata de cada NFT
    struct NFTMetadata {
        string playerName;
        uint256 kills;
        uint256 matchId;
        uint256 timestamp;
        string rarity; // Common, Rare, Epic, Legendary
        string arenaType; // BattleRoyale, TeamDeathmatch, etc
        uint256 placement; // 1st, 2nd, 3rd, etc
        uint256 damageDealt;
        uint256 survivalTime;
    }
    
    // Mapeo de token ID a metadata
    mapping(uint256 => NFTMetadata) public nftMetadata;
    
    // Rarity counts
    mapping(string => uint256) public rarityCount;
    
    // Direcciones autorizadas para mintear
    mapping(address => bool) public authorizedMinters;
    
    // Base URI para metadata
    string private _baseTokenURI;
    
    // Eventos
    event NFTMinted(
        uint256 indexed tokenId,
        address indexed player,
        string rarity,
        uint256 matchId
    );
    
    constructor(string memory baseURI) ERC721("BattleArena NFT", "BNFT") {
        _baseTokenURI = baseURI;
        authorizedMinters[msg.sender] = true;
    }
    
    /**
     * @dev Modificador para minters autorizados
     */
    modifier onlyMinter() {
        require(authorizedMinters[msg.sender], "No autorizado");
        _;
    }
    
    /**
     * @dev Añadir minter autorizado
     */
    function addMinter(address minter) external onlyOwner {
        authorizedMinters[minter] = true;
    }
    
    /**
     * @dev Remover minter
     */
    function removeMinter(address minter) external onlyOwner {
        authorizedMinters[minter] = false;
    }
    
    /**
     * @dev Mintear NFT de victoria
     */
    function mintVictoryNFT(
        address winner,
        string memory playerName,
        uint256 kills,
        uint256 matchId,
        string memory rarity,
        string memory arenaType,
        uint256 placement,
        uint256 damageDealt,
        uint256 survivalTime,
        string memory tokenURI
    ) public onlyMinter returns (uint256) {
        _tokenIds.increment();
        uint256 newNftId = _tokenIds.current();
        
        _mint(winner, newNftId);
        _setTokenURI(newNftId, tokenURI);
        
        nftMetadata[newNftId] = NFTMetadata(
            playerName,
            kills,
            matchId,
            block.timestamp,
            rarity,
            arenaType,
            placement,
            damageDealt,
            survivalTime
        );
        
        rarityCount[rarity]++;
        
        emit NFTMinted(newNftId, winner, rarity, matchId);
        
        return newNftId;
    }
    
    /**
     * @dev Batch mint NFTs
     */
    function batchMintNFTs(
        address[] memory winners,
        string[] memory playerNames,
        uint256[] memory killCounts,
        uint256[] memory matchIds,
        string[] memory rarities,
        string[] memory arenaTypes,
        uint256[] memory placements,
        uint256[] memory damageDealtArr,
        uint256[] memory survivalTimes,
        string[] memory tokenURIs
    ) external onlyMinter {
        require(winners.length == playerNames.length, "Arrays length mismatch");
        
        for (uint256 i = 0; i < winners.length; i++) {
            mintVictoryNFT(
                winners[i],
                playerNames[i],
                killCounts[i],
                matchIds[i],
                rarities[i],
                arenaTypes[i],
                placements[i],
                damageDealtArr[i],
                survivalTimes[i],
                tokenURIs[i]
            );
        }
    }
    
    /**
     * @dev Obtener metadata de NFT
     */
    function getNFTMetadata(uint256 tokenId) 
        external 
        view 
        returns (NFTMetadata memory) 
    {
        require(_exists(tokenId), "NFT no existe");
        return nftMetadata[tokenId];
    }
    
    /**
     * @dev Obtener todos los NFTs de un jugador
     */
    function getPlayerNFTs(address player) 
        external 
        view 
        returns (uint256[] memory) 
    {
        uint256 balance = balanceOf(player);
        uint256[] memory tokenIds = new uint256[](balance);
        uint256 counter = 0;
        
        for (uint256 i = 1; i <= _tokenIds.current(); i++) {
            if (_exists(i) && ownerOf(i) == player) {
                tokenIds[counter] = i;
                counter++;
            }
        }
        
        return tokenIds;
    }
    
    /**
     * @dev Obtener conteo por rareza
     */
    function getRarityStats() 
        external 
        view 
        returns (
            uint256 legendary,
            uint256 epic,
            uint256 rare,
            uint256 common
        ) 
    {
        return (
            rarityCount["Legendary"],
            rarityCount["Epic"],
            rarityCount["Rare"],
            rarityCount["Common"]
        );
    }
    
    /**
     * @dev Set base URI
     */
    function setBaseURI(string memory baseURI) external onlyOwner {
        _baseTokenURI = baseURI;
    }
    
    /**
     * @dev Override base URI
     */
    function _baseURI() internal view override returns (string memory) {
        return _baseTokenURI;
    }
    
    /**
     * @dev Override tokenURI
     */
    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }
    
    /**
     * @dev Override burn
     */
    function _burn(uint256 tokenId) 
        internal 
        override(ERC721, ERC721URIStorage) 
    {
        super._burn(tokenId);
    }
}
