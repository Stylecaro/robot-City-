"""
wallets — Wallet Management Layer
Provides address validation, chain-specific wallet metadata,
and safe storage boundaries.
Private key handling is intentionally left as placeholders.
"""
from .wallet_validator import WalletValidator
from .wallet_metadata import WalletMetadata, ChainWalletInfo
from .wallet_manager import WalletManager

__all__ = ["WalletValidator", "WalletMetadata", "ChainWalletInfo", "WalletManager"]
