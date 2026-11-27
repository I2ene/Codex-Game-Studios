#!/usr/bin/env bash
# references-save.sh — save explicitly accessible supplied images, without private host logs.
# Usage: bash .game-studio/scripts/references-save.sh FILE... [--root DIR]
# Numeric paste references return not_assessed; ask for accessible attachments instead.
# Output: saved|kept references/<name> <input>, missing <input>, or not_assessed <why>.
# Exits: 0 saved/kept; 2 bad input; 3 inaccessible host paste; 4 a file is missing.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
. "$HERE/native-runtime.sh"
ROOT="$HERE/../.."
FILES=()
while [ $# -gt 0 ]; do
  case "$1" in
    --root) [ $# -ge 2 ] || exit 2; ROOT="$2"; shift 2 ;;
    -h|--help) sed -n '2,7p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -?*) echo "references-save: unknown argument $1" >&2; exit 2 ;;
    *) FILES[${#FILES[@]}]="$1"; shift ;;
  esac
done
gs_native references "${FILES[@]}" --root "$ROOT"
