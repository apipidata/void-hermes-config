# Evidence-first inventory

Artifacts considered: 2

## Seven-phase status
1. Scope: explicit input root and seeds.
2. Recon: offline metadata and hashes recorded.
3. Analysis: file signatures only; no vulnerability assertion.
4. Test design: not performed.
5. Validation: inventory only; no samples executed.
6. Remediation: not assessed.
7. Report: this report and evidence.json.

## Evidence

- E0001: "start.md"; observed; SHA-256: d93bfaddef5bd9d86fd381eefbea369145eb5d8ef2647c2a6ef7f729831ee941
- E0002: "notes.txt"; observed; SHA-256: ff438799170b5bc8045deacaa0fc7d15b7146c288062c1caf0409100bcdbe1e0

## Limitations
Not a vulnerability scanner.
Metadata and hashes only; no exploitability conclusion.
Use immutable inputs in an isolated VM; this script is not an OS sandbox.
