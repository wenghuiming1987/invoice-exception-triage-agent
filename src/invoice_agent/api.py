"""FastAPI wrapper and dependency-light CLI for invoice triage."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .audit_report import write_audit_report
from .decision_engine import triage_invoice
from .extraction import InvoiceValidationError, load_invoice
from .risk_rules import load_reference_data

try:  # FastAPI is optional so the CLI remains dependency-light.
    from fastapi import FastAPI, HTTPException
except ImportError:  # pragma: no cover - exercised only when FastAPI is absent.
    FastAPI = None
    HTTPException = None


def create_app() -> Any:
    if FastAPI is None:
        raise RuntimeError("FastAPI is not installed. Install with: pip install -e '.[api]'")

    api = FastAPI(
        title="Invoice Exception Triage Agent API",
        version="0.1.0",
        description="Deterministic invoice exception triage endpoint for UiPath API Workflow integration.",
    )

    @api.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "invoice-exception-triage-agent"}

    @api.post("/triage/invoice")
    def triage_endpoint(payload: dict[str, Any]) -> dict[str, Any]:
        try:
            return triage_invoice(payload)
        except InvoiceValidationError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    return api


app = create_app() if FastAPI is not None else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run deterministic invoice exception triage.")
    parser.add_argument("--invoice", required=True, help="Path to invoice JSON.")
    parser.add_argument("--output", help="Optional path for JSON or Markdown audit report.")
    parser.add_argument(
        "--mock-erp-dir",
        default=str(Path(__file__).resolve().parents[2] / "data" / "mock_erp"),
        help="Directory containing approved_suppliers.json, purchase_orders.json, and processed_invoices.json.",
    )
    args = parser.parse_args(argv)

    try:
        invoice = load_invoice(args.invoice)
        reference_data = load_reference_data(args.mock_erp_dir)
        result = triage_invoice(invoice, reference_data=reference_data)
    except InvoiceValidationError as exc:
        parser.error(str(exc))
        return 2

    if args.output:
        write_audit_report(invoice, result, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

