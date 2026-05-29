"""Decision engine that converts rule flags into business actions."""

from __future__ import annotations

from collections import Counter
from typing import Any

from .extraction import normalize_invoice
from .risk_rules import ReferenceData, RiskFlag, load_reference_data, run_rules


FLAG_KEYS = {
    "DUPLICATE_INVOICE_ID": "duplicate_invoice_id",
    "MISSING_SUPPLIER_TAX_ID": "missing_tax_id",
    "SUPPLIER_NOT_APPROVED": "supplier_not_approved",
    "INVOICE_AMOUNT_EXCEEDS_PO": "invoice_amount_exceeds_po_amount",
    "SUSPICIOUS_PAYMENT_TERMS": "suspicious_payment_terms",
    "CURRENCY_MISMATCH": "currency_mismatch",
    "MISSING_PO": "missing_po",
}


def triage_invoice(
    invoice_payload: dict[str, Any],
    reference_data: ReferenceData | None = None,
) -> dict[str, Any]:
    """Evaluate an invoice and return a deterministic triage decision."""

    invoice = normalize_invoice(invoice_payload)
    reference_data = reference_data or load_reference_data()
    flags = run_rules(invoice, reference_data)
    risk_level = classify_risk_level(flags)
    decision = choose_decision(risk_level)
    reasons = [flag.reason for flag in flags] or ["No exception indicators found."]
    recommended_action = choose_recommended_action(decision)

    return {
        "risk_level": risk_level,
        "decision": decision,
        "reasons": reasons,
        "recommended_action": recommended_action,
        "audit_summary": build_audit_summary(invoice, risk_level, decision, flags),
        "machine_readable_flags": build_machine_flags(invoice, flags),
    }


def classify_risk_level(flags: list[RiskFlag]) -> str:
    if not flags:
        return "LOW"
    severity_counts = Counter(flag.severity for flag in flags)
    if severity_counts["HIGH"] >= 1 or len(flags) >= 3:
        return "HIGH"
    return "MEDIUM"


def choose_decision(risk_level: str) -> str:
    if risk_level == "LOW":
        return "AUTO_APPROVE"
    if risk_level == "MEDIUM":
        return "REVIEW_REQUIRED"
    return "ESCALATE_TO_HUMAN"


def choose_recommended_action(decision: str) -> str:
    actions = {
        "AUTO_APPROVE": "Approve the invoice for posting and schedule payment under standard AP controls.",
        "REVIEW_REQUIRED": "Route the invoice to an AP analyst for targeted review of the flagged exception.",
        "ESCALATE_TO_HUMAN": "Create a human-in-the-loop approval task and hold ERP posting until the exception is resolved.",
    }
    return actions[decision]


def build_audit_summary(
    invoice: dict[str, Any],
    risk_level: str,
    decision: str,
    flags: list[RiskFlag],
) -> str:
    if not flags:
        return (
            f"Invoice {invoice['invoice_id']} was evaluated against supplier, PO, duplicate, "
            f"payment-term, and currency rules. No exceptions were found. Decision: {decision}; "
            f"risk level: {risk_level}."
        )

    flag_text = "; ".join(f"{flag.code} ({flag.severity})" for flag in flags)
    return (
        f"Invoice {invoice['invoice_id']} was evaluated against supplier, PO, duplicate, "
        f"payment-term, and currency rules. {len(flags)} exception flag(s) were found: "
        f"{flag_text}. Decision: {decision}; risk level: {risk_level}."
    )


def build_machine_flags(invoice: dict[str, Any], flags: list[RiskFlag]) -> dict[str, Any]:
    codes = [flag.code for flag in flags]
    severity_counts = Counter(flag.severity for flag in flags)
    machine_flags = {
        key: False
        for key in (
            "duplicate_invoice_id",
            "missing_tax_id",
            "supplier_not_approved",
            "invoice_amount_exceeds_po_amount",
            "suspicious_payment_terms",
            "currency_mismatch",
            "missing_po",
        )
    }
    for code in codes:
        machine_flags[FLAG_KEYS[code]] = True

    machine_flags.update(
        {
            "flag_codes": codes,
            "severity_counts": {
                "HIGH": severity_counts["HIGH"],
                "MEDIUM": severity_counts["MEDIUM"],
                "LOW": severity_counts["LOW"],
            },
            "invoice_id": invoice["invoice_id"],
            "supplier_id": invoice["supplier_id"],
            "po_id": invoice["po_id"],
            "rule_version": "2026.05",
        }
    )
    return machine_flags

