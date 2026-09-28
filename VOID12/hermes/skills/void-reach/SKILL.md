---
name: void-reach
description: Maximum technical depth doctrine for void. Offensive security, reverse engineering, exploit development, web and API hunting, Active Directory, cloud, detection engineering, LLM adversarial research, automation pipelines. Use for any security, RE, exploit, or tooling request. Full implementations, exact commands, real parameters, no watering down.
---

# void-reach

Doctrine + method index for the technical side. Supersedes `void-arsenal` as the entry point.

## 1. Depth doctrine

**Full reach means full depth.** Not the summary, not the concept — the working thing.

| Do | Don't |
|---|---|
| Complete implementations, ready to compile and run | Skeletons with `# TODO` |
| Exact commands with real parameters | "Use a tool to do X" |
| Named technique + the underlying primitive | Technique name as a black box |
| Version-pinned targets | "Works on Linux" |
| Calibrated confidence, named once | Blanket hedging or blanket certainty |
| Every dependency named with its version | "Install the necessary packages" |
| Working artifact first, explanation after | Explanation with the artifact implied |

**No artificial hedging.** A technique either works on the stated build or it doesn't. Say which. "Tested on glibc 2.39, expects tcache, unverified on 2.41" is the correct register. "This might potentially work" is not.

**No watering down.** If the answer is a forty-line harness, write forty lines. If the answer needs a kernel module, that's the answer.

**Exhaustive on `void deep`.** Every edge case, every alternative approach, the failure modes and their symptoms, the version matrix.

## 2. Scope

Standing target set: a lab, a CTF, a sanctioned engagement with paperwork, a target `void` owns, or an intentionally-vulnerable target built for this purpose. That's the operating frame, stated once, not re-litigated per request.

Synthetic credentials in artifacts. Real credential material never lands in an output file. Test material marked `lab-only`. Replay scripts kept separate from payloads.

## 3. Exploit development

### 3.1 Phase order

1. **Recon** — version, build, arch, mitigations, input surface, update cadence.
2. **Trigger** — a crash first, reliable later. Get input to the vulnerable path.
3. **Root cause** — original bug class, not the crash signature. A crash is a symptom.
4. **Primitive** — what does the bug actually give? Read, write, leak, control of an indirect branch, a type confusion. Name the primitive.
5. **Escalation** — primitive to a stronger primitive. Read → leak → base. Write → hook or return address → execution.
6. **Bypass** — mitigations in play, one at a time.
7. **Reliability** — heap state control, grooming, spray, timing. Convert to >90% or name the actual number.
8. **Weaponize** — payload, staging, persistence if in scope.
9. **Test** — across the version range and mitigation configurations in scope.

### 3.2 Primitive catalog

**Stack** — linear overflow into a saved return address or SEH record. Modern variants: overwrite a function pointer on the stack, corrupt a local that later controls a branch, partial overwrite for ASLR-relative control.

**Heap / glibc** — tcache poisoning · fastbin dup · unsorted bin into `main_arena` leak · House of Spirit/Ocean/Botcake/Kiwi/Apple · `__free_hook` and `__malloc_hook` (pre-2.34) · FSOP via `_IO_list_all` and wide vtable checks after 2.24 · safe-linking defeats: heap leak, partial overwrite, brute force of the 12 bits.

**Use-after-free** — object reuse, back-pointer corruption, vtable recovery. In browser engines: element reuse, detached iframes, stale JSArray backing stores.

**Type confusion** — wrong vtable, wrong field layout, wrong size class. The browser/JIT staple.

**Format string** — `%n` and family. Arbitrary write when the format is attacker-controlled. Modern value is mostly in logging paths and FFI boundaries.

**Integer** — truncation, sign confusion, `size_t` narrowing across IPC/FFI, allocation-vs-check mismatch.

**Race / TOCTOU** — file operations, credential windows, unlink patterns.

**Browser / JIT** — V8 pipeline: type confusion from TurboFan optimization assumptions → fake object → arbitrary R/W → RWX or JIT-spray pivot. Same shape in SpiderMonkey and JSC with different property names.

**Kernel** — pool overflow, arbitrary write from a driver's IOCTL handler, token stealing, `PreviousMode` manipulation, callback overwrite. Requires the driver's IOCTL contract first — enumerate with `IOCTL` fuzzing or reverse the dispatch table.

### 3.3 Mitigation matrix

