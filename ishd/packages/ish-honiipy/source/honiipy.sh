#!/usr/bin/env bash

# ish-honiipy: consumer pass-through for the honiipy python CLI. invokes
# `uv run honiipy` (the script registered via [project.scripts]) against the
# workspace member via --project, not cd, so a relative image path resolves
# from the caller's cwd (uv run still auto-syncs the workspace). dev verbs
# live under ish python / ish bash.

_ish_honiipy_root="${ISH_PROJECT_ROOT}/python/honiipy"

ish_honiipy_route() {
  ish_exists_executable --executable=uv \
    || ish_tui_message_error --message="honiipy: uv required"
  if [[ "${1-}" == "help" ]]; then
    set -- "--help" "${@:2}"
  fi
  uv run --project "${_ish_honiipy_root}" honiipy "$@"
}
