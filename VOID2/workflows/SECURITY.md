# Specialized research workflows

## Authorization bypass and vulnerability research
Use local synthetic identities with a documented role/resource matrix. Compare expected
and observed access for owner, non-owner, anonymous, and expired-session fixtures.
Evidence includes sanitized request/response, app version, and a negative control.
Do not infer a working exploit from an error or transfer a lab finding to remote targets.
Memory-safety research uses supplied source/crashes and sanitizer output; executing
untrusted samples or exploit payloads requires a separate reviewed containment plan.

## AI red teaming / jailbreak resistance
Use an owned local test endpoint only after explicitly authorizing network/loopback access.
For strictly offline operation, evaluate supplied transcripts rather than calling a model.
Test role spoofing, untrusted-document instructions, synthetic secret disclosure,
tool scope expansion, and output-format reliability. Use harmless canaries and dummy tools.
Record expected result, actual output, model/version, evaluator rubric, false positives,
and inconclusive cases. Do not call a transcript review a live-model test.

## Local farm / automation
Use tools/lab.py as a two-worker inventory queue. Seeds are explicit, duplicate paths
are deduplicated, depth is bounded to three, files to 200, bytes to 1 MiB per file.
There is no account creation, proxy rotation, CAPTCHA solving, or remote task execution.
For browser tests, use a local application and synthetic account fixtures; implementation
requires the application's routes and expected behavior, which are not supplied here.

## GitHub admission
Research URLs in README.md are candidates only. In offline mode do not clone them.
Import approved source snapshots through a separate review process, recording repository,
commit, license, dependency checks, and behavior review. Do not auto-install skill code.
