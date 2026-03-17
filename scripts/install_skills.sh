#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "usage: $0 <codex|cursor> <global|project> [project-path]"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TARGET="$1"
SCOPE="$2"
shift 2

ARGS=(install-skills --target "${TARGET}" --scope "${SCOPE}" -U)

if [ "${SCOPE}" = "project" ]; then
  if [ "$#" -lt 1 ]; then
    echo "project scope requires a project path"
    exit 1
  fi
  PROJECT_DIR="$(cd "$1" && pwd)"
  ARGS+=(--project "${PROJECT_DIR}")
fi

uv run --directory "${REPO_ROOT}" forgeflow "${ARGS[@]}"
