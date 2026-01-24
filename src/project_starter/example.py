"""Path, directory, and file utilities."""

import inspect
from os import PathLike
from pathlib import Path
from typing import Final


def module_relative(path: str | PathLike = "") -> Path:
  """Return the provided path as absolute path relative to the directory of the calling module.

  Allows loading files relative to a module's file location which is useful for tests and tools
  that may have required data file and directories to function properly.  Another way is to use
  the constant DCSIM_ROOT, also defined in this module.  It standardizes how we specify paths
  relative to our project rool, regardless where we may move this module.

  Args:
      path: Path relative to function caller.

  Returns:
      Absolute path of given path.
  """
  return (Path(inspect.stack()[1].filename).parent / path).resolve()


DCSIM_ROOT: Final[Path] = module_relative(path="../../..")
"""Absolute path of the root of this project."""
