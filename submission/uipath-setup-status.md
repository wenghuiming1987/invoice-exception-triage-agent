# UiPath Setup Status

Update this file as the real UiPath setup progresses.

## Current Target

Minimum strong submission target:

- [ ] Real UiPath Studio Web API Workflow calls the coded agent HTTPS endpoint.
- [x] Public HTTPS endpoint tested from local machine.
- [x] Clean invoice returns `AUTO_APPROVE` from local API.
- [x] Risky invoice returns `ESCALATE_TO_HUMAN` from public HTTPS endpoint.
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
https://53962868a6f7eb.lhr.life/triage/invoice
```

Note: this is a temporary localhost.run tunnel and only remains valid while the local `uvicorn` and SSH tunnel sessions are running.

## Tenant Notes

- UiPath account: TODO
- Tenant / folder: TODO
- Studio Web API Workflow name: `Invoice Triage API`
- Maestro process name: `Invoice Exception Triage`
