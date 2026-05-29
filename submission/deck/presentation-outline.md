# Presentation Deck Outline

## Slide 1: Invoice Exception Triage Agent

- UiPath AgentHack 2026 submission
- Coded agent plus UiPath orchestration
- AP exception triage with auditability

## Slide 2: Business Problem

- AP teams manually check duplicate history, supplier status, PO match, tax ID, terms, and currency.
- Clean invoices wait unnecessarily.
- Risky invoices need human accountability before ERP posting.

## Slide 3: Solution

- Python coded agent returns deterministic decision.
- UiPath API Workflow calls `/triage/invoice`.
- Maestro branches the case.
- Action Center handles high-risk human approval.

## Slide 4: Workflow

Start -> Receive invoice -> Call triage API -> Decision gateway -> Auto approve / Review / Human escalation -> Audit -> End

## Slide 5: Demo Evidence

- Tests passing.
- Clean invoice: `AUTO_APPROVE`.
- Risky invoice: `ESCALATE_TO_HUMAN`.
- UiPath Studio Web API Workflow debug: HTTP `200`.
- Audit report with reasons and flags.

## Slide 6: UiPath Fit

- Studio Web / API Workflow
- Maestro BPMN
- Action Center
- Orchestrator / Automation Cloud governance

## Slide 7: Codex Evidence

- Codex helped scaffold and harden code, tests, OpenAPI, UiPath docs, and demo materials.
- Generated output is integrated into the runnable project.

## Slide 8: Next Steps

- Connect real ERP data.
- Add authentication.
- Add document extraction intake.
- Add AP metrics dashboard.
