from __future__ import annotations

from copy import deepcopy

from invoice_agent.extraction import normalize_invoice
from invoice_agent.risk_rules import load_reference_data, run_rules


def base_invoice() -> dict:
    return {
        "invoice_id": "INV-UNIT-001",
        "supplier_id": "SUP-1001",
        "supplier_name": "Northwind Office Supplies",
        "supplier_tax_id": "US-12-3456789",
        "po_id": "PO-9001",
        "invoice_amount": 100.0,
        "po_amount": 125.0,
        "currency": "USD",
        "invoice_date": "2026-05-01",
        "due_date": "2026-05-31",
        "line_items": [{"description": "Test item", "quantity": 1, "unit_price": 100.0, "line_total": 100.0}],
    }


def flag_codes(invoice: dict) -> set[str]:
    return {flag.code for flag in run_rules(normalize_invoice(invoice), load_reference_data())}


def test_clean_invoice_has_no_flags() -> None:
    assert flag_codes(base_invoice()) == set()


def test_duplicate_invoice_id_rule() -> None:
    invoice = base_invoice()
    invoice["invoice_id"] = "INV-DUP-1002"
    assert "DUPLICATE_INVOICE_ID" in flag_codes(invoice)


def test_missing_tax_id_rule() -> None:
    invoice = base_invoice()
    invoice["supplier_tax_id"] = ""
    assert "MISSING_SUPPLIER_TAX_ID" in flag_codes(invoice)


def test_supplier_not_approved_rule() -> None:
    invoice = base_invoice()
    invoice["supplier_id"] = "SUP-4040"
    assert "SUPPLIER_NOT_APPROVED" in flag_codes(invoice)


def test_invoice_amount_exceeds_po_amount_rule() -> None:
    invoice = base_invoice()
    invoice["invoice_amount"] = 200.0
    invoice["po_amount"] = 125.0
    assert "INVOICE_AMOUNT_EXCEEDS_PO" in flag_codes(invoice)


def test_suspicious_payment_terms_rule_for_due_date_before_invoice_date() -> None:
    invoice = base_invoice()
    invoice["invoice_date"] = "2026-05-10"
    invoice["due_date"] = "2026-05-09"
    assert "SUSPICIOUS_PAYMENT_TERMS" in flag_codes(invoice)


def test_suspicious_payment_terms_rule_for_long_terms() -> None:
    invoice = base_invoice()
    invoice["invoice_date"] = "2026-05-01"
    invoice["due_date"] = "2026-09-01"
    assert "SUSPICIOUS_PAYMENT_TERMS" in flag_codes(invoice)


def test_currency_mismatch_rule() -> None:
    invoice = base_invoice()
    invoice["po_id"] = "PO-9006"
    invoice["currency"] = "EUR"
    assert "CURRENCY_MISMATCH" in flag_codes(invoice)


def test_missing_po_rule_for_blank_po() -> None:
    invoice = base_invoice()
    invoice["po_id"] = ""
    assert "MISSING_PO" in flag_codes(invoice)


def test_missing_po_rule_for_unknown_po() -> None:
    invoice = deepcopy(base_invoice())
    invoice["po_id"] = "PO-DOES-NOT-EXIST"
    assert "MISSING_PO" in flag_codes(invoice)

