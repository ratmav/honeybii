#!/usr/bin/env bats

setup() {
  load '../test_helper/common-setup'
  _common_setup
}

@test "ish bash help lists verbs" {
  run "${ISH_BIN}" bash help
  assert_success
  assert_output --partial "lint"
  assert_output --partial "fmt"
  assert_output --partial "fix"
  assert_output --partial "test"
  assert_output --partial "audit"
}

@test "ish bash no args shows help" {
  run "${ISH_BIN}" bash
  assert_success
  assert_output --partial "usage: ish bash"
}

@test "ish bash unknown command errors" {
  run "${ISH_BIN}" bash bogus
  assert_failure
  assert_output --partial "unknown command"
}
