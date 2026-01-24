# 🐱 Wallcat

**Wallpaper Catalog & Classifier**

Wallcat é uma ferramenta **CLI open source** para **organizar wallpapers automaticamente por categorias**, de forma **segura, explicável e extensível**.

Inspirado em ferramentas como Terraform, o Wallcat separa **decisão** de **execução**, permitindo simulação antes de qualquer alteração no filesystem.

---

## ✨ Features

- 📂 Organização automática de wallpapers por categoria
- 🧠 Classificação baseada em regras (keywords)
- 🔍 Decisões explicáveis (regra aplicada + confiança)
- 🛡️ Modo seguro (`--plan` / `--dry-run`)
- 🚀 Execução explícita (`--apply`)
- 🎯 Filtro por nível de confiança
- 🧩 Arquitetura preparada para ML e visão computacional
- 🖥️ CLI simples e rápida

---

## 🗂️ Example Folder Structure

```bash
src/
 └── wallcat/
     ├── __init__.py
     ├── main.py
     ├── cli.py
     └── core/
         ├── __init__.py
         ├── pipeline.py
         ├── rules.py
         └── organizer.py

config/
 └── categories.yaml

tests/
 └── test_rules.py

```

---

## 📦 Instalação

### Usando `uv` (recomendado)

```bash
uv pip install wallcat
```

> ou em desenvolvimento local

```bash
git clone https://github.com/heliomarpm/wallcat.git
cd wallcat
uv venv
uv pip install -e .
```

## 🚀 Uso Básico

> Nota: Para executar comandos em desenvolvimento, use `uv run` antes de `wallcat`

### Simular classificação (nenhuma alteração no disco)

```bash
wallcat classify ./Wallpapers --plan
# ou
wallcat classify ./Wallpapers --dry-run
```

### Aplicar classificação (executa de verdade)

```bash
wallcat classify ./Wallpapers --apply

uv run wallcat ./Wallpapers
# apply (default)

uv run wallcat ./Wallpapers --plan
# só mostra

uv run wallcat ./Wallpapers --apply
# executa

uv run wallcat ./Wallpapers --plan --apply
# mostra + executa

```

> [!WARNING]
> Wallcat nunca cria pastas ou move arquivos sem o uso explícito de --apply.

## 🎯 Filtro por Confiança

Ignora classificações fracas:

```bash
wallcat classify ./Wallpapers --plan --min-confidence 0.7
```

## 🧠 Classificação Explicável

Cada arquivo classificado retorna:

- Categoria
- Regra aplicada
- Nível de confiança

Exemplo interno:

```python
ClassificationResult(
    file=Path("SPBMX.png"),
    category="BMX",
    rule="keyword:bmx",
    confidence=0.8
)
```

Isso permite:

- Revisão humana
- Auditoria
- Evolução para ML
- Testes determinísticos

## ⚙️ Arquivo de Configuração

> Right-click any folder and select “Classify Wallpapers”

## ⚙️ Classification Modes

As categorias são definidas em YAML.

`config/categories.yaml`

```yaml
Nature:
  - nature
  - forest
  - mountain
  - lake
  - landscape

BMX:
  - bmx
  - bike
  - cycling

Utopia:
  - future
  - utopia
  - cyber

_PostApocalyptic:
  - apocalypse
  - ruin
  - decay
```

> Arquivos sem match são enviados para: `_Unclassified/`

## 🧩 Arquitetura

### Fluxo de Trabalho

> scan → classify → plan → apply

### Componentes principais

```bash
wallcat/
├── cli.py              # CLI (Click)
├── main.py             # Entry point
├── core/
│   ├── models.py       # ClassificationResult
│   ├── rules.py        # RuleEngine
│   └── organizer.py    # Plan / Apply
```

## 🛡️ Filosofia de Segurança

- ❌ Nenhuma modificação implícita
- ✅ Execução somente com --apply
- 🧪 Simulação sempre disponível
- 📜 Logs claros e rastreáveis

Wallcat é feito para confiança antes de automação.

---

## 🛣️ Roadmap

✅ Fase 1 — Base (concluída)

- [x] CLI funcional
- [x] Classificação por regras
- [x] Modo plan/apply
- [x] Decisões explicáveis

🔜 Fase 2 — Integração com SO

- [ ] Menu contextual (Windows / Linux / macOS)
- [ ] Execução com botão direito

🔜 Fase 3 — Inteligência

- [ ] Classificação por conteúdo da imagem
- [ ] CLIP / embeddings
- [ ] Aprendizado incremental

🔜 Fase 4 — UX

- [ ] UI gráfica
- [ ] Preview antes de aplicar
- [ ] Undo / rollback

## 🤝 Contribuindo

Pull requests são bem-vindos.

Sugestões:

- Novas regras
- Melhorias de UX
- Integração com ML
- Testes e documentação

## 📜 License

MIT License
> “Organizar não é mover arquivos, é tomar decisões seguras.”
---
