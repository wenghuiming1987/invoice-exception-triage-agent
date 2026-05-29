"""Input loading and normalization for invoice triage."""

from __future__ import annotations

from copy import deepcopy
from datetime import date
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = (
    "invoice_id",
    "supplier_id",
    "supplier_name",
    "supplier_tax_id",
    "po_id",
    "invoice_amount",
    "po_amount",
    "currency",
    "invoice_date",
    "due_date",
    "line_items",
)


class InvoiceValidationError(ValueError):
    """Raised when an invoice payload is missing required shape or values."""


def load_json(path: str | Path) -> dict[str, Any]:
    """Load a JSON document from disk."""

    with Path(path).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise InvoiceValidationError("Invoice JSON must be an object.")
    return payload


def load_invoice(path: str | Path) -> dict[str, Any]:
    """Load and normalize an invoice JSON file."""

    return normalize_invoice(load_json(path))


def normalize_invoice(raw_invoice: dict[str, Any]) -> dict[str, Any]:
    """Validate required fields and convert money/date values to safe types."""

    if not isinstance(raw_invoice, dict):
        raise InvoiceValidationError("Invoice payload must be a JSON object.")

    missing = [field for field in REQUIRED_FIELDS if field not in raw_invoice]
    if missing:
        raise InvoiceValidationError(f"Invoice is missing required field(s): {', '.join(missing)}")

    invoice = deepcopy(raw_invoice)
    invoice["invoice_id"] = _as_non_empty_string(invoice["invoice_id"], "invoice_id")
    invoice["supplier_id"] = _as_non_empty_string(invoice["supplier_id"], "supplier_id")
    invoice["supplier_name"] = _as_non_empty_string(invoice["supplier_name"], "supplier_name")
    invoice["supplier_tax_id"] = _as_string(invoice["supplier_tax_id"]).strip()
    invoice["po_id"] = _as_string(invoice["po_id"]).strip()
    invoice["invoice_amount"] = _as_money(invoice["invoice_amount"], "invoice_amount")
    invoice["po_amount"] = _as_money(invoice["po_amount"], "po_amount")
    invoice["currency"] = _as_currency(invoice["currency"])
    invoice["invoice_date"] = _as_date(invoice["invoice_date"], "invoice_date")
    invoice["due_date"] = _as_date(invoice["due_date"], "due_date")

    if not isinstance(invoice["line_items"], list):
        raise InvoiceValidationError("line_items must be a list.")

    return invoice


def invoice_to_jsonable(invoice: dict[str, Any]) -> dict[str, Any]:
    """Convert a normalized invoice back to JSON-safe primitives."""

    safe_invoice = deepcopy(invoice)
    for amount_field in ("invoice_amount", "po_amount"):
        if isinstance(safe_invoice.get(amount_field), Decimal):
            safe_invoice[amount_field] = _money_to_string(safe_invoice[amount_field])
    for date_field in ("invoice_date", "due_date"):
        if isinstance(safe_invoice.get(date_field), date):
            safe_invoice[date_field] = safe_invoice[date_field].isoformat()
    return safe_invoice


def _as_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def _as_non_empty_string(value: Any, field_name: str) -> str:
    text = _as_string(value).strip()
    if not text:
        raise InvoiceValidationError(f"{field_name} must be a non-empty string.")
    return text


def _as_currency(value: Any) -> str:
    currency = _as_non_empty_string(value, "currency").upper()
    if len(currency) != 3 or not currency.isalpha():
        raise InvoiceValidationError("currency must be a three-letter ISO-style currency code.")
    return currency


def _as_money(value: Any, field_name: str) -> Decimal:
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise InvoiceValidationError(f"{field_name} must be a valid number.") from exc
    if amount < Decimal("0"):
        raise InvoiceValidationError(f"{field_name} must not be negative.")
    return amount.quantize(Decimal("0.01"))


def _as_date(value: Any, field_name: str) -> date:
    try:
        return date.fromisoformat(str(value))
    except ValueError as exc:
        raise InvoiceValidationError(f"{field_name} must be an ISO date in YYYY-MM-DD format.") from exc


def _money_to_string(amount: Decimal) -> str:
    return f"{amount:.2f}"
