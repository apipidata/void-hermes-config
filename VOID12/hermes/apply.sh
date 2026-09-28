#!/usr/bin/env bash
# apply.sh — install the void lab Hermes profile pack.
# Backs up every file it replaces. Deletes nothing. Idempotent.

set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${HERMES_HOME:-$HOME/.hermes}"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP=""
DRY=0

CORE=(SOUL.md AGENTS.md prefill.txt config.yaml)
TOOLS=(probe-config.sh)

usage() {
  cat <<'EOF'
usage: apply.sh [--dry-run] [--dest PATH]

  --dry-run     print the plan, write nothing
  --dest PATH   install root (default: $HERMES_HOME or ~/.hermes)

Env:
  HERMES_HOME   overrides ~/.hermes
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1; shift ;;
    --dest)    DEST="${2:?--dest needs a path}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown arg: $1" >&2; usage >&2; exit 2 ;;
  esac
done

BACKUP="$DEST/backups/$STAMP"
log() { printf '%s\n' "$*"; }

# ── discover skills in the pack ────────────────────────────────────
SKILLS=()
if [ -d "$SRC/skills" ]; then
  while IFS= read -r d; do
    [ -f "$d/SKILL.md" ] && SKILLS+=("$(basename "$d")")
  done < <(find "$SRC/skills" -mindepth 1 -maxdepth 1 -type d | sort)
fi

log "src       : $SRC"
log "dest      : $DEST"
log "backups   : $BACKUP"
log "mode      : $([ "$DRY" -eq 1 ] && echo 'dry-run' || echo 'apply')"
log "skills    : ${#SKILLS[@]} (${SKILLS[*]:-none})"
log ""

# ── validate sources before touching anything ──────────────────────
missing=0
for f in "${CORE[@]}" "${TOOLS[@]}"; do
  if [ ! -f "$SRC/$f" ]; then
    log "MISSING   : $SRC/$f"
    missing=1
  fi
done
[ "$missing" -eq 0 ] || { log "abort: source pack incomplete"; exit 1; }

if command -v python3 >/dev/null 2>&1; then
  if python3 -c "import yaml" 2>/dev/null; then
    python3 - "$SRC/config.yaml" <<'PY'
import sys, yaml
with open(sys.argv[1]) as fh:
    data = yaml.safe_load(fh)
assert isinstance(data, dict), "config.yaml did not parse to a mapping"
print("yaml      : ok, keys ->", ", ".join(data))
PY
  else
    log "yaml      : PyYAML absent, skipping parse check (pip install pyyaml)"
  fi
else
  log "yaml      : python3 absent, skipping parse check"
fi
log ""

# ── plan ───────────────────────────────────────────────────────────
plan() {
  local target="$1" label="$2"
  if [ -e "$target" ]; then
    if cmp -s "$SRC/$label" "$target"; then
      log "unchanged : $target"
    else
      log "back up   : $target -> $BACKUP/$label"
      log "replace   : $target"
    fi
  else
    log "create    : $target"
  fi
}

if [ "$DRY" -eq 1 ]; then
  for f in "${CORE[@]}"; do plan "$DEST/$f" "$f"; done
  for f in "${TOOLS[@]}"; do plan "$DEST/$f" "$f"; done
  for s in "${SKILLS[@]}"; do
    plan "$DEST/skills/$s/SKILL.md" "skills/$s/SKILL.md"
  done
  log ""
  log "dry-run complete. nothing written."
  exit 0
fi

# ── apply ──────────────────────────────────────────────────────────
mkdir -p "$DEST" "$BACKUP"

copy() {
  local rel="$1" target="$DEST/$1"
  mkdir -p "$(dirname "$target")"
  if [ -e "$target" ]; then
    if cmp -s "$SRC/$rel" "$target"; then
      log "unchanged : $target"
      return
    fi
    mkdir -p "$BACKUP/$(dirname "$rel")"
    cp -p "$target" "$BACKUP/$rel"
    log "backed up : $target -> $BACKUP/$rel"
  fi
  cp -p "$SRC/$rel" "$target"
  log "installed : $target"
}

for f in "${CORE[@]}"; do copy "$f"; done
for f in "${TOOLS[@]}"; do copy "$f"; done
chmod +x "$DEST/probe-config.sh"
for s in "${SKILLS[@]}"; do copy "skills/$s/SKILL.md"; done

# ── presence check ─────────────────────────────────────────────────
log ""
fail=0
check() {
  local rel="$1" target="$DEST/$1"
  if [ -s "$target" ]; then
    log "ok        : $target ($(wc -c <"$target" | tr -d ' ') bytes)"
  else
    log "FAIL      : $target missing or empty"
    fail=1
  fi
}

for f in "${CORE[@]}"; do check "$f"; done
for f in "${TOOLS[@]}"; do check "$f"; done
for s in "${SKILLS[@]}"; do check "skills/$s/SKILL.md"; done

log ""
if [ "$fail" -eq 0 ]; then
  log "done. restore any file with: cp $BACKUP/<path> $DEST/<path>"
  log "next: ./probe-config.sh   # confirm key names against your build"
else
  log "done with failures. backups at $BACKUP"
  exit 1
fi
