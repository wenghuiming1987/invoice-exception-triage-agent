# Screenshot Checklist

Save final screenshots under `submission/screenshots/`.

## Required / High-Value Screenshots

- [x] `01-tests-passing.png`: generated evidence image showing `python -m pytest` and `35 passed`.
- [x] `02-clean-auto-approve.png`: generated evidence image showing clean invoice `AUTO_APPROVE`.
- [x] `03-risky-human-escalation.png`: generated evidence image showing risky invoice `ESCALATE_TO_HUMAN`.
- [x] `04-audit-report.png`: generated evidence image with reasons and flags.
- [x] `05-uipath-flow.png`: generated BPMN-style UiPath flow image.
- [x] `07-uipath-debug-success.png`: Studio Web API Workflow debug output showing HTTP `200`, `HIGH`, and `ESCALATE_TO_HUMAN`.
- [ ] `06-uipath-api-workflow.png`: Studio Web API Workflow configuration.
- [ ] `07-uipath-maestro-branching.png`: Maestro BPMN decision gateway or flow view.
- [ ] `08-action-center-task.png`: Action Center human approval task, if available.
- [ ] `09-codex-evidence.png`: Codex evidence document or session export placeholder.
- [x] `06-github-repo.png`: generated evidence image with public GitHub repository URL.

## If Maestro / Action Center Is Not Available

Capture these instead:

- [x] API Workflow test call output from Studio Web.
- [ ] `uipath/maestro-bpmn-notes.md` showing the reproducible BPMN flow.
- [ ] `uipath/studio-web-setup.md` checklist.
