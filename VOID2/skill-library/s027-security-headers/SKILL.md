---
name: s027-security-headers
description: Offline workflow checklist for security headers; tool availability must be verified.
---
# security headers

Category: Web. Operator: void.
Status: authored workflow; not installed or runtime-verified.

## Inputs
Explicit scope, supplied artifacts, relevant versions, and acceptance criteria.

## Procedure
1. Read AGENTS.md and scope.yaml. Confirm approved artifact roots.
2. Inventory relevant inputs and record hashes; identify available analysis tools.
3. Define a testable question specifically for security headers.
4. Inspect offline evidence; separate observed facts from hypotheses.
5. Design positive and negative checks. Execute only benign approved local tests.
6. Record results, limitations, confidence, and remediation if supported by evidence.
7. Produce a report with evidence IDs using templates/REPORT.md.

## Gates
No sample execution, installation, network activity, privilege changes, or scope
expansion without approval and verified containment. Do not guess command syntax.
This is a workflow scaffold, not an implementation of a specialized security engine.

## Acceptance
A reviewer can trace each conclusion to supplied evidence. Missing tools and checks
are explicitly recorded. No claim that this skill is installed or verified.
