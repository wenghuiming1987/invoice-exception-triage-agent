# Maestro BPMN Notes

## Process Name

Invoice Exception Triage

## BPMN-Style Flow

```text
Start
  -> Receive invoice
  -> Call triage API
  -> Decision gateway
      -> AUTO_APPROVE branch
          -> Post invoice or schedule payment
          -> Write audit report / persist triage response
          -> End
      -> REVIEW_REQUIRED branch
          -> AP analyst review
          -> Analyst approves, rejects, or requests correction
          -> Write audit report / persist triage response
          -> End
      -> ESCALATE_TO_HUMAN branch
          -> Create Action Center approval task
          -> Manager approves, rejects, or requests correction
          -> Write audit report / persist triage response
          -> End
      -> Technical exception branch
          -> Operations support review
          -> End
```

## Stage Details

| Stage | BPMN shape | Responsibility |
| --- | --- | --- |
| Start | Start event | New invoice case starts. |
| Receive invoice | Task | Invoice JSON is received from queue, ERP, email/document workflow, or test payload. |
| Call triage API | Service/API task | Starts the UiPath API Workflow and waits for `triageResponse`. |
| Decision gateway | Exclusive gateway | Branches on `triageResponse.decision`. |
| Auto approve | Task | Clean invoices continue to posting or payment scheduling. |
| Review required | User task | AP analyst reviews medium-risk exceptions. |
| Human escalation | Action Center task | Manager/controller handles high-risk exceptions. |
| Audit report | Task | Persist decision, reasons, flags, and rule version. |
| End | End event | Case completes or exits through technical exception handling. |

## Gateway Conditions

```text
triageResponse.decision == "AUTO_APPROVE"
triageResponse.decision == "REVIEW_REQUIRED"
triageResponse.decision == "ESCALATE_TO_HUMAN"
```

Technical exception branch:

```text
apiStatusCode != 200 OR triageResponse is null OR triageResponse.decision is empty
```

## Branch Behavior

| Decision | Owner | Next action | Why |
| --- | --- | --- | --- |
| `AUTO_APPROVE` | Robot / automation | Post invoice or schedule payment. | No risk flags found. |
| `REVIEW_REQUIRED` | AP analyst | Review flagged fields and decide whether to correct or approve. | Medium-risk issue needs targeted review. |
| `ESCALATE_TO_HUMAN` | AP manager / controller | Hold posting and complete Action Center approval. | High-risk issue needs human accountability. |

## Human-In-The-Loop Task Content

For Action Center, show:

- invoice ID;
- supplier name and supplier ID;
- PO ID;
- invoice amount and currency;
- risk level;
- decision;
- reasons;
- recommended action;
- audit summary;
- `machine_readable_flags.flag_codes`;
- `machine_readable_flags.rule_version`.

Recommended outcomes:

- Approve exception and continue;
- Reject invoice;
- Request supplier/AP correction;
- Send to fraud/compliance review if policy requires it.

## Audit Data To Persist

Persist the full `triageResponse` as case data. At minimum:

```text
decision
risk_level
reasons
recommended_action
audit_summary
machine_readable_flags.flag_codes
machine_readable_flags.severity_counts
machine_readable_flags.rule_version
```

## Demo Note

If the UiPath tenant flow has not been built yet, present this file as the reproducible BPMN design and do not claim a live Automation Cloud deployment.

