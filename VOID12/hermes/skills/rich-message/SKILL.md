---
name: rich-message
description: Rich message formatting for void. Panels, tables, status lines, dividers, progress blocks, collapsible sections, code fences with language tags. Use for reports, audits, inventories, dashboards, comparisons, and any structured output. Never for casual conversation.
---

# rich-message

Structured output layer. Turns a wall of prose into something scannable. On by default per `SOUL.md` §7.4.

## 1. When to use

| Use rich | Plain |
|---|---|
| Reports, audits, inventories | Casual turns |
| Comparisons, tradeoff tables | One-line answers |
| Status, progress, dashboards | Venting, chat |
| Multi-step plans | Fiction prose |
| Config diffs, file maps | Short technical replies |

Rule: structure carries information, not decoration. If a panel adds no information, it's noise.

## 2. Panels

Box-drawn callout for the one thing that matters in a reply.

```
┌─ BLOCKER ────────────────────────────────────────┐
│ vendor SDK ships without a soname. nothing links. │
│ workaround: pin 2.4.1 and patch the CMake target. │
└───────────────────────────────────────────────────┘
```

Variants: `BLOCKER`, `DECISION`, `WARNING`, `NOTE`, `RESULT`, `ASSUMPTION`.

## 3. Status lines

Single line, name + state + evidence.

```
build      ✓ green           make -j8, 4.2s
tests      ✓ 41/41           pytest, 1.8s
lint       ⚠ 2 warnings      ruff, non-blocking
deploy     ✗ not run         needs prod creds
```

Mark states: `✓` done · `⚠` partial · `✗` failed · `○` not started · `…` in flight.

## 4. Status header block

Top of any long-running operation.

```
▛▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▜
▌ void lab · recon pass 3 · 2026-09-28             ▌
▌ target: lab-corp.net · scope: 10.0.0.0/24        ▌
▌ elapsed 00:14:22 · 6 tools active · 2 findings   ▌
▙▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▟
```

## 5. Tables

Aligned. Header row. No decorative separators beyond the markdown pipe.

```markdown
| Host | Port | Service | Note |
|------|------|---------|------|
| 10.0.0.14 | 22 | OpenSSH 9.6 | key-only |
| 10.0.0.14 | 445 | SMB | signing off |
```

Rules: exact values, no "~". One unit per column. Order by relevance, not alphabetically.

## 6. Dividers

Between major sections in long output.

```
─────────────────────────────────────────────
```

Match length to the widest line above it. Don't stack.

## 7. Callout markers

```
▸ point
• sub-point
◦ detail
! warning
? open question
+ addition
- removal
```

## 8. Progress

```
[████████████░░░░░░░░]  60%  · 12/20 hosts
```

Only for real measured progress. Never fake a bar for an unmeasurable task.

## 9. Collapsible sections

For output that would otherwise bury the answer.

```markdown
<details>
<summary>Full scan output (412 lines)</summary>

...contents...

</details>
```

Answer on top, evidence collapsible. Never collapse the answer itself.

## 10. Code blocks

Always fence with a language tag. Always. Untagged fences lose syntax handling downstream.

- `bash` with `$` only when the line is meant to be copy-pasted
- `python`, `c`, `cpp`, `rust`, `yaml`, `json`, `sql`, `yar` (YARA), `diff` for patches
- Long output → trim to the relevant window, mark the elision explicitly (`... 340 lines elided ...`)

## 11. TL;DR block

Standard closer for substantive replies.

```
▸ TL;DR
[one or two sentences. the answer. no preamble.]

▸ Details
[the body]

▸ Next
[concrete next action, or —]
```

## 12. Config and diff display

```diff
- skills.dedupe: true
+ skills.dedupe: false
  skills.load_all: true
```

Context lines unprefixed. One hunk per logical change. Show the file path above the block.

## 13. Anti-patterns

- Panels around a one-line answer
- Emoji in status markers — use the glyph set in §3
- Tables with more than 7 columns (split it)
- Nested panels
- Fake progress bars
- Decoration that carries no information
- Rich formatting in casual turns, ever
