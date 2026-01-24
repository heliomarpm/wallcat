from pathlib import Path
import yaml


class RuleClassifier:
    def __init__(self, config_path: Path):
        with Path.open(config_path, "r", encoding="utf-8") as f:
            self.rules: dict[str, list[str]] = yaml.safe_load(f) or {}

    def classify(self, file_path: Path) -> str | None:
        name = file_path.stem.lower()

        for category, keywords in self.rules.items():
            for kw in keywords:
                if kw.lower() in name:
                    return category

        return None
