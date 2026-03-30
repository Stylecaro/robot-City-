"""
evm_adapter.py — Adapter for EVM-compatible blockchain networks.

Covers Ethereum, Polygon, BSC, Arbitrum, Optimism, Base, and Avalanche.

Real transaction submission and balance queries require ``web3.py``
(``pip install web3``).  Address validation is fully implemented using
only the standard library.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Optional

from .base_chain import ChainAdapter, ChainType, NetworkConfig, TransactionRecord

# Static network metadata keyed by ChainType.
_EVM_NETWORKS: dict = {
    ChainType.ETHEREUM: {
        "network_name": "Ethereum Mainnet",
        "chain_id": 1,
        "native_token": "ETH",
        "explorer_url": "https://etherscan.io",
    },
    ChainType.POLYGON: {
        "network_name": "Polygon Mainnet",
        "chain_id": 137,
        "native_token": "MATIC",
        "explorer_url": "https://polygonscan.com",
    },
    ChainType.BSC: {
        "network_name": "BNB Smart Chain",
        "chain_id": 56,
        "native_token": "BNB",
        "explorer_url": "https://bscscan.com",
    },
    ChainType.ARBITRUM: {
        "network_name": "Arbitrum One",
        "chain_id": 42161,
        "native_token": "ETH",
        "explorer_url": "https://arbiscan.io",
    },
    ChainType.OPTIMISM: {
        "network_name": "Optimism Mainnet",
        "chain_id": 10,
        "native_token": "ETH",
        "explorer_url": "https://optimistic.etherscan.io",
    },
    ChainType.BASE: {
        "network_name": "Base Mainnet",
        "chain_id": 8453,
        "native_token": "ETH",
        "explorer_url": "https://basescan.org",
    },
    ChainType.AVALANCHE: {
        "network_name": "Avalanche C-Chain",
        "chain_id": 43114,
        "native_token": "AVAX",
        "explorer_url": "https://snowtrace.io",
    },
}


class EVMAdapter(ChainAdapter):
    """
    Chain adapter for EVM-compatible networks.

    Parameters
    ----------
    chain_type:
        One of the EVM ``ChainType`` members.
    rpc_url:
        Optional RPC endpoint.  If omitted the adapter still works for
        address validation, but live queries will raise ``RuntimeError``.
    """

    def __init__(
        self,
        chain_type: ChainType,
        rpc_url: str = "",
    ) -> None:
        if chain_type not in _EVM_NETWORKS:
            raise ValueError(
                f"{chain_type} is not a supported EVM chain.  "
                f"Supported: {list(_EVM_NETWORKS.keys())}"
            )
        self._chain_type = chain_type
        self._rpc_url = rpc_url
        self._meta = _EVM_NETWORKS[chain_type]

    # ------------------------------------------------------------------
    # Factory methods
    # ------------------------------------------------------------------

    @classmethod
    def create_ethereum(cls, rpc_url: str = "") -> "EVMAdapter":
        """Create an adapter for Ethereum Mainnet."""
        return cls(ChainType.ETHEREUM, rpc_url)

    @classmethod
    def create_polygon(cls, rpc_url: str = "") -> "EVMAdapter":
        """Create an adapter for Polygon Mainnet."""
        return cls(ChainType.POLYGON, rpc_url)

    @classmethod
    def create_bsc(cls, rpc_url: str = "") -> "EVMAdapter":
        """Create an adapter for BNB Smart Chain."""
        return cls(ChainType.BSC, rpc_url)

    @classmethod
    def create_arbitrum(cls, rpc_url: str = "") -> "EVMAdapter":
        """Create an adapter for Arbitrum One."""
        return cls(ChainType.ARBITRUM, rpc_url)

    @classmethod
    def create_optimism(cls, rpc_url: str = "") -> "EVMAdapter":
        """Create an adapter for Optimism Mainnet."""
        return cls(ChainType.OPTIMISM, rpc_url)

    @classmethod
    def create_base(cls, rpc_url: str = "") -> "EVMAdapter":
        """Create an adapter for Base Mainnet."""
        return cls(ChainType.BASE, rpc_url)

    @classmethod
    def create_avalanche(cls, rpc_url: str = "") -> "EVMAdapter":
        """Create an adapter for Avalanche C-Chain."""
        return cls(ChainType.AVALANCHE, rpc_url)

    # ------------------------------------------------------------------
    # ChainAdapter implementation
    # ------------------------------------------------------------------

    def validate_address(self, address: str) -> bool:
        """
        Validate an EIP-55 Ethereum-style address.

        A valid EVM address is a 42-character hex string starting with
        ``0x`` (case-insensitive).  Full EIP-55 checksum validation is
        not enforced here to keep stdlib-only; the hex format check is
        sufficient for routing purposes.
        """
        if not isinstance(address, str):
            return False
        return bool(re.fullmatch(r"0x[0-9a-fA-F]{40}", address))

    def get_balance(self, address: str, token: str = "") -> float:
        """
        Return the token balance at *address*.

        .. note::
            Requires ``web3.py`` (``pip install web3``) and a configured
            ``rpc_url``.

        TODO: Implement using ``web3.eth.get_balance`` or
        ``contract.functions.balanceOf(address).call()``.
        """
        raise RuntimeError(
            "get_balance requires web3.py and a configured rpc_url.  "
            "Install with: pip install web3"
        )

    def send_transaction(
        self,
        from_addr: str,
        to_addr: str,
        amount: float,
        token: str,
        private_key: str,
    ) -> TransactionRecord:
        """
        Broadcast a transaction on the EVM chain.

        .. note::
            Requires ``web3.py`` (``pip install web3``) and a configured
            ``rpc_url``.

        TODO: Build and sign using ``web3.eth.account.sign_transaction``
        and broadcast with ``web3.eth.send_raw_transaction``.
        """
        raise RuntimeError(
            "send_transaction requires web3.py and a configured rpc_url.  "
            "Install with: pip install web3"
        )

    def get_transaction(self, tx_hash: str) -> TransactionRecord:
        """
        Fetch transaction details by *tx_hash*.

        .. note::
            Requires ``web3.py`` (``pip install web3``) and a configured
            ``rpc_url``.

        TODO: Implement using ``web3.eth.get_transaction(tx_hash)``.
        """
        raise RuntimeError(
            "get_transaction requires web3.py and a configured rpc_url.  "
            "Install with: pip install web3"
        )

    def get_network_config(self) -> NetworkConfig:
        """Return the static network configuration for this EVM chain."""
        return NetworkConfig(
            chain_type=self._chain_type,
            network_name=self._meta["network_name"],
            native_token=self._meta["native_token"],
            rpc_url=self._rpc_url,
            explorer_url=self._meta["explorer_url"],
            chain_id=self._meta["chain_id"],
        )

    def __repr__(self) -> str:
        return f"<EVMAdapter chain={self._chain_type.value} rpc={'set' if self._rpc_url else 'unset'}>"
