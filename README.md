# Invoice Exception Triage Agent

Invoice Exception Triage Agent is a working UiPath AgentHack 2026 prototype for accounts-payable invoice exception triage.

It combines:

- a **Python coded agent** that makes deterministic invoice risk decisions;
- **UiPath low-code orchestration design** for API Workflow, Maestro BPMN, Action Center, and Automation Cloud governance.

The repository is runnable locally. It includes source code, tests, sample invoices, mock ERP data, expected audit outputs, an OpenAPI contract, UiPath setup notes, a short demo script, and a prepared local demo video asset under `submission/demo/`.

## 3-Minute Judge Path

Use this path after cloning the repository and opening a terminal in the project root.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[api,dev]"
python -m pytest
mkdir -p reports
python -m invoice_agent --invoice data/sample_invoices/clean_invoice.json --output reports/clean_invoice_audit.json
python -m invoice_agent --invoice data/sample_invoices/multiple_high_risk_flags_invoice.json --output reports/risky_invoice_audit.json
```

Expected outcomes:

- clean invoice: `LOW` risk, `AUTO_APPROVE`;
- risky invoice: `HIGH` risk, `ESCALATE_TO_HUMAN`;
- audit reports written under `reports/`.

## Detailed Judge Setup Instructions

These steps are written for a judge or reviewer who wants to reproduce the working prototype from a clean checkout.

### 1. Prerequisites

Install or confirm:

- Python 3.11 or newer;
- Git;
- a terminal on macOS, Linux, or Windows WSL;
- optional: UiPath Automation Cloud / Studio Web access if you want to reproduce the low-code orchestration call;
- optional: an HTTPS tunnel or hosted API endpoint if UiPath Automation Cloud must call the local API.

Check Python:

```bash
python3 --version
```

### 2. Clone Or Open The Repository

```bash
git clone https://github.com/wenghuiming1987/invoice-exception-triage-agent.git
cd invoice-exception-triage-agent
```

If you are reviewing a downloaded zip, open a terminal in the extracted `invoice-exception-triage-agent` folder.

### 3. Create The Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

### 4. Install The Prototype

Install the package, test tools, and optional FastAPI server dependencies:

```bash
python -m pip install -e ".[api,dev]"
```

If you only want the CLI and tests, `python -m pip install -e ".[dev]"` is enough.

### 5. Verify The Build

```bash
python -m pytest
```

Expected result:

```text
35 passed
```

### 6. Run The CLI Demo

Generate an auto-approved clean invoice audit report:

```bash
mkdir -p reports
python -m invoice_agent \
  --invoice data/sample_invoices/clean_invoice.json \
  --output reports/clean_invoice_audit.json
```

Expected key fields:

```json
{
  "risk_level": "LOW",
  "decision": "AUTO_APPROVE"
}
```

Generate a high-risk human escalation audit report:

```bash
python -m invoice_agent \
  --invoice data/sample_invoices/multiple_high_risk_flags_invoice.json \
  --output reports/risky_invoice_audit.json
