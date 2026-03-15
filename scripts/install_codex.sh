#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SKILLS_DIR="${CODEX_HOME}/skills"
BIN_DIR="${HOME}/.local/bin"

mkdir -p "${SKILLS_DIR}" "${BIN_DIR}"

for skill_dir in "${REPO_ROOT}"/targets/codex/skills/*; do
  skill_name="$(basename "${skill_dir}")"
  target="${SKILLS_DIR}/${skill_name}"
  rm -rf "${target}"
  ln -s "${skill_dir}" "${target}"
  echo "linked codex skill: ${target}"
done

rm -f "${BIN_DIR}/forgeflow"
cat > "${BIN_DIR}/forgeflow" <<EOF
#!/usr/bin/env bash
python3 "${REPO_ROOT}/scripts/forgeflow.py" "\$@"
EOF
chmod +x "${BIN_DIR}/forgeflow"

echo "installed forgeflow CLI to ${BIN_DIR}/forgeflow"
echo "add ${BIN_DIR} to PATH if needed"
