"""
wallet_metadata.py — Static metadata for supported blockchain networks.

Provides human-readable chain information without requiring any
network calls or external libraries.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ChainWalletInfo:
    """
    Static information about a blockchain network's wallet conventions.

    Attributes
    ----------
    chain_name:
        Human-readable network name.
    native_token:
        Symbol of the chain's native currency.
    address_format:
        Short description of the expected address format.
    explorer_url_template:
        URL template where ``{address}`` is replaced with an address.
    notes:
        Any additional context for users or developers.
    """

    chain_name: str
    native_token: str
    address_format: str
    explorer_url_template: str
    notes: str = ""


# Pre-populated chain metadata.
_CHAIN_INFO: Dict[str, ChainWalletInfo] = {
    "ETH": ChainWalletInfo(
        chain_name="Ethereum",
        native_token="ETH",
        address_format="0x + 40 hex characters (EIP-55)",
        explorer_url_template="https://etherscan.io/address/{address}",
        notes="Same address format works for all EVM-compatible chains.",
    ),
    "BTC": ChainWalletInfo(
        chain_name="Bitcoin",
        native_token="BTC",
        address_format="Legacy (1…), P2SH (3…), or Bech32 (bc1…)",
        explorer_url_template="https://blockstream.info/address/{address}",
        notes="Bech32 (bc1…) is recommended for lowest transaction fees.",
    ),
    "SOL": ChainWalletInfo(
        chain_name="Solana",
        native_token="SOL",
        address_format="Base58, 32–44 characters",
        explorer_url_template="https://solscan.io/account/{address}",
    ),
    "TRX": ChainWalletInfo(
        chain_name="Tron",
        native_token="TRX",
        address_format="T + 33 base58 characters (34 chars total)",
        explorer_url_template="https://tronscan.org/#/address/{address}",
    ),
    "BNB": ChainWalletInfo(
        chain_name="BNB Smart Chain",
        native_token="BNB",
        address_format="0x + 40 hex characters (EVM-compatible)",
        explorer_url_template="https://bscscan.com/address/{address}",
        notes="Uses the same address format as Ethereum.",
    ),
    "MATIC": ChainWalletInfo(
        chain_name="Polygon",
        native_token="MATIC",
        address_format="0x + 40 hex characters (EVM-compatible)",
        explorer_url_template="https://polygonscan.com/address/{address}",
    ),
    "AVAX": ChainWalletInfo(
        chain_name="Avalanche C-Chain",
        native_token="AVAX",
        address_format="0x + 40 hex characters (EVM-compatible)",
        explorer_url_template="https://snowtrace.io/address/{address}",
    ),
    "ARB": ChainWalletInfo(
        chain_name="Arbitrum One",
        native_token="ETH",
        address_format="0x + 40 hex characters (EVM-compatible)",
        explorer_url_template="https://arbiscan.io/address/{address}",
    ),
    "OP": ChainWalletInfo(
        chain_name="Optimism",
        native_token="ETH",
        address_format="0x + 40 hex characters (EVM-compatible)",
        explorer_url_template="https://optimistic.etherscan.io/address/{address}",
    ),
    "BASE": ChainWalletInfo(
        chain_name="Base",
        native_token="ETH",
        address_format="0x + 40 hex characters (EVM-compatible)",
        explorer_url_template="https://basescan.org/address/{address}",
    ),
}


class WalletMetadata:
    """
    Provides static chain metadata for display and validation purposes.
    """

    @staticmethod
    def get_chain_info(chain_type_str: str) -> Optional[ChainWalletInfo]:
        """
        Return ``ChainWalletInfo`` for *chain_type_str*.

        Parameters
        ----------
        chain_type_str:
            Case-insensitive chain identifier, e.g. ``"ETH"``, ``"BTC"``.

        Returns
        -------
        ChainWalletInfo or None
            ``None`` if the chain is not in the pre-populated list.
        """
        return _CHAIN_INFO.get(chain_type_str.upper().strip())

    @staticmethod
    def list_supported_chains() -> List[str]:
        """Return a sorted list of supported chain identifiers."""
        return sorted(_CHAIN_INFO.keys())

    @staticmethod
    def get_explorer_url(chain_type_str: str, address: str) -> Optional[str]:
        """
        Build a block-explorer URL for *address* on *chain_type_str*.

        Returns ``None`` if the chain is not recognised.
        """
        info = _CHAIN_INFO.get(chain_type_str.upper().strip())
        if info is None:
            return None
        return info.explorer_url_template.replace("{address}", address)
