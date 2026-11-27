#!/usr/bin/env bash
# project-state.sh — TSV bridge to the effective native project facts.
# Usage: bash .game-studio/scripts/project-state.sh [--stage] [--root DIR]
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
. "$HERE/native-runtime.sh"
ROOT="$HERE/../.."
STAGE=()
while [ $# -gt 0 ]; do
  case "$1" in
    --root) [ $# -ge 2 ] || exit 2; ROOT="$2"; shift 2 ;;
    --root=*) ROOT="${1#--root=}"; shift ;;
    --stage) STAGE=(--stage); shift ;;
    -h|--help) sed -n '2,3p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "project-state: unknown argument $1" >&2; exit 2 ;;
  esac
done
gs_native project-state "${STAGE[@]}" --root "$ROOT"
