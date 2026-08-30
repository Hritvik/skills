#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skill_target="${HOME}/.agents/skills"
agent_target="${HOME}/.codex/agents"

mkdir -p "${skill_target}" "${agent_target}"

link_children() {
  local source_dir="$1"
  local target_dir="$2"
  local pattern="$3"

  if [[ ! -d "${source_dir}" ]]; then
    return
  fi

  while IFS= read -r source_path; do
    local name
    name="$(basename "${source_path}")"
    local target_path="${target_dir}/${name}"

    if [[ -e "${target_path}" && ! -L "${target_path}" ]]; then
      echo "Refusing to replace non-symlink: ${target_path}" >&2
      exit 1
    fi

    ln -sfn "${source_path}" "${target_path}"
    echo "Linked ${target_path}"
  done < <(find "${source_dir}" -mindepth 1 -maxdepth 1 -name "${pattern}" -print | sort)
}

link_children "${repo_root}/skills" "${skill_target}" "*"
link_children "${repo_root}/agents/codex" "${agent_target}" "*.toml"

echo
echo "Standalone skills and custom agents are linked."
echo "Register plugins once with:"
echo "  codex plugin marketplace add \"${repo_root}/.agents/plugins\""
echo "Then install a plugin, for example:"
echo "  codex plugin add decision-guide@hritvik-skills"
