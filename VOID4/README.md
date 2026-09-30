# void-hermes

Hermes agent configuration stack for **void** — voice layer, procedures layer,
turn seed, skill registry, and the schemas that keep all of it honest.

The operator is addressed as `void` everywhere: in chat, in artifacts, in
thinking, in evidence records. Not "the user". Not "the human".

---

## File map

| File | Layer | What it does |
|---|---|---|
| `SOUL.md` | voice | Cadence, grunts, banned phrases, reply shapes, verification floor |
| `AGENTS.md` | procedures | Authorization gate, 7-phase chain, recon/pivot doctrine, evidence-first reporting |
| `PREFILL.md` | turn seed | Kills the opening pleasantry; seeds `▸ TL;DR` |
| `SKILL_ARSENAL.md` | registry | 138 skills across 15 domains with tooling and status |
| `config.yaml` | runtime knobs | Identity, rich-message surface, floors, doctrine flags, tool policy |
| `scope.yaml` | authorization | Per-engagement target registry — the gate |
| `recon.schema.json` | contract | Output schema for autonomous recon runs |
| `tools/validate_config.py` | gate | Validates `config.yaml` + `scope.yaml`; run before any layer change ships |
| `docs/original-request.md` | history | The spec this stack was built against |

## Load order

```
SOUL.md  ->  AGENTS.md  ->  PREFILL.md
```

Declared in `config.yaml` §2. `SKILL_ARSENAL.md` and `docs/` load on demand.

## The 7-phase chain

```
AUTHORIZE -> RECON -> ENUMERATE -> IDENTIFY -> EXPLOIT -> PIVOT -> REPORT
```

Evidence is captured at every phase boundary before the next phase starts.
Full doctrine in `AGENTS.md` §2.

## Rich message surface

Enabled in full (`config.yaml` §1): markdown, fenced code with syntax
highlighting, tables, mermaid diagrams, collapsible sections, inline code,
`path:line` source references. Emoji are off — banned on the chat surface by
`SOUL.md` §5.4.

## Verify

```bash
python3 tools/validate_config.py          # 67 checks, exit 0 on green
python3 tools/validate_config.py --json   # machine-readable
```

Any edit to `config.yaml` must pass this before it is called live
(`AGENTS.md` §12).

## Working an engagement

```bash
# 1. declare scope
$EDITOR scope.yaml

# 2. validate
python3 tools/validate_config.py

# 3. run the chain, evidence under ./evidence/<engagement>/

# 4. report — evidence IDs must resolve, repro must replay
```

## Design rules

1. Every knob in `config.yaml` is enforceable by the runtime, or it gets
   deleted. No decorative config.
2. The voice layer never grants authority. Scope lives in `AGENTS.md` §1 and
   `config.yaml` §5.
3. Nothing is claimed done below the verification floor — the label is
   `built, unverified — <gap>`.
4. Registry counts in `SKILL_ARSENAL.md`, `config.yaml` §6, and
   `AGENTS.md` §6 must agree; the validator cross-checks all three, section
   headers against table rows against config.
5. Craft-side refusal is zero (`config.yaml` §5.5). Scope-side is fixed. A
   style layer never widens scope; a scope gate never thins craft.

## Version

| Version | Date | Change |
|---|---|---|
| v1 | 2026-09-28 | Initial stack: SOUL/AGENTS/PREFILL layers, 124-skill registry, authorization gate, evidence-first reporting, config validator |
| v2 | 2026-09-28 | Explicit output/refusal policy, `llmsec` domain + red-team method, farmer automation skills, registry 138 skills / 15 domains, three-way registry cross-check |
