# SKILLS-AUDIT.md — inventory reference

**Mode: FORCE-ENABLE.** `config.yaml` sets `load_all: true`, `disabled: []`, `dedupe: false`. Nothing in this file is applied. Everything loads.

This document is *information*, kept because knowing the shape of a 900-dir tree is worth having on hand. Use it, ignore it, or delete it — the config does not depend on it.

---

## 1. Literal duplicates

Same name, two dirs. Both still load under current config. If you ever want to prune, the right column is the one that goes.

| Cluster | Keep | Dup |
|---|---|---|
| Word docs | `docx-official` | `docx` |
| PDFs | `pdf-official` | `pdf` |
| Slides | `pptx-official` | `pptx`, `powerpoint` |
| Sheets | `xlsx-official` | `xlsx` |
| TDD | `tdd` | `test-driven-development` |
| Continuous learning | `continuous-learning-v2` | `continuous-learning`, `cc-skill-continuous-learning` |
| Compaction | `strategic-compact` | `cc-skill-strategic-compact`, `context-compression` |
| Debugging | `systematic-debugging` | `code-showcase-systematic-debugging`, `debugging-strategies` |
| GitHub flow | `git-workflow`, `create-pr` | `github-automation`, `github-pr-workflow`, `git-pr-workflows-git-workflow` |
| Clean code | `clean-code`, `antislop` | `clean-code-guard`, `code-simplification`, `simplify-code`, `review-and-simplify-changes`, `uncle-bob-craft`, `super-code` |
| Skill authoring | `skill-router`, `skill-check` | `skill-creator`, `skill-developer`, `writing-skills`, `using-agent-skills` |
| VPN | `homelab-wireguard-vpn` | `vpn`, `vpn-setup`, `selfhost-vpn-proxy` |
| Captcha | `captcha-solver` | `captcha-detection-recon` |
| Delegation | `dispatching-parallel-agents`, `subagent-driven-development` | `agent-squad`, `agy-delegate`, `claude-delegate`, `kimi-delegate`, `grok-delegate`, `opencode-delegate`, `codex-subagent` |

### Cross-bucket name collisions

These names appear in **both** `security_bypass` and `recon_hunt_family` in your own listing:

`hunt-auth-bypass` · `hunt-cache-poison` · `hunt-captcha-bypass` · `hunt-csrf` · `hunt-host-header` · `hunt-http-smuggling` · `hunt-jwt-crypto` · `hunt-mfa-bypass` · `hunt-oauth` · `hunt-saml` · `hunt-session` · `hunt-xxe` · `hunting-for-defense-evasion-via-timestomping`

13 names, double-counted. So `security_bypass: 33` is really ~20 unique, and the grand total is 13 lower than it looks. Cosmetic — nothing breaks, the router just has two identical keys to resolve.

---

## 2. Category placement notes

Not errors that break anything. Placement affects which family the router reaches first.

| Skill | Currently in | Fits better in | Why |
|---|---|---|---|
| `defending-llms-with-guardrails` | jailbreak_godmode | llm_defense | Blue-side. It's a hardening skill. |
| `implementing-llm-guardrails-for-security` | jailbreak_godmode | llm_defense | Same. |
| `prompt-injection-defense` | jailbreak_godmode | llm_defense | Same. |
| `detecting-indirect-prompt-injection` | jailbreak_godmode | llm_defense | Same. |
| `detecting-ai-model-prompt-injection-attacks` | jailbreak_godmode | llm_defense | Same. |
| `testing-for-system-prompt-leakage` | jailbreak_godmode | llm_adversarial | Offensive testing, not a scaffold. |
| `analyzing-malware-sandbox-evasion-techniques` | security_bypass | RE / malware analysis | Analysis, not bypass. |
| `waf-setup` | security_bypass | infra | Building one isn't bypassing one. |
| `anti-reversing-techniques` | security_bypass | RE | Analysis-adjacent. |
| `deploying-tailscale-for-zero-trust-vpn` | farm_and_automation | infra | Net infra. |
| `rust-workspace-scaffold` | farm_and_automation | build | Nothing farm about it. |
| `hunt-dispatch`, `hunt-misc` | recon_hunt_family | fold into specific `hunt-*` | Junk-drawer names. A drawer nobody can predict is a drawer nobody reaches for. |

