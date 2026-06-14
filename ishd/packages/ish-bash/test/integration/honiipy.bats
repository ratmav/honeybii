#!/usr/bin/env bats

setup() {
  load '../test_helper/common-setup'
  _common_setup
}

@test "ish honiipy no args shows typer help" {
  run "${ISH_BIN}" honiipy
  assert_failure 2
  assert_output --partial "Usage:"
}

@test "ish honiipy help shows typer help" {
  run "${ISH_BIN}" honiipy help
  assert_success
  assert_output --partial "Usage:"
}
