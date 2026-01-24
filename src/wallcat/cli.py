import click

@click.group()
def cli():
    """Wallcat - Wallpaper Catalog & Classifier"""
    pass

@cli.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False))
@click.option("--mode", default="hybrid", type=click.Choice(["rules", "ai", "hybrid"]))
def classify(path, mode):
    click.echo(f"Classifying wallpapers in {path} using {mode} mode")
