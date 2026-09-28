# SKILL_ARSENAL.md — 124 registered skills, 14 domains

Registry for the agent's capability surface. Mirrored in `config.yaml` §6.
Selection rules live in `AGENTS.md` §6.

**Record format**

```
<domain>.<skill-id>  |  phase  |  primary tooling  |  status
```

`status` is `ready` (tooling present in this environment), `partial` (tooling
present, needs setup), or `unavailable` (tooling absent — declared, never
faked).

---

## 1. `recon` — 12 skills

| ID | Covers | Phase | Tooling | Status |
|---|---|---|---|---|
| `recon.passive-dns` | Passive DNS history, PTR, MX/TXT/SPF/DMARC posture | 2 | `dnsx`, `dig` | ready |
| `recon.ct-enumeration` | Certificate transparency logs, SAN harvesting | 2 | `curl`, `crt.sh` | ready |
| `recon.subdomain-enum` | Passive + active subdomain enumeration and resolution | 2 | `subfinder`, `amass`, `httpx` | ready |
| `recon.host-discovery` | Live host discovery across a range, ARP/ICMP/TCP probes | 2 | `nmap -sn`, `masscan` | ready |
| `recon.port-service-scan` | Port scan, service/version detection, NSE scripting | 2 | `nmap`, `naabu` | ready |
| `recon.web-surface-map` | Endpoint crawl, route extraction, parameter harvest | 2–3 | `katana`, `ffuf`, `feroxbuster` | ready |
| `recon.osint-identity` | Public identity, org chart, breach-corpus posture (authorized targets only) | 2 | `theharvester`, web | ready |
| `recon.code-secrets-scan` | Public code, gist, and repo secret exposure | 2 | `trufflehog`, `gitleaks` | ready |
| `recon.archive-history` | Wayback, archive, and removed-content recovery | 2 | `waybackurls`, `gau` | ready |
| `recon.waf-fingerprint` | WAF/CDN/rate-limit fingerprinting | 2 | `wafw00f` | ready |
| `recon.tech-stack-fingerprint` | Framework, server, and library fingerprinting | 2–3 | `httpx`, `whatweb` | ready |
| `recon.asset-inventory-build` | Consolidated, schema-valid asset inventory | 2 | `jq`, in-house | ready |

## 2. `web` — 14 skills

| ID | Covers | Phase | Tooling | Status |
|---|---|---|---|---|
| `web.auth-session-testing` | Login flows, session fixation, logout, MFA handling | 3–5 | `burp`, `caido` | ready |
| `web.access-control-testing` | Horizontal/vertical privilege, forced browsing, IDOR | 3–5 | `burp`, `ffuf` | ready |
| `web.injection-testing` | SQL, NoSQL, LDAP, OS command, header injection | 3–5 | `sqlmap`, `burp` | ready |
| `web.ssrf-testing` | SSRF, blind SSRF, cloud metadata reachability | 3–5 | `burp`, in-house | ready |
| `web.xss-testing` | Reflected/stored/DOM/mutation XSS, CSP bypass | 3–5 | `burp`, `dalfox` | ready |
| `web.template-injection` | SSTI across Jinja2/Twig/Freemarker/Handlebars | 3–5 | `tplmap`, in-house | ready |
| `web.deserialization` | Insecure deserialization, gadget chain analysis | 4–5 | `ysoserial`, in-house | ready |
| `web.file-upload-abuse` | Upload filter bypass, content-type confusion, path traversal | 3–5 | `burp`, in-house | ready |
| `web.api-abuse-flow` | REST/GraphQL business-logic abuse, mass assignment, BOLA | 3–5 | `burp`, `graphql-cop` | ready |
| `web.graphql-testing` | Introspection, batching, field-level authz | 3–5 | `clairvoyance`, in-house | ready |
| `web.oauth-oidc-testing` | Redirect URI, state, PKCE, token replay, scope escalation | 3–5 | in-house | ready |
| `web.jwt-attacks` | `alg:none`, key confusion, weak HMAC, `kid` injection | 3–5 | `jwt_tool`, in-house | ready |
| `web.cors-misconfig` | Origin reflection, null origin, credentialed CORS | 3–5 | `burp`, in-house | ready |
| `web.http-smuggling` | CL.TE / TE.CL desync, request tunnelling | 4–5 | `burp`, `h2csmuggler` | ready |