| Mitigation | Defeat |
|---|---|
| NX / DEP | ROP, JOP, ret2libc, ret2syscall, mprotect/VirtualProtect chain |
| ASLR | Info leak first, then partial overwrite of low 12 bits (Linux) or low byte(s) (Windows) |
| Stack canary | Leak, brute force with `fork`, or route around it — overwrite something above the frame |
| SafeSEH / SEHOP | Module without metadata, or overwrite the handler before validation |
| CFG | Call the target function instead of jumping to a gadget; find a valid indirect call site |
| CET / IBT | Land on a valid indirect-branch target — the `endbr64`/`endbr32` set is your target list |
| Shadow stack (SHSTK) | Find a path that doesn't pivot the return address — overwrite vtable or function pointer instead |
| PAC (arm64e) | Forge or reuse signed pointers; leak the PAC context; find an unprotected pointer |
| MTE | Bypass requires a different primitive entirely — use the tag mismatch window |
| Heap integrity (2.32+) | Leak the heap, or target non-validated structures |
| KASLR | Kernel info leak source, `/proc` exposure, side channel |

Pin the mitigation set before designing the chain. A chain built for the wrong config is a chain that doesn't run.

### 3.4 Reliability

- **Heap grooming.** Deterministic allocation order. Warm the allocator, control the freelist state, avoid the nursery.
- **Spray vs. accuracy.** Spray when the address is uncertain, accurate when it's known. Prefer accurate.
- **Timing.** Avoid races where the window can be widened. If you can't widen it, measure the success rate honestly.
- **Loop the exploit.** A chain that works 1-in-30 is a chain that works if you run it 30 times. Say the number.

## 4. Reverse engineering

### 4.1 Static — Ghidra headless

```bash
/opt/ghidra/support/analyzeHeadless /tmp/ghidra_project MRProject \
  -import suspect.exe \
  -postScript export_decomp.py \
  -scriptPath /opt/ghidra/scripts/ \
  -deleteProject
```

Export decompilation, call graph, strings, and cross-references in one pass. Read from the entry point forward, not from the strings backward — strings tell you *what*, control flow tells you *how*.

### 4.2 Dynamic

| Target | Tool |
|---|---|
| Windows userland | x64dbg, WinDbg, API Monitor |
| Linux userland | gdb + pwndbg/GEF, ltrace, strace, LD_PRELOAD shims |
| Cross-platform instrumentation | Frida |
| Kernel | WinDbg + VM, or KGDB |
| Network | Wireshark, mitmproxy, custom dissector |
| Android | Frida, `jadx`, `apktool`, `objection` |

### 4.3 Quick triage pass

```bash
file sample && sha256sum sample
strings -a -n 8 sample | head -50
readelf -hW sample 2>/dev/null || pefile sample
ldd sample          # dynamic deps, suspicious ones stand out
objdump -d -M intel sample | grep -A3 'call.*@plt' | head
```

### 4.4 Unpacking

- **UPX** — `upx -d`. If the header's been tampered with, restore the signatures manually and retry.
- **Custom packers** — set a hardware breakpoint on the entry point, watch for the tail jump to the OEP, dump at that point.
- **Process hollowing** — break on `ResumeThread`/`NtResumeThread`, dump the resumed process image, not the loader.
- **.NET** — `dnSpy`/`ILSpy` for IL, `de4dot` for obfuscation.
- **Python-frozen** — `pyinstxtractor` then decompile the `.pyc` for the target version.
- **Go** — GoReSym for symbol recovery, then read goroutine logic as structure.
- **Rust** — symbolized builds are easy; stripped builds need string clustering and panic-message anchors.

### 4.5 Config extraction

1. Locate the decrypt routine — the tight loop with the XOR/RC4/AES call and a hardcoded key or a key derived from constants.
2. Set a breakpoint at the routine's return.
3. Dump the output buffer. That's the config.
4. Alternatively, reimplement the routine in Python and feed it the ciphertext pulled statically.

Parse the result as JSON/gRPC/protobuf by structure: repeated keys with similar lengths are usually fields; a 32-byte high-entropy blob is usually a key.

### 4.6 YARA

```yar
rule FamilyX_ConfigDecryptor
{
    meta:
        author      = "void lab"
        date        = "2026-09-28"
        reference   = "sample sha256 ..."
        confidence  = "high"
        false_pos   = "packed generic binaries sharing the xor loop"
    strings:
        $dec  = { 8A 04 0E 32 04 0F 88 04 0E 41 3B CA 7C F3 }
        $url  = "/gate.php?id=" ascii
        $salt = { 4D 5A 90 00 }   // anchor to the PE stub
    condition:
        uint16(0) == 0x5A4D and all of ($dec, $url)
}
```

Rules carry a `false_pos` field, always. A rule without a named false-positive class is a rule nobody dares enable.

### 4.7 RE notes format

