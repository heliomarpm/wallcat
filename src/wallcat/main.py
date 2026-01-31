import shutil
from pathlib import Path

import click
import clip
import torch
import yaml
from loguru import logger
from PIL import Image

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".jfif", ".bmp"}

_model = None
_preprocess = None
_device = "cuda" if torch.cuda.is_available() else "cpu"


def get_clip() -> tuple:
    global _model, _preprocess
    if _model is None:
        logger.opt(colors=True).info(f"Carregando modelo CLIP no dispositivo: <yellow>{_device.upper()}</yellow>")
        # Usando float16 se estiver em GPU para maior velocidade
        _model, _preprocess = clip.load("ViT-B/32", device=_device)
    return _model, _preprocess


def default_categories() -> dict:
    """Retorna um dicionário básico caso o YAML falhe."""
    logger.warning("Usando categorias de fallback.")
    return {
        "Natureza": {
            "prompt": "A peaceful photo of nature, mountains, forests, oceans or green landscapes",
            "keywords": ["nature", "natureza", "landscape", "forest", "mountain", "floresta", "ocean", "beach", "lake"],
        },
        "Tecnologia": {
            "prompt": "A photo of computers, hardware, circuits, electronics or high-tech gadgets",
            "keywords": ["tech", "technology", "setup", "pc", "computer", "hardware", "cpu", "server", "eletronico"],
        },
        "Space": {
            "prompt": "A stunning photo of outer space, stars, galaxies, planets, nebulas or the universe",
            "keywords": ["space", "espaco", "galaxy", "galaxia", "stars", "planet", "planeta", "nebula", "cosmos", "universe"],
        },
        "Cyberpunk": {
            "prompt": "A futuristic city at night with neon lights, rainy streets, and synthwave aesthetics",
            "keywords": ["cyberpunk", "neon", "night-city", "futuristic", "synthwave", "retrowave", "blade-runner"],
        },
        "Minimalista": {
            "prompt": "A minimalist wallpaper with clean lines, simple colors, lots of whitespace and few objects",
            "keywords": ["minimalist", "minimalista", "clean", "simple", "flat", "whitespace"],
        },
        "Anime": {
            "prompt": "A high-quality illustration in Japanese anime, manga art style or studio ghibli style",
            "keywords": ["anime", "manga", "otaku", "fanart", "ghibli", "kawaii", "illustration"],
        },
        "Abstrato": {
            "prompt": "Abstract art with geometric shapes, colorful patterns, liquid textures or 3D renders",
            "keywords": ["abstract", "abstrato", "geometric", "pattern", "liquid", "texture", "shapes", "3d-render"],
        },
        "Arquitetura": {
            "prompt": "A professional photo of modern buildings, skyscrapers, bridges, or urban cityscapes",
            "keywords": ["architecture", "arquitetura", "building", "skyscraper", "cityscape", "bridge", "urban", "monument"],
        },
        "Digital_Art": {
            "prompt": "A digital painting, concept art, fantasy illustration or wallpaper art",
            "keywords": ["digital-art", "concept-art", "painting", "fantasy", "artwork", "deviantart", "vfx"],
        },
        "Ciclismo": {
            "prompt": "A photo of bicycles, BMX bikes, pump tracks, dirt jump parks, or bicycle racing",
            "keywords": ["bmx", "bike", "bicycle", "bicicleta", "cycling", "ciclismo", "freestyle", "pumptrack", "dirtjump", "velodromo"],
        },
        "Cinema": {
            "prompt": "A cinematic shot from a movie, film frame, or movie poster",
            "keywords": ["movie", "film", "cinema", "hollywood", "shot", "poster"],
        },
        "Pos-apocalipse": {
            "prompt": "A wasteland with ruins, destroyed buildings, and post-apocalyptic scenery like Fallout",
            "keywords": ["apocalypse", "apocalipse", "wasteland", "ruins", "ruinas", "destroyed", "decay"],
        },
        "Utopia": {
            "prompt": "A futuristic utopian city with white buildings, green plants, and advanced clean technology",
            "keywords": ["utopia", "utopian", "future", "solarpunk", "advanced", "paradise"],
        },
    }


def load_config(config_path: str) -> dict:
    """Carrega as definições do arquivo YAML com suporte a caminhos relativos."""
    p = Path(config_path)
    if not p.exists():
        logger.error(f"Arquivo não encontrado: <red>{p.absolute()}</red>")
        return default_categories()

    try:
        with open(p, encoding="utf-8") as f:
            config = yaml.safe_load(f)
            return config.get("categories", {}) if config else default_categories()
    except Exception as e:
        logger.error(f"Erro ao processar o YAML: {e}")
        return default_categories()


