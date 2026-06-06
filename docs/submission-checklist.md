# UiPath AgentHack Submission Checklist

Use this as the final submission record. It is written to avoid false deployment claims: the repository includes a working coded agent, local API, tests, sample data, UiPath setup instructions, and Studio Web API Workflow debug evidence. A full exported Maestro / Action Center tenant package is not included.

## Organizer Feedback Remediation

Feedback received through Devpost on 2026-06-06:

- README needed detailed setup instructions.
- Deck needed to use the official UiPath AgentHack Google Slides template.
- YouTube video needed to show the project functioning on the device/environment, not only explain the concept.

Remediation status:

- [x] README expanded with step-by-step judge setup, run, CLI, API, and UiPath reproduction instructions.
- [x] Demo script updated to require terminal/API/UiPath evidence and keep the video under 5 minutes.
- [x] Official template downloaded for deck rebuild: `submission/template-review/uipath-agenthack-template.pptx`.
- [x] Template-compliant deck replaced at `submission/deck/invoice-exception-triage-agent.pptx`.
- [x] Local demo video regenerated to show functioning terminal/API/UiPath evidence.
- [ ] Devpost deck link verified after pushing the template-compliant deck.
- [ ] Devpost YouTube link verified after uploading the regenerated working demo video if a new video URL is published.

## Required Submission Assets

- [x] Devpost draft project page created.
- [x] Devpost final submission completed: https://devpost.com/software/invoice-exception-triage-agent
- [x] Public GitHub repository created: https://github.com/wenghuiming1987/invoice-exception-triage-agent
- [x] Public GitHub repository linked from Devpost.
- [x] MIT license included in `LICENSE`.
- [x] README included and judge-readable in under 3 minutes.
- [x] Setup instructions included in `README.md`.
- [x] Demo script kept under 5 minutes and focused on live project behavior: `docs/demo-script.md`.
- [x] Demo video recorded and kept under 5 minutes: `submission/demo/invoice-exception-triage-agent-demo.mp4`.
- [x] Demo video uploaded to YouTube as unlisted and linked from Devpost: https://youtu.be/3wf-Y2KLSe4
- [x] Local demo video confirmed to show live terminal/API/UI evidence after organizer feedback.
- [ ] Published YouTube link confirmed to use the regenerated working demo video.
- [x] Presentation deck prepared or attached if required by the submission phase.
- [x] Presentation deck link prepared: https://github.com/wenghuiming1987/invoice-exception-triage-agent/blob/main/submission/deck/invoice-exception-triage-agent.pptx
- [x] Presentation deck confirmed to follow the official UiPath AgentHack template after replacement.
- [x] Screenshots attached to Devpost and stored in `submission/screenshots/`.
- [x] Codex evidence included in `docs/codex-evidence/`.
- [x] Sample data included in `data/sample_invoices/` and `data/mock_erp/`.
- [x] Tests passing locally with `python -m pytest`.

## UiPath Platform Readiness

- [x] UiPath API Workflow contract documented in `uipath/api-workflow-contract.md`.
- [x] Studio Web setup checklist documented in `uipath/studio-web-setup.md`.
- [x] Maestro BPMN-style flow documented in `uipath/maestro-bpmn-notes.md`.
- [x] Human-in-the-loop branch documented for Action Center.
- [x] Technical exception lane documented.
- [x] UiPath Automation Cloud running flow evidence: Studio Web API Workflow debug-tested against a hosted endpoint.
- [x] API Workflow tested from UiPath Studio Web against hosted endpoint.
- [ ] Maestro process tested with clean, medium-risk, and high-risk payloads.
- [ ] Action Center approval task screenshot captured.
- [ ] Full Maestro / Action Center tenant deployment exported or captured. This is not claimed as complete in the README.

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
| Demo video under 5 minutes | `docs/demo-script.md`, `submission/demo/invoice-exception-triage-agent-demo.mp4`, and https://youtu.be/3wf-Y2KLSe4. |
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
