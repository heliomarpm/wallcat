from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ClassificationResult:
    file: Path
    category: str
    rule: str | None
    confidence: float
