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

@test "ish honiipy convert resolves a relative path from the caller's cwd" {
  local img="test/images/snake.jpg"
  cd "${ISH_PROJECT_ROOT}"
  run "${ISH_BIN}" honiipy convert "${img}"
  assert_success
  [ -n "${output}" ]
  local from_relative="${output}"
  run "${ISH_BIN}" honiipy convert "${ISH_PROJECT_ROOT}/${img}"
  assert_success
  assert_equal "${from_relative}" "${output}"
}