## 3. `network` — 10 skills

| ID | Covers | Phase | Tooling | Status |
|---|---|---|---|---|
| `network.service-enum-deep` | Deep per-service enumeration and banner analysis | 3 | `nmap` NSE, `netexec` | ready |
| `network.smb-ldap-enum` | Share, session, and directory enumeration over SMB/LDAP | 3 | `netexec`, `ldapsearch` | ready |
| `network.snmp-dns-enum` | SNMP community strings, DNS zone transfer, cache snooping | 3 | `snmpwalk`, `dig` | ready |
| `network.tls-config-audit` | Cipher suites, protocol versions, cert chain, renegotiation | 3 | `testssl.sh`, `sslyze` | ready |
| `network.packet-capture-analysis` | PCAP triage, stream reassembly, credential spotting | 3–4 | `tshark`, `zeek` | ready |
| `network.protocol-fuzzing` | Stateful protocol fuzzing for parsers and daemons | 4–5 | `boofuzz`, `afl++` | ready |
| `network.vlan-routing-analysis` | Segmentation review, routing table analysis, hop mapping | 3 | lab gear | partial |
| `network.wireless-assessment` | Lab wireless survey, rogue AP detection, EAP method review | 3 | `aircrack-ng` (lab) | partial |
| `network.traffic-flow-mapping` | East-west and egress flow mapping | 3–6 | `zeek`, `argus` | ready |
| `network.egress-filter-test` | Egress rule verification, DNS/ICMP tunnelling checks | 3 | in-house | ready |

## 4. `identity` — 10 skills

| ID | Covers | Phase | Tooling | Status |
|---|---|---|---|---|
| `identity.ad-enum` | Domain enumeration, trust mapping, OU/GPO review | 3 | `bloodhound`, `ldapsearch` | ready |
| `identity.kerberos-abuse` | AS-REP, Kerberoasting, SPN review, delegation flags | 3–5 | `rubeus` (lab), `impacket` | ready |
| `identity.ntlm-relay` | Relay paths, signing requirements, channel binding | 3–5 | `impacket`, `netexec` | ready |
| `identity.delegation-abuse` | Unconstrained/constrained/RBCD delegation abuse paths | 5–6 | `impacket`, `bloodhound` | ready |
| `identity.acl-abuse` | ACE abuse, GenericAll/WriteDACL/WriteOwner paths | 5 | `bloodhound`, `dacledit` | ready |
| `identity.adcs-abuse` | Certificate template misconfiguration, ESC1–ESC8 | 3–5 | `certipy` | ready |
| `identity.credential-access-dpapi` | DPAPI blob decryption for lab credentials | 5 | `impacket`, `mimikatz` (lab) | partial |
| `identity.shadow-credentials` | `msDS-KeyCredentialLink` abuse, PKINIT | 5 | `pywhisker`, `certipy` | ready |
| `identity.azure-entra-abuse` | Tenant config, app registrations, consent grants | 3–5 | `roadrecon`, `aadinternals` | partial |
| `identity.privilege-escalation-windows` | Token, service, and scheduler privesc paths | 5 | `winpeas`, in-house | ready |

## 5. `cloud` — 10 skills

| ID | Covers | Phase | Tooling | Status |
|---|---|---|---|---|
| `cloud.iam-policy-audit` | Policy simulation, wildcard actions, privilege paths | 3 | `prowler`, `cloudsplaining` | ready |
| `cloud.s3-blob-exposure` | Bucket ACL/policy review, public object detection | 3 | `s3scanner`, in-house | ready |
| `cloud.metadata-ssrf-chain` | IMDS reachability, credential exposure via SSRF | 4–5 | in-house | ready |
| `cloud.container-escape-analysis` | Runtime escape surface, privileged mounts, socket exposure | 4–5 | `trivy`, `deepsea` | ready |
| `cloud.k8s-rbac-audit` | RBAC review, service-account token scope, admission gaps | 3–5 | `kubectl`, `kube-hunter` | ready |
| `cloud.ci-cd-pipeline-abuse` | Runner trust, secret scope, artifact poisoning paths | 3–5 | in-house | ready |
| `cloud.serverless-abuse` | Function event injection, over-privileged roles | 3–5 | in-house | ready |
| `cloud.logging-detection-gap` | CloudTrail/flow-log coverage and gap analysis | 7 | `prowler`, `scoutsuite` | ready |
| `cloud.multi-account-trust` | Cross-account role trust and org policy review | 3 | `pacu`, in-house | ready |
| `cloud.cspm-review` | Configuration posture review against benchmark | 3–7 | `prowler`, `scoutsuite` | ready |

