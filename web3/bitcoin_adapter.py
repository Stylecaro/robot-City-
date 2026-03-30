"""
bitcoin_adapter.py — Adapter for Bitcoin (and Lightning Network).

Address validation covers:

- **Legacy** (P2PKH) — starts with ``1``
- **P2SH / SegWit** — starts with ``3``
- **Bech32 / native SegWit** — starts with ``bc1``

Real transaction submission requires a Bitcoin node or third-party API
(e.g. Blockstream Esplora, Bitcoin Core RPC).

A ``LightningAdapter`` subclass is provided as a placeholder for
Lightning Network invoice creation and payment.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Optional

from .base_chain import ChainAdapter, ChainType, NetworkConfig, TransactionRecord

# Regex patterns for the three main Bitcoin address formats.
_LEGACY_RE = re.compile(r"^1[1-9A-HJ-NP-Za-km-z]{25,34}$")
_P2SH_RE = re.compile(r"^3[1-9A-HJ-NP-Za-km-z]{25,34}$")
_BECH32_RE = re.compile(r"^bc1[ac-hj-np-z02-9]{6,87}$", re.IGNORECASE)


class BitcoinAdapter(ChainAdapter):
    """
    Chain adapter for Bitcoin Mainnet.

    Parameters
    ----------
    rpc_url:
        Optional Bitcoin node or Esplora API endpoint.
    """

    def __init__(self, rpc_url: str = "") -> None:
        self._rpc_url = rpc_url

    # ------------------------------------------------------------------
    # ChainAdapter implementation
    # ------------------------------------------------------------------

    def validate_address(self, address: str) -> bool:
        """
        Validate a Bitcoin address.

        Accepts legacy (P2PKH, starts with ``1``), P2SH (starts with
        ``3``), and native-SegWit Bech32 (starts with ``bc1``) formats.
        """
        if not isinstance(address, str):
            return False
        return bool(
            _LEGACY_RE.match(address)
            or _P2SH_RE.match(address)
            or _BECH32_RE.match(address)
        )

    def get_balance(self, address: str, token: str = "") -> float:
        """
        Return the BTC balance at *address*.

        .. note::
            Requires a Bitcoin node (Bitcoin Core RPC) or a REST API
            such as Blockstream Esplora.

        TODO: Implement using ``requests.get`` against an Esplora
        endpoint, e.g. ``GET /address/{address}/utxo``.
        """
        raise RuntimeError(
            "get_balance requires a Bitcoin node or Esplora API endpoint.  "
            "Set rpc_url to your preferred provider."
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
        Broadcast a signed Bitcoin transaction.

        .. note::
            Requires a signing library such as ``bitcoin-utils``
            (``pip install bitcoin-utils``) and an API to broadcast.

        TODO: Build a PSBT / raw transaction, sign with WIF private key,
        and broadcast via ``POST /tx`` to an Esplora endpoint.
        """
        raise RuntimeError(
            "send_transaction requires a Bitcoin signing library and broadcast API.  "
            "Consider: pip install bitcoin-utils"
        )

    def get_transaction(self, tx_hash: str) -> TransactionRecord:
        """
        Fetch transaction details by *tx_hash*.

        TODO: Implement using ``GET /tx/{tx_hash}`` against Esplora.
        """
        raise RuntimeError(
            "get_transaction requires a Bitcoin API endpoint (e.g. Esplora).  "
            "Set rpc_url to your preferred provider."
        )

    def get_network_config(self) -> NetworkConfig:
        """Return the static Bitcoin Mainnet configuration."""
        return NetworkConfig(
            chain_type=ChainType.BITCOIN,
            network_name="Bitcoin Mainnet",
            native_token="BTC",
            rpc_url=self._rpc_url,
            explorer_url="https://blockstream.info",
        )

    def __repr__(self) -> str:
        return f"<BitcoinAdapter rpc={'set' if self._rpc_url else 'unset'}>"


class LightningAdapter(BitcoinAdapter):
    """
    Placeholder adapter for the Bitcoin Lightning Network.

    Inherits Bitcoin address validation from ``BitcoinAdapter``.
    Invoice operations require an LND, CLN, or Eclair node.
    """

    def get_network_config(self) -> NetworkConfig:
        """Return the Lightning Network configuration."""
        return NetworkConfig(
            chain_type=ChainType.LIGHTNING,
            network_name="Bitcoin Lightning Network",
            native_token="BTC",
            rpc_url=self._rpc_url,
            explorer_url="https://amboss.space",
        )

    def create_invoice(
        self, amount_sats: int, memo: str = ""
    ) -> dict:
        """
        Create a BOLT-11 Lightning invoice.

        .. note::
            Requires an LND/CLN node with REST API access.

        TODO: Call ``POST /v1/invoices`` on an LND node.

        Parameters
        ----------
        amount_sats:
            Invoice amount in satoshis.
        memo:
            Optional human-readable description.
        """
        raise RuntimeError(
            "create_invoice requires an LND or CLN node.  "
            "Configure rpc_url with your node's REST endpoint."
        )

    def pay_invoice(self, payment_request: str) -> dict:
        """
        Pay a BOLT-11 *payment_request* string.

        .. note::
            Requires an LND/CLN node with REST API access.

        TODO: Call ``POST /v1/channels/transactions`` on an LND node.
        """
        raise RuntimeError(
            "pay_invoice requires an LND or CLN node.  "
            "Configure rpc_url with your node's REST endpoint."
        )
