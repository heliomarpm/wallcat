

from pathlib import Path
import typer

from loguru import logger

from wallcat.core.rules import RuleClassifier
from wallcat.core.organizer import Organizer
from wallcat.core.ai.clip import ClipClassifier

app = typer.Typer(help="Wallcat - Organizador inteligente de wallpapers")


    # path: Path = typer.Argument(..., help="Folder with wallpapers"),
    # config: Path = typer.Option(
    #     Path("config/categories.yaml"), help="Categories config file"
    # ),
    # plan: bool = typer.Option(False, help="Dry run"),
    # apply: bool = typer.Option(False, help="Apply changes"),
    # ai: bool = typer.Option(False, help="Use AI as fallback"),
    # ai_only: bool = typer.Option(False, help="Use only AI"),


@app.command()
def run(
    path: Path = typer.Argument(..., help="Pasta com imagens"),
    config: Path = typer.Option(Path("config/categories.yaml"), help="Arquivo YAML de regras"),
    plan: bool = typer.Option(False, "--plan", help="Dry-run (não move arquivos)"),
    apply: bool = typer.Option(False, "--apply", help="Executar movimentação"),
    ai: bool = typer.Option(False, "--ai", help="Habilitar IA como fallback"),
    ai_only: bool = typer.Option(False, "--ai-only", help="Usar apenas IA"),
    min_confidence: float = typer.Option(0.30, "--min-confidence", help="Confiança mínima da IA"),
):
    dry_run = plan or not apply

    # Sempre carregamos o YAML para obter categorias
    rules = RuleClassifier(config)
    rule_classifier = None if ai_only else rules

    ai_classifier = None
    if ai or ai_only:
        categories = list(rules.rules.keys())
        if not categories:
            raise typer.BadParameter(
                "Arquivo de categorias está vazio — IA precisa de ao menos uma categoria."
            )

        ai_classifier = ClipClassifier(categories)

    organizer = Organizer(
        base_path=path,
        rule_classifier=rule_classifier,
        ai_classifier=ai_classifier,
        use_ai=ai,
        ai_only=ai_only,
        min_confidence=min_confidence,
        dry_run=dry_run,
    )

    organizer.run()