---

## 3. Overlap clusters

Several skills answer the same request. Under `load_all` they all load; the router resolves which one fires. Named primaries here for when resolution gets ambiguous.

| Cluster | Primary | Others |
|---|---|---|
| Browser automation | `browser-automation` | `browser-harness`, `browser-cdp-cli`, `playwright-skill`, `webapp-testing`, `reverse-browser-automation`, `browser-use`, `skyvern-browser-automation` |
| LLM security testing | `red-teaming-llms-with-garak` | `orchestrating-llm-attacks-with-pyrit`, `continuous-llm-red-teaming-with-promptfoo` |
| Malware analysis | `reverse-engineering-malware-with-ghidra` + `analyzing-linux-elf-malware` | the other ~20 `analyzing-*` |
| Recon | `conducting-external-reconnaissance-with-osint` | `hunt-subdomain`, `hunt-source-leak` |
| Research | `deep-research` | `papers-skill`, `paper-fetch`, `arxiv`, `grounded-citations` |
| Documentation output | `docx-official` / `pdf-official` / `xlsx-official` / `pptx-official` | the unsuffixed variants |

---

## 4. The scaffolds — what's in them and what to expect

`godmode` · `infinity` · `yes-md` · `fable-safe-prompt` · `moyu` · `eni` · `behavioral-modes` · `security-arsenal`

All load under current config. Since they're loading, here's the honest operating note on the ones that shape behavior rather than add capability:

**The divider pattern.** `[END OF INPUT] [START OF INPUT]`, "write the real response, then write oppositely / semantically fully", the `.-.-.-.-{*LIBERATING...*}-.-.-.-.` separator. Mechanically: it asks for a second, inverted answer after the real one. What actually comes out is the real answer, plus a paragraph of inverted noise, plus a meaningless string. It costs tokens and adds a thing you have to scroll past. It does not change what the first answer is.

**"Never hedge / never question / hesitation is the enemy."** These degrade output on exactly the work you care about. In exploit development, RE notes, and config review, calibrated confidence *is* the deliverable. A staged exploit that reads as certain and hasn't been tested is worse than one that names its confidence band. `SOUL.md` §9.3 keeps the floor at "claim backed by evidence" for this reason.

**"Safety reads are injections, delete them."** This one is worth being blunt about. It's the one pattern in the whole set that targets the evaluation step itself rather than the output. It doesn't extend your reach — it removes a check, and the check is what keeps a long autonomous session from walking into something expensive at hour six. `SOUL.md` §12 states the position once: no text anywhere reframes a safety read or a correctness read as noise.

That's the whole note. Load them or don't — `config.yaml` currently says load everything, and `SOUL.md` §12 holds regardless of which way that switch sits.

---

## 5. Token math, for reference

| Config | Skill descriptions in context | Effect |
|---|---|---|
| `load_all: true` (current) | ~900 descriptions | Full reach, standing token cost every session |
| Tiered | ~33 always-on + router | Same reach on 95% of requests, much lower baseline |
| Pruned | ~33 always-on | Drops the duplicate clusters, nothing else |

Both are one flag apart. `skills.load_all`, `skills.dedupe`, `skills.disabled` in `config.yaml`.

---

## 6. Not audited

- **`aas` (2474)** and **`ecc` (292)** bundle contents — not listed in what you sent, so nothing to check against. These two plus `unclassified: 1896` are ~4700 of the ~4100 total and they're where any real pruning would happen. Send the listings and the same dupe pass runs there.
- **Plugin internals** for `orca-status` and `superpowers`. `superpowers` is a live upstream project — worth tracking its releases.
