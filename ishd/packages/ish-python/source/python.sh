#!/usr/bin/env bash

# ish-python: local package for honiipy's python dev verbs. the dev half of the
# project tooling; the cli pass-through is ish-honiipy. each verb cds the package
# and calls uv run (uv auto-syncs the workspace, enforcing venv discipline).

_ish_python_root="${ISH_PROJECT_ROOT}/python/honiipy"
_ish_python_source="source/honiipy"
_ish_python_tests="tests"

ish_python_help() {
  ish_stream_multiline_stderr <<EOF
usage: ish python <command>

commands:
  lint     ruff check + format --check on source and tests
  fmt      ruff format on source and tests
  fix      ruff check --fix on source and tests
  test     pytest on honiipy
  laconic  laconic size + structure checks on source
  audit    lint + test + laconic
  help     show this help message
EOF
}

ish_python_lint() {
  ish_exists_executable --executable=uv \
    || ish_tui_message_error --message="python: uv required"
  cd "${_ish_python_root}" \
    && uv run ruff check "${_ish_python_source}" "${_ish_python_tests}" \
    && uv run ruff format --check "${_ish_python_source}" "${_ish_python_tests}"
}

ish_python_fmt() {
  ish_exists_executable --executable=uv \
    || ish_tui_message_error --message="python: uv required"
  cd "${_ish_python_root}" \
    && uv run ruff format "${_ish_python_source}" "${_ish_python_tests}"
}

ish_python_fix() {
  ish_exists_executable --executable=uv \
    || ish_tui_message_error --message="python: uv required"
  cd "${_ish_python_root}" \
    && uv run ruff check --fix "${_ish_python_source}" "${_ish_python_tests}"
}

ish_python_test() {
  ish_exists_executable --executable=uv \
    || ish_tui_message_error --message="python: uv required"
  cd "${_ish_python_root}" \
    && uv run pytest --cov=honiipy --cov-report= --cov-fail-under=90 \
       -q --tb=short -rf --no-header "${_ish_python_tests}" "$@"
}

ish_python_laconic() {
  ish_exists_executable --executable=uv \
    || ish_tui_message_error --message="python: uv required"
  cd "${_ish_python_root}" \
    && uv run laconic check --source="${_ish_python_source}" "$@"
}

ish_python_audit() {
  local failed=0
  ish_python_lint || failed=1
  ish_python_test || failed=1
  ish_python_laconic || failed=1
  return "${failed}"
}

ish_python_route() {
  case "${1-}" in
    lint)    shift; ish_python_lint "$@" ;;
    fmt)     shift; ish_python_fmt "$@" ;;
    fix)     shift; ish_python_fix "$@" ;;
    test)    shift; ish_python_test "$@" ;;
    laconic) shift; ish_python_laconic "$@" ;;
    audit)   shift; ish_python_audit "$@" ;;
    help|"") ish_python_help ;;
    *)
      ish_python_help
      ish_tui_message_error --message="unknown command: ${1-}"
      ;;
  esac
}
