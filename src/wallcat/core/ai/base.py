from pathlib import Path
from abc import ABC, abstractmethod


class AIClassifier(ABC):
    @abstractmethod
    def classify(self, image_path: Path) -> tuple[str, float]:
        pass
