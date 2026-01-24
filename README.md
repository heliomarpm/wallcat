# Wallcat - Wallpaper Catalog & Classifier

**Wallcat** is an open-source tool that automatically organizes wallpaper images into categories using a hybrid classification pipeline based on filename rules and AI-powered image understanding.

Designed to be simple, fast, and privacy-friendly — all processing runs locally.

---

## ✨ Features

- 📁 Automatic wallpaper organization by category
- ⚡ Fast rule-based classification
- 🤖 AI fallback using CLIP for visual understanding
- 🧠 Hybrid pipeline (rules first, AI when needed)
- 🖱️ Windows context menu integration
- 🧾 Metadata indexing for reclassification
- 🛑 Dry-run mode (preview changes)

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

## 🚀 Quick Start

### 1. Install

```bash
git clone https://github.com/<your-user>/wallcat.git
cd wallcat
pip install -r requirements.txt
```

### 2. Run (CLI)

```bash
python wallcat.py classify ./Wallpapers --mode hybrid
```

### 3. Windows Context Menu

```bash
wallcat install-context-menu
```

> Right-click any folder and select “Classify Wallpapers”

## ⚙️ Classification Modes

| Mode | Description |
|------|-------------|
| **rules** | Filename-based rules only |
| **hybrid** | Rules first, AI fallback (default) |
| **ai** | AI-based classification only |

## 🧠 How It Works

1. Scan image files
2. Try rule-based classification
3. If not matched, apply AI classification
4. Move file to target category
5. Save metadata locally

## 📦 Tech Stack

1. Python 3.10+
2. OpenCLIP
3. PyInstaller
4. YAML (configuration)
5. JSON (metadata)

## 🛣️ Roadmap

See [ROADMAP.md](./ROADMAP.md)

## 📜 License

MIT License

---