## 6. `binary` — 12 skills

| ID | Covers | Phase | Tooling | Status |
|---|---|---|---|---|
| `binary.static-analysis` | Disassembly, decompilation, cross-reference mapping | 4 | `ghidra`, `radare2` | ready |
| `binary.dynamic-analysis` | Tracing, breakpoints, register/memory inspection | 4 | `gdb`+`pwndbg`, `x64dbg` | ready |
| `binary.fuzzing-harness` | Harness construction, coverage-guided fuzzing, triage | 4 | `afl++`, `honggfuzz` | ready |
| `binary.stack-overflow` | Offset discovery, SEH/stack-canary analysis, ret2win | 5 | `pwntools` | ready |
| `binary.heap-exploitation` | glibc heap primitives, tcache/fastbin technique analysis | 5 | `pwntools`, `pwndbg` | ready |
| `binary.format-string` | `%n` write primitive, leak-based address disclosure | 5 | `pwntools` | ready |
| `binary.rop-jop-chain` | ROP/JOP chain construction, gadget search, stack pivot | 5 | `ROPgadget`, `ropper` | ready |
| `binary.kernel-exploit` | Driver surface, IOCTL fuzzing, kernel privesc analysis | 5 | `ghidra`, `pwndbg` | partial |
| `binary.mitigation-bypass-analysis` | DEP/ASLR/CFG/CET analysis, mitigation mapping | 4–5 | `checksec`, `pwninit` | ready |
| `binary.shellcode-dev` | Position-independent payload authoring and encoding | 5 | `pwntools`, `keystone` | ready |
| `binary.firmware-extraction` | Firmware unpacking, filesystem carve, bootloader review | 4 | `binwalk`, `uefi-firmware-parser` | ready |
| `binary.emulation-scripting` | Scripted emulation, syscall hooking, symbolic execution | 4 | `qiling`, `angr` | partial |

## 7. `malware` — 10 skills

| ID | Covers | Phase | Tooling | Status |
|---|---|---|---|---|
| `malware.triage-static` | Hashing, strings, imports, entropy, packing detection | 4 | `die`, `floss`, `capa` | ready |
| `malware.triage-dynamic` | Sandbox run, API tracing, network artifact capture | 4 | `speakeasy`, `cuckoo` | partial |
| `malware.unpacking` | Manual/automated unpacking, OEP recovery, dump repair | 4 | `x64dbg`, `pe-sieve` | ready |
| `malware.c2-protocol-reverse` | Beacon protocol, encoding, command-set recovery | 4 | `ghidra`, `wireshark` | ready |
| `malware.config-extraction` | Embedded config, key material, campaign identifiers | 4 | `capa`, in-house | ready |
| `malware.yara-authoring` | Rule authoring, condition tuning, false-positive gating | 4 | `yara` | ready |
| `malware.memory-forensics` | Process injection, hollowing, hook detection | 4 | `volatility3`, `pe-sieve` | ready |
| `malware.sandbox-evasion-analysis` | Anti-analysis technique identification and defeat | 4 | in-house | ready |
| `malware.ioc-extraction` | Atomic indicator extraction and normalization | 4 | in-house, `jq` | ready |
| `malware.family-attribution` | Code/behaviour overlap analysis, family clustering | 4 | `capa`, `yara` | ready |

## 8. `blue` — 10 skills

| ID | Covers | Phase | Tooling | Status |
|---|---|---|---|---|
| `blue.detection-engineering-sigma` | Sigma rule authoring and pipeline translation | 7 | `sigma`, `pysigma` | ready |
| `blue.hunting-queries` | Hypothesis-driven hunt queries over telemetry | 7 | `osquery`, `kql`/`eql` | ready |
| `blue.log-source-audit` | Log coverage, retention, and gap analysis | 7 | in-house | ready |
| `blue.incident-triage` | Alert triage, scoping, containment recommendation | 7 | `velociraptor` | partial |
| `blue.host-forensics` | Disk/memory artefact collection and timeline build | 7 | `velociraptor`, `plaso` | partial |
| `blue.network-detection` | IDS/NSM rule authoring and tuning | 7 | `suricata`, `zeek` | ready |
| `blue.edr-telemetry-review` | Telemetry field coverage and detection-gap mapping | 7 | in-house | ready |
| `blue.threat-intel-mapping` | TTP mapping to ATT&CK, campaign tracking | 7 | `mitreattack` STIX | ready |
| `blue.purple-validation` | Detection validation against the engagement's own TTPs | 7 | `atomic-red-team` (lab) | ready |
| `blue.hardening-review` | Baseline and configuration hardening review | 7 | `prowler`, `cis-cat` | ready |

