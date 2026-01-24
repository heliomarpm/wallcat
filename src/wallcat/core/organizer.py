from pathlib import Path

from loguru import logger

from wallcat.core.models import ClassificationResult
from wallcat.core.rules import RuleEngine

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".jfif"}


def organize_wallpapers(
    base_path: Path,
    config_path: Path,
    plan: bool = False,
    apply: bool = False,
    min_confidence: float = 0.0,
) -> list[ClassificationResult]:
    rule_engine = RuleEngine(config_path)
    results: list[ClassificationResult] = []

    for file_path in base_path.iterdir():
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        result = rule_engine.classify(file_path)

        if result.confidence < min_confidence:
            continue

        results.append(result)

    if plan:
        _print_plan(results)
        return results

    if apply:
        _apply_plan(base_path, results)
        return results

    return results


def _print_plan(results: list[ClassificationResult]) -> None:
    logger.info("[PLAN]")
    for r in results:
        logger.info(
            "{} -> {} (rule={}, confidence={})",
            r.file.name,
            r.category,
            r.rule,
            r.confidence,
        )


def _apply_plan(base_path: Path, results: list[ClassificationResult]) -> None:
    for r in results:
        target_dir = base_path / r.category
        target_dir.mkdir(exist_ok=True)

        target_file = target_dir / r.file.name

        if target_file.exists():
            logger.warning("File already exists, skipping: {}", target_file)
            continue

        logger.info("{} -> {}", r.file.name, r.category)
        r.file.rename(target_file)
