const hre = require("hardhat");

async function main() {
  console.log("🚀 Desplegando contratos de Battle Arena...\n");

  // Obtener deployer
  const [deployer] = await hre.ethers.getSigners();
  console.log("📍 Desplegando con cuenta:", deployer.address);
  
  const balance = await deployer.provider.getBalance(deployer.address);
  console.log("💰 Balance:", hre.ethers.formatEther(balance), "MATIC\n");

  // 1. Desplegar MVTToken
  console.log("1️⃣ Desplegando MVTToken...");
  const MVTToken = await hre.ethers.getContractFactory("MVTToken");
  const mvtToken = await MVTToken.deploy();
  await mvtToken.waitForDeployment();
  const mvtAddress = await mvtToken.getAddress();
  
  console.log("✅ MVTToken desplegado en:", mvtAddress);
  console.log("   Suministro inicial:", hre.ethers.formatEther(await mvtToken.totalSupply()), "MVT\n");

  // 2. Desplegar BattleArenaNFT
  console.log("2️⃣ Desplegando BattleArenaNFT...");
  const baseURI = "ipfs://QmBattleArenaNFT/"; // Actualizar con IPFS real
  const BattleArenaNFT = await hre.ethers.getContractFactory("BattleArenaNFT");
  const battleNFT = await BattleArenaNFT.deploy(baseURI);
  await battleNFT.waitForDeployment();
  const nftAddress = await battleNFT.getAddress();
  
  console.log("✅ BattleArenaNFT desplegado en:", nftAddress);
  console.log("   Base URI:", baseURI, "\n");

  // 3. Configurar permisos
  console.log("3️⃣ Configurando permisos...");
  
  // Añadir servidor backend como minter autorizado
  const backendAddress = process.env.BACKEND_ADDRESS || deployer.address;
  
  await mvtToken.addMinter(backendAddress);
  console.log("✅ Backend autorizado como minter de tokens");
  
  await battleNFT.addMinter(backendAddress);
  console.log("✅ Backend autorizado como minter de NFTs\n");

  // 4. Guardar direcciones
  console.log("4️⃣ Guardando configuración...\n");
  
  const config = {
    network: hre.network.name,
    chainId: (await hre.ethers.provider.getNetwork()).chainId.toString(),
    contracts: {
      MVTToken: {
        address: mvtAddress,
        deployer: deployer.address,
        deployedAt: new Date().toISOString()
      },
      BattleArenaNFT: {
        address: nftAddress,
        deployer: deployer.address,
        deployedAt: new Date().toISOString(),
        baseURI: baseURI
      }
    },
    authorizedMinters: [backendAddress]
  };

  const fs = require('fs');
  const configPath = './deployment-config.json';
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
  
  console.log("📄 Configuración guardada en:", configPath);
  console.log("\n" + "=".repeat(60));
  console.log("🎉 DESPLIEGUE COMPLETO");
  console.log("=".repeat(60));
  console.log("\n📋 Resumen:");
  console.log("   Red:", hre.network.name);
  console.log("   MVTToken:", mvtAddress);
  console.log("   BattleArenaNFT:", nftAddress);
  console.log("   Backend autorizado:", backendAddress);
  
  console.log("\n🔧 Próximos pasos:");
  console.log("   1. Verificar contratos en PolygonScan:");
  console.log("      npx hardhat verify --network", hre.network.name, mvtAddress);
  console.log("      npx hardhat verify --network", hre.network.name, nftAddress, `"${baseURI}"`);
  console.log("\n   2. Actualizar backend con direcciones de contratos");
  console.log("\n   3. Configurar IPFS para metadata de NFTs");
  console.log("\n   4. Iniciar servidor backend");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Error:", error);
    process.exit(1);
  });
