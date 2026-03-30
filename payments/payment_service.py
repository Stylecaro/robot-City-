"""
payment_service.py — High-level crypto payment orchestration service.

Manages invoice creation, tracking, and fulfilment.  Payment addresses
are placeholders; in production they should be derived from an HD wallet
or returned by a custody/API provider.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .crypto_invoice import CryptoInvoice, InvoiceStatus, SupportedAsset
from .payment_receipt import PaymentReceipt

# Placeholder receiving addresses per asset.
# Replace with real addresses (or an HD-wallet derivation) in production.
_PLACEHOLDER_ADDRESSES: Dict[SupportedAsset, str] = {
    SupportedAsset.BTC: "bc1qplaceholderbtcaddress",
    SupportedAsset.ETH: "0xPlaceholderEthAddress0000000000000000000",
    SupportedAsset.USDT: "0xPlaceholderUsdtAddress000000000000000000",
    SupportedAsset.USDC: "0xPlaceholderUsdcAddress000000000000000000",
    SupportedAsset.SOL: "PlaceholderSolanaAddress111111111111111111",
    SupportedAsset.BNB: "0xPlaceholderBnbAddress0000000000000000000",
    SupportedAsset.MATIC: "0xPlaceholderMaticAddress000000000000000000",
    SupportedAsset.TRX: "TPlaceholderTronAddress00000000000000000",
}

# URN/URI scheme prefixes for QR code generation.
_QR_SCHEME: Dict[SupportedAsset, str] = {
    SupportedAsset.BTC: "bitcoin",
    SupportedAsset.ETH: "ethereum",
    SupportedAsset.SOL: "solana",
    SupportedAsset.TRX: "tron",
    SupportedAsset.USDT: "ethereum",
    SupportedAsset.USDC: "ethereum",
    SupportedAsset.BNB: "ethereum",
    SupportedAsset.MATIC: "ethereum",
}


class CryptoPaymentService:
    """
    Manages the full lifecycle of crypto invoices.

    This service is stateful (in-memory store).  For production use,
    replace ``self._invoices`` with a database-backed repository.
    """

    def __init__(self) -> None:
        self._invoices: Dict[str, CryptoInvoice] = {}
        self._receipts: Dict[str, PaymentReceipt] = {}

    # ------------------------------------------------------------------
    # Invoice management
    # ------------------------------------------------------------------

    def create_invoice(
        self,
        asset: SupportedAsset,
        amount: float,
        description: str = "",
        expires_minutes: int = 60,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> CryptoInvoice:
        """
        Create and store a new payment invoice.

        Parameters
        ----------
        asset:
            Cryptocurrency to be paid.
        amount:
            Expected amount in the asset's native unit.
        description:
            Human-readable purpose of the payment.
        expires_minutes:
            Invoice lifetime in minutes (default 60).
        metadata:
            Optional key/value bag attached to the invoice.
        """
        address = _PLACEHOLDER_ADDRESSES.get(asset, "")
        invoice = CryptoInvoice(
            asset=asset,
            amount=amount,
            payment_address=address,
            description=description,
            expires_minutes=expires_minutes,
            metadata=metadata or {},
        )
        invoice.status = InvoiceStatus.AWAITING_PAYMENT
        self._invoices[invoice.invoice_id] = invoice
        return invoice

    def get_invoice(self, invoice_id: str) -> CryptoInvoice:
        """
        Retrieve an invoice by *invoice_id*.

        Raises
        ------
        KeyError
            If the invoice does not exist.
        """
        if invoice_id not in self._invoices:
            raise KeyError(f"Invoice {invoice_id!r} not found.")
        return self._invoices[invoice_id]

    def get_payment_instructions(self, invoice_id: str) -> Dict[str, Any]:
        """
        Return human-readable + machine-readable payment instructions.

        Includes a URI suitable for QR code generation.
        """
        invoice = self.get_invoice(invoice_id)
        scheme = _QR_SCHEME.get(invoice.asset, invoice.asset.value.lower())
        qr_uri = (
            f"{scheme}:{invoice.payment_address}"
            f"?amount={invoice.amount}"
            f"&label={uuid.uuid4().hex[:8]}"
        )
        return {
            "invoice_id": invoice.invoice_id,
            "asset": invoice.asset.value,
            "amount": invoice.amount,
            "payment_address": invoice.payment_address,
            "qr_code_data": qr_uri,
            "expires_at": invoice.expires_at.isoformat(),
            "network": scheme,
            "notes": (
                "Payment addresses are placeholders.  "
                "Configure real addresses in CryptoPaymentService._PLACEHOLDER_ADDRESSES."
            ),
        }

    def track_invoice(self, invoice_id: str) -> Dict[str, Any]:
        """
        Return the current status and details of an invoice.

        Automatically transitions the status to EXPIRED if the invoice
        deadline has passed.
        """
        invoice = self.get_invoice(invoice_id)
        if invoice.is_expired() and invoice.status not in (
            InvoiceStatus.PAID,
            InvoiceStatus.CANCELLED,
        ):
            invoice.status = InvoiceStatus.EXPIRED

        return {
            "invoice_id": invoice.invoice_id,
            "status": invoice.status.value,
            "asset": invoice.asset.value,
            "amount": invoice.amount,
            "payment_address": invoice.payment_address,
            "created_at": invoice.created_at.isoformat(),
            "expires_at": invoice.expires_at.isoformat(),
            "is_expired": invoice.is_expired(),
        }

    def mark_paid(
        self, invoice_id: str, tx_hash: str, amount_received: float
    ) -> PaymentReceipt:
        """
        Record a payment against *invoice_id* and return a receipt.

        Raises
        ------
        ValueError
            If payment validation fails (e.g. wrong amount, expired).
        """
        invoice = self.get_invoice(invoice_id)
        result = invoice.validate_payment_intent(tx_hash, amount_received)

        if not result.get("valid"):
            raise ValueError(
                f"Payment validation failed: {result.get('notes', 'unknown error')}"
            )

        receipt = PaymentReceipt(
            invoice_id=invoice.invoice_id,
            asset=invoice.asset,
            amount_requested=invoice.amount,
            amount_received=amount_received,
            tx_hash=tx_hash,
            payment_address=invoice.payment_address,
        )
        self._receipts[receipt.receipt_id] = receipt
        return receipt

    # ------------------------------------------------------------------
    # Listing and statistics
    # ------------------------------------------------------------------

    def list_invoices(
        self, status: Optional[InvoiceStatus] = None
    ) -> List[Dict[str, Any]]:
        """
        Return all invoices, optionally filtered by *status*.
        """
        invoices = list(self._invoices.values())
        if status is not None:
            invoices = [i for i in invoices if i.status == status]
        return [i.to_dict() for i in invoices]

    def get_stats(self) -> Dict[str, Any]:
        """
        Return aggregate statistics across all invoices.
        """
        by_status: Dict[str, int] = {s.value: 0 for s in InvoiceStatus}
        by_asset: Dict[str, int] = {a.value: 0 for a in SupportedAsset}

        for inv in self._invoices.values():
            by_status[inv.status.value] += 1
            by_asset[inv.asset.value] += 1

        return {
            "total_invoices": len(self._invoices),
            "total_receipts": len(self._receipts),
            "by_status": by_status,
            "by_asset": by_asset,
        }
