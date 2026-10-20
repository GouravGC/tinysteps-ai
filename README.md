# SlothSort AI 🦥

**AI-Powered, Local-First File Organizer**

SlothSort AI scans a selected folder, uses AI to suggest meaningful file categories and filenames, and lets you review changes before applying them. It supports local AI through Ollama and cloud AI through OpenRouter.

## 🚀 Live Demo

**[Launch SlothSort AI](https://slothsort-ai-latest.onrender.com/)**

> Note: The hosted demo runs remotely. It cannot directly access files on your personal computer or your local Ollama installation.

## 🔗 Project Links

- **Live Application:** https://slothsort-ai-latest.onrender.com/
- **GitHub Repository:** https://github.com/GouravGC/slothsort-ai
- **Latest Commit:** https://github.com/GouravGC/slothsort-ai/commits/main/
- **CI/CD Workflows:** https://github.com/GouravGC/slothsort-ai/actions
- **GitHub Packages (Docker Image):** https://github.com/GouravGC?tab=packages

## ⚙️ CI/CD Pipeline

SlothSort AI uses GitHub Actions to automate testing, containerization, publishing, and deployment.

**Pipeline:** Push to `main` → Install dependencies → Run tests → Build Docker image → Publish to GitHub Container Registry (GHCR) → Trigger Render deployment.

[![CI/CD Pipeline](https://github.com/GouravGC/slothsort-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/GouravGC/slothsort-ai/actions)

View [workflow runs and build logs](https://github.com/GouravGC/slothsort-ai/actions) to inspect the pipeline's latest status.

## ✨ Features

- AI-powered file categorization and filename suggestions
- Local AI support with Ollama
- Cloud AI integration through OpenRouter
- Review suggestions before moving or renaming files
- Apply approved organization plans
- Undo supported organization changes
- Modular Python architecture
- Automated tests with pytest
- Docker-based deployment
- GitHub Actions CI/CD with GHCR and Render

## 🛠️ Tech Stack

- **Language:** Python 3.11
- **Interface:** Streamlit
- **AI:** Ollama, OpenRouter
- **Testing:** pytest
- **Containerization:** Docker
- **CI/CD:** GitHub Actions
- **Container Registry:** GitHub Container Registry (GHCR)
- **Deployment:** Render

## 🧪 Run Locally

```bash
git clone https://github.com/GouravGC/slothsort-ai.git
cd slothsort-ai

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

Configure credentials in your local `.env` file when needed. **Never commit API keys or `.env` secrets.**

## ✅ Tests

Run the test suite with:

```bash
PYTHONPATH=src python -m pytest -q
```

The project's local test suite passed **7 tests** during development.

## 📦 Docker Image

```bash
docker pull ghcr.io/gouravgc/slothsort-ai:latest
```

## 🔐 Safety by Design

SlothSort AI is designed around human approval: it proposes changes for review before applying them. Cloud AI mode may send filenames and extracted file snippets to the configured provider, so review sensitive data before enabling it.

## 👨‍💻 Author

**Gourav GC**

[GitHub Profile](https://github.com/GouravGC) · [Project Repository](https://github.com/GouravGC/slothsort-ai)
