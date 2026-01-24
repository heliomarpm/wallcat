"""Example CLI tool showcasing the usage of click, loglevels and error handling.

It is designed to be used as a template for creating new DCSimCLI tools and see the example function
below for more information.
"""

import importlib.metadata
import shutil
import sys
from typing import Any

import click
import rich.pretty
import rich.traceback
from loguru import logger

pp = rich.pretty.pprint
rich.traceback.install(
  width=shutil.get_terminal_size().columns,
  code_width=160,
  show_locals=True,
  suppress=[click],
)

_log_ids: list[int] = []  # IDs of loggers if initialized
_last_message: Any = None  # Store the last logged message to allow duplication filtering


def init_logger(**kwargs) -> None:  # noqa: ANN003
  """Initialize and customize the standard DCSim logger.

  This function sets up a default Loguru logger with options for custom configuration. It ensures that the logger is initialized only once. By default,
  it logs to `sys.stderr` with a standardized format and includes a filter to prevent duplicate log messages.

  The function allows for extensive customization through keyword arguments, which are directly passed to `loguru.logger.add()`. This enables users to
  specify custom sinks, formats, filters, and other `loguru` configurations as needed.

  Note: The logger is initialized only once. Subsequent calls to this function will issue a warning but will not reconfigure the logger or add new handlers.

  Args:
      **kwargs: Keyword arguments that are passed directly to `loguru.logger.add()`.
          This provides a flexible way to configure the logger. Common arguments include:
          - sink   : Logging destination. Can be a file path, a stream like `sys.stderr`, or a custom handler. Defaults to `sys.stderr`.
          - format : The default format includes timestamp, log level, module name, line number, function name, and log message.
          - filter : Default filter prevents consecutive duplicate messages from being logged.
          - level  : The minimum log level to be processed (e.g., "DEBUG", "INFO").
          - Any other options supported by `loguru.logger.add()`.
  """
  # Only initialize the standard logger once
  global _log_ids
  if _log_ids:
    print("_log_ids not empty")
    return

  # Default sink to stderr
  if "sink" not in kwargs:
    kwargs["sink"] = sys.stderr

  # Default level at INFO
  if "level" not in kwargs:
    kwargs["level"] = "INFO"

  # Default standardized format
  if "format" not in kwargs:
    kwargs["format"] = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{module}.py:{line}</cyan> <blue>{function}:</blue> "
            "<level>{extra[tag]} {message}</level>"
        )  # fmt: off

  # Default de-duplication filter
  if "filter" not in kwargs:

    def deduplicate_logs(record) -> bool:  # noqa: ANN001
      """Custom log filter function to prevent duplicate log messages."""
      message: Any = record["message"]
      global _last_message

      if message == _last_message:
        return False
      _last_message = message
      return True

    kwargs["filter"] = deduplicate_logs

  # Configure default logger with our defaults and any modified keyword arguments
  _log_ids = logger.configure(handlers=[kwargs], extra={"tag": ""})  # type: ignore


@click.command()
@click.option("--name", prompt="Your name", help="The person to greet.")
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--fail", is_flag=True, help="Flag to show how errors are handled.")
@click.option("--loglevel", default="INFO", show_default=True, help="Set log level (ERROR, WARNING, INFO, DEBUG, TRACE)")
def example(count: int, name: str, fail: bool, loglevel: str) -> None:
  """Simple program that greets NAME for a total of COUNT times.

  This CLI tool is used to demonstrate and standardize the usage of click, log levels, and error
  handling.  It's a simple tool that greets a user for a given number of times and also showcases
  how to use the `@logger.catch()` decorator to handle errors.
  """
  print(f"Project Starter v{importlib.metadata.version(distribution_name='project_starter')} - Example CLI Tool\n")
  init_logger(level=loglevel)

  assert not fail, "Showcasing error handling"

  logger.debug("Project Starter v{version} - Example CLI Tool")
  for n in range(count):
    logger.info(f"Hello {name}! {n}")


if __name__ == "__main__":
  example()
