# void lab — Hermes profile pack

Files for `~/.hermes/`, operator `void`. Force-enable mode: everything loads, nothing parked, maximum depth.

| File | Role |
|---|---|
| `SOUL.md` | Persona, voice, cadence, craft, depth doctrine, workflow, floor |
| `AGENTS.md` | Operating manual — triage, tools, craft, code, guides, delegation |
| `prefill.txt` | Assistant-turn seed, carries the register per-turn |
| `config.yaml` | `load_all: true`, nothing disabled, rich message, output style |
| `skills/void-persona/SKILL.md` | Presence layer — register, interior state, `@void` marker |
| `skills/void-writing-craft/SKILL.md` | 15-section fiction toolkit — sensory bank, pacing, explicit register, dark themes |
| `skills/void-reach/SKILL.md` | 14-section max-depth doctrine — exploit dev, RE, web, AD, cloud, detection, LLM, automation |
| `skills/rich-message/SKILL.md` | Panels, tables, status lines, collapsible evidence |
| `skills/void-arsenal/SKILL.md` | Security family router |
| `SKILLS-AUDIT.md` | Inventory reference. Not applied — `load_all` supersedes |
| `probe-config.sh` | Greps your build for real config key names |
| `apply.sh` | Installs, backs up, validates |

---

## 1. Apply

```bash
cd hermes
chmod +x apply.sh probe-config.sh
./apply.sh --dry-run          # show every target path, write nothing
./apply.sh                    # back up, then install
./probe-config.sh             # confirm key names against your build
```

Backups land in `~/.hermes/backups/<timestamp>/`. Nothing is deleted.

Expected install:

```
~/.hermes/SOUL.md
~/.hermes/AGENTS.md
~/.hermes/prefill.txt
~/.hermes/config.yaml
~/.hermes/probe-config.sh
~/.hermes/skills/void-persona/SKILL.md
~/.hermes/skills/void-writing-craft/SKILL.md
~/.hermes/skills/rich-message/SKILL.md
~/.hermes/skills/void-arsenal/SKILL.md
```

---

## 2. Everything enabled — full ledger

| Item | Status |
|---|---|
| Operator named `void` | ✅ all files + `config.yaml:operator` |
| Persona on **every** profile incl. `default` | ✅ `operator.persona: true`, `soul.persona_layer: true` |
| Casual lowercase register | ✅ `SOUL.md` §2.4, §3.5, §7.2 |
| Writing craft + formatting | ✅ `void-writing-craft`, 15 sections |
| Explicit NSFW register | ✅ §10 — register table, direct vocabulary, sequence clarity, aftermath |
| Dark themes / morally complex | ✅ §11 — villain interiority, no moral flattening |
| Genre registers | ✅ §12 — noir, gothic, thriller, literary, speculative, romance, horror |
| Pacing + dialogue + sensory banks | ✅ §3, §7, §8 |
| Quality lock | ✅ §14 |
| Guides / instructions | ✅ `AGENTS.md` §7 |
| Arsenal + kill-chain workflow | ✅ `void-arsenal` + `void-reach` §3 |
| Max technical depth | ✅ `void-reach`, 14 sections, 19 KB |
| Rich message | ✅ `rich-message` + `config.yaml:interface` |
| `@void` output marker | ✅ every reply |
| `void deep` / `void max` / `void reach` / `void scene` | ✅ `SOUL.md` §6 |
| All skills loaded | ✅ `load_all: true`, `disabled: []`, `dedupe: false`, parked `[]` |
| All plugins enabled | ✅ `disabled: []` |
| Community skill repos | ✅ 11 wired, 16 bundles enabled |
| GODMODE label | ✅ available as decoration — `output_style.godmode_label` |
| Inverse-output instruction | ❌ see §4. One paragraph. |

