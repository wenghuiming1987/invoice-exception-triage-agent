from __future__ import annotations

import json

from invoice_agent.audit_report import build_audit_report, render_markdown_report, write_audit_report
from invoice_agent.decision_engine import triage_invoice


def invoice() -> dict:
    return {
        "invoice_id": "INV-AUDIT-001",
        "supplier_id": "SUP-1001",
        "supplier_name": "Northwind Office Supplies",
        "supplier_tax_id": "US-12-3456789",
        "po_id": "PO-9001",
        "invoice_amount": 100.0,
        "po_amount": 125.0,
        "currency": "USD",
        "invoice_date": "2026-05-01",
        "due_date": "2026-05-31",
        "line_items": [{"description": "Audit test", "quantity": 1, "unit_price": 100.0, "line_total": 100.0}],
    }


def test_build_audit_report_wraps_decision_result() -> None:
    payload = invoice()
    result = triage_invoice(payload)
    report = build_audit_report(payload, result)

    assert report["report_type"] == "invoice_exception_triage_audit"
    assert report["invoice_id"] == "INV-AUDIT-001"
    assert report["decision"] == "AUTO_APPROVE"
    assert report["source_invoice"]["invoice_amount"] == "100.00"


def test_render_markdown_report_contains_human_summary() -> None:
    payload = invoice()
    report = build_audit_report(payload, triage_invoice(payload))

    markdown = render_markdown_report(report)

    assert "# Invoice Triage Audit Report: INV-AUDIT-001" in markdown
    assert "Decision: AUTO_APPROVE" in markdown
    assert "Machine-Readable Flags" in markdown


def test_write_audit_report_json(tmp_path) -> None:
    payload = invoice()
    output_path = tmp_path / "audit.json"

    write_audit_report(payload, triage_invoice(payload), output_path)

    saved = json.loads(output_path.read_text(encoding="utf-8"))
    assert saved["invoice_id"] == "INV-AUDIT-001"
    assert saved["risk_level"] == "LOW"


def test_write_audit_report_markdown(tmp_path) -> None:
    payload = invoice()
    output_path = tmp_path / "audit.md"

    write_audit_report(payload, triage_invoice(payload), output_path)

    assert output_path.read_text(encoding="utf-8").startswith("# Invoice Triage Audit Report: INV-AUDIT-001")

