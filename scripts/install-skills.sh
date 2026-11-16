#!/usr/bin/env bash
# Link every authored skill into each client's skill directory.
#
# Destinations:
#   ~/.agents/skills      read by Codex and OpenCode
#   ~/.claude/skills      read by Claude Code
#   ~/.codex/agents       personal Codex custom agents
#
# Safe by construction: existing directories, files, and unrelated links are
# never replaced. Blocked paths are reported and the script exits non-zero while
# still linking everything that is safe.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skill_targets=("${HOME}/.agents/skills" "${HOME}/.claude/skills")
agent_target="${HOME}/.codex/agents"
dry_run=false
prune=false

usage() {
  echo 'Usage: install-skills.sh [--dry-run] [--prune]'
  echo '  --dry-run  Show the plan without writing'
  echo '  --prune    Remove links that point into this repo but are no longer authored'
}

for arg in "$@"; do
  case "${arg}" in
    --dry-run) dry_run=true ;;
    --prune) prune=true ;;
    --help|-h) usage; exit 0 ;;
    *) echo "Unknown option: ${arg}" >&2; usage >&2; exit 2 ;;
  esac
done

skill_names=()
skill_sources=()

add_skill() {
  skill_names+=("$(basename "$1")")
  skill_sources+=("$1")
}

for dir in "${repo_root}"/skills/*/; do
  [[ -f "${dir}SKILL.md" ]] || continue
  add_skill "${dir%/}"
done
for dir in "${repo_root}"/plugins/*/skills/*/; do
  [[ -f "${dir}SKILL.md" ]] || continue
  add_skill "${dir%/}"
done

status=0
for ((i = 0; i < ${#skill_names[@]}; i++)); do
  for ((j = i + 1; j < ${#skill_names[@]}; j++)); do
    if [[ "${skill_names[$i]}" == "${skill_names[$j]}" ]]; then
      echo "Duplicate skill name '${skill_names[$i]}':" >&2
      echo "  ${skill_sources[$i]}" >&2
      echo "  ${skill_sources[$j]}" >&2
      status=1
    fi
  done
done
if [[ ${status} -ne 0 ]]; then
  echo 'Rename one of the duplicates; a client resolves one folder per name.' >&2
  exit 1
fi

names=()
sources=()
targets=()

for target_root in "${skill_targets[@]}"; do
  for ((i = 0; i < ${#skill_names[@]}; i++)); do
    names+=("${skill_names[$i]}")
    sources+=("${skill_sources[$i]}")
    targets+=("${target_root}/${skill_names[$i]}")
  done
done
skill_target_count=${#targets[@]}

for source_path in "${repo_root}"/agents/codex/*.toml; do
  [[ -f "${source_path}" ]] || continue
  names+=("$(basename "${source_path}" .toml)")
  sources+=("${source_path}")
  targets+=("${agent_target}/$(basename "${source_path}")")
done

blocked=()
pending=()
already=0

for ((i = 0; i < ${#targets[@]}; i++)); do
  target_path="${targets[$i]}"
  source_path="${sources[$i]}"

  parent_path="${target_path%/*}"
  parent_ok=true
  while [[ -n "${parent_path}" ]]; do
    if [[ -n "${parent_path}" && "${parent_path}" != / ]] \
       && [[ ( -e "${parent_path}" || -L "${parent_path}" ) && ! -d "${parent_path}" ]]; then
      blocked+=("${target_path} (parent is not a directory)")
      parent_ok=false
      break
    fi
    [[ "${parent_path}" == / ]] && break
    parent_path="${parent_path%/*}"
  done
  ${parent_ok} || continue

  if [[ -L "${target_path}" && "$(readlink "${target_path}")" == "${source_path}" ]]; then
    already=$((already + 1))
    continue
  fi
  if [[ -e "${target_path}" || -L "${target_path}" ]]; then
    if [[ -L "${target_path}" && "$(readlink "${target_path}")" == "${repo_root}"/* ]]; then
      blocked+=("${target_path} (stale link; rerun with --prune)")
    else
      blocked+=("${target_path} (existing path is not this repo's link)")
    fi
    continue
  fi
  pending+=("${i}")
done

for ((k = 0; k < ${#pending[@]}; k++)); do
  index="${pending[$k]}"
  target_path="${targets[$index]}"
  if ${dry_run}; then
    echo "Would link: ${target_path} -> ${sources[$index]}"
  else
    mkdir -p "${target_path%/*}"
    ln -s "${sources[$index]}" "${target_path}"
    echo "Linked: ${target_path} -> ${sources[$index]}"
  fi
done

if ${prune}; then
  for target_root in "${skill_targets[@]}"; do
    [[ -d "${target_root}" ]] || continue
    for entry in "${target_root}"/* "${target_root}"/.[!.]* "${target_root}"/..?*; do
      [[ -L "${entry}" ]] || continue
      link_target="$(readlink "${entry}")"
      [[ "${link_target}" == "${repo_root}"/* ]] || continue
      keep=false
      for ((i = 0; i < skill_target_count; i++)); do
        if [[ "${targets[$i]}" == "${entry}" ]]; then
          keep=true
          break
        fi
      done
      ${keep} && continue
      if ${dry_run}; then
        echo "Would prune: ${entry}"
      else
        rm "${entry}"
        echo "Pruned: ${entry}"
      fi
    done
  done
fi

if ${dry_run}; then
  echo "Plan: ${already} already linked, ${#pending[@]} to link, ${#blocked[@]} blocked."
else
  echo "Plan: ${already} already linked, ${#pending[@]} linked, ${#blocked[@]} blocked."
fi

if [[ ${#blocked[@]} -gt 0 ]]; then
  echo
  echo 'Blocked destinations (existing paths were not touched):'
  for item in "${blocked[@]}"; do
    echo "  ${item}"
  done
  echo
  echo 'Resolve each deliberately: remove an unrelated copy, or rename the skill.'
  exit 1
fi

echo 'Skills are linked for Codex, OpenCode, and Claude Code. Run scripts/verify-discovery.py to confirm.'
