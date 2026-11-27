# Workflow automation case studies

These case studies describe work on document processing, spreadsheet automation, auditing, and operational reporting. The public implementations use fictional examples and generic field names. Project notes describe the behavior and validation status of the underlying workflows.

## Run the synthetic workflow demo

    python workflow_demo.py

The first example uses split weekday windows. A request opened on Friday at 16:30 and completed on Monday at 09:15 consumes 105 working minutes. The second example fills a review template from a reference export, flags a missing row separately from a matched zero, and rejects duplicate keys. The examples run locally with the Python standard library.

## Leave Operations Workflow

A modular Python workflow with desktop and command-line interfaces. It validates leave schedules, organizes company and batch folders, and hands off completed outputs for review. A dry-run mode is useful when rename and validation rules change together. The modular distribution was retained to make debugging and maintenance easier. Portal integration requires environment-specific validation. This case study shows the offline workflow and its file handoffs.

## Statutory Contributions and Monthly Adjustment Workbook Automation

The reference report is authoritative for each company, location, and pay item. The workflow extracts scoped totals and writes them to designated template cells. It preserves formulas and distinguishes missing records from real zeroes. Similar monthly adjustment workflows populate selected columns for review. The public demo illustrates the lookup and audit status in memory.

## Net Pay and Bank Batch Reconciliation

Net pay and outbound payment exports can agree at the aggregate level while including different records. This workflow compares payment populations and reports differences by payment key. It complements [the public reconciliation demo](reconcile_payroll.py), which detects missing rows, unexpected rows, and amount differences using Python and SQLite.

## Payroll Deduction Reconciliation

A spreadsheet validation workflow for reconciling deductions across regular payroll and vacation payments. It aligns inputs by pay period, produces a difference report, and leaves ambiguous rules for review. Its scope is data reconciliation and traceability.

## Employment Fund Statement Reconciliation

Compares detailed, termination-purpose, and summary statement totals. The workflow separates PDF files, extracts structured amounts, and highlights discrepancies. Scanned statements take a separate OCR path when text extraction is unavailable.

## Tax Receipt PDF Text Extraction

A Python CLI extracts searchable PDF text in page order and writes UTF-8 output for downstream processing. Empty extraction is reported explicitly to route scanned documents to OCR. The related structured payroll PDF converter preserves headings and columns when producing Excel output.

## Workforce Lifecycle Reporting

SQL reports count hires, leave starts, and departures by month. Departure date and payment date are modeled separately so follow-up payments can fall in a different reporting period. The monthly counts and the exploratory classification of follow-up payments are separate pieces of work.

## Payroll Event and Pay Item Audit Queries

Read-only SQL reporting for comparing payroll exports with submission and processing records. The patterns include parameterized period filters, pay-item lookups, and distinguishing the latest event from the latest successful event. Queries under review can be treated as diagnostics until independently validated.

## Service Request SLA Reporting

Reporting by request priority, stage, and month with turnaround measured in working windows. The public demonstration applies a weekday schedule with a lunch break and shows how weekend gaps are excluded. It is deliberately independent of any request-management system.

## XML Invoice Analytics

A Power BI reporting project with company, period, and transaction-code filters, summary metrics, rankings, and trends. This case study describes the reporting design. Company-level data and dashboard exports stay private.

## Archived Market Simulation Experiments

Two historical paper-trading prototypes explored how to record simulated observations and maintain a journal for separate asset scenarios. This entry documents the experiment design and state tracking. It makes no claims about investment results.
