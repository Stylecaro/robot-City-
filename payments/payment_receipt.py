"""
payment_receipt.py — Immutable record of a completed crypto payment.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict

from .crypto_invoice import SupportedAsset


@dataclass
class PaymentReceipt:
    """
    Immutable receipt generated when an invoice is successfully paid.

    Attributes
    ----------
    receipt_id:
        Auto-generated UUID for this receipt.
    invoice_id:
        The invoice that was fulfilled.
    asset:
        Cryptocurrency that was paid.
    amount_requested:
        Original invoice amount.
    amount_received:
        Amount actually received (may be >= amount_requested).
    tx_hash:
        On-chain transaction hash confirming the payment.
    payment_address:
        Address that received the funds.
    paid_at:
        UTC timestamp of payment confirmation.
    status:
        Always ``"paid"`` for a valid receipt; kept for extensibility.
    """

    invoice_id: str
    asset: SupportedAsset
    amount_requested: float
    amount_received: float
    tx_hash: str
    payment_address: str
    receipt_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    paid_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "paid"

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serialisable representation of the receipt."""
        return {
            "receipt_id": self.receipt_id,
            "invoice_id": self.invoice_id,
            "asset": self.asset.value,
            "amount_requested": self.amount_requested,
            "amount_received": self.amount_received,
            "tx_hash": self.tx_hash,
            "payment_address": self.payment_address,
            "paid_at": self.paid_at.isoformat(),
            "status": self.status,
        }