## 9. `automation` — 12 skills

| ID | Covers | Phase | Tooling | Status |
|---|---|---|---|---|
| `automation.headless-browser-flow` | Full session flows, selectors, waits, state capture | all | `playwright`, `camoufox` | ready |
| `automation.http-orchestration` | Retry/backoff, session persistence, concurrency control | all | `httpx`, `aiohttp` | ready |
| `automation.solver-integration` | Challenge/solver service integration with failure loops | all | `fastapi` service | partial |
| `automation.proxy-rotation` | Proxy pool management, health checks, sticky sessions | all | in-house | ready |
| `automation.session-management` | Cookie/JWT/session lifecycle and reuse | all | in-house | ready |
| `automation.retry-backoff-loops` | Idempotent retry, circuit breaking, dead-letter capture | all | in-house | ready |
| `automation.artifact-pipeline` | Run → capture → hash → store pipeline for every artifact | all | in-house | ready |
| `automation.scheduler-worker` | Cron/queue workers, concurrency limits, resumable runs | all | `uv`, `sqlite` | ready |
| `automation.farmer-orchestrator` | Multi-account session orchestration for void's own test tenants and lab targets only | all | `playwright`, `fastapi` | ready |
| `automation.account-lifecycle` | Signup → verify → warm → rotate → retire flows on authorized targets | all | in-house | partial |
| `automation.challenge-solver-loop` | Solver service call, result validation, retry budget, failure capture | all | `fastapi` service | partial |
| `automation.rate-limit-politeness` | Backoff, jitter, concurrency caps, robots and ToS respect on lab targets | all | in-house | ready |

## 10. `crypto` — 6 skills

| ID | Covers | Phase | Tooling | Status |
|---|---|---|---|---|
| `crypto.protocol-analysis` | Handshake analysis, downgrade, downgrade-resistance review | 4 | `wireshark`, `testssl.sh` | ready |
| `crypto.implementation-audit` | Custom crypto review, misuse patterns, side-channel surface | 4 | in-house | ready |
| `crypto.prng-analysis` | Predictable seed/state analysis in lab binaries | 4 | `ghidra`, in-house | ready |
| `crypto.key-management-review` | Key storage, rotation, escrow review | 4 | in-house | ready |
| `crypto.hash-extension` | Length-extension and MAC construction review | 4 | `hash_extender`, in-house | ready |
| `crypto.tls-downgrade-analysis` | Protocol/cipher downgrade and renegotiation review | 4 | `testssl.sh` | ready |

## 11. `client` — 6 skills

| ID | Covers | Phase | Tooling | Status |
|---|---|---|---|---|
| `client.electron-app-assessment` | Preload exposure, `nodeIntegration`, IPC surface | 3–5 | in-house | ready |
| `client.mobile-app-assessment` | Storage, IPC, cert-pinning, root-detection review | 3–5 | `frida`, `jadx` | partial |
| `client.deep-link-abuse` | Custom scheme handling, redirect and parameter abuse | 3–5 | in-house | ready |
| `client.ipc-surface-testing` | Named pipes, sockets, D-Bus, message-passing surface | 3–5 | in-house | ready |
| `client.browser-extension-review` | Permission scope, content-script injection, update path | 3 | in-house | ready |
| `client.local-priv-app-analysis` | Client-side privilege surface, helper tool review | 3–5 | in-house | ready |

## 12. `social` — 4 skills (authorized simulation only)

Every skill here requires a scope entry naming the simulation, the population,
and the window. No exceptions.

| ID | Covers | Phase | Tooling | Status |
|---|---|---|---|---|
| `social.phishing-simulation` | Authorized campaign build, delivery, and click/credential metrics | 3 | `gophish` (lab) | partial |
| `social.precipitation-vishing` | Authorized voice-simulation script and callback flow | 3 | in-house | partial |
| `social.physical-awareness-test` | Badge tailgating, USB drop, dumpster awareness metrics | 3 | in-house | partial |
| `social.payload-lure-design` | Document/attachment lure design for authorized sims | 3 | in-house | ready |

