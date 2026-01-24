from pathlib import Path
from loguru import logger

from .rules import RuleClassifier
from .ai.base import AIClassifier


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".jfif", ".bmp"}


class Organizer:
    def __init__(
        self,
        base_path: Path,
        rule_classifier: RuleClassifier | None,
        ai_classifier: AIClassifier | None,
        use_ai: bool,
        ai_only: bool,
        min_confidence: float,
        dry_run: bool,
    ):
        self.base_path = base_path
        self.rule_classifier = rule_classifier
        self.ai_classifier = ai_classifier
        self.use_ai = use_ai
        self.ai_only = ai_only
        self.min_confidence = min_confidence
        self.dry_run = dry_run

    def run(self):
        for file in self.base_path.iterdir():
            if not file.is_file() or file.suffix.lower() not in IMAGE_EXTENSIONS:
                continue

            category = None

            # 1️⃣ Regras por nome
            if self.rule_classifier and not self.ai_only:
                category = self.rule_classifier.classify(file)
                if category:
                    logger.success(f"[RULE] {file.name} -> {category}")

            # 2️⃣ IA
            if (not category and self.use_ai) or self.ai_only:
                if not self.ai_classifier:
                    raise RuntimeError("AI habilitada mas nenhum classificador foi configurado")

                ai_category, confidence = self.ai_classifier.classify(file)

                if confidence >= self.min_confidence:
                    category = ai_category
                    logger.success(f"[AI] {file.name} -> {category} ({confidence:.2f})")
                else:
                    logger.info(f"[AI] {file.name} -> _Unclassified ({confidence:.2f})")

            if not category:
                category = "_Unclassified"

            self._move(file, category)

    def _move(self, file: Path, category: str):
        target_dir = self.base_path / category
        target_dir.mkdir(exist_ok=True)

        target = target_dir / file.name

        if self.dry_run:
            logger.info(f"[PLAN] {file.name} -> {category}/")
            return

        file.rename(target)
