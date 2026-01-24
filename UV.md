# 🚀 Instalação e Verificação

* Instalar UV (Linux/macOS):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sudo sh
```

* Instalar UV (Windows via PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

* Verificar a instalação:

```bash
uv version
```

## 📂 Projetos e Ambientes

* Inicializar um novo projeto:

```bash
uv init <project-name>
```

* Criar ambiente virtual:

```bash
uv venv
```

* Sincronizar dependências e ambiente:

```bash
uv sync
# ou para todos os grupos
uv sync --all-groups
```

📦 Gerenciamento de Dependências

* Adicionar pacotes:

```bash
uv add <package-name>
# ou com versao especifica
uv add <package-name>==<version>
```

* Remover pacotes:

```bash
uv remove <package-name>
```

* Atualizar dependências e ambiente:

```bash
uv update
```

* Instalar a partir de requirements.txt:

```bash
uv pip install -r requirements.txt
```

* Listar pacotes instalados:

```bash
uv pip list
```

* Congelar dependências (equivalente ao pip freeze):

```bash
uv pip freeze
```

## 🛠️ Execução de Scripts e Ferramentas

* Rodar scripts Python dentro do ambiente UV:

```bash
uv run script.py
```

* Executar ferramentas sem instalar no projeto (ex.: Black, Flake8, Pytest):

```bash
uvx ruff check
uvx black arquivo.py
uvx pytest
uv tool <tool-name>
```

## 🐍 Gerenciamento de Versões Python

* Listar versões Python disponíveis:

```bash
uv python list --only-installed
```

* Trocar versão Python do projeto:

```bash
uv python pin 3.11.7
uv sync
```

## 🔒 Lockfiles e Exportação

* Gerar arquivo de lock (`uv.lock`):

> (feito automaticamente ao adicionar/remover pacotes)

* Exportar dependências para `requirements.txt`:

```bash
uv export -o requirements.txt
```

## 📑 Extras e Grupos de Dependências

* Adicionar dependências opcionais:

```bash
uv add --optional <package-name>
uv add pandas --optional plot excel
```

* Criar grupos de dependências (ex.: dev, test):

```bash
uv add --group dev <package-name>
uv add --group test <package-name>
```

* Listar grupos de dependências:

```bash
uv list --groups
```

## 🛠️ Ferramentas Extras

* Instalar ferramentas extras:

```bash
uv tool install <tool-name>
```

---