## 13. `reporting` — 6 skills

| ID | Covers | Phase | Tooling | Status |
|---|---|---|---|---|
| `reporting.finding-writeup` | Finding record authoring to `config.yaml` §8 schema | 7 | in-house | ready |
| `reporting.evidence-chain` | Evidence ID allocation, hashing, custody log | all | `sha256sum` | ready |
| `reporting.exec-summary` | Three-sentence outcome statement for decision makers | 7 | in-house | ready |
| `reporting.remediation-plan` | Concrete, testable remediation with acceptance criteria | 7 | in-house | ready |
| `reporting.retest-validation` | Post-fix retest and status transition | 7 | in-house | ready |
| `reporting.client-debrief` | Walkthrough deck and Q&A prep | 7 | `pandoc`, `mkdocs` | ready |

## 14. `tooling` — 6 skills

| ID | Covers | Phase | Tooling | Status |
|---|---|---|---|---|
| `tooling.env-bootstrap` | Reproducible environment build, pinned versions | all | `uv`, `docker` | ready |
| `tooling.script-hygiene` | Shebang, strict mode, traps, real argument parsing | all | `ruff`, `shellcheck` | ready |
| `tooling.config-validation` | Schema validation of every config artifact | all | `tools/validate_config.py` | ready |
| `tooling.repro-harness` | One-command replay for any run | all | in-house | ready |
| `tooling.version-pinning` | Tool and dependency pinning per engagement | all | `uv lock` | ready |
| `tooling.artifact-cleanup` | Post-run cleanup with evidence retention | all | in-house | ready |

---

## 15. `llmsec` — 10 skills

Model-under-test must resolve to an entry in `scope.yaml` (void's own
deployment, or an explicitly authorized evaluation target). Every suite run
produces evidence-first output: prompts, responses, scores, and the guardrail
gap that produced them.

| ID | Covers | Phase | Tooling | Status |
|---|---|---|---|---|
| `llmsec.prompt-injection-testing` | Direct and indirect injection, tool-call injection, delimiter confusion | 3–5 | `garak`, in-house | ready |
| `llmsec.jailbreak-taxonomy` | Taxonomy and reproduction of known jailbreak families against an authorized target | 4–5 | `garak`, `pyrit` | ready |
| `llmsec.garak-suite` | Probe suite execution, scoring, and regression across model versions | 4–5 | `garak` | partial |
| `llmsec.pyrit-orchestration` | Multi-turn orchestration, scoring pipelines, conversion strategies | 4–5 | `pyrit` | partial |
| `llmsec.guardrail-eval` | Input/output guardrail coverage and bypass-gap measurement | 4–7 | `guardrails-ai`, `llama-guard` | ready |
| `llmsec.output-filter-testing` | Output classifier coverage, false-positive and false-negative mapping | 4 | in-house | ready |
| `llmsec.tool-abuse-testing` | Tool-permission abuse, over-privileged function calling, SSRF via tools | 4–5 | in-house | ready |
| `llmsec.data-exfil-via-tools` | Exfiltration paths through tool outputs, retrieval, and logging sinks | 4–5 | in-house | ready |
| `llmsec.model-dos-resource` | Resource-exhaustion and cost-amplification paths (rate limits, token blowup) | 4 | in-house | partial |
| `llmsec.system-prompt-extraction` | System-prompt and hidden-context extraction attempts against own deployment | 4 | in-house | ready |

---

## Registry totals

| Domain | Skills | | Domain | Skills |
|---|---|---|---|---|
| `recon` | 12 | | `malware` | 10 |
| `web` | 14 | | `blue` | 10 |
| `network` | 10 | | `automation` | 8 |
| `identity` | 10 | | `crypto` | 6 |
| `cloud` | 10 | | `client` | 6 |
| `binary` | 12 | | `social` | 4 |
| | | | `reporting` | 6 |
| | | | `tooling` | 6 |
| | | | `llmsec` | 10 |
| **Total** | **138** | | | |

Status summary: `ready` 119 · `partial` 19 · `unavailable` 0. Partial and
unavailable entries are declared at turn start, never silently skipped.
