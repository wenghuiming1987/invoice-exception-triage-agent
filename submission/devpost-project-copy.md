# Devpost Project Copy

This is the source text used for the submitted Devpost page.

Submitted Devpost project:

https://devpost.com/software/invoice-exception-triage-agent

## Project Title

Invoice Exception Triage Agent

## Tagline

A UiPath-orchestrated coded agent that triages AP invoice exceptions, auto-approves clean invoices, and escalates risky cases to human approval with a deterministic audit trail.

## Inspiration

Accounts payable teams spend too much time checking routine invoice exceptions across supplier data, purchase orders, duplicate history, tax IDs, payment terms, and currency rules. Clean invoices should not wait in a manual queue, but risky invoices should never be approved without accountability.

## What It Does

Invoice Exception Triage Agent evaluates normalized invoice JSON and returns:

- risk level: `LOW`, `MEDIUM`, or `HIGH`;
- decision: `AUTO_APPROVE`, `REVIEW_REQUIRED`, or `ESCALATE_TO_HUMAN`;
- plain-English reasons;
- recommended action;
- audit summary;
- machine-readable flags for UiPath routing.

UiPath API Workflow calls the coded agent endpoint. Maestro BPMN branches the case:

- `AUTO_APPROVE`: continue to ERP posting or payment scheduling;
- `REVIEW_REQUIRED`: route to AP analyst review;
- `ESCALATE_TO_HUMAN`: create a human-in-the-loop approval task through Action Center.

## How We Built It

- Python coded agent for deterministic invoice validation, risk rules, decisioning, and audit report generation.
- FastAPI wrapper for the `/triage/invoice` endpoint.
- Dependency-light CLI fallback for local demo and reproducible sample outputs.
- Mock ERP reference data for approved suppliers, purchase orders, and processed invoice history.
- Pytest suite covering rules, input validation, decisions, and reproducible audit outputs.
- OpenAPI contract for UiPath API Workflow integration.
- UiPath setup documentation for Studio Web, API Workflow, Maestro BPMN, and Action Center.

## UiPath Components

- UiPath Studio Web / API Workflow
- UiPath Maestro BPMN
- UiPath Action Center
- UiPath Orchestrator / Automation Cloud governance
- Optional unattended robot step for ERP posting or payment scheduling

## Agent Type

Both:

- **Coded agent**: Python decision engine and API service.
- **Low-code orchestration**: UiPath API Workflow and Maestro BPMN.

## Business Impact

The prototype reduces AP queue noise by letting clean invoices move forward automatically while preserving human accountability for risky exceptions. Every decision includes reasons, a recommended action, machine-readable flags, and a rule version for auditability.

## Demo Flow

1. Run tests.
2. Process a clean invoice and show `AUTO_APPROVE`.
3. Process a high-risk invoice and show `ESCALATE_TO_HUMAN`.
4. Open generated audit report.
5. Show API contract and UiPath BPMN branch design.
6. Show Codex evidence.

## Built With

- Python
- FastAPI
- Pytest
- OpenAPI
- UiPath Automation Cloud design
- UiPath Studio Web / API Workflow
- UiPath Maestro
- UiPath Action Center
- OpenAI Codex

## Challenges

The main challenge was keeping the solution demo-ready while avoiding fake deployment claims. The repository separates the fully runnable coded agent and tested UiPath Studio Web API Workflow from the Maestro and Action Center setup notes that explain how to reproduce the broader cloud workflow.

## Accomplishments

- Working deterministic coded agent.
- Sample invoices covering `LOW`, `MEDIUM`, and `HIGH`.
- Reproducible audit outputs.
- Tests passing.
- OpenAPI contract.
- UiPath integration documentation.
- Codex usage evidence.

## What We Learned

Agentic business workflows need both automation and governance. The coded agent can make fast deterministic decisions, while UiPath provides the orchestration, human-in-the-loop controls, and operational visibility needed for an enterprise AP workflow.

## What's Next

- Connect to a real ERP purchase order and supplier master data source.
- Add authentication to the API endpoint.
- Replace sample JSON invoice intake with document extraction output.
- Add dashboard metrics for auto-approval rate, exception reasons, and AP cycle-time savings.
- Expand Action Center forms for manager comments and correction requests.

## Repository

https://github.com/wenghuiming1987/invoice-exception-triage-agent

## Demo Video

Local source file:

`submission/demo/invoice-exception-triage-agent-demo.mp4`

Duration: about 2 minutes 17 seconds.

Devpost-required published video URL:

https://youtu.be/3wf-Y2KLSe4

## Presentation Deck

GitHub deck link:

https://github.com/wenghuiming1987/invoice-exception-triage-agent/blob/main/submission/deck/invoice-exception-triage-agent.pptx