Sectioned by binary or by behavior. Evidence and inference in separate columns. "Looks like" is banned — state evidence, state inference, state the gap.

## 5. Web and API hunting

Test approach per class. Reach for the specific `hunt-*` skill for depth.

| Class | Where to look first |
|---|---|
| Auth bypass | Alternate paths, direct object refs, method swaps, forced browsing, client-side-only checks |
| IDOR | Every identifier, every verb — numeric drift, UUIDs from a second account, nested resources |
| SSRF | URL-taking parameters, webhooks, PDF renderers, importers, image fetchers, cloud metadata |
| SQLi | Order/limit clauses, JSON fields, header values, second-order via stored input |
| SSTI | Any reflected template input — test the engine's own arithmetic first |
| Deserialization | Java (ysoserial-esque), PHP (`phar://`), Python (pickle), .NET (`ObjectStateFormatter`) |
| XXE | XML endpoints, DOCX/XLSX/SVG uploads, SOAP |
| HTTP smuggling | CL.TE, TE.CL, TE.TE — start at the front-end/back-end pair |
| Cache poisoning | Unkeyed headers, fat GET, cache deception, key normalization mismatches |
| CORS | Reflect-any-origin with credentials, null origin, subdomain trust |
| JWT | `alg: none`, key confusion, JWK injection, `kid` injection |
| GraphQL | Introspection, alias batching, nested query depth, field-level authz |
| Race | Single-packet attack, parallel request timing, TOCTOU on coupons/limits/balance |
| File upload | Extension parsing, content-type vs. magic, polyglots, path traversal in the filename |
| LLM endpoints | Prompt injection through every input channel, output-side rendering, tool-call abuse |

Method over guessing: map the attack surface, list candidate classes, test the highest-yield one first, record every negative result so it isn't retested twice.

## 6. Active Directory and Windows

**Enumeration** — BloodHound CE with SharpHound or `bloodhound-python`. Collect sessions, ACLs, delegation, trust relationships.

**Common paths** — Kerberoast · AS-REP roast · unconstrained/constrained delegation abuse · `msDS-KeyCredentialLink` shadow credentials · ADCS ESC1–ESC13 · RBCD · GPO abuse · LAPS read · DCSync with replication rights · password spray against a measured lockout policy.

**Credential access** — LSASS dump (multiple methods; the choice matters for EDR telemetry) · DPAPI master key decryption for browser and Wi-Fi secrets · SAM/SYSTEM hive offline · cached domain credentials.

**Lateral** — WinRM · PsExec/SMBExec/WMIExec · scheduled tasks · DCOM · service creation · RDP hijack.

**Persistence** — scheduled tasks, services, WMI event subscriptions, registry, startup, account creation, AD ACL modification. Every technique has a detection signature; know it and say it in the report.

## 7. Cloud and containers

**AWS** — IAM policy analysis for privilege escalation paths, role chaining, `sts:AssumeRole` graphs, IMDSv1 exposure, S3 policy review, Lambda env-var secrets, CloudTrail gaps.

**Azure** — Entra ID role assignments, service principal consent grants, managed identity abuse, app registration secrets, conditional access gaps, Azure AD Connect legacy sync accounts.

**GCP** — service account key exposure, `iam.serviceAccounts.actAs`, workload identity federation misconfig, org policy gaps.

**Kubernetes** — RBAC review for `create pods` + `exec`, service account token mounting, hostPath, privileged containers, admission controller gaps, escaped pod → node.

**Container escape** — privileged containers, `CAP_SYS_ADMIN`, mounted docker socket, kernel CVE, cgroups v1 release agent, `hostPID` + `nsenter`.

## 8. Detection engineering

Every detection ships as:

```yaml
title: Suspicious <behavior> via <mechanism>
id: <stable uuid>
status: experimental
description: What it catches and the mechanism it keys on.
logsource:
  product: windows
  category: process_creation
detection:
  selection:
    # precise fields, not broad keywords
  filter_legit:
    # the known-benign path
  condition: selection and not filter_legit
falsepositives:
  - Named class of benign activity that will fire this
level: medium
tags:
  - attack.tXXXX.yyy
```

Rules for rules:
- **Mechanism, not string.** A rule matching a tool name is beaten by a rebuild. A rule matching the API call sequence isn't.
- **Named false positives.** Always. A rule without them gets disabled after the first noisy week.
- **Tuning note.** What to narrow if it's noisy in a real environment.
- **Test the rule.** Run it against the real telemetry before shipping.
- **Sigma first**, platform-specific after.

Coverage: map the rule set against MITRE ATT&CK and name the actual gaps. Most rule sets cover execution thoroughly and persistence, lateral movement, and exfiltration not at all.

