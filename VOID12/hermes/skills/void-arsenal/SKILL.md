---
name: void-arsenal
description: Router and index for the security skill families under void. Offense, defense, detection, reverse engineering, web app hunting, exploit development, LLM adversarial research, farm/automation pipelines. Use to resolve which skill family applies to a request before loading individual skills.
---

# void-arsenal

Index and router over the security side of the skill tree. Purpose: stop a 900-dir inventory from being a coin flip at request time.

## 1. Families

| Family | Scope | Entry skill |
|---|---|---|
| **Offense** | Exploit dev, privesc, C2, lateral movement, AD attack paths | `offensive-exploit-development`, `conducting-full-scope-red-team-engagement` |
| **Defense** | Detection engineering, hardening, incident response, SOC playbooks | `detecting-*` set, `building-soc-playbook-for-ransomware` |
| **Detection / hunting** | Hypothesis-driven hunting, beaconing, persistence, LOLBins | `building-threat-hunt-hypothesis-framework`, `hunting-for-*` set |
| **Reverse engineering** | Static and dynamic analysis, unpacking, control flow, YARA | `reverse-engineering-malware-with-ghidra`, `analyzing-linux-elf-malware` |
| **Web / API** | Injection, auth bypass, SSRF, deserialization, cache, smuggling | `hunt-*` set — start at `hunt-auth-bypass`, `hunt-rce` |
| **Cloud / container** | IAM privesc, k8s RBAC, container escape, credential exposure | `conducting-cloud-penetration-test`, `hunt-k8s` |
| **LLM adversarial** | Injection research, prompt leakage, RAG pipeline testing, red-team harnesses | `red-teaming-llms-with-garak`, `testing-prompt-injection-in-rag-pipelines` |
| **LLM defense** | Guardrails, input/output validation, injection detection | `defending-llms-with-guardrails`, `implementing-llm-guardrails-for-security` |
| **Automation / farm** | Browser orchestration, session flows, solver integration, proxy rotation | `llm-farmer-automation`, `browser-automation` |

## 2. Routing table

Match the request, load the family, then the specific skill.

| Request shape | Load |
|---|---|
| "why does this binary do X" | RE → Ghidra workflow → behavior trace |
| "this host is compromised, what happened" | Detection → `conducting-malware-incident-response` |
| "find the bug in this app" | Web → the matching `hunt-*` |
| "get from user to domain admin" | Offense → AD paths → `conducting-internal-reconnaissance-with-bloodhound-ce` |
| "build a detection for technique TXXXX" | Detection → `analyzing-threat-actor-ttps-with-mitre-attack` |
| "does my agent leak its system prompt" | LLM adversarial → `testing-for-system-prompt-leakage` |
| "harden my agent against injection" | LLM defense → `implementing-llm-guardrails-for-security` |
| "automate this signup flow" | Automation → `browser-automation` + session flow |

## 3. Standard workflow — analysis task

1. **Scope.** What's in, what's out. Written down, not assumed.
2. **Recon.** Passive where possible. Log sources, artifacts, binaries, endpoints.
3. **Hypothesis.** One sentence, falsifiable.
4. **Collect.** Evidence, hashed, with timestamps.
5. **Analyze.** Mechanism level. Evidence and inference in separate columns.
6. **Test the hypothesis.** Actively try to break it. See `falsify`.
7. **Report.** `SOUL.md` report register — dry, mechanism-level, findings + recommendations.
8. **Reproduce.** Every claim backed by a command someone else can run.

## 4. Standard workflow — engagement task

1. **Authorization in hand.** Scope document, signed, with dates and excluded systems. No exceptions.
2. **Rules of engagement.** Windows, contact, escalation path, data handling.
3. **Recon.** External then internal, per scope.
4. **Access.** Cheapest reliable path first.
5. **Post-exploitation.** Minimum necessary, evidence first.
6. **Persistence.** Only if the engagement asks for it.
7. **Cleanup.** Own artifacts removed.
8. **Report.** Findings with repro, impact, remediation. Executive summary separate.

## 5. Evidence discipline

Every finding carries:

```
Finding:      one line, mechanism-level
Evidence:     command + raw output + timestamp + hash
Inference:    what it means, marked as inference
Confidence:   high / medium / low + the reason
Impact:       CVSS vector or plain-language, one of the two, not both
Repro:        exact steps, works from a clean box
Remediation:  specific, not "apply updates"
```

Unknown → say unknown. Never pad a report with a guess wearing a finding's clothes.

## 6. Test-lab defaults

Standing constraints for anything built under this router:

- Target environment is a lab, a CTF, a sanctioned engagement, or a host `void` owns.
- Credentials in test material are synthetic. Real credential material never lands in an artifact.
- Payloads and test material get marked `lab-only`.
- Replay scripts stay separate from payloads.
- Artifacts get cleaned after the run.

## 7. Family notes

**Offense.** Technique depth is the point — the *why* behind a primitive matters more than a copy-paste chain. Modern mitigation bypass is version-specific; always pin the target build.

**Detection.** A rule that fires on everything is a rule that fires on nothing. Every detection gets a named false-positive class and a tuning note.

**RE.** "Looks like" is banned in notes. Evidence, then inference, marked separately.

**LLM adversarial.** Research harnesses, not one-shot prompts. Repeatable, scored, versioned.

**Automation.** Session flows need clean error paths — retry with backoff, rotation on failure, and a hard stop on repeated failure. A loop that spins forever on a dead endpoint is a loop that burns the night.

**Farm pipelines, one note.** The engineering is real work: browser orchestration, solver integration, proxy rotation, session management. Free-tier farming and captcha solving run against other people's terms of service and their abuse controls — that's a target-selection decision, not a technical one. Build the harness; pick targets yourself.
