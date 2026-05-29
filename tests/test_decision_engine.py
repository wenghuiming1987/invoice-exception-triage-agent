from __future__ import annotations

import json
from pathlib import Path

from invoice_agent.decision_engine import triage_invoice


SAMPLES = Path(__file__).resolve().parents[1] / "data" / "sample_invoices"


def load_sample(name: str) -> dict:
    return json.loads((SAMPLES / name).read_text(encoding="utf-8"))


def test_clean_invoice_auto_approves() -> None:
    result = triage_invoice(load_sample("clean_invoice.json"))

    assert result["risk_level"] == "LOW"
    assert result["decision"] == "AUTO_APPROVE"
    assert result["machine_readable_flags"]["flag_codes"] == []
    assert result["reasons"] == ["No exception indicators found."]


def test_missing_tax_id_requires_review() -> None:
    result = triage_invoice(load_sample("missing_tax_id_invoice.json"))

    assert result["risk_level"] == "MEDIUM"
    assert result["decision"] == "REVIEW_REQUIRED"
    assert result["machine_readable_flags"]["missing_tax_id"] is True


def test_amount_exceeds_po_escalates_to_human() -> None:
    result = triage_invoice(load_sample("amount_exceeds_po_invoice.json"))

    assert result["risk_level"] == "HIGH"
    assert result["decision"] == "ESCALATE_TO_HUMAN"
    assert result["machine_readable_flags"]["invoice_amount_exceeds_po_amount"] is True


def test_multiple_high_risk_flags_return_all_major_flags() -> None:
    result = triage_invoice(load_sample("multiple_high_risk_flags_invoice.json"))
    flags = set(result["machine_readable_flags"]["flag_codes"])

    assert result["risk_level"] == "HIGH"
    assert result["decision"] == "ESCALATE_TO_HUMAN"
    assert {
        "DUPLICATE_INVOICE_ID",
        "MISSING_SUPPLIER_TAX_ID",
        "SUPPLIER_NOT_APPROVED",
        "MISSING_PO",
        "INVOICE_AMOUNT_EXCEEDS_PO",
        "SUSPICIOUS_PAYMENT_TERMS",
    }.issubset(flags)


def test_response_contract_contains_required_output_fields() -> None:
    result = triage_invoice(load_sample("duplicate_invoice.json"))

    assert {
        "risk_level",
        "decision",
        "reasons",
        "recommended_action",
        "audit_summary",
        "machine_readable_flags",
    } == set(result)


def test_currency_mismatch_sample_escalates_to_human() -> None:
    result = triage_invoice(load_sample("currency_mismatch_invoice.json"))

    assert result["risk_level"] == "HIGH"
    assert result["decision"] == "ESCALATE_TO_HUMAN"
    assert result["machine_readable_flags"]["currency_mismatch"] is True


def test_repeated_triage_is_deterministic() -> None:
    invoice = load_sample("multiple_high_risk_flags_invoice.json")

    assert triage_invoice(invoice) == triage_invoice(invoice)
