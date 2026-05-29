# UiPath Setup Status

Update this file as the real UiPath setup progresses.

## Current Target

Minimum strong submission target:

- [x] Real UiPath Studio Web API Workflow calls the coded agent HTTPS endpoint.
- [x] Public HTTPS endpoint tested from local machine.
- [x] Clean invoice returns `AUTO_APPROVE` from local API.
- [x] Risky invoice returns `ESCALATE_TO_HUMAN` from public HTTPS endpoint.
- [x] Screenshot captured.

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
https://bf5b9a90a3340d.lhr.life/triage/invoice
```

Note: this is a temporary localhost.run tunnel and only remains valid while the local `uvicorn` and SSH tunnel sessions are running.

## Tenant Notes

- UiPath account: `authur`
- Tenant / folder: default Studio Web workspace observed in Automation Cloud.
- Studio Web API Workflow name: `API Workflow`
- Maestro process name: `Invoice Exception Triage`

## Verified Studio Web Debug Result

- Date/time: 2026-05-30 Asia/Shanghai
- Result: UiPath Studio Web API Workflow debug completed with HTTP Request `Successful`.
- Status code: `200`
- Returned decision: `ESCALATE_TO_HUMAN`
- Returned risk level: `HIGH`
- Evidence screenshot: `submission/screenshots/07-uipath-debug-success.png`
