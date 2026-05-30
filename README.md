# Invoice Exception Triage Agent

Invoice Exception Triage Agent is a working UiPath AgentHack 2026 prototype for accounts-payable invoice exception triage.

It combines:

- a **Python coded agent** that makes deterministic invoice risk decisions;
- **UiPath low-code orchestration design** for API Workflow, Maestro BPMN, Action Center, and Automation Cloud governance.

The repository is runnable locally. It includes source code, tests, sample invoices, mock ERP data, expected audit outputs, an OpenAPI contract, UiPath setup notes, a short demo script, and a prepared local demo video asset under `submission/demo/`.

## 3-Minute Judge Path

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest
python -m invoice_agent --invoice data/sample_invoices/clean_invoice.json --output reports/clean_invoice_audit.json
python -m invoice_agent --invoice data/sample_invoices/multiple_high_risk_flags_invoice.json --output reports/risky_invoice_audit.json
```

Expected outcomes:

- clean invoice: `LOW` risk, `AUTO_APPROVE`;
- risky invoice: `HIGH` risk, `ESCALATE_TO_HUMAN`;
- audit reports written under `reports/`.

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

## Setup

Use Python 3.11 or newer.

1. Create a virtual environment:

```bash
python3 -m venv .venv
```

2. Activate it:

```bash
source .venv/bin/activate
```

3. Install the project with test dependencies:

```bash
python -m pip install -e ".[dev]"
```

4. Optional: install API server dependencies:

```bash
python -m pip install -e ".[api,dev]"
```

If your environment already maps `python` to Python 3.11+, `python -m venv .venv` also works.

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

Prepared local video: `submission/demo/invoice-exception-triage-agent-demo.mp4` (about 2 minutes 17 seconds).

Published demo video: https://youtu.be/3wf-Y2KLSe4

The fastest live demo:

1. Run tests.
2. Run the clean invoice CLI command and show `AUTO_APPROVE`.
3. Run the risky invoice CLI command and show `ESCALATE_TO_HUMAN`.
4. Open the generated audit report.
5. Show the UiPath BPMN notes and API contract.
6. Show Codex evidence.

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
