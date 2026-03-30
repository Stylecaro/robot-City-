"""
base_chain.py — Abstract base classes for multi-chain blockchain adapters.

Defines the chain taxonomy (ChainType), per-network configuration
(NetworkConfig), a common transaction record (TransactionRecord), and
the abstract ChainAdapter contract that every chain implementation must
fulfil.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional


class ChainType(Enum):
    """Supported blockchain networks."""

    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    BSC = "bsc"
    ARBITRUM = "arbitrum"
    OPTIMISM = "optimism"
    BASE = "base"
    AVALANCHE = "avalanche"
    SOLANA = "solana"
    BITCOIN = "bitcoin"
    LIGHTNING = "lightning"
    TRON = "tron"


@dataclass
class NetworkConfig:
    """
    Static configuration for a specific chain / network.

    ``rpc_url`` and ``explorer_url`` are intentionally left as empty
    strings by default — callers must supply their own endpoints.
    """

    chain_type: ChainType
    network_name: str
    native_token: str
    rpc_url: str = ""
    explorer_url: str = ""
    chain_id: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chain_type": self.chain_type.value,
            "network_name": self.network_name,
            "native_token": self.native_token,
            "rpc_url": self.rpc_url or "<configure your own RPC URL>",
            "explorer_url": self.explorer_url,
            "chain_id": self.chain_id,
        }


@dataclass
class TransactionRecord:
    """An immutable record of a submitted or retrieved transaction."""

    tx_hash: str
    chain_type: ChainType
    from_address: str
    to_address: str
    amount: float
    token_symbol: str
    status: str  # e.g. "pending", "confirmed", "failed"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    block_number: Optional[int] = None
    fee: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tx_hash": self.tx_hash,
            "chain_type": self.chain_type.value,
            "from_address": self.from_address,
            "to_address": self.to_address,
            "amount": self.amount,
            "token_symbol": self.token_symbol,
            "status": self.status,
            "timestamp": self.timestamp.isoformat(),
            "block_number": self.block_number,
            "fee": self.fee,
        }


class ChainAdapter(ABC):
    """
    Abstract adapter that every chain implementation must implement.

    Concrete subclasses are expected to raise ``NotImplementedError``
    (or a clear ``RuntimeError`` with setup instructions) for methods
    that require an external library not yet installed.
    """

    @abstractmethod
    def validate_address(self, address: str) -> bool:
        """Return ``True`` if *address* is a valid address on this chain."""

    @abstractmethod
    def get_balance(self, address: str, token: str = "") -> float:
        """
        Return the balance of *token* at *address*.

        Parameters
        ----------
        address:
            On-chain address.
        token:
            Token symbol or contract address.  Use the native token
            symbol (e.g. ``"ETH"``), or an empty string for the default.
        """

    @abstractmethod
    def send_transaction(
        self,
        from_addr: str,
        to_addr: str,
        amount: float,
        token: str,
        private_key: str,
    ) -> TransactionRecord:
        """
        Broadcast a transaction.

        .. warning::
            ``private_key`` is passed here solely as a conceptual
            interface.  Production code must use a hardware wallet or
            secure enclave — never log or persist private keys.
        """

    @abstractmethod
    def get_transaction(self, tx_hash: str) -> TransactionRecord:
        """Retrieve a previously submitted transaction by its hash."""

    @abstractmethod
    def get_network_config(self) -> NetworkConfig:
        """Return the static network configuration for this adapter."""
