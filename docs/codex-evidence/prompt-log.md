# Prompt Log

This file records the main development prompt used to create the prototype and demonstrates coding-agent usage for the AgentHack submission.

## Initial Build Prompt

The user requested a UiPath AgentHack 2026 submission repository named **Invoice Exception Triage Agent** with:

- runnable code, not a README-only project;
- deterministic invoice triage engine;
- invoice JSON input fields including invoice ID, supplier, PO, amount, currency, dates, and line items;
- rules for duplicate invoice ID, missing tax ID, unapproved supplier, amount above PO, suspicious payment terms, currency mismatch, and missing PO;
- output fields for risk level, decision, reasons, recommended action, audit summary, and machine-readable flags;
- at least six sample invoices;
- pytest tests;
- optional FastAPI wrapper and dependency-light CLI fallback;
- OpenAPI contract;
- UiPath API Workflow, Studio Web, and Maestro BPMN setup notes;
- README, architecture docs, demo script, submission checklist, and Codex evidence docs;
- no fake claim that the UiPath Cloud workflow is already deployed.

## Implementation Notes From Codex Session

Codex checked public UiPath AgentHack and UiPath documentation background before implementation, then created:

- core Python modules in `src/invoice_agent/`;
- sample data in `data/`;
- tests in `tests/`;
- API contract in `openapi/`;
- integration notes in `uipath/`;
- submission docs in `docs/`.

## Verification Prompt / Action

Codex ran the test suite in a local virtual environment and used the CLI to generate expected audit outputs for the sample invoices.

