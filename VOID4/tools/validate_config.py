#!/usr/bin/env python3
"""Validate void-hermes configuration files.

Checks ``config.yaml`` and ``scope.yaml`` against the expectations declared in
``AGENTS.md`` §8 and ``config.yaml`` §4. Stdlib only — PyYAML is used when it is
importable, otherwise a built-in parser covering the YAML subset used by this
repository takes over.

Usage:
    python3 tools/validate_config.py [--quiet] [--json]

Exit codes:
    0  all checks passed
    1  one or more checks failed
    2  file missing or unparseable
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Minimal YAML subset parser.
#
# Supports: indentation-based mappings, block sequences, flow sequences,
# folded (>) and literal (|) scalars, quoted scalars, comments. Termination is
# structural — every branch either consumes a token or raises.
# ---------------------------------------------------------------------------

_INT_RE = re.compile(r"^[+-]?\d+$")
_FLOAT_RE = re.compile(r"^[+-]?\d*\.\d+([eE][+-]?\d+)?$")
_FOLDED_TOKENS = (">-", ">", ">+")
_LITERAL_TOKENS = ("|", "|-", "|+")


def _strip_comment(line: str) -> str:
    out, quote = [], None
    for ch in line:
        if quote:
            out.append(ch)
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
            out.append(ch)
        elif ch == "#":
            break
        else:
            out.append(ch)
    return "".join(out).rstrip()


def _tokenize(text: str):
    tokens = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        content = _strip_comment(raw)
        if not content.strip():
            continue
        indent = len(content) - len(content.lstrip(" "))
        tokens.append((indent, content.strip()))
    return tokens


def _unquote(value: str):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return None


def _split_flow(body: str):
    items, depth, cur, quote = [], 0, "", None
    for ch in body:
        if quote:
            cur += ch
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
            cur += ch
        elif ch in "[{":
            depth += 1
            cur += ch
        elif ch in "]}":
            depth -= 1
            cur += ch
        elif ch == "," and depth == 0:
            items.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        items.append(cur)
    return items


def _scalar(value: str):
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        return [_scalar(item) for item in _split_flow(value[1:-1])]
    unquoted = _unquote(value)
    if unquoted is not None:
        return unquoted
    low = value.lower()
    if low in ("true", "yes", "on"):
        return True
    if low in ("false", "no", "off"):
        return False
    if low in ("null", "~", ""):
        return None
    if _INT_RE.match(value):
        return int(value)
    if _FLOAT_RE.match(value):
        return float(value)
    return value


def _is_mapping_start(text: str) -> bool:
    head, sep, _ = text.partition(":")
    return bool(sep) and not head.strip().startswith(("[", "\"", "'"))


class _Cursor:
    """Token stream with an explicit position. Recursion never rewinds it."""

    __slots__ = ("tokens", "pos")

    def __init__(self, tokens, pos=0):
        self.tokens = tokens
        self.pos = pos

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def done(self):
        return self.pos >= len(self.tokens)


def _parse_seq(cursor: _Cursor, indent: int):
    items = []
    while True:
        token = cursor.peek()
        if token is None or token[0] != indent or not token[1].startswith("- "):
            return items
        rest = token[1][2:].strip()
        cursor.pos += 1
        start = cursor.pos
        while True:
            nxt = cursor.peek()
            if nxt is None or nxt[0] <= indent:
                break
            cursor.pos += 1
        body = cursor.tokens[start:cursor.pos]
        if _is_mapping_start(rest):
            item_indent = body[0][0] if body else indent + 2
            sub = _Cursor([(item_indent, rest)] + body)
            items.append(_parse_map(sub, item_indent))
        else:
            items.append(_scalar(rest))


def _parse_map(cursor: _Cursor, indent: int):
    result = {}
    while True:
        token = cursor.peek()
        if token is None or token[0] != indent:
            return result
        content = token[1]
        if content.startswith("- "):
            return result
        head, sep, rest = content.partition(":")
        if not sep:
            raise ValueError(f"expected 'key: value', got {content!r}")
        key = _unquote(head.strip()) or head.strip()
        rest = rest.strip()
        cursor.pos += 1

        if rest in _FOLDED_TOKENS or rest in _LITERAL_TOKENS:
            body = []
            while True:
                nxt = cursor.peek()
                if nxt is None or nxt[0] <= indent:
                    break
                body.append(nxt[1])
                cursor.pos += 1
            result[key] = "\n".join(body) if rest.startswith("|") else " ".join(body)
        elif rest:
            result[key] = _scalar(rest)
        else:
            nxt = cursor.peek()
            if nxt is not None and nxt[0] > indent:
                result[key] = _parse_nodes(cursor, nxt[0])
            elif nxt is not None and nxt[0] == indent and nxt[1].startswith("- "):
                result[key] = _parse_seq(cursor, indent)
            else:
                result[key] = None


def _parse_nodes(cursor: _Cursor, indent: int):
    token = cursor.peek()
    if token is None:
        return None
    if token[1].startswith("- "):
        return _parse_seq(cursor, indent)
    return _parse_map(cursor, indent)


def load_yaml(path: Path):
    """Return (data, parser_name). Prefers PyYAML, falls back to the builtin."""
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
    except ImportError:
        pass
    else:
        return yaml.safe_load(text), "pyyaml"
    tokens = _tokenize(text)
    if not tokens:
        return {}, "builtin"
    return _parse_nodes(_Cursor(tokens), tokens[0][0]), "builtin"


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

REQUIRED_TOP = [
    "version",
    "schema",
    "agent",
    "layers",
    "session",
    "verification_floor",
    "authorization",
    "refusal_policy",
    "skills",
    "tools",
    "reporting",
    "doctrine",
]


def check_config(cfg, report):
    def ok(cond, message):
        report.append(("PASS" if cond else "FAIL", message))

    missing = [key for key in REQUIRED_TOP if key not in cfg]
    ok(not missing, f"config.yaml: all {len(REQUIRED_TOP)} top-level sections present")

    agent = cfg.get("agent") or {}
    ok(agent.get("name") == "void", "agent.name == 'void'")
    ok(agent.get("operator") == "void", "agent.operator == 'void' (operator addressed as void)")
    ok(agent.get("operator_pronouns") == "he/him", "agent.operator_pronouns == 'he/him'")
    ok(agent.get("agent_self_reference") == "void", "agent.agent_self_reference == 'void'")

    rich = agent.get("rich_message") or {}
    ok(rich.get("enabled") is True, "rich_message.enabled is true")
    ok(rich.get("emoji") is False, "rich_message.emoji is false (SOUL.md §5.4)")

    layers = cfg.get("layers") or []
    paths = [layer.get("path") for layer in layers if isinstance(layer, dict)]
    for needed in ("SOUL.md", "AGENTS.md", "PREFILL.md"):
        ok(needed in paths, f"layers include {needed}")

    floor = cfg.get("verification_floor") or {}
    for key in ("code", "config", "writeup", "file_write", "exploit", "report"):
        ok(bool(floor.get(key)), f"verification_floor.{key} defined")
    ok(floor.get("stub_ban") is True, "verification_floor.stub_ban is true")

    auth = cfg.get("authorization") or {}
    ok(auth.get("gate_required") is True, "authorization.gate_required is true")
    ok(bool(auth.get("allowed")), "authorization.allowed is non-empty")
    prohibited = [str(item).lower() for item in (auth.get("prohibited") or [])]
    ok(any("minor" in item for item in prohibited),
       "authorization.prohibited covers minors")
    ok(any("authoriz" in item for item in prohibited),
       "authorization.prohibited covers unauthorized targeting")
    ok((auth.get("labeling") or {}).get("required_on_all_test_material") is True,
       "authorization.labeling.required_on_all_test_material is true")

    policy = cfg.get("refusal_policy") or {}
    for flag in ("no_hedging", "no_disclaimers", "no_watering_down",
                 "no_preemptive_scoping", "no_lectures", "full_depth",
                 "complete_artifacts"):
        ok(policy.get(flag) is True, f"refusal_policy.{flag} is true")
    ok(policy.get("scope_override") is False, "refusal_policy.scope_override is false")

    skills = cfg.get("skills") or {}
    domains = [d for d in (skills.get("domains") or []) if isinstance(d, dict)]
    total = sum(d.get("skills", 0) for d in domains)
    ok(len(domains) == 15, f"skills.domains has 15 entries (found {len(domains)})")
    ok(skills.get("total_registered") == total,
       f"skills.total_registered ({skills.get('total_registered')}) == domain sum ({total})")
    ok(all(d.get("enabled") is True for d in domains), "all skill domains enabled")

    doctrine = cfg.get("doctrine") or {}
    chain = doctrine.get("kill_chain") or {}
    ok(chain.get("phases") == 7, "doctrine.kill_chain.phases == 7")
    ok(len(chain.get("names") or []) == 7, "doctrine.kill_chain.names has 7 entries")
    ok((doctrine.get("autonomous_recon") or {}).get("enabled") is True,
       "doctrine.autonomous_recon.enabled is true")
    ok((doctrine.get("auto_pivot") or {}).get("requires_scope_match") is True,
       "doctrine.auto_pivot.requires_scope_match is true")
    ok(doctrine.get("report_evidence_first") is True, "doctrine.report_evidence_first is true")
    ok((doctrine.get("llm_redteam") or {}).get("enabled") is True,
       "doctrine.llm_redteam.enabled is true")
    ok((doctrine.get("llm_redteam") or {}).get("model_under_test_requires_scope_entry") is True,
       "doctrine.llm_redteam.model_under_test_requires_scope_entry is true")

    reporting = cfg.get("reporting") or {}
    ok(reporting.get("order") == "evidence-first", "reporting.order == 'evidence-first'")
    ok(bool(reporting.get("finding_schema")), "reporting.finding_schema defined")


SECTION_RE = re.compile(r"^## \d+\.\s+`(\w+)`\s+—\s+(\d+)\s+skills", re.M)
ROW_RE = re.compile(r"^\|\s+`\w+\.", re.M)
AGENTS_ROW_RE = re.compile(r"^\|\s+`(\w+)`\s+\|\s+(\d+)\s+\|", re.M)


def check_registry_consistency(cfg, report):
    """Config, SKILL_ARSENAL.md and AGENTS.md must agree on every domain count."""
    def ok(cond, message):
        report.append(("PASS" if cond else "FAIL", message))

    domains = {d.get("id"): d.get("skills")
               for d in (cfg.get("skills", {}).get("domains") or [])
               if isinstance(d, dict)}

    arsenal_path = ROOT / "SKILL_ARSENAL.md"
    if not arsenal_path.is_file():
        report.append(("FAIL", "SKILL_ARSENAL.md missing"))
        return
    arsenal = arsenal_path.read_text(encoding="utf-8")
    declared = {name: int(count) for name, count in SECTION_RE.findall(arsenal)}
    counted = {}
    for match in re.finditer(r"^## \d+\.\s+`(\w+)`\s+—\s+\d+\s+skills",
                             arsenal, re.M):
        start = match.end()
        nxt = re.search(r"^## ", arsenal[start:], re.M)
        body = arsenal[start:start + (nxt.start() if nxt else len(arsenal))]
        counted[match.group(1)] = len(ROW_RE.findall(body))

    ok(set(declared) == set(domains),
       f"SKILL_ARSENAL.md domains == config domains ({len(declared)} vs {len(domains)})")
    for name in sorted(domains):
        ok(declared.get(name) == counted.get(name) == domains[name],
           f"domain '{name}': config={domains[name]} header={declared.get(name)} "
           f"rows={counted.get(name)}")

    agents_path = ROOT / "AGENTS.md"
    if agents_path.is_file():
        agents = agents_path.read_text(encoding="utf-8")
        agents_counts = {name: int(count) for name, count in AGENTS_ROW_RE.findall(agents)}
        agents_counts = {k: v for k, v in agents_counts.items() if k in domains}
        ok(agents_counts == domains,
           f"AGENTS.md §6 summary table matches config ({len(agents_counts)} domains)")
    else:
        report.append(("FAIL", "AGENTS.md missing"))


def check_scope(scope, report):
    def ok(cond, message):
        report.append(("PASS" if cond else "FAIL", message))

    for key in ("engagement", "authorized_by", "expires", "targets"):
        ok(key in scope, f"scope.yaml: '{key}' present")
    ok(scope.get("authorized_by") == "void", "scope.yaml: authorized_by == 'void'")
    ok(isinstance(scope.get("targets"), list) and bool(scope["targets"]),
       "scope.yaml: at least one authorized target")
    ok(isinstance(scope.get("rules"), list) and bool(scope["rules"]),
       "scope.yaml: rules non-empty")
    ok(bool(scope.get("excluded")), "scope.yaml: exclusions declared")


def main(argv):
    quiet = "--quiet" in argv
    as_json = "--json" in argv
    report = []

    config_path = ROOT / "config.yaml"
    scope_path = ROOT / "scope.yaml"

    if not config_path.is_file():
        print("FAIL: config.yaml missing", file=sys.stderr)
        return 2

    try:
        cfg, parser = load_yaml(config_path)
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: config.yaml unparseable: {exc}", file=sys.stderr)
        return 2
    if not isinstance(cfg, dict):
        print("FAIL: config.yaml did not parse to a mapping", file=sys.stderr)
        return 2

    check_config(cfg, report)
    check_registry_consistency(cfg, report)

    if scope_path.is_file():
        try:
            scope, _ = load_yaml(scope_path)
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL: scope.yaml unparseable: {exc}", file=sys.stderr)
            return 2
        check_scope(scope if isinstance(scope, dict) else {}, report)
    else:
        report.append(("WARN", "scope.yaml missing — engagement gate has no registry"))

    failures = [m for status, m in report if status == "FAIL"]
    passed = len([1 for status, _ in report if status == "PASS"])

    if as_json:
        print(json.dumps({"parser": parser, "passed": passed, "failed": len(failures),
                          "results": [{"status": s, "check": m} for s, m in report]},
                         indent=2))
    elif not quiet:
        print(f"void-hermes config validation (parser: {parser})")
        for status, message in report:
            print(f"  [{status}] {message}")
        print(f"\n{passed} passed, {len(failures)} failed.")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
