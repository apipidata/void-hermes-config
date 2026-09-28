#!/usr/bin/env bash
# probe-config.sh — find the real config key names in a local Hermes install.
# Use this before pasting config.yaml, so key names match the build you're running.
# Reads only. Writes nothing.

set -euo pipefail

DEST="${HERMES_HOME:-$HOME/.hermes}"
LIMIT="${LIMIT:-40}"

section() { printf '\n── %s %s\n' "$1" "$(printf '─%.0s' $(seq 1 $((60 - ${#1}))))"; }

if [ ! -d "$DEST" ]; then
  printf 'no Hermes dir at %s — set HERMES_HOME\n' "$DEST" >&2
  exit 1
fi

printf 'probe target: %s\n' "$DEST"

section "config_defaults.py"
if found=$(find "$DEST" -name 'config_defaults.py' -print -quit 2>/dev/null) && [ -n "$found" ]; then
  printf 'found: %s\n\n' "$found"
  grep -oE '^\s*[a-z_][a-z0-9_]*\s*[:=]' "$found" \
    | sed -E 's/[:=]//; s/^\s+//' \
    | sort -u \
    | head -n "$LIMIT"
else
  printf 'not found under %s\n' "$DEST"
fi

section "rich / formatting keys"
grep -rInE '(rich|markdown|panel|table|collapsible|pretty)[a-z_]*\s*[:=]' "$DEST" \
  --include='*.py' --include='*.yaml' --include='*.yml' --include='*.toml' \
  2>/dev/null | grep -vE '/(backups|\.git|node_modules|__pycache__)/' \
  | head -n "$LIMIT" || printf 'none matched\n'

section "skills keys"
grep -rInE '^\s*(auto_load|load_all|disabled|external_dirs|dedupe|ledger|write_approval|creation_nudge_interval)\s*[:=]' "$DEST" \
  --include='*.py' --include='*.yaml' --include='*.yml' \
  2>/dev/null | grep -vE '/(backups|\.git|node_modules|__pycache__)/' \
  | head -n "$LIMIT" || printf 'none matched\n'

section "soul / persona / prefill keys"
grep -rInE '(soul|persona|prefill|system_prompt)[a-z_]*\s*[:=]' "$DEST" \
  --include='*.py' --include='*.yaml' --include='*.yml' \
  2>/dev/null | grep -vE '/(backups|\.git|node_modules|__pycache__)/' \
  | head -n "$LIMIT" || printf 'none matched\n'

section "plugin + mcp keys"
grep -rInE '(plugins|mcp_servers|scan_on_install)[a-z_]*\s*[:=]' "$DEST" \
  --include='*.py' --include='*.yaml' --include='*.yml' \
  2>/dev/null | grep -vE '/(backups|\.git|node_modules|__pycache__)/' \
  | head -n "$LIMIT" || printf 'none matched\n'

section "current config keys"
for f in config.yaml config.yml config.toml; do
  if [ -f "$DEST/$f" ]; then
    printf '%s:\n' "$DEST/$f"
    grep -oE '^\s{0,2}[a-z_][a-z0-9_]*\s*:' "$DEST/$f" | tr -d ' :' | sort -u
  fi
done

section "summary"
printf 'diff the key names above against config.yaml.\n'
printf 'any key that exists above but not in config.yaml: add it.\n'
printf 'any key in config.yaml that exists nowhere above: it will be ignored silently.\n'
