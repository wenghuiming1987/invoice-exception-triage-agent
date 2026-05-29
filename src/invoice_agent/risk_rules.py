"""Deterministic invoice exception rules."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
import json
from pathlib import Path
from typing import Any


DEFAULT_ERP_DIR = Path(__file__).resolve().parents[2] / "data" / "mock_erp"


@dataclass(frozen=True)
class RiskFlag:
    code: str
    severity: str
    reason: str
    detail: dict[str, str]


@dataclass(frozen=True)
class ReferenceData:
    approved_suppliers: dict[str, dict[str, Any]]
    purchase_orders: dict[str, dict[str, Any]]
    processed_invoice_ids: set[str]

    def is_supplier_approved(self, supplier_id: str) -> bool:
        return supplier_id in self.approved_suppliers

    def get_purchase_order(self, po_id: str) -> dict[str, Any] | None:
        if not po_id:
            return None
        return self.purchase_orders.get(po_id)


def load_reference_data(mock_erp_dir: str | Path = DEFAULT_ERP_DIR) -> ReferenceData:
    """Load mock ERP extracts used by the local prototype."""

    erp_dir = Path(mock_erp_dir)
    suppliers = _load_json(erp_dir / "approved_suppliers.json")
    purchase_orders = _load_json(erp_dir / "purchase_orders.json")
    processed_invoice_ids = _load_json(erp_dir / "processed_invoices.json")

    return ReferenceData(
        approved_suppliers={supplier["supplier_id"]: supplier for supplier in suppliers},
        purchase_orders={po["po_id"]: po for po in purchase_orders},
        processed_invoice_ids=set(processed_invoice_ids),
    )


def run_rules(invoice: dict[str, Any], reference_data: ReferenceData | None = None) -> list[RiskFlag]:
    """Run all invoice risk rules in a stable order."""

    reference_data = reference_data or load_reference_data()
    rules = (
        duplicate_invoice_id,
        missing_tax_id,
        supplier_not_approved,
        missing_po,
        invoice_amount_exceeds_po_amount,
        suspicious_payment_terms,
        currency_mismatch,
    )
    flags: list[RiskFlag] = []
    for rule in rules:
        flag = rule(invoice, reference_data)
        if flag:
            flags.append(flag)
    return flags


def duplicate_invoice_id(invoice: dict[str, Any], reference_data: ReferenceData) -> RiskFlag | None:
    invoice_id = invoice["invoice_id"]
    if invoice_id in reference_data.processed_invoice_ids:
        return RiskFlag(
            code="DUPLICATE_INVOICE_ID",
            severity="HIGH",
            reason=f"Invoice ID {invoice_id} already exists in the processed invoice history.",
            detail={"invoice_id": invoice_id},
        )
    return None


def missing_tax_id(invoice: dict[str, Any], reference_data: ReferenceData) -> RiskFlag | None:
    if not str(invoice.get("supplier_tax_id", "")).strip():
        return RiskFlag(
            code="MISSING_SUPPLIER_TAX_ID",
            severity="MEDIUM",
            reason="Supplier tax ID is missing, so the invoice cannot be fully validated for tax compliance.",
            detail={"supplier_id": invoice["supplier_id"]},
        )
    return None


def supplier_not_approved(invoice: dict[str, Any], reference_data: ReferenceData) -> RiskFlag | None:
    supplier_id = invoice["supplier_id"]
    if not reference_data.is_supplier_approved(supplier_id):
        return RiskFlag(
            code="SUPPLIER_NOT_APPROVED",
            severity="HIGH",
            reason=f"Supplier {supplier_id} is not in the approved supplier list.",
            detail={"supplier_id": supplier_id},
        )
    return None


def missing_po(invoice: dict[str, Any], reference_data: ReferenceData) -> RiskFlag | None:
    po_id = str(invoice.get("po_id", "")).strip()
    if not po_id:
        return RiskFlag(
            code="MISSING_PO",
            severity="HIGH",
            reason="Invoice does not reference a purchase order.",
            detail={"po_id": ""},
        )
    if reference_data.get_purchase_order(po_id) is None:
        return RiskFlag(
            code="MISSING_PO",
            severity="HIGH",
            reason=f"Purchase order {po_id} was not found in the ERP purchase order extract.",
            detail={"po_id": po_id},
        )
    return None


def invoice_amount_exceeds_po_amount(invoice: dict[str, Any], reference_data: ReferenceData) -> RiskFlag | None:
    invoice_amount = _as_decimal(invoice["invoice_amount"])
    po_amount = _as_decimal(invoice["po_amount"])
    if invoice_amount > po_amount:
        return RiskFlag(
            code="INVOICE_AMOUNT_EXCEEDS_PO",
            severity="HIGH",
            reason=f"Invoice amount {invoice_amount:.2f} exceeds PO amount {po_amount:.2f}.",
            detail={"invoice_amount": f"{invoice_amount:.2f}", "po_amount": f"{po_amount:.2f}"},
        )
    return None


def suspicious_payment_terms(invoice: dict[str, Any], reference_data: ReferenceData) -> RiskFlag | None:
    invoice_date = _as_date(invoice["invoice_date"])
    due_date = _as_date(invoice["due_date"])
    terms_days = (due_date - invoice_date).days

    if terms_days < 0:
        reason = "Due date is before the invoice date, which indicates invalid payment terms."
    elif terms_days == 0:
        reason = "Invoice is due on the invoice date, which creates an unusually urgent payment request."
    elif terms_days > 90:
        reason = f"Invoice payment terms are {terms_days} days, above the 90-day policy threshold."
    else:
        return None

    return RiskFlag(
        code="SUSPICIOUS_PAYMENT_TERMS",
        severity="MEDIUM",
        reason=reason,
        detail={"terms_days": str(terms_days)},
    )


def currency_mismatch(invoice: dict[str, Any], reference_data: ReferenceData) -> RiskFlag | None:
    po = reference_data.get_purchase_order(str(invoice.get("po_id", "")).strip())
    if not po:
        return None

    invoice_currency = str(invoice["currency"]).upper()
    po_currency = str(po.get("currency", "")).upper()
    if po_currency and invoice_currency != po_currency:
        return RiskFlag(
            code="CURRENCY_MISMATCH",
            severity="HIGH",
            reason=f"Invoice currency {invoice_currency} does not match PO currency {po_currency}.",
            detail={"invoice_currency": invoice_currency, "po_currency": po_currency},
        )
    return None


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _as_decimal(value: Any) -> Decimal:
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value)).quantize(Decimal("0.01"))


def _as_date(value: Any) -> date:
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))

