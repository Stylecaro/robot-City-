"""
solana_adapter.py — Adapter for the Solana blockchain.

Address validation is fully implemented using only the standard library.
Real balance queries and transaction submission require ``solana-py``
(``pip install solana``).
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

from .base_chain import ChainAdapter, ChainType, NetworkConfig, TransactionRecord

# Base58 alphabet used by Solana addresses.
_BASE58_ALPHABET: str = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
_BASE58_RE: re.Pattern = re.compile(
    rf"^[{re.escape(_BASE58_ALPHABET)}]{{32,44}}$"
)


class SolanaAdapter(ChainAdapter):
    """
    Chain adapter for Solana Mainnet.

    Parameters
    ----------
    rpc_url:
        Optional RPC endpoint.  Defaults to the public Solana mainnet
        endpoint when left empty; supply your own for production use.
    """

    _DEFAULT_RPC = "https://api.mainnet-beta.solana.com"

    def __init__(self, rpc_url: str = "") -> None:
        self._rpc_url = rpc_url or self._DEFAULT_RPC

    # ------------------------------------------------------------------
    # ChainAdapter implementation
    # ------------------------------------------------------------------

    def validate_address(self, address: str) -> bool:
        """
        Validate a Solana address (base58-encoded public key).

        A valid Solana address is 32–44 characters long and uses only
        the base58 alphabet.
        """
        if not isinstance(address, str):
            return False
        return bool(_BASE58_RE.match(address))

    def get_balance(self, address: str, token: str = "") -> float:
        """
        Return the SOL (or SPL token) balance at *address*.

        .. note::
            Requires ``solana-py`` (``pip install solana``) and a
            working RPC endpoint.

        TODO: Implement using ``solana.rpc.api.Client.get_balance`` or
        ``get_token_account_balance`` for SPL tokens.
        """
        raise RuntimeError(
            "get_balance requires solana-py.  Install with: pip install solana"
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
        Broadcast a SOL transfer transaction.

        .. note::
            Requires ``solana-py`` (``pip install solana``).

        TODO: Build a ``Transaction`` with ``SystemProgram.transfer``,
        sign with ``Keypair.from_secret_key``, and submit via
        ``Client.send_transaction``.
        """
        raise RuntimeError(
            "send_transaction requires solana-py.  Install with: pip install solana"
        )

    def get_transaction(self, tx_hash: str) -> TransactionRecord:
        """
        Fetch transaction details by *tx_hash* (Solana signature).

        .. note::
            Requires ``solana-py`` (``pip install solana``).

        TODO: Implement using ``Client.get_transaction(signature)``.
        """
        raise RuntimeError(
            "get_transaction requires solana-py.  Install with: pip install solana"
        )

    def get_network_config(self) -> NetworkConfig:
        """Return the static Solana Mainnet configuration."""
        return NetworkConfig(
            chain_type=ChainType.SOLANA,
            network_name="Solana Mainnet Beta",
            native_token="SOL",
            rpc_url=self._rpc_url,
            explorer_url="https://solscan.io",
        )

    def __repr__(self) -> str:
        return f"<SolanaAdapter rpc={self._rpc_url!r}>"