def obter_categoria_por_nome(nome_arquivo: str, categorias_config: dict) -> dict | None:
    """Verifica se alguma palavra-chave está no nome do arquivo (Modo Rápido)."""
    nome_lower = nome_arquivo.lower()
    for categoria, dados in categorias_config.items():
        keywords = dados.get("keywords", [])
        if any(key in nome_lower for key in keywords):
            return categoria
    return None


@click.group()
def main():
    """Wallcat: IA Wallpaper Cataloger powered by CLIP & Loguru."""
    logger.remove()  # Remove o log padrão para evitar duplicidade no console
    logger.add(lambda msg: click.echo(msg, nl=False), colorize=True, level="INFO")
    logger.add("wallcat.log", rotation="500 MB", level="INFO")


@main.command()
@click.argument("source", type=click.Path(exists=True))
@click.option("--output", "-o", default=None, help="Pasta de destino.")
@click.option("--config", "-c", default="config.yaml", help="Caminho para o arquivo YAML de categorias.")
@click.option("--min-conf", default=0.60, help="Confiança mínima para a IA mover arquivos (0.0 a 1.0)")
@click.option("--dry-run", is_flag=True, help="Simula sem mover arquivos.")
def classify(source: str, output: str, config: str, min_conf: float, dry_run) -> None:
    """Classifica imagens usando busca híbrida: Keywords + IA CLIP."""

    source_path = Path(source).resolve()
    output_path = Path(output).resolve() if output else source_path

    # 1. Preparação
    categorias = load_config(config)
    labels_humanos = list(categorias.keys())
    # Extrai corretamente o campo 'prompt' de cada categoria para o CLIP
    descricoes_ia = [dados.get("prompt", f"a photo of {name}") for name, dados in categorias.items()]

    model, preprocess = get_clip()
    text_inputs = clip.tokenize(descricoes_ia).to(_device)

    arquivos = [f for f in source_path.iterdir() if f.suffix.lower() in IMAGE_EXTENSIONS]

    if not arquivos:
        logger.warning(f"Nenhuma imagem encontrada em: {source_path}")
        return

    logger.opt(colors=True).info(f"Iniciando: <blue>{source_path}</blue> -> <blue>{output_path}</blue>")
    if dry_run:
        logger.opt(colors=True).info("<yellow>MODO SIMULAÇÃO ATIVADO</yellow>")

    # 2. Processamento
    with torch.no_grad():
        for img_path in arquivos:
            try:
                # Evita que o script tente classificar pastas já criadas se o output for o mesmo do source
                if img_path.is_dir():
                    continue

                # --- ESTRATÉGIA 1: KEYWORDS (NOME DO ARQUIVO) ---
                metodo = "undefined"
                confianca = 0
                categoria_final = None
                categoria_final = obter_categoria_por_nome(img_path.name, categorias)
                if categoria_final:
                    metodo = "KEYWORD"

                if not categoria_final:
                    try:
                        image_input = preprocess(Image.open(img_path)).unsqueeze(0).to(_device)
                        logits_per_image, _ = model(image_input, text_inputs)
                        probs = logits_per_image.softmax(dim=-1).cpu().numpy()[0]

                        idx_max = probs.argmax()
                        confianca = probs[idx_max]
                        metodo = f"AI ({confianca:.2%})"
                        categoria_final = labels_humanos[idx_max]

                        if confianca < min_conf:
                            confianca = 0

                    except Exception as e:
                        logger.error(f"IA falhou em classificar o arquivo `{img_path.name}`: {e}")
                        continue

                if confianca < min_conf or not categoria_final:
                    logger.info(f"Ignorado: {img_path.name} -> {categoria_final} ({metodo})")
                    continue

                # -- MOVE FILES --
                if categoria_final:
                    dest_dir = output_path / categoria_final

                    if not dry_run:
                        dest_dir.mkdir(parents=True, exist_ok=True)
                        # Usamos shutil.move para mover o arquivo para a subpasta
                        shutil.move(str(img_path), str(dest_dir / img_path.name))
                        logger.success(f"Organizado: {img_path.name} -> {categoria_final} ({metodo})")
                    else:
                        logger.success(f"[DRY-RUN] {img_path.name} -> {categoria_final} ({metodo})")


            except Exception as e:
                logger.error(f"Falha em {img_path.name}: {e}")

    logger.info("✨ Processo concluído.")


if __name__ == "__main__":
    main()