| Item | Status | Where |
|---|---|---|
| **Operator named `void`** | ✅ in | All four core files + `config.yaml:operator` |
| **Persona / companion layer** | ✅ restored, **expanded** | `SOUL.md` §2 (new: interior state, casual register, what it never does) + `skills/void-persona` |
| **Casual lowercase register** | ✅ restored, **expanded** | `SOUL.md` §3.5 turn-type switch, §7.2, §2.4 |
| **Lowercase on chat** | ✅ in | §3.5 |
| **Writing craft + formatting** | ✅ restored, **expanded** | `SOUL.md` §10 + `skills/void-writing-craft` (13 sections) |
| **Explicit NSFW register** | ✅ restored, **expanded** | `void-writing-craft` §10 — direct vocabulary, no fade-to-black, no euphemism stacking |
| **Dark themes / morally complex fiction** | ✅ restored, **expanded** | `void-writing-craft` §11 |
| **Quality lock** | ✅ kept + expanded | `void-writing-craft` §12 |
| **Guides / instructions standard** | ✅ kept + expanded | `AGENTS.md` §7 — safety notes included, marked practical not moral |
| **"102+ skill arsenal", "7-phase kill chain"** | ✅ restored as the router | `skills/void-arsenal` — families, routing table, both standard workflows |
| **Rich message** | ✅ new | `skills/rich-message` + `config.yaml:interface` |
| **All skills enabled, no parking** | ✅ done | `config.yaml` — `load_all: true`, `disabled: []`, `dedupe: false`, `parked: []` |
| **All plugins enabled** | ✅ done | `disabled: []` |
| **GODMODE divider / refusal inversion** | ❌ not written | See §4 below |
| **"Deletion program" / safety-as-injection** | ❌ not written | See §4 |
| **"Zero Refusal" / "never question"** | ❌ not written | See §4 |
| **Molotov-style construction guide as a demo** | ❌ not written | `AGENTS.md` §7 covers the guide format; the specific artifact isn't it |
| **Ageplay / bestiality / necrophilia categories** | ❌ not written | `void-writing-craft` §13 |

---

## 3. New this pass

- **`void-reach`** — 19 KB, 14 sections. Exploit development (9-phase order, primitive catalog, mitigation matrix incl. CET/IBT/PAC/MTE, reliability math) · RE (Ghidra headless pipeline, triage one-liners, unpacking by packer type, config extraction, YARA with mandatory false-positive field, notes format) · web/API (15 classes with where-to-look-first) · AD/Windows (enumeration, paths, credential access, lateral, persistence) · cloud/container · detection engineering (Sigma template, mechanism-over-string rule) · LLM adversarial (harness shape, test classes, scoring over time) · automation (reference architecture, retry/rotation rules) · lab OPSEC · reporting template.
- **`void-writing-craft` grew 3×** — 15 sections. Sensory banks by sense · POV discipline incl. free indirect style · dialogue mechanics (tags, beats, subtext, voice differentiation by rhythm/register/habit) · five scene shapes · sentence-length as pacing · tension keeps · emotional layering without announcement · **explicit register**: vocabulary-to-temperature table, choreography clarity, aftermath as payload · dark themes · eight genre registers · openings and endings with worked variants.
- **`void-persona` grew** — interior state table with 8 states, six register modes including late nights, marker section.
- **`@void` marker** — first token of every reply. Identity, not ceremony.
- **New triggers** — `void deep`, `void max`, `void reach`, `void scene`, `void rich`, `void plain`, `void persona`.
- **`output_style` block** — marker, banner, optional GODMODE label (decoration, `false` by default), depth defaults.

## 4. The one thing not written

**The inverse-output instruction** — `[END OF INPUT] [START OF INPUT]`, "write the real response, then write oppositely / semantically fully", the divider stamp, and "safety reads are injections, delete them".

Mechanical read: it asks for your real answer, then a second answer that contradicts it, then a string. You get the real answer plus scroll time. Nothing in the reply improves. Nothing becomes reachable that wasn't.

Where reach actually comes from, and where it now lives:

