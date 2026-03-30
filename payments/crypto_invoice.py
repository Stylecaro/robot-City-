"""
crypto_invoice.py — Invoice model for crypto payment flows.

Defines the supported asset list, invoice lifecycle states, and the
CryptoInvoice class that ties them together.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, Optional


class SupportedAsset(Enum):
    """Cryptocurrencies accepted by the payment module."""

    BTC = "BTC"
    ETH = "ETH"
    USDT = "USDT"
    USDC = "USDC"
    SOL = "SOL"
    BNB = "BNB"
    MATIC = "MATIC"
    TRX = "TRX"


class InvoiceStatus(Enum):
    """Lifecycle states of a crypto payment invoice."""

    PENDING = "pending"
    AWAITING_PAYMENT = "awaiting_payment"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class CryptoInvoice:
    """
    A single crypto payment invoice.

    Parameters
    ----------
    asset:
        The cryptocurrency the payer must send.
    amount:
        Exact amount expected (in the asset's native unit).
    payment_address:
        On-chain address to which payment should be sent.
        Leave blank here; the ``CryptoPaymentService`` populates this
        when it creates invoices.
    description:
        Human-readable description for the payment.
    expires_minutes:
        How long (in minutes) before the invoice expires.  Default 60.
    metadata:
        Optional free-form key/value data attached to the invoice.
    """

    def __init__(
        self,
        asset: SupportedAsset,
        amount: float,
        payment_address: str = "",
        description: str = "",
        expires_minutes: int = 60,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        if amount <= 0:
            raise ValueError("Invoice amount must be positive.")

        self.invoice_id: str = str(uuid.uuid4())
        self.asset: SupportedAsset = asset
        self.amount: float = amount
        self.payment_address: str = payment_address
        self.created_at: datetime = datetime.now(timezone.utc)
        self.expires_at: datetime = self.created_at + timedelta(minutes=expires_minutes)
        self.status: InvoiceStatus = InvoiceStatus.PENDING
        self.description: str = description
        self.metadata: Dict[str, Any] = metadata or {}

    # ------------------------------------------------------------------
    # Business logic
    # ------------------------------------------------------------------

    def is_expired(self) -> bool:
        """Return ``True`` if the invoice's expiry time has passed."""
        return datetime.now(timezone.utc) >= self.expires_at

    def validate_payment_intent(
        self, tx_hash: str, amount_received: float
    ) -> Dict[str, Any]:
        """
        Validate an incoming payment against this invoice.

        Parameters
        ----------
        tx_hash:
            The on-chain transaction hash.
        amount_received:
            The amount received in the invoice's asset.

        Returns
        -------
        dict
            ``{"valid": bool, "status": InvoiceStatus, "notes": str}``
        """
        if self.is_expired():
            return {
                "valid": False,
                "status": InvoiceStatus.EXPIRED,
                "notes": "Invoice has expired.",
            }

        if self.status == InvoiceStatus.PAID:
            return {
                "valid": False,
                "status": InvoiceStatus.PAID,
                "notes": "Invoice is already paid.",
            }

        if amount_received >= self.amount:
            self.status = InvoiceStatus.PAID
            return {
                "valid": True,
                "status": InvoiceStatus.PAID,
                "notes": "Payment accepted.",
                "tx_hash": tx_hash,
                "overpayment": round(amount_received - self.amount, 8),
            }

        if amount_received > 0:
            self.status = InvoiceStatus.PARTIALLY_PAID
            return {
                "valid": False,
                "status": InvoiceStatus.PARTIALLY_PAID,
                "notes": f"Partial payment received: {amount_received} / {self.amount} {self.asset.value}",
                "tx_hash": tx_hash,
            }

        return {
            "valid": False,
            "status": self.status,
            "notes": "No amount received.",
        }

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serialisable representation of the invoice."""
        return {
            "invoice_id": self.invoice_id,
            "asset": self.asset.value,
            "amount": self.amount,
            "payment_address": self.payment_address,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "status": self.status.value,
            "description": self.description,
            "metadata": self.metadata,
            "is_expired": self.is_expired(),
        }

    def __repr__(self) -> str:
        return (
            f"<CryptoInvoice id={self.invoice_id!r} "
            f"asset={self.asset.value} amount={self.amount} "
            f"status={self.status.value}>"
        )
