#!/usr/bin/env bash

# ish-bash: local package for honiipy's bash dev verbs. lints, formats, and
# tests the listed ish wrapper bash sources with shellcheck,
# shfmt, and the bats submodules vendored under this package's test/.

_ish_bash_bats_root="${ISH_PROJECT_ROOT}/ishd/packages/ish-bash/test"

ish_bash_help() {
  ish_stream_multiline_stderr <<EOF
usage: ish bash <command>

commands:
  lint     shellcheck on bash sources
  fmt      shfmt -d (diff; non-mutating)
  fix      shfmt -w (write; format in place)
  test     bats integration tests
  audit    lint + test
  help     show this help message
EOF
}

_ish_bash_sources() {
  find \
    "${ISH_PROJECT_ROOT}/ishd/packages/ish-python/source" \
    "${ISH_PROJECT_ROOT}/ishd/packages/ish-bash/source" \
    "${ISH_PROJECT_ROOT}/ishd/packages/ish-honiipy/source" \
    -name '*.sh' -print0
}

ish_bash_lint() {
  ish_exists_executable --executable=shellcheck \
    || ish_tui_message_error --message="bash: shellcheck required"
  _ish_bash_sources | xargs -0 shellcheck
}

ish_bash_fmt() {
  ish_exists_executable --executable=shfmt \
    || ish_tui_message_error --message="bash: shfmt required"
  _ish_bash_sources | xargs -0 shfmt -d
}

ish_bash_fix() {
  ish_exists_executable --executable=shfmt \
    || ish_tui_message_error --message="bash: shfmt required"
  _ish_bash_sources | xargs -0 shfmt -w
}

ish_bash_test() {
  local bats="${_ish_bash_bats_root}/bats/bin/bats"
  [[ -x "${bats}" ]] || ish_tui_message_error \
    --message="bash: bats submodule missing at ${bats}"
  "${bats}" --recursive "${_ish_bash_bats_root}/integration/"
}

ish_bash_audit() {
  local failed=0
  ish_bash_lint || failed=1
  ish_bash_test || failed=1
  return "${failed}"
}

ish_bash_route() {
  case "${1-}" in
    lint)    shift; ish_bash_lint "$@" ;;
    fmt)     shift; ish_bash_fmt "$@" ;;
    fix)     shift; ish_bash_fix "$@" ;;
    test)    shift; ish_bash_test "$@" ;;
    audit)   shift; ish_bash_audit "$@" ;;
    help|"") ish_bash_help ;;
    *)
      ish_bash_help
      ish_tui_message_error --message="unknown command: ${1-}"
      ;;
  esac
}
