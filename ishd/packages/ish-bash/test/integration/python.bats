#!/usr/bin/env bats

setup() {
  load '../test_helper/common-setup'
  _common_setup
}

@test "ish python help lists verbs" {
  run "${ISH_BIN}" python help
  assert_success
  assert_output --partial "lint"
  assert_output --partial "fmt"
  assert_output --partial "fix"
  assert_output --partial "test"
  assert_output --partial "audit"
}

@test "ish python no args shows help" {
  run "${ISH_BIN}" python
  assert_success
  assert_output --partial "usage: ish python"
}

@test "ish python unknown command errors" {
  run "${ISH_BIN}" python bogus
  assert_failure
  assert_output --partial "unknown command"
}
