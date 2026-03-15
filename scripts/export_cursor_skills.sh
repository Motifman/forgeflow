#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "usage: $0 /path/to/project"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PROJECT_DIR="$(cd "$1" && pwd)"
TARGET_DIR="${PROJECT_DIR}/.cursor/skills"

mkdir -p "${TARGET_DIR}"
rm -rf "${TARGET_DIR}/flow-idea" \
       "${TARGET_DIR}/flow-plan" \
       "${TARGET_DIR}/flow-exec" \
       "${TARGET_DIR}/flow-review" \
       "${TARGET_DIR}/flow-ship" \
       "${TARGET_DIR}/flow-status" \
       "${TARGET_DIR}/flow-doctor"

cp -R "${REPO_ROOT}/targets/cursor/skills/." "${TARGET_DIR}/"
echo "exported cursor skills to ${TARGET_DIR}"
