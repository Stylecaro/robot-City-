# Payments — Crypto Payment Module

Manages the full crypto invoice/payment workflow for Robot City:  
create → instruct → track → confirm → receipt.

---

## Supported Assets

| Symbol | Network |
|---|---|
| BTC | Bitcoin |
| ETH | Ethereum |
| USDT | Ethereum (ERC-20) |
| USDC | Ethereum (ERC-20) |
| SOL | Solana |
| BNB | BNB Smart Chain |
| MATIC | Polygon |
| TRX | Tron |

---

## Quick Start

```python
from payments import CryptoPaymentService, SupportedAsset, InvoiceStatus

svc = CryptoPaymentService()

# 1. Create an invoice
invoice = svc.create_invoice(
    asset=SupportedAsset.ETH,
    amount=0.05,
    description="Robot rental fee",
    expires_minutes=30,
)
print(invoice.invoice_id)

# 2. Get payment instructions (includes QR URI)
instructions = svc.get_payment_instructions(invoice.invoice_id)
print(instructions["qr_code_data"])

# 3. Track status
status = svc.track_invoice(invoice.invoice_id)
print(status["status"])  # "awaiting_payment"

# 4. Confirm payment (called by your webhook / blockchain listener)
receipt = svc.mark_paid(
    invoice_id=invoice.invoice_id,
    tx_hash="0xabc123...",
    amount_received=0.05,
)
print(receipt.to_dict())

# 5. Statistics
print(svc.get_stats())
```

---

## Invoice Lifecycle

```
PENDING ──create──► AWAITING_PAYMENT
                         │
              partial pay▼
                  PARTIALLY_PAID
                         │
               full pay  ▼
                       PAID
                         │
              (or timeout▼)
                      EXPIRED
                         │
              (or manual ▼)
                    CANCELLED
```

---

## Production Notes

1. **Payment addresses** — Replace the placeholder addresses in  
   `payment_service.py` with real addresses derived from your HD wallet  
   or custody provider API.

2. **Invoice storage** — The default in-memory store is not persistent.  
   Swap `self._invoices` dict for a database-backed repository.

3. **Webhook listener** — Call `svc.mark_paid(invoice_id, tx_hash, amount)`  
   from your blockchain event listener or exchange webhook.

4. **Over/underpayments** — `CryptoInvoice.validate_payment_intent` handles  
   both cases; overpayments are noted in the receipt.

---

## Module Structure

```
payments/
├── __init__.py          # Public API
├── crypto_invoice.py    # SupportedAsset, InvoiceStatus, CryptoInvoice
├── payment_service.py   # CryptoPaymentService
└── payment_receipt.py   # PaymentReceipt
```
