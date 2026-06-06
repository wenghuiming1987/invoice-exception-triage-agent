# Final Submission Runbook

## Local Verification

```bash
cd "/Volumes/Untitled 1/比赛项目/invoice-exception-triage-agent"
source .venv/bin/activate
python -m pytest
mkdir -p reports
python -m invoice_agent --invoice data/sample_invoices/clean_invoice.json --output reports/clean_invoice_audit.json
python -m invoice_agent --invoice data/sample_invoices/multiple_high_risk_flags_invoice.json --output reports/risky_invoice_audit.json
```

Expected:

- `35 passed`
- clean invoice: `AUTO_APPROVE`
- risky invoice: `ESCALATE_TO_HUMAN`

## Demo Video

- [x] Local demo video generated: `submission/demo/invoice-exception-triage-agent-demo.mp4`
- [x] Duration verified under 5 minutes: about 2 minutes 6 seconds.
- [x] Regenerated video shows functioning terminal/API/UiPath evidence after organizer feedback.
- [x] Narration source saved: `submission/demo/demo-narration.json`
- [x] YouTube upload metadata prepared: `submission/demo/youtube-upload-metadata.md`
- [x] Previously uploaded to YouTube as unlisted: https://youtu.be/3wf-Y2KLSe4
- [ ] Confirm the published YouTube link has been replaced with the regenerated working demo video if a new upload is required.
- [ ] Confirm the updated video link is saved on Devpost after any new upload.

## GitHub

- [x] Initialize git repository.
- [x] Commit all submission files.
- [x] Create public GitHub repository: https://github.com/wenghuiming1987/invoice-exception-triage-agent
- [x] Push default branch.
- [x] Confirm public GitHub repository is visible.
- [x] Add GitHub URL to Devpost.

## UiPath

- [x] Start coded agent API.
- [x] Expose API through HTTPS.
- [x] Create Studio Web API Workflow.
- [ ] Test clean invoice.
- [x] Test high-risk invoice.
- [ ] Add Maestro BPMN flow if tenant supports it.
- [ ] Add Action Center task if tenant supports it.
- [x] Capture screenshots.

## Devpost

- [x] Create draft project page.
- [x] Submit project: https://devpost.com/software/invoice-exception-triage-agent
- [x] Add title and tagline.
- [x] Paste project story based on `submission/devpost-project-copy.md`.
- [x] Add public GitHub repository.
- [x] Add published demo video link.
- [ ] Re-check published demo video link after regenerated video upload.
- [x] Add screenshots.
- [x] Add presentation deck link.
- [ ] Re-check deck link after pushing official-template deck replacement.
- [x] Add Codex evidence note in project story.
- [x] Fill additional info and reach final submit page.
- [x] Final review with user.
- [x] User confirms final submit.
