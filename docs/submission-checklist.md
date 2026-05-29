# UiPath AgentHack Submission Checklist

Use this as the final pre-submission gate. Items marked complete are satisfied by this repository. Items left open require external Devpost, GitHub, video, deck, screenshot, or UiPath tenant work.

## Required Submission Assets

- [ ] Devpost project page created.
- [ ] Public GitHub repository created and linked from Devpost.
- [x] MIT license included in `LICENSE`.
- [x] README included and judge-readable in under 3 minutes.
- [x] Setup instructions included in `README.md`.
- [ ] Demo video recorded and kept under 5 minutes.
- [x] Presentation deck prepared or attached if required by the submission phase.
- [x] Screenshots attached to Devpost or stored in a submission folder.
- [x] Codex evidence included in `docs/codex-evidence/`.
- [x] Sample data included in `data/sample_invoices/` and `data/mock_erp/`.
- [x] Tests passing locally with `python -m pytest`.

## UiPath Platform Readiness

- [x] UiPath API Workflow contract documented in `uipath/api-workflow-contract.md`.
- [x] Studio Web setup checklist documented in `uipath/studio-web-setup.md`.
- [x] Maestro BPMN-style flow documented in `uipath/maestro-bpmn-notes.md`.
- [x] Human-in-the-loop branch documented for Action Center.
- [x] Technical exception lane documented.
- [x] UiPath Automation Cloud running flow configured in a tenant.
- [x] API Workflow tested from UiPath Studio Web against hosted endpoint.
- [ ] Maestro process tested with clean, medium-risk, and high-risk payloads.
- [ ] Action Center approval task screenshot captured.

## Working Prototype Checks

- [x] Runnable Python package under `src/invoice_agent`.
- [x] Deterministic invoice triage engine.
- [x] Dependency-light CLI can process each sample invoice.
- [x] CLI can write JSON and Markdown audit reports.
- [x] Optional FastAPI wrapper provided in `src/invoice_agent/api.py`.
- [x] OpenAPI contract provided in `openapi/invoice-triage-api.yaml`.
- [x] Tests cover rule behavior, input validation, decisions, and reproducible outputs.

## Business Workflow Fit

- [x] Real procure-to-pay / AP exception triage problem.
- [x] Clean invoices can be auto-approved.
- [x] Medium-risk invoices route to AP analyst review.
- [x] High-risk invoices route to human approval.
- [x] Audit summary and machine-readable flags are generated.
- [x] Non-2xx API failures are treated as technical exceptions, not business approvals.

## Sample Coverage

- [x] Clean invoice sample.
- [x] Duplicate invoice sample.
- [x] Missing tax ID sample.
- [x] Amount exceeds PO sample.
- [x] Supplier not approved sample.
- [x] Currency mismatch sample.
- [x] Multiple high-risk flags sample.
- [x] Sample set covers `LOW`, `MEDIUM`, and `HIGH`.
- [x] Expected outputs are stored in `data/expected_outputs/`.
- [x] Expected outputs are reproducible and tested.

## AgentHack Alignment

| AgentHack signal | Repository evidence |
| --- | --- |
| Working solution, not a concept | CLI, Python package, tests, sample outputs. |
| Public repository readiness | README, license, setup, docs, tests. |
| Demo video under 5 minutes | `docs/demo-script.md`. |
| Enterprise workflow complexity | Invoice exception triage with AP review and human escalation. |
| UiPath platform usage | API Workflow, Maestro BPMN, Action Center, Automation Cloud governance docs. |
| Human-in-the-loop | `ESCALATE_TO_HUMAN` branch and Action Center task notes. |
| Auditability | Audit reports, reasons, flags, rule version. |
| Coding agent bonus evidence | `docs/codex-evidence/codex-usage.md`. |

## Final Commands Before Recording

```bash
source .venv/bin/activate
python -m pytest
mkdir -p reports
python -m invoice_agent --invoice data/sample_invoices/clean_invoice.json --output reports/clean_invoice_audit.json
python -m invoice_agent --invoice data/sample_invoices/multiple_high_risk_flags_invoice.json --output reports/risky_invoice_audit.json
```

## Final No-Fake-Claims Check

- [x] README distinguishes the tested Studio Web API Workflow from Maestro / Action Center setup notes.
- [x] UiPath docs describe how to reproduce the flow.
- [x] Demo script distinguishes local prototype from tenant deployment.
- [x] Real UiPath Studio Web API Workflow debug evidence added in `submission/uipath-setup-status.md`.
