#!/usr/bin/env bash

_common_setup() {
  local test_helper_dir
  test_helper_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

  export ISH_ROOT="$(ish root)"
  export ISH_CORE="${ISH_ROOT}/core"
  export ISH_BIN="${ISH_ROOT}/core/bin/ish"

  load "${test_helper_dir}/bats-support/load"
  load "${test_helper_dir}/bats-assert/load"
}
