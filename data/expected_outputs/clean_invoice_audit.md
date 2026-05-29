# Invoice Triage Audit Report: INV-2026-1001

- Supplier: Northwind Office Supplies (SUP-1001)
- Purchase order: PO-9001
- Risk level: LOW
- Decision: AUTO_APPROVE
- Recommended action: Approve the invoice for posting and schedule payment under standard AP controls.

## Reasons

- No exception indicators found.

## Audit Summary

Invoice INV-2026-1001 was evaluated against supplier, PO, duplicate, payment-term, and currency rules. No exceptions were found. Decision: AUTO_APPROVE; risk level: LOW.

## Machine-Readable Flags

```json
{
  "currency_mismatch": false,
  "duplicate_invoice_id": false,
  "flag_codes": [],
  "invoice_amount_exceeds_po_amount": false,
  "invoice_id": "INV-2026-1001",
  "missing_po": false,
  "missing_tax_id": false,
  "po_id": "PO-9001",
  "rule_version": "2026.05",
  "severity_counts": {
    "HIGH": 0,
    "LOW": 0,
    "MEDIUM": 0
  },
  "supplier_id": "SUP-1001",
  "supplier_not_approved": false,
  "suspicious_payment_terms": false
}
```
