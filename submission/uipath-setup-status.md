# UiPath Setup Status

Update this file as the real UiPath setup progresses.

## Current Target

Minimum strong submission target:

- [ ] Real UiPath Studio Web API Workflow calls the coded agent HTTPS endpoint.
- [ ] Clean invoice returns `AUTO_APPROVE`.
- [ ] Risky invoice returns `ESCALATE_TO_HUMAN`.
- [ ] Screenshot captured.

Enhanced target:

- [ ] Maestro BPMN process created.
- [ ] Gateway branches on `triageResponse.decision`.
- [ ] Action Center task created for `ESCALATE_TO_HUMAN`.
- [ ] Screenshots captured.

## Endpoint

Local endpoint:

```text
http://127.0.0.1:8000/triage/invoice
```

Public HTTPS endpoint:

```text
TODO
```

## Tenant Notes

- UiPath account: TODO
- Tenant / folder: TODO
- Studio Web API Workflow name: `Invoice Triage API`
- Maestro process name: `Invoice Exception Triage`

