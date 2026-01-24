import yaml
from pathlib import Path
from loguru import logger
from wallcat.core.models import ClassificationResult


class RuleEngine:
    def __init__(self, config_path: Path):
        self.rules = self._load_rules(config_path)

    def _load_rules(self, path: Path) -> dict[str, list[str]]:
        logger.debug("Loading rules from {}", path)

        with path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if "categories" not in data:
            raise ValueError("Invalid config file: missing 'categories' key")

        return data["categories"]

    def classify(self, file_path: Path) -> ClassificationResult:
        filename = file_path.stem.lower()

        for category, keywords in self.rules.items():
            for keyword in keywords:
                if keyword.lower() in filename:
                    logger.debug(
                        "Rule matched: {} -> {} (keyword: {})",
                        file_path.name,
                        category,
                        keyword,
                    )
                    return ClassificationResult(
                        file=file_path,
                        category=category,
                        rule=keyword,
                        confidence=1.0,
                    )

        return ClassificationResult(
            file=file_path,
            category="_Unclassified",
            rule=None,
            confidence=0.0,
        )