```

Expected key fields:

```json
{
  "risk_level": "HIGH",
  "decision": "ESCALATE_TO_HUMAN"
}
```

Generate reproducible audit reports for every sample invoice:

```bash
mkdir -p reports
for file in data/sample_invoices/*.json; do
  name="$(basename "$file" .json)"
  python -m invoice_agent --invoice "$file" --output "reports/${name}_audit.json"
done
```

### 7. Run The Local API

Start the FastAPI wrapper:

```bash
uvicorn invoice_agent.api:app --host 127.0.0.1 --port 8000
```

In a second terminal with the same virtual environment active:

```bash
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/triage/invoice \
  -H "Content-Type: application/json" \
  -d @data/sample_invoices/amount_exceeds_po_invoice.json
```

The endpoint contract is documented in `openapi/invoice-triage-api.yaml` and `uipath/api-workflow-contract.md`.

### 8. Reproduce The UiPath Call

1. Start the local API or deploy it to an approved HTTPS host.
2. If running locally, expose `127.0.0.1:8000` through an approved HTTPS tunnel so UiPath Automation Cloud can reach it.
3. In UiPath Studio Web, create an API Workflow named `Invoice Triage API`.
4. Add an input argument named `invoicePayload`.
5. Add an HTTP Request step:
   - Method: `POST`
   - URL: `https://<your-host>/triage/invoice`
   - Headers: `Content-Type: application/json`, `Accept: application/json`
   - Body: `JSON.stringify(invoicePayload)`
6. Parse the JSON response into `triageResponse`.
7. In Maestro, branch on `triageResponse.decision`:
   - `AUTO_APPROVE`: continue ERP posting or payment scheduling.
   - `REVIEW_REQUIRED`: route to AP analyst review.
   - `ESCALATE_TO_HUMAN`: create an Action Center approval task and hold posting.
8. Route HTTP failures, malformed payloads, or timeouts to a technical exception lane. Do not auto-approve when the API call fails.

Full UiPath setup notes are in `uipath/studio-web-setup.md`, `uipath/maestro-bpmn-notes.md`, and `uipath/api-workflow-contract.md`.

## Business Problem

AP teams lose time on invoice exceptions that require repetitive checks across supplier master data, purchase orders, duplicate invoice history, tax IDs, currency, and payment terms. Clean invoices should continue automatically, but risky invoices need human accountability before ERP posting or payment.

This prototype solves that gap with a governed workflow:

1. Receive normalized invoice JSON from an AP queue, document extraction step, email workflow, or ERP event.
2. Call a coded triage agent from a UiPath API Workflow.
3. Return a deterministic decision with reasons and machine-readable flags.
4. Let Maestro BPMN route the case to auto-approval, AP analyst review, or human escalation.
5. Preserve the audit summary for governance and later review.

## UiPath Components Used In The Design

This repository does **not** claim that a UiPath tenant workflow is already deployed. It provides a runnable coded agent and practical setup instructions for reproducing the flow in UiPath Automation Cloud.

| UiPath component | How it is used |
| --- | --- |
| UiPath Studio Web / API Workflow | Sends invoice JSON to `/triage/invoice` and returns the structured triage response. |
| UiPath Maestro BPMN | Orchestrates Start -> Receive invoice -> Call triage API -> Decision gateway -> business branch -> audit -> End. |
| UiPath Action Center | Handles `ESCALATE_TO_HUMAN` cases with manager approval or rejection. |
| UiPath Orchestrator / Automation Cloud | Governs process execution, logs, credentials, folders, and operational monitoring. |
| Robots / unattended automations | Optional ERP posting or payment scheduling for `AUTO_APPROVE` cases. |

## Agent Type

- **Coded agent**: implemented in Python under `src/invoice_agent/`.
- **Low-code orchestration**: documented UiPath API Workflow and Maestro BPMN setup under `uipath/`.

The coded agent owns deterministic exception judgment. UiPath owns process orchestration, audit visibility, retries, approvals, and human-in-the-loop routing.

## Triage Rules

The engine evaluates:

- duplicate invoice ID;
- missing supplier tax ID;
- supplier not in approved supplier list;
- invoice amount exceeds PO amount;
- suspicious payment terms;
- currency mismatch;
- missing or unknown PO.

Decision policy:

| Risk level | Decision | Typical route |
| --- | --- | --- |
| `LOW` | `AUTO_APPROVE` | Continue to ERP posting or payment scheduling. |
| `MEDIUM` | `REVIEW_REQUIRED` | Route to AP analyst review. |
| `HIGH` | `ESCALATE_TO_HUMAN` | Hold posting and create human approval task. |

## Sample Data Coverage

| Sample invoice | Expected risk | Expected decision |
| --- | --- | --- |
| `clean_invoice.json` | `LOW` | `AUTO_APPROVE` |
| `missing_tax_id_invoice.json` | `MEDIUM` | `REVIEW_REQUIRED` |
| `duplicate_invoice.json` | `HIGH` | `ESCALATE_TO_HUMAN` |
| `amount_exceeds_po_invoice.json` | `HIGH` | `ESCALATE_TO_HUMAN` |
| `supplier_not_approved_invoice.json` | `HIGH` | `ESCALATE_TO_HUMAN` |
| `currency_mismatch_invoice.json` | `HIGH` | `ESCALATE_TO_HUMAN` |
| `multiple_high_risk_flags_invoice.json` | `HIGH` | `ESCALATE_TO_HUMAN` |

Expected audit outputs are stored in `data/expected_outputs/` and are covered by tests.

## Repository Structure

```text
.
├── data/
│   ├── expected_outputs/
│   ├── mock_erp/
│   └── sample_invoices/
├── docs/
│   ├── architecture.md
│   ├── codex-evidence/
│   ├── demo-script.md
│   └── submission-checklist.md
├── openapi/
│   └── invoice-triage-api.yaml
├── src/
│   └── invoice_agent/
├── tests/
└── uipath/
```

## Run Tests

```bash
python -m pytest
```

The tests cover rule behavior, input validation, decision outcomes, deterministic audit output, and sample data coverage for `LOW`, `MEDIUM`, and `HIGH`.

## CLI Demo

Create a report directory:

```bash
mkdir -p reports
```

Clean invoice:

```bash
python -m invoice_agent \
  --invoice data/sample_invoices/clean_invoice.json \
  --output reports/clean_invoice_audit.json
```

High-risk invoice:

```bash
python -m invoice_agent \
  --invoice data/sample_invoices/multiple_high_risk_flags_invoice.json \
  --output reports/risky_invoice_audit.json
```

Generate reproducible reports for all sample invoices:

```bash
mkdir -p reports
for file in data/sample_invoices/*.json; do
  case "$(basename "$file")" in ._*) continue ;; esac
  name="$(basename "$file" .json)"
  python -m invoice_agent --invoice "$file" --output "reports/${name}_audit.json"
done
```

Use a `.md` output extension for a human-readable Markdown report.

## Local API Demo

Install optional API dependencies, then start the service:

```bash
python -m pip install -e ".[api,dev]"
uvicorn invoice_agent.api:app --host 127.0.0.1 --port 8000
```

Call the endpoint:

```bash
curl -s http://127.0.0.1:8000/triage/invoice \
  -H "Content-Type: application/json" \
  -d @data/sample_invoices/amount_exceeds_po_invoice.json
```

OpenAPI contract: `openapi/invoice-triage-api.yaml`.

For UiPath Studio Web HTTP Request activities, use `JSON.stringify(invoicePayload)` as the Body expression. The API accepts both a normal invoice JSON object and this UiPath stringified JSON form.

## UiPath Integration

Practical setup docs:

- `uipath/studio-web-setup.md`: Studio Web / API Workflow checklist.
- `uipath/api-workflow-contract.md`: exact request and response examples.
- `uipath/maestro-bpmn-notes.md`: BPMN-style flow and branch conditions.

Current tenant status: a UiPath Studio Web API Workflow has been configured and debug-tested against a temporary HTTPS tunnel. Maestro and Action Center are documented as reproducible setup steps, not claimed as deployed runtime artifacts.

Recommended Maestro flow:

```text
Start -> Receive invoice -> Call triage API -> Decision gateway
  -> AUTO_APPROVE -> ERP posting/payment step -> Audit report -> End
  -> REVIEW_REQUIRED -> AP analyst review -> Audit report -> End
  -> ESCALATE_TO_HUMAN -> Action Center approval -> Audit report -> End
```

## Demo Video Path

Prepared local demo video: `submission/demo/invoice-exception-triage-agent-demo.mp4` (under 5 minutes).

Published demo video: https://youtu.be/if6iNBls7CM

Submitted Devpost project: https://devpost.com/software/invoice-exception-triage-agent

Official-template presentation deck: `submission/deck/invoice-exception-triage-agent.pptx`.

The video should show the project working, not only describe the idea. The recommended live demo path:

1. Run tests.
2. Run the clean invoice CLI command and show `AUTO_APPROVE`.
3. Run the risky invoice CLI command and show `ESCALATE_TO_HUMAN`.
4. Open the generated audit report.
5. Show the local API response or UiPath Studio Web debug response.
6. Show the UiPath BPMN notes and Action Center branch.
7. Show Codex evidence and the official template deck.

Detailed script: `docs/demo-script.md`.

## Exception Handling

Invalid invoice payloads raise `InvoiceValidationError` in the Python engine. In the FastAPI wrapper, validation errors return HTTP `422`.

In UiPath, non-2xx API responses should go to a technical exception lane. They should not be treated as AP business exceptions and must not auto-approve an invoice.

Business exceptions are encoded in the triage response:

- `AUTO_APPROVE`: no exception indicators.
- `REVIEW_REQUIRED`: limited medium-risk issue, such as missing tax ID.
- `ESCALATE_TO_HUMAN`: high-risk or multi-flag issue requiring human accountability.

## Codex / Coding Agent Usage Evidence

OpenAI Codex was used to scaffold and harden this repository. Evidence is included in:

- `docs/codex-evidence/codex-usage.md`
- `docs/codex-evidence/prompt-log.md`

The Codex-generated output is integrated into the working project through source code, tests, sample data, OpenAPI, UiPath setup docs, and demo materials.

## Limitations

- Mock ERP data is stored in JSON files for demo reproducibility.
- The repository does not include tenant credentials or a deployed UiPath Cloud process.
- Invoice OCR and document extraction are out of scope; input starts as normalized invoice JSON.
- Production hosting, authentication, secret storage, and ERP writeback must be configured by the implementer.
- The model is deterministic and rules-based; it does not use an LLM to make AP approval decisions.

## License

MIT. See `LICENSE`.
