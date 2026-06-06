# Codex Usage Evidence

OpenAI Codex was used as the coding agent for this UiPath AgentHack prototype.

## Coding Agent Used

- Coding agent: OpenAI Codex
- Usage type: repository scaffolding, Python implementation, test creation, API contract drafting, UiPath integration documentation, demo-readiness hardening
- Integration dates: 2026-05-30 initial build; 2026-06-07 submission hardening after organizer feedback

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
- `tests/test_api.py`

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

Submission materials:

- `submission/deck/invoice-exception-triage-agent.pptx`
- `submission/deck/presentation-outline.md`
- `submission/demo/youtube-upload-metadata.md`
- `submission/demo/demo-narration.json`
- `submission/remediation-notes.md`

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
- configure and debug a real UiPath Studio Web API Workflow against a temporary HTTPS endpoint;
- harden the README and demo script for judge review;
- respond to organizer feedback by making setup instructions more explicit, aligning the deck to the official template, and documenting that the demo video must show the working project.

## Meaningful Integration Into The Working Project

The Codex-generated output is not a separate note or mockup. It is integrated into the working prototype:

- The Python modules under `src/invoice_agent/` are imported by the CLI, API wrapper, and tests.
- The test suite verifies rule behavior, validation errors, deterministic audit reports, and sample invoice coverage.
- The sample invoices and mock ERP data drive real CLI output.
- The expected outputs under `data/expected_outputs/` are reproducible from the current engine and guarded by tests.
- The OpenAPI contract documents the same request and response fields returned by `triage_invoice`.
- The UiPath docs explain how the response fields drive Maestro branching and Action Center approval.
- The Studio Web debug evidence shows the UiPath API Workflow calling the coded agent and receiving `ESCALATE_TO_HUMAN`.
- The submission deck follows the UiPath AgentHack template structure and summarizes the same working repository evidence.
- The demo script uses real CLI/API/UiPath evidence rather than a concept-only walkthrough.

## Verification Evidence

Local verification command:

```bash
python -m pytest
```

Latest local result during hardening:

```text
35 passed
```

Sample CLI verification:

```bash
python -m invoice_agent --invoice data/sample_invoices/clean_invoice.json --output reports/clean_invoice_audit.json
python -m invoice_agent --invoice data/sample_invoices/multiple_high_risk_flags_invoice.json --output reports/risky_invoice_audit.json
```

## Screenshot / Session Export Evidence

Evidence links and placeholders:

- Screenshot: terminal output with `python -m pytest`: `submission/screenshots/01-tests-passing.png`
- Screenshot: generated audit report: `submission/screenshots/04-audit-report.png`
- Screenshot: UiPath Studio Web API Workflow debug success: `submission/screenshots/07-uipath-debug-success.png`
- Demo video generated from Codex-prepared narration: `submission/demo/invoice-exception-triage-agent-demo.mp4`
- Published demo video: https://youtu.be/if6iNBls7CM
- Screenshot: Devpost ready-to-submit page: `submission/screenshots/08-devpost-ready-to-submit.png`
- Screenshot: original YouTube video published/unlisted evidence: `submission/screenshots/09-youtube-video-published.png`
- Screenshot: updated YouTube demo showing live terminal/API run: `submission/screenshots/11-youtube-video-updated.png`
- Screenshot: updated YouTube demo visibility set to public: `submission/screenshots/12-youtube-video-public.png`
- Screenshot: Devpost submitted project page: `submission/screenshots/10-devpost-submitted.png`
- Devpost project: https://devpost.com/software/invoice-exception-triage-agent

Placeholder for additional evidence if requested by the judges:

- Screenshot: official-template deck attached on Devpost: `submission/deck/contact-sheet.png`
- Session export link or transcript: `TODO`

## Boundary

Codex assisted with implementation, documentation, and Studio Web API Workflow setup. This repository claims a tested UiPath Studio Web API Workflow call, but does not claim a deployed Maestro or Action Center production process.
