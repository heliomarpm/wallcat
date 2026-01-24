from pathlib import Path
import re

import click
from loguru import logger

from wallcat.core.organizer import organize_wallpapers


@click.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False), required=True)
@click.option("--config", "-c", default="config/categories.yaml", show_default=True, help="Path to categories configuration file")
@click.option("--plan", is_flag=True, help="Show classification plan without moving files")
@click.option("--apply", is_flag=True, help="Apply classification and move files")
@click.option("--min-confidence", default=0.0, show_default=True, type=float, help="Minimum confidence required to include a file")
def cli(path, config, plan, apply, min_confidence):
    """
    Organize wallpapers in PATH based on filename rules.
    """

    base_path = Path(path)
    config_path = Path(config)

    # UX rule: default behavior = apply
    if not plan and not apply:
        apply = True

    logger.info("Target folder: {}", base_path)
    logger.info("Config file: {}", config_path)
    logger.info("Plan: {}", plan)
    logger.info("Apply: {}", apply)

    organize_wallpapers(
        base_path=base_path,
        config_path=config_path,
        plan=plan,
        apply=apply,
        min_confidence=min_confidence,
    )
