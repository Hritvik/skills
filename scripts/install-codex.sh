#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skill_target="${HOME}/.agents/skills"
agent_target="${HOME}/.codex/agents"
dry_run=false
case "${1:-}" in
  --dry-run) dry_run=true; shift ;;
  --help|-h) echo 'Usage: install-codex.sh [--dry-run]'; exit 0 ;;
esac
if [[ $# -ne 0 ]]; then
  echo 'Usage: install-codex.sh [--dry-run]' >&2
  exit 2
fi

sources=()
targets=()
for source_path in "${repo_root}"/skills/*; do
  [[ -d "${source_path}" && -f "${source_path}/SKILL.md" ]] || continue
  sources+=("${source_path}")
  targets+=("${skill_target}/$(basename "${source_path}")")
done
for source_path in "${repo_root}"/agents/codex/*.toml; do
  [[ -f "${source_path}" ]] || continue
  sources+=("${source_path}")
  targets+=("${agent_target}/$(basename "${source_path}")")
done

# Preflight the entire plan before creating directories or links.
for ((i=0; i<${#sources[@]}; i++)); do
  target_path="${targets[$i]}"
  parent_path="$(dirname "${target_path}")"
  while [[ "${parent_path}" != / ]]; do
    if [[ ( -e "${parent_path}" || -L "${parent_path}" ) && ! -d "${parent_path}" ]]; then
      echo "Destination parent is not a directory: ${parent_path}" >&2
      exit 1
    fi
    parent_path="$(dirname "${parent_path}")"
  done
  if [[ -L "${target_path}" && "$(readlink "${target_path}")" == "${sources[$i]}" ]]; then
    continue
  fi
  if [[ -e "${target_path}" || -L "${target_path}" ]]; then
    echo "Refusing to replace existing path: ${target_path}" >&2
    exit 1
  fi
done

for ((i=0; i<${#sources[@]}; i++)); do
  target_path="${targets[$i]}"
  if [[ -L "${target_path}" ]]; then
    echo "Already linked: ${target_path}"
  elif ${dry_run}; then
    echo "Would link: ${target_path} -> ${sources[$i]}"
  else
    mkdir -p "$(dirname "${target_path}")"
    ln -s "${sources[$i]}" "${target_path}"
    echo "Linked: ${target_path}"
  fi
done

echo 'Shared skills use ~/.agents/skills; Codex agents use ~/.codex/agents.'
echo 'Plugin installation is separate; see README.md for marketplace instructions.'
