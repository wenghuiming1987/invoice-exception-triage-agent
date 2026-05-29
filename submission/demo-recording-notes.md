# Demo Recording Notes

## Recording Goal

Keep the video under 5 minutes and show a real working path:

1. tests pass;
2. clean invoice auto-approved;
3. risky invoice escalated to human;
4. audit report generated;
5. UiPath orchestration path explained;
6. Codex evidence shown.

## Commands To Keep Ready

```bash
source .venv/bin/activate
python -m pytest
mkdir -p reports
python -m invoice_agent --invoice data/sample_invoices/clean_invoice.json --output reports/clean_invoice_audit.json
python -m invoice_agent --invoice data/sample_invoices/multiple_high_risk_flags_invoice.json --output reports/risky_invoice_audit.json
```

## Files To Show

- `README.md`
- `reports/clean_invoice_audit.json`
- `reports/risky_invoice_audit.json`
- `uipath/maestro-bpmn-notes.md`
- `uipath/api-workflow-contract.md`
- `docs/codex-evidence/codex-usage.md`
- `docs/submission-checklist.md`

