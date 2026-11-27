# Selected Software Projects

## Run the payroll reconciliation demo

Run this command from the repository root with Python 3:

```sh
python reconcile_payroll.py -o reconciliation.csv
```

The script loads two synthetic CSV exports into SQLite and runs [the reconciliation query](payroll_reconciliation.sql). It uses company, period, employee ID, and pay code as a composite key. Money is compared in integer cents so the calculation does not depend on floating-point rounding.

The example produces three rows: a value mismatch of -24.99, a missing record for 120.50, and an unexpected record for 85.00. Matching records are excluded. To use your own inputs, run `python reconcile_payroll.py expected.csv actual.csv -o reconciliation.csv`. The CSVs must follow the headers in [sample_expected.csv](sample_expected.csv), with dot-decimal amounts and one row per key.


I’m Rafael Nobre, based in São Paulo, Brazil. This portfolio covers collaborative projects and hands-on work in web development, integrations, Python automation, and reporting.

## Full-stack applications and integrations

- **[ContabilX](https://github.com/suporter2one-arch/ContabilxDev)** — Collaborative ERP development with Next.js, TypeScript, React, and Firebase. Access is scoped by company membership. Journal writes are blocked after an accounting period closes. The linked repository is the public development version.
- **S.N. Automator** — Dashboard and API for scheduled business workflows. Browser tasks run through Playwright, and Windows workflows use Python workers. Dispatching the jobs separately lets users track progress without keeping the original web request open.
- **WhatsApp Case Updates Bot** — Node.js service that polls a court-data API and forwards updates to subscribed WhatsApp groups. SQLite stores local state and an Express dashboard provides a read-only view of recent activity.
- **R2 One Website** — Collaborative portfolio site for a two-person digital services team, with a project gallery and contact flows.

## Python automation and data tools

- **Payroll Close Automation** — Matches payroll exports to review templates by company, location, and pay-item code. Updates designated cells while preserving formulas and flags mismatches or missing records for review.
- **Vacation Pay and Schedule Validation** — Cross-checks scheduled leave, payment records, and credit dates, then organizes the output by company.
- **FGTS Statement Processing** — Splits Brazilian employment fund statements and extracts deposit records for reconciliation by company and reporting period.
- **PDF Report to Excel** — Converts structured, text-based reports to Excel while retaining the columns and headings used for downstream checks.
- **Service Request and SLA Reporting** — Uses SQL and Python to report volumes by priority and calculate turnaround within working windows, including requests that cross lunch or the end of the day.
- **XML Invoice Analytics** — Power BI report with period and company filters, transaction-code analysis, company rankings, and trend views.

Client-facing work is described here through its workflow and design choices. The portfolio uses sample data for any public demonstrations.

[LinkedIn](https://www.linkedin.com/in/rafael-nobre-a4882a345/)
