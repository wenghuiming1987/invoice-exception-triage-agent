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

- `30 passed`
- clean invoice: `AUTO_APPROVE`
- risky invoice: `ESCALATE_TO_HUMAN`

## GitHub

- [ ] Initialize git repository.
- [ ] Commit all submission files.
- [ ] Create public GitHub repository.
- [ ] Push default branch.
- [ ] Confirm README renders correctly.
- [ ] Add GitHub URL to Devpost.

## UiPath

- [ ] Start coded agent API.
- [ ] Expose API through HTTPS.
- [ ] Create Studio Web API Workflow.
- [ ] Test clean invoice.
- [ ] Test high-risk invoice.
- [ ] Add Maestro BPMN flow if tenant supports it.
- [ ] Add Action Center task if tenant supports it.
- [ ] Capture screenshots.

## Devpost

- [ ] Create project page.
- [ ] Add title and tagline.
- [ ] Paste project copy from `submission/devpost-project-copy.md`.
- [ ] Add public GitHub repository.
- [ ] Add demo video.
- [ ] Add screenshots.
- [ ] Add license note.
- [ ] Add Codex evidence note.
- [ ] Final review with user.
- [ ] User confirms final submit.

