# Submission Remediation Notes

Date: 2026-06-07

Purpose: track the changes made after organizer feedback on the Devpost submission.

## Feedback Received

The organizer feedback identified three submission-readiness gaps:

1. `README.md` needed detailed, step-by-step setup instructions.
2. The presentation deck needed to use the official UiPath AgentHack Google Slides template.
3. The YouTube demo video needed to show the project functioning on the target device/environment, not only explain the concept.

## Repository Remediation

### README

Status: completed.

Changes:

- Added detailed judge setup instructions.
- Added prerequisite checks.
- Added clone/open, virtual environment, install, test, CLI, API, and UiPath reproduction steps.
- Added expected clean and high-risk decision outputs.
- Clarified local API and UiPath Automation Cloud connectivity requirements.
- Clarified that Maestro / Action Center are documented setup paths unless separately deployed.

### Deck

Status: completed locally.

Official template source:

- `submission/template-review/uipath-agenthack-template.pptx`

Final deck:

- `submission/deck/invoice-exception-triage-agent.pptx`

Notes:

- Replaced the earlier self-made 8-slide deck with a 7-slide official-template deck.
- Removed placeholder text such as `Jane Doe`, `Lorem Ipsum`, and `Presentation title goes here`.
- Added a rendered contact sheet at `submission/deck/contact-sheet.png`.

### Demo Video

Status: local video regenerated; external YouTube link must be checked after any new upload.

Changes:

- Updated `docs/demo-script.md` to require real working evidence:
  - local terminal;
  - tests passing;
  - clean invoice auto-approved;
  - risky invoice escalated to human;
  - generated audit report;
  - API or UiPath Studio Web response;
  - Maestro / Action Center branch;
  - Codex evidence.
- Regenerated `submission/demo/invoice-exception-triage-agent-demo.mp4` to show terminal/API/UiPath evidence.
- Added `submission/demo/live-demo-evidence.md`.

## External Submission Items To Verify

- Devpost repository link: `https://github.com/wenghuiming1987/invoice-exception-triage-agent`
- Devpost project page: `https://devpost.com/software/invoice-exception-triage-agent`
- Deck link should point to the GitHub path for `submission/deck/invoice-exception-triage-agent.pptx`.
- YouTube link should point to a video that shows the project working, not only a concept walkthrough.

## Verification Commands

```bash
source .venv/bin/activate
python -m pytest
mkdir -p reports
python -m invoice_agent --invoice data/sample_invoices/clean_invoice.json --output reports/clean_invoice_audit.json
python -m invoice_agent --invoice data/sample_invoices/multiple_high_risk_flags_invoice.json --output reports/risky_invoice_audit.json
```
