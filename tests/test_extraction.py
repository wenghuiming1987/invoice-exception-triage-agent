from __future__ import annotations

from decimal import Decimal

import pytest

from invoice_agent.extraction import InvoiceValidationError, normalize_invoice


def valid_invoice() -> dict:
    return {
        "invoice_id": "INV-VALID-001",
        "supplier_id": "SUP-1001",
        "supplier_name": "Northwind Office Supplies",
        "supplier_tax_id": "US-12-3456789",
        "po_id": "PO-9001",
        "invoice_amount": "100.005",
        "po_amount": 125,
        "currency": "usd",
        "invoice_date": "2026-05-01",
        "due_date": "2026-05-31",
        "line_items": [{"description": "Validation item", "quantity": 1, "line_total": 100.0}],
    }


def test_normalize_invoice_converts_money_dates_and_currency() -> None:
    normalized = normalize_invoice(valid_invoice())

    assert normalized["invoice_amount"] == Decimal("100.00")
    assert normalized["po_amount"] == Decimal("125.00")
    assert normalized["currency"] == "USD"
    assert normalized["invoice_date"].isoformat() == "2026-05-01"


def test_missing_required_field_raises_clear_validation_error() -> None:
    invoice = valid_invoice()
    del invoice["invoice_id"]

    with pytest.raises(InvoiceValidationError, match="invoice_id"):
        normalize_invoice(invoice)


def test_blank_required_identity_field_is_rejected() -> None:
    invoice = valid_invoice()
    invoice["supplier_id"] = " "

    with pytest.raises(InvoiceValidationError, match="supplier_id must be a non-empty string"):
        normalize_invoice(invoice)


def test_negative_amount_is_rejected() -> None:
    invoice = valid_invoice()
    invoice["invoice_amount"] = -1

    with pytest.raises(InvoiceValidationError, match="invoice_amount must not be negative"):
        normalize_invoice(invoice)


def test_invalid_date_is_rejected() -> None:
    invoice = valid_invoice()
    invoice["invoice_date"] = "05/01/2026"

    with pytest.raises(InvoiceValidationError, match="invoice_date must be an ISO date"):
        normalize_invoice(invoice)


def test_invalid_currency_is_rejected() -> None:
    invoice = valid_invoice()
    invoice["currency"] = "US"

    with pytest.raises(InvoiceValidationError, match="currency must be a three-letter"):
        normalize_invoice(invoice)


def test_line_items_must_be_a_list() -> None:
    invoice = valid_invoice()
    invoice["line_items"] = {"description": "not a list"}

    with pytest.raises(InvoiceValidationError, match="line_items must be a list"):
        normalize_invoice(invoice)
