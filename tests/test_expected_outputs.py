from __future__ import annotations

import json
from pathlib import Path

from invoice_agent.audit_report import build_audit_report
from invoice_agent.decision_engine import triage_invoice


ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "data" / "sample_invoices"
EXPECTED = ROOT / "data" / "expected_outputs"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_all_sample_outputs_are_reproducible() -> None:
    sample_files = sorted(path for path in SAMPLES.glob("*.json") if not path.name.startswith("._"))
    assert len(sample_files) >= 6

    for sample_path in sample_files:
        invoice = load_json(sample_path)
        current_report = build_audit_report(invoice, triage_invoice(invoice))
        expected_report = load_json(EXPECTED / f"{sample_path.stem}_audit.json")
        assert current_report == expected_report


def test_sample_set_covers_all_risk_levels_and_decisions() -> None:
    outcomes = set()
    for sample_path in SAMPLES.glob("*.json"):
        if sample_path.name.startswith("._"):
            continue
        result = triage_invoice(load_json(sample_path))
        outcomes.add((result["risk_level"], result["decision"]))

    assert ("LOW", "AUTO_APPROVE") in outcomes
    assert ("MEDIUM", "REVIEW_REQUIRED") in outcomes
    assert ("HIGH", "ESCALATE_TO_HUMAN") in outcomes
