# UiPath API Workflow Contract

## Purpose

The API Workflow is the governed UiPath callout layer between Maestro BPMN and the Python coded triage agent.

It accepts normalized invoice JSON, calls the coded agent endpoint, and returns a stable JSON response that Maestro can branch on.

## Endpoint

Local demo endpoint:

```text
POST http://127.0.0.1:8000/triage/invoice
```

Production or cloud demo endpoint:

```text
POST https://<approved-host>/triage/invoice
```

Use an approved HTTPS host or demo tunnel if UiPath Automation Cloud must reach a local machine. Store base URL and credentials in tenant-approved assets or secret configuration.

## Headers

```text
Content-Type: application/json
Accept: application/json
```

If the hosted API is protected, add the tenant-approved authentication header, for example:

```text
Authorization: Bearer <token-from-secure-asset>
```

## Exact Request Example: Clean Invoice

```json
{
  "invoice_id": "INV-2026-1001",
  "supplier_id": "SUP-1001",
  "supplier_name": "Northwind Office Supplies",
  "supplier_tax_id": "US-12-3456789",
  "po_id": "PO-9001",
  "invoice_amount": 1240.0,
  "po_amount": 1250.0,
  "currency": "USD",
  "invoice_date": "2026-05-01",
  "due_date": "2026-05-31",
  "line_items": [
    {
      "description": "Printer paper cartons",
      "quantity": 40,
      "unit_price": 22.5,
      "line_total": 900.0
    },
    {
      "description": "Ink cartridges",
      "quantity": 10,
      "unit_price": 34.0,
      "line_total": 340.0
    }
  ]
}
```

## Exact Response Example: Clean Invoice

```json
{
  "audit_summary": "Invoice INV-2026-1001 was evaluated against supplier, PO, duplicate, payment-term, and currency rules. No exceptions were found. Decision: AUTO_APPROVE; risk level: LOW.",
  "decision": "AUTO_APPROVE",
  "machine_readable_flags": {
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
  },
  "reasons": [
    "No exception indicators found."
  ],
  "recommended_action": "Approve the invoice for posting and schedule payment under standard AP controls.",
  "risk_level": "LOW"
}
```

## Exact Request Example: High-Risk Invoice

```json
{
  "invoice_id": "INV-DUP-1002",
  "supplier_id": "SUP-7777",
  "supplier_name": "Urgent Wire Vendor",
  "supplier_tax_id": "",
  "po_id": "PO-4040",
  "invoice_amount": 9999.0,
  "po_amount": 1000.0,
  "currency": "EUR",
  "invoice_date": "2026-05-09",
  "due_date": "2026-05-08",
  "line_items": [
    {
      "description": "Emergency consulting retainer",
      "quantity": 1,
      "unit_price": 9999.0,
      "line_total": 9999.0
    }
  ]
}
```

## Exact Response Example: High-Risk Invoice

```json
{
  "audit_summary": "Invoice INV-DUP-1002 was evaluated against supplier, PO, duplicate, payment-term, and currency rules. 6 exception flag(s) were found: DUPLICATE_INVOICE_ID (HIGH); MISSING_SUPPLIER_TAX_ID (MEDIUM); SUPPLIER_NOT_APPROVED (HIGH); MISSING_PO (HIGH); INVOICE_AMOUNT_EXCEEDS_PO (HIGH); SUSPICIOUS_PAYMENT_TERMS (MEDIUM). Decision: ESCALATE_TO_HUMAN; risk level: HIGH.",
  "decision": "ESCALATE_TO_HUMAN",
  "machine_readable_flags": {
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
  },
  "reasons": [
    "Invoice ID INV-DUP-1002 already exists in the processed invoice history.",
    "Supplier tax ID is missing, so the invoice cannot be fully validated for tax compliance.",
    "Supplier SUP-7777 is not in the approved supplier list.",
    "Purchase order PO-4040 was not found in the ERP purchase order extract.",
    "Invoice amount 9999.00 exceeds PO amount 1000.00.",
    "Due date is before the invoice date, which indicates invalid payment terms."
  ],
  "recommended_action": "Create a human-in-the-loop approval task and hold ERP posting until the exception is resolved.",
  "risk_level": "HIGH"
}
```

## UiPath API Workflow Inputs And Outputs

| Name | Direction | Type | Notes |
| --- | --- | --- | --- |
| `invoicePayload` | Input | Object / JSON | Full invoice request body. |
| `triageResponse` | Output | Object / JSON | Full parsed response from `/triage/invoice`. |
| `decision` | Output or local variable | String | `triageResponse.decision`. |
| `riskLevel` | Output or local variable | String | `triageResponse.risk_level`. |
| `auditSummary` | Output or local variable | String | `triageResponse.audit_summary`. |
| `flags` | Output or local variable | Object / JSON | `triageResponse.machine_readable_flags`. |

## Maestro Branch Fields

The minimum field for routing is:

```text
triageResponse.decision
```

Recommended fields to persist as case data:

```text
triageResponse.risk_level
triageResponse.reasons
triageResponse.recommended_action
triageResponse.audit_summary
triageResponse.machine_readable_flags.flag_codes
triageResponse.machine_readable_flags.rule_version
```

## Error Handling

HTTP `200`: parse `triageResponse` and continue to the business decision gateway.

HTTP `422`: invoice JSON is malformed or missing required fields. Route to the technical validation lane.

Timeout or non-2xx response: retry according to tenant policy, then route to operations support. Do not auto-approve when the API call fails.

