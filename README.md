<div id="top" align="center">
<h1>
  <!-- <img src="./logo.png" alt="Hybrid WebCache" width="128" /> -->
  <br>🐱 Wallcat <a href="https://navto.me/heliomarpm" target="_blank"><img src="https://navto.me/assets/navigatetome-brand.png" width="32"/></a>

  <!-- [![DeepScan grade][url-deepscan-badge]][url-deepscan] -->
  <!-- [![CodeFactor][url-codefactor-badge]][url-codefactor] -->
  <!-- [![Test][url-test-badge]][url-test] -->
  <!-- [![Coverage][url-coverage-badge]][url-coverage-report] -->

  <!-- [![NPM version][url-npm-badge]][url-npm] -->
  <!-- [![Downloads][url-downloads-badge]][url-downloads] -->

</h1>

<div class="badges">

  [![GitHub Sponsors][url-github-sponsors-badge]][url-github-sponsors]
  [![PayPal][url-paypal-badge]][url-paypal]
  [![Ko-fi][url-kofi-badge]][url-kofi]
  [![Liberapay][url-liberapay-badge]][url-liberapay]
  
</div>
</div>

<!-- # 🐱 Wallcat -->

**Wallpaper Catalog & Classifier**

**Wallcat** é um organizador de papéis de parede inteligente que utiliza Inteligência Artificial (**OpenAI CLIP**) e processamento de linguagem natural para catalogar suas imagens automaticamente.

Diferente de organizadores comuns que dependem apenas de nomes de arquivos, o Wallcat "vê" o conteúdo da imagem e o classifica em categorias semânticas (como _Cyberpunk_, _Minimalista_ ou _Ciclismo_) usando um sistema híbrido de busca.

---

## ✨ Funcionalidades

- **Busca Híbrida**: 1. **Modo Rápido**: Verifica palavras-chave no nome do arquivo. 2. Modo IA: Se não encontrar no nome, utiliza o modelo **CLIP** para analisar a imagem.
- **Configuração via YAML**: Personalize categorias, prompts da IA e palavras-chave sem mexer no código.
- **Logs Inteligentes**: Integração com Loguru para um histórico detalhado e colorido das movimentações.
- **Modo Simulação**: (`--dry-run`): Visualize o que será feito antes de mover qualquer arquivo.
- **Alta Performance**: Otimizado com **uv** e suporte a **GPU (CUDA)** para classificação em segundos.

---

## 🚀 Instalação

