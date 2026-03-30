"""
tron_adapter.py — Adapter for the Tron blockchain.

Address validation is implemented using only the standard library.
Real balance queries and transaction submission require ``tronpy``
(``pip install tronpy``).
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

from .base_chain import ChainAdapter, ChainType, NetworkConfig, TransactionRecord

# Tron addresses: 'T' followed by 33 base58 characters (total 34).
_TRON_BASE58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
_TRON_RE = re.compile(
    rf"^T[{re.escape(_TRON_BASE58)}]{{33}}$"
)


class TronAdapter(ChainAdapter):
    """
    Chain adapter for Tron Mainnet (TRC-10 / TRC-20).

    Parameters
    ----------
    rpc_url:
        Optional Tron full-node or TronGrid API endpoint.
    """

    _DEFAULT_RPC = "https://api.trongrid.io"

    def __init__(self, rpc_url: str = "") -> None:
        self._rpc_url = rpc_url or self._DEFAULT_RPC

    # ------------------------------------------------------------------
    # ChainAdapter implementation
    # ------------------------------------------------------------------

    def validate_address(self, address: str) -> bool:
        """
        Validate a Tron address.

        A valid Tron mainnet address is exactly 34 characters long,
        starts with ``T``, and uses the base58 alphabet.
        """
        if not isinstance(address, str):
            return False
        return bool(_TRON_RE.match(address))

    def get_balance(self, address: str, token: str = "") -> float:
        """
        Return the TRX (or TRC-20 token) balance at *address*.

        .. note::
            Requires ``tronpy`` (``pip install tronpy``) and a working
            RPC endpoint.

        TODO: Implement using ``tronpy.Tron`` client:
        ``tron.get_account_balance(address)`` for TRX, or
        ``contract.functions.balanceOf(address)`` for TRC-20.
        """
        raise RuntimeError(
            "get_balance requires tronpy.  Install with: pip install tronpy"
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
        Broadcast a TRX transfer.

        .. note::
            Requires ``tronpy`` (``pip install tronpy``).

        TODO: Use ``tron.trx.transfer(from_addr, to_addr, amount).build()
        .sign(private_key).broadcast()``.
        """
        raise RuntimeError(
            "send_transaction requires tronpy.  Install with: pip install tronpy"
        )

    def get_transaction(self, tx_hash: str) -> TransactionRecord:
        """
        Fetch transaction details by *tx_hash*.

        .. note::
            Requires ``tronpy`` (``pip install tronpy``).

        TODO: Implement using ``tron.get_transaction(tx_hash)``.
        """
        raise RuntimeError(
            "get_transaction requires tronpy.  Install with: pip install tronpy"
        )

    def get_network_config(self) -> NetworkConfig:
        """Return the static Tron Mainnet configuration."""
        return NetworkConfig(
            chain_type=ChainType.TRON,
            network_name="Tron Mainnet",
            native_token="TRX",
            rpc_url=self._rpc_url,
            explorer_url="https://tronscan.org",
        )

    def __repr__(self) -> str:
        return f"<TronAdapter rpc={self._rpc_url!r}>"
