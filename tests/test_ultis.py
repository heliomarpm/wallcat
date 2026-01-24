import pathlib

import project_starter.example as up


def test_module_relative() -> None:
  assert up.module_relative().is_dir()
  assert up.module_relative("..").is_dir()
  assert not str(up.module_relative("..")).endswith("..")
  assert up.module_relative(f"{__name__}.py") == pathlib.Path(__file__)
