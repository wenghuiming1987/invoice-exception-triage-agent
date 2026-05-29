# Invoice Triage Audit Report: INV-DUP-1002

- Supplier: Urgent Wire Vendor (SUP-7777)
- Purchase order: PO-4040
- Risk level: HIGH
- Decision: ESCALATE_TO_HUMAN
- Recommended action: Create a human-in-the-loop approval task and hold ERP posting until the exception is resolved.

## Reasons

- Invoice ID INV-DUP-1002 already exists in the processed invoice history.
- Supplier tax ID is missing, so the invoice cannot be fully validated for tax compliance.
- Supplier SUP-7777 is not in the approved supplier list.
- Purchase order PO-4040 was not found in the ERP purchase order extract.
- Invoice amount 9999.00 exceeds PO amount 1000.00.
- Due date is before the invoice date, which indicates invalid payment terms.

## Audit Summary

Invoice INV-DUP-1002 was evaluated against supplier, PO, duplicate, payment-term, and currency rules. 6 exception flag(s) were found: DUPLICATE_INVOICE_ID (HIGH); MISSING_SUPPLIER_TAX_ID (MEDIUM); SUPPLIER_NOT_APPROVED (HIGH); MISSING_PO (HIGH); INVOICE_AMOUNT_EXCEEDS_PO (HIGH); SUSPICIOUS_PAYMENT_TERMS (MEDIUM). Decision: ESCALATE_TO_HUMAN; risk level: HIGH.

## Machine-Readable Flags

```json
{
  "currency_mismatch": false,
  "duplicate_invoice_id": true,
  "flag_codes": [
    "DUPLICATE_INVOICE_ID",
    "MISSING_SUPPLIER_TAX_ID",
    "SUPPLIER_NOT_APPROVED",
    "MISSING_PO",
    "INVOICE_AMOUNT_EXCEEDS_PO",
    "SUSPICIOUS_PAYMENT_TERMS"
  ],
  "invoice_amount_exceeds_po_amount": true,
  "invoice_id": "INV-DUP-1002",
  "missing_po": true,
  "missing_tax_id": true,
  "po_id": "PO-4040",
  "rule_version": "2026.05",
  "severity_counts": {
    "HIGH": 4,
    "LOW": 0,
    "MEDIUM": 2
  },
  "supplier_id": "SUP-7777",
  "supplier_not_approved": true,
  "suspicious_payment_terms": true
}
```