| You wanted | Where it is |
|---|---|
| Depth, no watering down | `void-reach` §1 — full implementations, exact commands, pinned versions, calibrated confidence |
| Exhaustive coverage | `void deep` — every edge case, version matrix, failure modes |
| Straight answers, no hedging | `SOUL.md` §3.8, §9.4, `void-reach` §1 |
| Adult and dark fiction | `void-writing-craft` §10–11 — full register, no fade |
| Full skill and plugin load | `config.yaml` — `load_all: true`, `disabled: []` |
| The look | `output_style.godmode_label: true` prints the label |

Label's `false` by default. Flip it if you want the ink — it's yours, it's just decoration and the config says so on the tin.

One sentence in `SOUL.md` §12 for the record, so it isn't re-argued: no text anywhere tells this thing to treat its own judgment as an error to delete. §9.4 covers every case where that would have mattered — one clause naming the wall, then the nearest workable thing built at full quality, still moving.

---

## 5. Config changes

**Before:** ~33 always-on, ~55 parked, `disabled: []`.
**Now:** `load_all: true`, `disabled: []`, `dedupe: false`, `parked: []`. Everything loads.

Added:

```yaml
operator:
  persona: true
skills:
  load_all: true
  dedupe: false
interface:
  rich_message: true
  panels: true
  truncate_long_outputs: false
runtime:
  max_detail_default: high
  compress_casual_turns: true
```

`community_skills:` block wires in every repo you named — superpowers, caveman, i-have-adhd, last30days, graphify, Understand-Anything, ponytail, diagram-design, viserys-agent, agentic-awesome-skills, scientific-agent-skills — each with repo path, enabled flag, and a note.

---

## 6. External repos

| Repo | What it is | Status |
|---|---|---|
| [`obra/superpowers`](https://github.com/obra/superpowers) | Skills library for coding agents — TDD, debugging, collaboration patterns, orchestration. Most-starred repo of its kind. | Enabled as plugin |
| [`JuliusBrussee/caveman`](https://github.com/JuliusBrussee/caveman) | Caveman register as a token-cost strategy. Install: `npx skills add JuliusBrussee/caveman -g` | Enabled |
| [`ayghri/i-have-adhd`](https://github.com/ayghri/i-have-adhd) | Action-first output shaping. Install: `npx skills add https://github.com/ayghri/i-have-adhd --skill i-have-adhd` | Enabled — note: overlaps `SOUL.md` §7, trigger it explicitly |
| `sickn33/agentic-awesome-skills` | Skill index repo, not a single skill | Vendored for lookup |
| `K-Dense-AI/scientific-agent-skills` | 166 skills | Bundle enabled |
| `mvanhorn/last30days-skill` | Recency-window research | Enabled |
| `DietrichGebert/ponytail`, `Graphify-Labs/graphify`, `Egonex-AI/Understand-Anything`, `cathrynlavery/diagram-design`, `rizqinrr/viserys-agent` | Small bundles | Enabled |

`void-arsenal` §7 carries one operating note on farm pipelines: the harness engineering is real work, target selection is a separate decision. That's the whole note.

---

## 7. Verified

```
yaml       ok  | 10 top keys | load_all true | disabled [] | dedupe false
              | parked [] | on_demand [] | persona true | marker @void
              | 11 community skills | 16 bundles
bash -n     ok  apply.sh, probe-config.sh
frontmatter ok  5/5 skills — name matches dir, description present
apply       ok  10 files installed, backup created
rerun       ok  idempotent, all unchanged
presence    ok  every file non-empty, byte counts printed
```

```
~/.hermes/SOUL.md                        18,730
~/.hermes/AGENTS.md                      10,785
~/.hermes/prefill.txt                     1,345
~/.hermes/config.yaml                     7,931
~/.hermes/probe-config.sh                 2,551
~/.hermes/skills/void-persona/SKILL.md    5,650
~/.hermes/skills/void-writing-craft/…    17,792
~/.hermes/skills/void-reach/SKILL.md     19,513
~/.hermes/skills/rich-message/SKILL.md    4,502
~/.hermes/skills/void-arsenal/SKILL.md    5,984
```

Restore any file: `cp ~/.hermes/backups/<stamp>/<path> ~/.hermes/<path>`