Este projeto utiliza o [uv](https://github.com/astral-sh/uv) para gerenciamento de dependências e execução.

1. **Clone o repositório:**

```bash
git clone https://github.com/heliomarpm/wallcat.git
cd wallcat
```

2. **Instale as dependências:**

```bash
uv sync
```

--- 

## 🛠 Configuração (`config.yaml`)

O comportamento do Wallcat é definido por um arquivo **YAML**. Você define a categoria, o que a IA deve buscar nela e quais termos no nome do arquivo ativam o modo rápido.

```yaml
categories:
  Natureza:
    prompt: "A peaceful photo of nature, mountains, forests or oceans"
    keywords: ["nature", "landscape", "forest", "floresta"]
  
  Ciclismo:
    prompt: "a photo of bicycles, bmx bikes, dirt jump tracks, or cycle racing"
    keywords: ["bmx", "bike", "bicycle", "ciclismo"]

  Cyberpunk:
    prompt: "A futuristic city at night with neon lights and rainy streets"
    keywords: ["cyberpunk", "neon", "futuristic"]
```

---

## 📖 Como Usar

### Uso Básico

Para organizar uma pasta de imagens (os arquivos serão movidos para subpastas de acordo com a categoria):

```bash
uv run wallcat "C:\Caminho\Para\Seus\Wallpapers"
```

### Simulação (Dry Run)

Para ver como a IA classificaria suas fotos sem mover nada:

```bash
uv run wallcat "C:\Caminho\Para\Seus\Wallpapers" --dry-run
```

### Ajuste de Confiança

Se a IA estiver sendo muito "permissiva", aumente o nível de confiança mínima (0.0 a 1.0):

```bash
uv run wallcat "C:\Caminho\Para\Seus\Wallpapers" --min-conf 0.8
```

--- 

## ⚙️ Argumentos e Opções

Opção | Descrição | Padrão
-- | -- | --
`SOURCE` | Caminho da pasta com as imagens. | (Obrigatório)
`-o, --output` | Pasta de destino (se omitido, organiza dentro da source). | `None`
`-c, --config` | Caminho para o arquivo YAML de categorias. | `config.yaml`
`--dry-run` | Simula a operação sem mover arquivos. | `False`
`--min-conf` | Nível de confiança mínimo para a IA classificar. | `0.60`

## 🗂️ Example Folder Structure

```shell
wallcat/
├── src/
│   └── wallcat/
│       ├── __init__.py    # Versão do app
│       └── main.py        # Core do sistema
├── config.yaml            # Configurações de IA e Keywords
├── pyproject.toml         # Metadados e dependências (Hatchling/uv)
└── wallcat.log            # Log gerado automaticamente
```

---

## 🤝 Contribuições

Agradecemos suas contribuições! Seja relatando um bug, sugerindo um novo recurso, melhorando a documentação ou enviando uma solicitação de pull request, sua ajuda é muito bem-vinda.

Por favor, certifique-se de ler antes de enviar uma solicitação de pull request:

- [Código de Conduta](docs/CODE_OF_CONDUCT.md)
- [Guia de Contribuição](docs/CONTRIBUTING.md)

Agradecemos a todos que já contribuíram para o projeto!

<a href="https://github.com/heliomarpm/wallcat/graphs/contributors" target="_blank">
  <img src="https://contrib.nn.ci/api?repo=heliomarpm/wallcat&no_bot=true" />
</a>

###### Made with [contrib.nn](https://contrib.nn.ci/?repo=heliomarpm/wallcat&no_bot=true).

Dito isso, existem várias maneiras de você contribuir com este projeto, como:

⭐ Favoritar o repositório \
🐞 Reportar bugs \
💡 Sugerir recursos \
🧾 Melhorar a documentação \
📢 Compartilhar este projeto e recomendá-lo aos seus amigos

## 💵 Apoie o Projeto

Se você gostou, considere fazer uma doação para o desenvolvedor através do GitHub Sponsors, Ko-fi, PayPal ou Liberapay. Você decide. 😉

<div class="badges">

  [![GitHub Sponsors][url-github-sponsors-badge]][url-github-sponsors]
  [![PayPal][url-paypal-badge]][url-paypal]
  [![Ko-fi][url-kofi-badge]][url-kofi]
  [![Liberapay][url-liberapay-badge]][url-liberapay]

</div>

## 📝 Licença

Distribuído sob a licença **MIT**. Veja [LICENSE](LICENSE) para mais informações.

---
por [© Heliomar P. Marques](LICENSE) <a href="#top">🔝</a>

---

<!-- Sponsor badges -->
[url-github-sponsors-badge]: https://img.shields.io/badge/GitHub%20-Sponsor-1C1E26?style=for-the-badge&labelColor=1C1E26&color=db61a2
[url-github-sponsors]: https://github.com/sponsors/heliomarpm
[url-paypal-badge]: https://img.shields.io/badge/donate%20on-paypal-1C1E26?style=for-the-badge&labelColor=1C1E26&color=0475fe
[url-paypal]: https://bit.ly/paypal-sponsor-heliomarpm
[url-kofi-badge]: https://img.shields.io/badge/kofi-1C1E26?style=for-the-badge&labelColor=1C1E26&color=ff5f5f
[url-kofi]: https://ko-fi.com/heliomarpm
[url-liberapay-badge]: https://img.shields.io/badge/liberapay-1C1E26?style=for-the-badge&labelColor=1C1E26&color=f6c915
[url-liberapay]: https://liberapay.com/heliomarpm

<!-- GitHub Actions badges -->
[url-codeql-badge]: https://github.com/heliomarpm/wallcat/actions/workflows/codeql.yml/badge.svg 
[url-codeql]: https://github.com/heliomarpm/wallcat/security/code-scanning
[url-test-badge]: https://github.com/heliomarpm/wallcat/actions/workflows/0.test.yml/badge.svg
[url-test]: https://github.com/heliomarpm/wallcat/actions/workflows/0.test.yml
[url-coverage-badge2]: https://img.shields.io/badge/coverage-dynamic.svg?label=coverage&color=informational&style=flat&logo=jest&query=$.coverage&url=https://heliomarpm.github.io/wallcat/coverage-badge.json
[url-coverage-badge]: https://img.shields.io/endpoint?url=https://heliomarpm.github.io/wallcat/coverage/coverage-badge.json
[url-coverage-report]: https://heliomarpm.github.io/wallcat/coverage

<!-- https://img.shields.io/endpoint?url=https://heliomarpm.github.io/wallcat/coverage-badge.json&label=coverage&suffix=%25 -->
[url-release-badge]: https://github.com/heliomarpm/wallcat/actions/workflows/3.release.yml/badge.svg
[url-release]: https://github.com/heliomarpm/wallcat/actions/workflows/3.release.yml
[url-publish-badge]: https://github.com/heliomarpm/wallcat/actions/workflows/4.publish-npm.yml/badge.svg 
[url-publish]: https://github.com/heliomarpm/wallcat/actions/workflows/4.publish-npm.yml

<!-- other badges -->
[url-npm-badge]: https://img.shields.io/npm/v/wallcat.svg
[url-npm]: https://www.npmjs.com/package/wallcat
[url-downloads-badge]: https://img.shields.io/npm/dy/wallcat.svg
[url-downloads]: http://badge.fury.io/js/wallcat.svg
[url-deepscan-badge]: https://deepscan.io/api/teams/19612/projects/28422/branches/916358/badge/grade.svg
[url-deepscan]: https://deepscan.io/dashboard#view=project&tid=19612&pid=28422&bid=916358
[url-codefactor-badge]: https://www.codefactor.io/repository/github/heliomarpm/wallcat/badge
[url-codefactor]: https://www.codefactor.io/repository/github/heliomarpm/wallcat
