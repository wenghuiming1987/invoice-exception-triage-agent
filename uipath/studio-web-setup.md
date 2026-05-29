# Studio Web / API Workflow Setup Checklist

This is a practical checklist for configuring the UiPath side of the demo. The repository does not include a deployed UiPath Cloud process or tenant credentials.

## A. Local Coded Agent API

- [ ] Create and activate a Python virtual environment.
- [ ] Install API dependencies:

```bash
python -m pip install -e ".[api,dev]"
```

- [ ] Start the API:

```bash
uvicorn invoice_agent.api:app --host 127.0.0.1 --port 8000
```

- [ ] Test locally:

```bash
curl -s http://127.0.0.1:8000/health
```

Expected:

```json
{
  "status": "ok",
  "service": "invoice-exception-triage-agent"
}
```

- [ ] If UiPath Automation Cloud must call the endpoint, expose the API through an approved HTTPS host or temporary demo tunnel.
- [ ] Record the public or internal endpoint URL for Studio Web.

## B. Create The API Workflow In Studio Web

- [ ] Open UiPath Studio Web.
- [ ] Create a new API Workflow named `Invoice Triage API`.
- [ ] Create input argument:
  - Name: `invoicePayload`
  - Type: object / JSON
  - Required: yes
- [ ] Create output argument:
  - Name: `triageResponse`
  - Type: object / JSON
- [ ] Add an HTTP request step:
  - Method: `POST`
  - URL: `<hosted-base-url>/triage/invoice`
  - Headers:
    - `Content-Type: application/json`
    - `Accept: application/json`
  - Body: `invoicePayload`
- [ ] Parse the response body as JSON.
- [ ] Assign parsed response to `triageResponse`.
- [ ] Return `triageResponse` from the workflow.

## C. Test The API Workflow

Use the clean sample payload from `data/sample_invoices/clean_invoice.json`.

Expected key fields:

```json
{
  "risk_level": "LOW",
  "decision": "AUTO_APPROVE"
}
```

Use the high-risk payload from `data/sample_invoices/multiple_high_risk_flags_invoice.json`.

Expected key fields:

```json
{
  "risk_level": "HIGH",
  "decision": "ESCALATE_TO_HUMAN"
}
```

Use the medium-risk payload from `data/sample_invoices/missing_tax_id_invoice.json`.

Expected key fields:

```json
{
  "risk_level": "MEDIUM",
  "decision": "REVIEW_REQUIRED"
}
```

## D. Publish / Make Available To Maestro

- [ ] Save the API Workflow.
- [ ] Publish or make it available in the target folder according to tenant policy.
- [ ] Confirm the folder has access to required connections, assets, and credentials.
- [ ] Confirm the workflow can be called from a Maestro process.

## E. Connect To Maestro BPMN

- [ ] Add a service/API task after invoice intake.
- [ ] Select the `Invoice Triage API` workflow.
- [ ] Map Maestro case invoice JSON to `invoicePayload`.
- [ ] Store the output in a case variable named `triageResponse`.
- [ ] Add a decision gateway using `triageResponse.decision`.
- [ ] Configure branches:
  - `AUTO_APPROVE`
  - `REVIEW_REQUIRED`
  - `ESCALATE_TO_HUMAN`
- [ ] Add a technical exception path for HTTP failures, malformed payloads, and timeouts.

## F. Human-In-The-Loop Configuration

For `ESCALATE_TO_HUMAN`:

- [ ] Create an Action Center approval task.
- [ ] Show invoice ID, supplier, PO ID, risk level, reasons, recommended action, and audit summary.
- [ ] Require the approver to choose approve, reject, or request correction.
- [ ] Resume the Maestro process after completion.
- [ ] Persist approver action and comments with the triage response.

## G. Governance Checks

- [ ] API base URL is stored outside the workflow code when possible.
- [ ] Authentication token or secret is stored in tenant-approved configuration.
- [ ] Non-2xx responses do not auto-approve invoices.
- [ ] Full `triageResponse` is logged or attached to the case.
- [ ] Demo script does not imply the UiPath flow is deployed unless these steps have actually been completed.

