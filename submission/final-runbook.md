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
- [x] Duration verified under 5 minutes: about 2 minutes 17 seconds.
- [x] Narration source saved: `submission/demo/demo-narration.json`
- [ ] Upload video to YouTube, Vimeo, or Youku and use that link in Devpost.

## GitHub

- [x] Initialize git repository.
- [x] Commit all submission files.
- [x] Create public GitHub repository: https://github.com/wenghuiming1987/invoice-exception-triage-agent
- [x] Push default branch.
- [x] Confirm public GitHub repository is visible.
- [ ] Add GitHub URL to Devpost.

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

- [ ] Create project page.
- [ ] Add title and tagline.
- [ ] Paste project copy from `submission/devpost-project-copy.md`.
- [ ] Add public GitHub repository.
- [ ] Add published demo video link after uploading `submission/demo/invoice-exception-triage-agent-demo.mp4`.
- [ ] Add screenshots.
- [ ] Add presentation deck link.
- [ ] Add license note.
- [ ] Add Codex evidence note.
- [ ] Final review with user.
- [ ] User confirms final submit.
