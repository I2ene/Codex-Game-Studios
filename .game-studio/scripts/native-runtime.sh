#!/usr/bin/env bash
# Native configuration/path boundary shared by the reused shell algorithms.
# Set GAME_STUDIO_PYTHON to an interpreter with the installed requirements.
_gs_here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
gs_python() {
  if [ -n "${GAME_STUDIO_PYTHON:-}" ]; then "$GAME_STUDIO_PYTHON" "$@"; return $?; fi
  local p
  for p in python3 python; do
    if command -v "$p" >/dev/null 2>&1 && "$p" -c 'import sys,yaml; sys.exit(sys.version_info < (3,11))' >/dev/null 2>&1; then
      "$p" "$@"; return $?
    fi
  done
  echo 'Game Studios: choose Python 3.11+ with requirements via GAME_STUDIO_PYTHON.' >&2
  return 2
}
gs_native() { gs_python "$_gs_here/../runtime/shell_bridge.py" "$@"; }
gs_get() { gs_native get "$1" --root "${ROOT:-$PWD}"; }
gs_argv() { gs_native argv "$1" --root "${ROOT:-$PWD}"; }
gs_clean() { gs_native clean --root "${ROOT:-$PWD}"; }
gs_path() { gs_native path "$1" --root "${ROOT:-$PWD}" >/dev/null; }
gs_tree() { gs_native tree "$1" --root "${ROOT:-$PWD}" >/dev/null; }
