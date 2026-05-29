# Demo Script

Target length: 4 minutes 30 seconds. Keep the video under 5 minutes.

## Live Demo Path

Use this path if recording quickly:

1. Run tests.
2. Run clean invoice -> show `AUTO_APPROVE`.
3. Run risky invoice -> show `ESCALATE_TO_HUMAN`.
4. Open generated audit report.
5. Show UiPath BPMN/API docs.
6. Show Codex evidence.

## 0:00-0:25 - Business Problem

Narration:

"Accounts payable teams spend time checking invoices against supplier master data, purchase orders, duplicate history, tax identifiers, currencies, and payment terms. Clean invoices should move automatically, but risky exceptions need human accountability before posting or payment."

Show:

- repository README top section;
- sample invoice folder.

## 0:25-0:55 - Solution Overview

Narration:

"Invoice Exception Triage Agent combines a Python coded agent with UiPath orchestration. The coded agent returns a deterministic risk decision. UiPath API Workflow calls it, Maestro branches the process, and Action Center handles human approval for high-risk exceptions."

Show:

- `src/invoice_agent/`;
- `uipath/maestro-bpmn-notes.md`;
- `uipath/api-workflow-contract.md`.

## 0:55-1:20 - Technical Proof

Run:

```bash
python -m pytest
```

Narration:

"The test suite covers business rules, input validation, deterministic audit output, and sample coverage for LOW, MEDIUM, and HIGH risk decisions."

Expected:

```text
30 passed
```

## 1:20-2:05 - Clean Invoice Auto-Approved

Run:

```bash
mkdir -p reports
python -m invoice_agent \
  --invoice data/sample_invoices/clean_invoice.json \
  --output reports/clean_invoice_audit.json
```

Narration:

"This invoice matches the approved supplier and PO data. There are no duplicate, tax, amount, payment term, or currency flags, so the agent returns LOW risk and AUTO_APPROVE."

Show:

- stdout `risk_level: LOW`;
- stdout `decision: AUTO_APPROVE`;
- `reports/clean_invoice_audit.json`.

## 2:05-2:55 - Risky Invoice Escalated To Human

Run:

```bash
python -m invoice_agent \
  --invoice data/sample_invoices/multiple_high_risk_flags_invoice.json \
  --output reports/risky_invoice_audit.json
```

Narration:

"This invoice is a duplicate, lacks a tax ID, comes from an unapproved supplier, references an unknown PO, exceeds the PO amount, and has invalid payment terms. The agent returns HIGH risk and ESCALATE_TO_HUMAN."

Show:

- `reasons`;
- `recommended_action`;
- `machine_readable_flags.flag_codes`.

Business impact:

"Instead of letting a risky invoice move forward, the process holds posting and creates a human approval step."

## 2:55-3:35 - UiPath Orchestration

Show:

- `uipath/maestro-bpmn-notes.md`;
- `uipath/studio-web-setup.md`;
- `uipath/api-workflow-contract.md`.

Narration:

"In UiPath, the API Workflow sends the invoice JSON and receives the triage response. Maestro uses a decision gateway: AUTO_APPROVE goes to ERP posting, REVIEW_REQUIRED goes to AP analyst review, and ESCALATE_TO_HUMAN creates an Action Center approval task."

## 3:35-4:05 - Audit And Exception Handling

Show:

- `reports/risky_invoice_audit.json`;
- `data/expected_outputs/multiple_high_risk_flags_invoice_audit.json`.

Narration:

"Each decision includes plain-English reasons, a recommended action, an audit summary, machine-readable flags, and a rule version. Technical failures, such as invalid JSON or API timeouts, go to a separate exception lane and do not auto-approve invoices."

## 4:05-4:30 - Codex Evidence And Submission Fit

Show:

- `docs/codex-evidence/codex-usage.md`;
- `docs/submission-checklist.md`.

Narration:

"OpenAI Codex helped scaffold and harden the implementation, tests, OpenAPI contract, UiPath docs, and demo materials. The output is integrated into a working project, not just documentation."

## Troubleshooting

If `python` is not found:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If `pytest` is not found:

```bash
python -m pip install -e ".[dev]"
```

If `python -m invoice_agent` cannot import the package:

```bash
python -m pip install -e ".[dev]"
```

If the API does not start:

```bash
python -m pip install -e ".[api,dev]"
uvicorn invoice_agent.api:app --host 127.0.0.1 --port 8000
```

If UiPath Automation Cloud cannot reach `127.0.0.1`, expose the service through an approved HTTPS endpoint or demo tunnel and update the API Workflow URL.
