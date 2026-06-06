# Presentation Deck Outline

Final deck: `submission/deck/invoice-exception-triage-agent.pptx`

Template source: official UiPath AgentHack Google Slides template, downloaded as `submission/template-review/uipath-agenthack-template.pptx`.

The final deck uses the official 7-slide template structure. The earlier self-made 8-slide deck was replaced to match organizer feedback.

## Slide 1: Cover

- Project title: Invoice Exception Triage Agent
- UiPath AgentHack 2026 submission

## Slide 2: Team / Project

- Individual submission by Arthur Weng
- Coded agent: Python rules, CLI, API
- UiPath layer: Studio Web and Maestro notes
- Codex evidence: OpenAI Codex assisted build

## Slide 3: Problem Statement And Proposed Solution

- Problem: AP teams manually check duplicates, suppliers, POs, tax IDs, currency, amounts, and terms.
- Impact: clean invoices wait; risky invoices need controlled escalation.
- Solution: deterministic coded agent returns risk, decision, reasons, audit summary, and flags.
- UiPath: API Workflow calls the agent; Maestro routes the case.

## Slide 4: Benefits And Technologies Used

- End users: AP analyst and AP manager.
- Department: Finance / AP / Procure-to-Pay.
- UiPath products: Studio Web, Maestro, Action Center, Automation Cloud.
- Other technologies: Python, FastAPI, pytest, OpenAPI, Codex.
- Benefits: auto-approve clean invoices, review medium exceptions, escalate high-risk exceptions, preserve audit evidence.

## Slide 5: Solution Architecture

1. Invoice JSON intake.
2. UiPath API Workflow calls `POST /triage/invoice`.
3. Python coded agent evaluates deterministic risk rules.
4. Response returns `AUTO_APPROVE`, `REVIEW_REQUIRED`, or `ESCALATE_TO_HUMAN`.
5. Maestro gateway routes to ERP posting, AP review, or Action Center approval.
6. Audit report and case log are preserved.

## Slide 6: Demo Evidence And Submission Assets

- `35 passed` test result.
- Seven sample invoices covering `LOW`, `MEDIUM`, and `HIGH`.
- CLI audit report generation.
- FastAPI wrapper and OpenAPI contract.
- UiPath Studio Web debug evidence.
- Step-by-step README.
- Codex evidence.

## Slide 7: Closing

- Coded agent decisions.
- UiPath governed orchestration.
- Human accountability for invoice exceptions.
