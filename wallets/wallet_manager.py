"""
wallet_manager.py — Safe multi-chain wallet record manager.

.. important::
    **Private keys are NEVER stored by WalletManager.**

    This module manages only wallet *identifiers* (wallet_id),
    *chain type* labels, and *public addresses*.  Any signing or
    key-derivation operations must be performed externally by a
    hardware wallet, secure enclave, or dedicated key-management
    service before passing signed transactions to the chain adapters.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .wallet_metadata import WalletMetadata
from .wallet_validator import WalletValidator


class WalletManager:
    """
    In-memory manager for public wallet records.

    Only the wallet identifier, chain type, and public address are
    stored.  Private keys are deliberately outside the scope of this
    class.

    For production use, replace the internal ``_wallets`` dict with a
    database-backed repository that enforces access controls.
    """

    def __init__(self) -> None:
        # wallet_id -> { wallet_id, chain_type, address, added_at, metadata }
        self._wallets: Dict[str, Dict[str, Any]] = {}

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def add_wallet(
        self,
        wallet_id: str,
        chain_type: str,
        address: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Register a wallet address.

        Parameters
        ----------
        wallet_id:
            Caller-supplied identifier (e.g. ``"user_42_btc"``).
        chain_type:
            Chain identifier string, e.g. ``"ETH"``, ``"BTC"``, ``"SOL"``.
        address:
            Public address on the given chain.
        metadata:
            Optional extra key/value data (label, tags, etc.).

        Returns
        -------
        dict
            The stored wallet record.

        Raises
        ------
        ValueError
            If *address* fails validation for *chain_type*.
        """
        validation = WalletValidator.validate_address(address, chain_type)
        if not validation["valid"]:
            raise ValueError(
                f"Invalid {chain_type} address '{address}': {validation['notes']}"
            )

        record: Dict[str, Any] = {
            "wallet_id": wallet_id,
            "chain_type": chain_type.upper().strip(),
            "address": address,
            "added_at": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
        }
        self._wallets[wallet_id] = record
        return record

    def get_wallet(self, wallet_id: str) -> Dict[str, Any]:
        """
        Retrieve a wallet record by *wallet_id*.

        Raises
        ------
        KeyError
            If the wallet is not registered.
        """
        if wallet_id not in self._wallets:
            raise KeyError(f"Wallet '{wallet_id}' not found.")
        return self._wallets[wallet_id]

    def list_wallets(
        self, chain_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Return all stored wallet records.

        Parameters
        ----------
        chain_type:
            If provided, filter by this chain identifier.
        """
        wallets = list(self._wallets.values())
        if chain_type is not None:
            target = chain_type.upper().strip()
            wallets = [w for w in wallets if w["chain_type"] == target]
        return wallets

    def remove_wallet(self, wallet_id: str) -> bool:
        """
        Delete a wallet record.

        Returns ``True`` if removed, ``False`` if not found.
        """
        if wallet_id in self._wallets:
            del self._wallets[wallet_id]
            return True
        return False

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate_wallet(self, wallet_id: str) -> Dict[str, Any]:
        """
        Re-validate the stored address of a registered wallet.

        Returns the validation result dict from ``WalletValidator``.
        """
        record = self.get_wallet(wallet_id)
        result = WalletValidator.validate_address(
            record["address"], record["chain_type"]
        )
        # Enrich with metadata from the chain info table.
        chain_info = WalletMetadata.get_chain_info(record["chain_type"])
        if chain_info:
            result["chain_name"] = chain_info.chain_name
            result["explorer_url"] = WalletMetadata.get_explorer_url(
                record["chain_type"], record["address"]
            )
        return result

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def get_stats(self) -> Dict[str, Any]:
        """
        Return aggregate statistics about stored wallets.

        Returns
        -------
        dict
            ``{"total": int, "by_chain": {chain: count}}``
        """
        by_chain: Dict[str, int] = {}
        for w in self._wallets.values():
            chain = w["chain_type"]
            by_chain[chain] = by_chain.get(chain, 0) + 1

        return {
            "total": len(self._wallets),
            "by_chain": by_chain,
        }
