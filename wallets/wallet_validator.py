"""
wallet_validator.py — Address validation for multiple blockchain networks.

Uses only the Python standard library.  No external dependencies.
"""

from __future__ import annotations

import re
from typing import Any, Dict

# ── EVM ──────────────────────────────────────────────────────────────
_EVM_RE = re.compile(r"^0x[0-9a-fA-F]{40}$")

# ── Solana ────────────────────────────────────────────────────────────
_SOL_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
_SOL_RE = re.compile(rf"^[{re.escape(_SOL_ALPHABET)}]{{32,44}}$")

# ── Bitcoin ───────────────────────────────────────────────────────────
_BTC_LEGACY_RE = re.compile(r"^1[1-9A-HJ-NP-Za-km-z]{25,34}$")
_BTC_P2SH_RE = re.compile(r"^3[1-9A-HJ-NP-Za-km-z]{25,34}$")
_BTC_BECH32_RE = re.compile(r"^bc1[ac-hj-np-z02-9]{6,87}$", re.IGNORECASE)

# ── Tron ──────────────────────────────────────────────────────────────
_TRON_BASE58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
_TRON_RE = re.compile(rf"^T[{re.escape(_TRON_BASE58)}]{{33}}$")


class WalletValidator:
    """
    Static address validators for major blockchain networks.

    All methods are pure functions (no network calls required).
    """

    @staticmethod
    def validate_evm_address(address: str) -> bool:
        """
        Validate an EVM-compatible address (Ethereum, Polygon, BSC, etc.).

        Accepts ``0x`` followed by exactly 40 hexadecimal characters
        (case-insensitive).  Full EIP-55 checksum is not enforced.
        """
        if not isinstance(address, str):
            return False
        return bool(_EVM_RE.match(address))

    @staticmethod
    def validate_solana_address(address: str) -> bool:
        """
        Validate a Solana address (base58-encoded public key).

        A valid address is 32–44 characters long, using only the
        base58 alphabet.
        """
        if not isinstance(address, str):
            return False
        return bool(_SOL_RE.match(address))

    @staticmethod
    def validate_bitcoin_address(address: str) -> bool:
        """
        Validate a Bitcoin address.

        Accepts:
        - Legacy P2PKH (starts with ``1``)
        - P2SH (starts with ``3``)
        - Native SegWit Bech32 (starts with ``bc1``)
        """
        if not isinstance(address, str):
            return False
        return bool(
            _BTC_LEGACY_RE.match(address)
            or _BTC_P2SH_RE.match(address)
            or _BTC_BECH32_RE.match(address)
        )

    @staticmethod
    def validate_tron_address(address: str) -> bool:
        """
        Validate a Tron address.

        A valid Tron mainnet address is exactly 34 characters long,
        starts with ``T``, and uses the base58 alphabet.
        """
        if not isinstance(address, str):
            return False
        return bool(_TRON_RE.match(address))

    @classmethod
    def validate_address(cls, address: str, chain_type_str: str) -> Dict[str, Any]:
        """
        Validate *address* for a named chain.

        Parameters
        ----------
        address:
            The address string to validate.
        chain_type_str:
            Case-insensitive chain name, e.g.  ``"ETH"``, ``"BTC"``,
            ``"SOL"``, ``"TRX"``, ``"MATIC"``, ``"BNB"``, ``"AVAX"``,
            ``"ARB"``, ``"OP"``, ``"BASE"``.

        Returns
        -------
        dict
            ``{"valid": bool, "chain": str, "address": str, "notes": str}``
        """
        chain = chain_type_str.upper().strip()

        evm_chains = {"ETH", "MATIC", "BNB", "AVAX", "ARB", "OP", "BASE", "USDT", "USDC"}

        if chain in evm_chains:
            valid = cls.validate_evm_address(address)
            notes = "EVM address: 0x + 40 hex chars required." if not valid else "Valid EVM address."
        elif chain == "SOL":
            valid = cls.validate_solana_address(address)
            notes = "Solana address: base58, 32–44 chars required." if not valid else "Valid Solana address."
        elif chain == "BTC":
            valid = cls.validate_bitcoin_address(address)
            notes = "Bitcoin: legacy (1…), P2SH (3…), or bech32 (bc1…) required." if not valid else "Valid Bitcoin address."
        elif chain == "TRX":
            valid = cls.validate_tron_address(address)
            notes = "Tron address: T + 33 base58 chars required." if not valid else "Valid Tron address."
        else:
            valid = False
            notes = f"Unknown chain '{chain_type_str}'.  Supported: ETH, MATIC, BNB, AVAX, ARB, OP, BASE, SOL, BTC, TRX."

        return {
            "valid": valid,
            "chain": chain,
            "address": address,
            "notes": notes,
        }
