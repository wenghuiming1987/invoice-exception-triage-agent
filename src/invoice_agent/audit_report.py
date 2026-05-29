"""Audit report generation for invoice triage decisions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .decision_engine import triage_invoice
from .extraction import invoice_to_jsonable, load_invoice, normalize_invoice
from .risk_rules import ReferenceData


def build_audit_report(invoice_payload: dict[str, Any], triage_result: dict[str, Any]) -> dict[str, Any]:
    invoice = normalize_invoice(invoice_payload)
    return {
        "report_type": "invoice_exception_triage_audit",
        "invoice_id": invoice["invoice_id"],
        "supplier_id": invoice["supplier_id"],
        "supplier_name": invoice["supplier_name"],
        "po_id": invoice["po_id"],
        "risk_level": triage_result["risk_level"],
        "decision": triage_result["decision"],
        "reasons": triage_result["reasons"],
        "recommended_action": triage_result["recommended_action"],
        "audit_summary": triage_result["audit_summary"],
        "machine_readable_flags": triage_result["machine_readable_flags"],
        "source_invoice": invoice_to_jsonable(invoice),
    }


def render_markdown_report(report: dict[str, Any]) -> str:
    reasons = "\n".join(f"- {reason}" for reason in report["reasons"])
    flags = json.dumps(report["machine_readable_flags"], indent=2, sort_keys=True)
    return (
        f"# Invoice Triage Audit Report: {report['invoice_id']}\n\n"
        f"- Supplier: {report['supplier_name']} ({report['supplier_id']})\n"
        f"- Purchase order: {report['po_id'] or 'MISSING'}\n"
        f"- Risk level: {report['risk_level']}\n"
        f"- Decision: {report['decision']}\n"
        f"- Recommended action: {report['recommended_action']}\n\n"
        "## Reasons\n\n"
        f"{reasons}\n\n"
        "## Audit Summary\n\n"
        f"{report['audit_summary']}\n\n"
        "## Machine-Readable Flags\n\n"
        f"```json\n{flags}\n```\n"
    )


def write_audit_report(
    invoice_payload: dict[str, Any],
    triage_result: dict[str, Any],
    output_path: str | Path,
) -> Path:
    """Write a JSON or Markdown audit report based on output file extension."""

    report = build_audit_report(invoice_payload, triage_result)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.suffix.lower() in {".md", ".markdown"}:
        path.write_text(render_markdown_report(report), encoding="utf-8")
    else:
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def process_invoice_file(
    invoice_path: str | Path,
    output_path: str | Path | None = None,
    reference_data: ReferenceData | None = None,
) -> dict[str, Any]:
    invoice = load_invoice(invoice_path)
    result = triage_invoice(invoice, reference_data=reference_data)
    if output_path:
        write_audit_report(invoice, result, output_path)
    return result

