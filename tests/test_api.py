from __future__ import annotations

import json
from pathlib import Path

import pytest

from invoice_agent.api import normalize_api_payload
from invoice_agent.decision_engine import triage_invoice
from invoice_agent.extraction import InvoiceValidationError

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "sample_invoices"


def load_sample(name: str) -> dict:
    return json.loads((SAMPLES / name).read_text(encoding="utf-8"))


def test_api_normalizer_accepts_direct_invoice_json() -> None:
    payload = normalize_api_payload(load_sample("clean_invoice.json"))

    assert triage_invoice(payload)["decision"] == "AUTO_APPROVE"


def test_api_normalizer_accepts_uipath_stringified_invoice_json() -> None:
    payload = normalize_api_payload(json.dumps(load_sample("multiple_high_risk_flags_invoice.json")))
    result = triage_invoice(payload)

    assert result["decision"] == "ESCALATE_TO_HUMAN"
    assert result["risk_level"] == "HIGH"


def test_api_normalizer_accepts_double_encoded_uipath_body() -> None:
    invoice = load_sample("multiple_high_risk_flags_invoice.json")
    payload = normalize_api_payload(json.dumps(json.dumps(json.dumps(invoice))))
    result = triage_invoice(payload)

    assert result["decision"] == "ESCALATE_TO_HUMAN"


def test_api_normalizer_accepts_uipath_bytes_body() -> None:
    invoice = json.dumps(load_sample("multiple_high_risk_flags_invoice.json")).encode("utf-8")
    payload = normalize_api_payload(invoice)
    result = triage_invoice(payload)

    assert result["decision"] == "ESCALATE_TO_HUMAN"


def test_api_normalizer_rejects_non_object_payload() -> None:
    with pytest.raises(InvoiceValidationError, match="invoice JSON object"):
        normalize_api_payload("[object Object]")
