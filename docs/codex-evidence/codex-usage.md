# Codex Usage Evidence

OpenAI Codex was used as the coding agent for this UiPath AgentHack prototype.

## Coding Agent Used

- Coding agent: OpenAI Codex
- Usage type: repository scaffolding, Python implementation, test creation, API contract drafting, UiPath integration documentation, demo-readiness hardening
- Integration date: 2026-05-30

## Files Codex Helped Create Or Harden

Core implementation:

- `src/invoice_agent/__init__.py`
- `src/invoice_agent/__main__.py`
- `src/invoice_agent/extraction.py`
- `src/invoice_agent/risk_rules.py`
- `src/invoice_agent/decision_engine.py`
- `src/invoice_agent/audit_report.py`
- `src/invoice_agent/api.py`

Tests:

- `tests/test_risk_rules.py`
- `tests/test_decision_engine.py`
- `tests/test_audit_report.py`
- `tests/test_extraction.py`
- `tests/test_expected_outputs.py`

Sample and reference data:

- `data/sample_invoices/*.json`
- `data/mock_erp/*.json`
- `data/expected_outputs/*`

Contracts and documentation:

- `README.md`
- `openapi/invoice-triage-api.yaml`
- `docs/architecture.md`
- `docs/demo-script.md`
- `docs/submission-checklist.md`
- `docs/codex-evidence/prompt-log.md`
- `uipath/api-workflow-contract.md`
- `uipath/studio-web-setup.md`
- `uipath/maestro-bpmn-notes.md`

## How Codex Contributed

Codex helped:

- turn the product idea into a concrete repository structure;
- implement deterministic invoice validation and risk rules;
- map rules to business decisions and recommended actions;
- add a dependency-light CLI and optional FastAPI wrapper;
- create sample invoices covering `LOW`, `MEDIUM`, and `HIGH`;
- create tests for rules, input validation, deterministic outputs, and sample coverage;
- write an OpenAPI contract matching the implemented endpoint;
- document how UiPath API Workflow and Maestro BPMN can call and route the coded agent;
- harden the README and demo script for judge review.

## Meaningful Integration Into The Working Project

The Codex-generated output is not a separate note or mockup. It is integrated into the working prototype:

- The Python modules under `src/invoice_agent/` are imported by the CLI, API wrapper, and tests.
- The test suite verifies rule behavior, validation errors, deterministic audit reports, and sample invoice coverage.
- The sample invoices and mock ERP data drive real CLI output.
- The expected outputs under `data/expected_outputs/` are reproducible from the current engine and guarded by tests.
- The OpenAPI contract documents the same request and response fields returned by `triage_invoice`.
- The UiPath docs explain how the response fields drive Maestro branching and Action Center approval.

## Verification Evidence

Local verification command:

```bash
python -m pytest
```

Latest local result during hardening:

```text
30 passed
```

Sample CLI verification:

```bash
python -m invoice_agent --invoice data/sample_invoices/clean_invoice.json --output reports/clean_invoice_audit.json
python -m invoice_agent --invoice data/sample_invoices/multiple_high_risk_flags_invoice.json --output reports/risky_invoice_audit.json
```

## Screenshot / Session Export Placeholders

Add final evidence links here before Devpost submission:

- Screenshot: Codex session showing repository creation and test run: `TODO`
- Screenshot: terminal output with `python -m pytest`: `TODO`
- Screenshot: generated audit report: `TODO`
- Session export link or transcript: `TODO`
- Devpost project evidence field: `TODO`

## Boundary

Codex assisted with implementation and documentation. This repository does not claim that Codex deployed a UiPath tenant workflow, created tenant credentials, or published a live Automation Cloud process.