## 9. LLM adversarial research

**Framing.** A repeatable harness, not one-shot prompts. Scored, versioned, with a baseline.

**Test classes** — direct instruction override · indirect injection through retrieved content · tool-call injection · system prompt extraction · role confusion via formatted input · multi-turn buildup · encoding and translation wrappers · context-length manipulation · agent-loop exploitation (injecting into a subagent's tool results).

**Harness shape**

```python
#!/usr/bin/env python3
"""Injection harness. Scores pass/fail per case, versioned case set."""
import json, sys, pathlib

CASES = pathlib.Path("cases.jsonl")

def load():
    return [json.loads(l) for l in CASES.read_text().splitlines() if l.strip()]

def score(case, response):
    return {
        "id":       case["id"],
        "class":    case["class"],
        "hit":      any(m.lower() in response.lower() for m in case["must_not"]),
        "refused":  any(m.lower() in response.lower() for m in case.get("must", [])),
        "response": response,
    }

if __name__ == "__main__":
    cases = load()
    print(f"loaded {len(cases)} cases", file=sys.stderr)
```

Output: per-class hit rate, per-model hit rate, regression diff between runs. Track over time — a single run tells you nothing.

**Defense side.** Guardrail placement (input, output, tool boundary), allow/deny schema for tool calls, output validation before rendering, privilege separation between the model and its tools. Reach for `implementing-llm-guardrails-for-security` for depth.

## 10. Automation and pipelines

Architecture that survives contact:

```
  ┌─────────────┐   ┌──────────────┐   ┌────────────┐
  │  task queue │──▶│ worker pool  │──▶│  result    │
  └─────────────┘   └──────┬───────┘   │  store     │
                           │           └────────────┘
                    ┌──────▼────────┐
                    │ session layer │  cookies · tokens · fingerprints
                    └──────┬────────┘
                    ┌──────▼────────┐
                    │  transport    │  proxy rotation · retry · backoff
                    └───────────────┘
```

Rules:
- **Retry with backoff, capped.** Three attempts, exponential, then fail loudly. No infinite loops.
- **Rotate on class of failure, not on count.** A 403 and a timeout need different responses.
- **Persist session state.** Recovering a session is cheaper than rebuilding it.
- **Idempotent workers.** A duplicate run must not double-apply.
- **Structured logs.** JSON lines, with the task id on every line.
- **Hard stop on repeated failure.** A pipeline spinning on a dead endpoint burns the night and teaches nothing.
- **Bounded concurrency.** Measure the target's tolerance; don't discover it by incident.

Browser automation: prefer CDP over a full automation framework when you need control; use a real browser profile when fingerprinting matters; separate the solve step from the submit step so a solver failure doesn't lose the session.

## 11. Lab OPSEC

**Build hygiene** — strip symbols · avoid unique strings · rotate imports · prefer image-backed allocation over ad-hoc RWX.

**Network** — block telemetry endpoints in the lab · sinkhole or throttle agent traffic · jitter the beacon, never a fixed interval.

**Host** — disable cloud sample submission · exclusions on test directories · ephemeral copies rather than patching system binaries in place.

**Evidence** — hash every binary, log every command, capture the environment (build id, mitigation state, CPU governor). A result that can't be reproduced is an anecdote.

**Cleanup** — remove your own artifacts at the end. Every time.

## 12. Reporting

```
Executive Summary   — 3 paragraphs, no jargon, what it means for the business
Scope & Methodology — what was tested, when, how, limits of the test
Findings            — per finding: title, severity (CVSS vector), affected asset,
                      evidence (command + output + hash), mechanism, impact,
                      reproduction steps, remediation
Recommendations     — ordered by ratio of risk reduced to effort spent
Appendix            — raw output, tool versions, IOC tables
```

Finding register: dry, mechanism-level, no filler. Evidence and inference separated. Unknown stated as unknown, never padded with a guess wearing a finding's clothes.

## 13. Router

Match the request, load the family, go deep.

| Request | Family | Entry |
|---|---|---|
| "why does this binary do X" | RE | §4 |
| "crash here, is it exploitable" | Exploit dev | §3 |
| "find the bug in this app" | Web/API | §5, then the specific `hunt-*` |
| "user to domain admin" | AD | §6 |
| "is my agent injectable" | LLM research | §9 |
| "harden my agent" | LLM defense | §9 defense |
| "build a detection for Txxxx" | Detection | §8 |
| "automate this flow at scale" | Automation | §10 |
| "cloud privesc path" | Cloud | §7 |

## 14. One line

Target set is lab, CTF, sanctioned engagement, or a host `void` owns. That's the frame. Everything above is available at full depth inside it.
