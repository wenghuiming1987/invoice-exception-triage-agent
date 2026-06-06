# Demo Script

Target length: 4 minutes 15 seconds. Keep the final YouTube video under 5 minutes.

Local demo video asset: `submission/demo/invoice-exception-triage-agent-demo.mp4`.

Published demo video: https://youtu.be/3wf-Y2KLSe4

## Recording Standard

The video must show the project functioning on the device/environment used for the demo. Do not record a concept-only slide walkthrough.

Show these live or screen-recorded elements:

- local terminal in the repository root;
- Python environment and tests passing;
- CLI processing a clean invoice and a high-risk invoice;
- generated audit report file;
- API or UiPath Studio Web debug response;
- UiPath BPMN / Action Center branch notes;
- Codex evidence and official template deck.

## Short Live Demo Path

Use this path if recording quickly:

1. Show the repository root and README setup section.
2. Run `python -m pytest`.
3. Run clean invoice -> show `AUTO_APPROVE`.
4. Run risky invoice -> show `ESCALATE_TO_HUMAN`.
5. Open generated audit report.
6. Show UiPath Studio Web debug output or the API response schema.
7. Show Maestro branching and human-in-the-loop note.
8. Show Codex evidence.

## 0:00-0:25 - Problem And Environment

Narration:

"This is Invoice Exception Triage Agent, a UiPath AgentHack prototype running locally on this machine with Python, a FastAPI-compatible coded agent, and UiPath orchestration documentation. The business problem is accounts payable exception triage: clean invoices should move automatically, while risky invoices need human accountability before ERP posting or payment."

Show:

- repository root;
- `README.md` setup section;
- `data/sample_invoices/`.

## 0:25-0:55 - Solution Architecture

Narration:

"The solution combines a Python coded agent with UiPath low-code orchestration. The coded agent returns deterministic risk, decision, reasons, recommended action, audit summary, and machine-readable flags. UiPath API Workflow calls the endpoint, and Maestro branches the process."

Show:

- `src/invoice_agent/decision_engine.py`;
- `openapi/invoice-triage-api.yaml`;
- `uipath/api-workflow-contract.md`.

## 0:55-1:20 - Tests Passing

Run:

```bash
source .venv/bin/activate
python -m pytest
```

Narration:

"The test suite verifies business rules, input validation, deterministic audit output, API compatibility, and sample coverage for LOW, MEDIUM, and HIGH decisions."

Expected:

```text
35 passed
```

## 1:20-1:55 - Clean Invoice Auto-Approved

Run:

```bash
mkdir -p reports
python -m invoice_agent \
  --invoice data/sample_invoices/clean_invoice.json \
  --output reports/clean_invoice_audit.json
```

Narration:

"This invoice matches approved supplier and purchase order data. There are no duplicate, tax, amount, payment-term, currency, or PO flags. The agent returns LOW risk and AUTO_APPROVE."

Show:

- terminal output containing `"risk_level": "LOW"`;
- terminal output containing `"decision": "AUTO_APPROVE"`;
- `reports/clean_invoice_audit.json`.

## 1:55-2:40 - Risky Invoice Escalated To Human

Run:

```bash
python -m invoice_agent \
  --invoice data/sample_invoices/multiple_high_risk_flags_invoice.json \
  --output reports/risky_invoice_audit.json
```

Narration:

"This invoice has multiple exception indicators: duplicate invoice ID, missing tax ID, unapproved supplier, missing PO, invoice amount over PO amount, and invalid payment terms. The agent returns HIGH risk and ESCALATE_TO_HUMAN."

Show:

- `reasons`;
- `recommended_action`;
- `machine_readable_flags.flag_codes`;
- `reports/risky_invoice_audit.json`.

Business impact:

"Instead of letting a risky invoice move forward, UiPath can hold posting and create a human approval step."

## 2:40-3:20 - UiPath Orchestration And Human-In-The-Loop

Show:

- `submission/screenshots/07-uipath-debug-success.png`;
- `uipath/studio-web-setup.md`;
- `uipath/maestro-bpmn-notes.md`;
- `uipath/api-workflow-contract.md`.

Narration:

"In UiPath Studio Web, the API Workflow sends invoice JSON to `/triage/invoice` and receives a structured response. Maestro uses an exclusive gateway: AUTO_APPROVE continues to posting, REVIEW_REQUIRED routes to AP analyst review, and ESCALATE_TO_HUMAN creates an Action Center approval task. Technical failures go to a separate exception lane and never auto-approve."

## 3:20-3:50 - Audit And Exception Handling

Show:

- `reports/risky_invoice_audit.json`;
- `data/expected_outputs/multiple_high_risk_flags_invoice_audit.json`;
- `openapi/invoice-triage-api.yaml`.

Narration:

"The output is audit-ready: plain-English reasons for reviewers, deterministic flags for UiPath branching, and a stable rule version for governance. The expected outputs are stored in the repository and reproduced by tests."

## 3:50-4:15 - Submission Fit And Codex Evidence

Show:

- official-template deck file under `submission/deck/`;
- `docs/codex-evidence/codex-usage.md`;
- `docs/submission-checklist.md`.

Narration:

"This is a coded agent plus UiPath orchestration prototype. OpenAI Codex helped create and harden the code, tests, OpenAPI contract, UiPath docs, and demo materials. The Codex output is integrated into the working project, not separate from it."

## Troubleshooting

If `python` points to the wrong interpreter or dependencies are missing:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[api,dev]"
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

If the video is rejected as concept-only, re-record using the short live demo path above and show the terminal output, generated audit file, and UiPath/API response.
