# ⚡ TinySteps AI

> Turn overwhelming engineering tasks into structured, actionable execution roadmaps with dual-backend AI support.

[![CI/CD Pipeline](https://github.com/GouravGC/tinysteps-ai/actions/workflows/deploy.yml/badge.svg)](https://github.com/GouravGC/tinysteps-ai/actions)
[![GitHub Repository](https://img.shields.io/badge/GitHub-tinysteps--ai-blue?logo=github)](https://github.com/GouravGC/tinysteps-ai)
[![Live Demo](https://img.shields.io/badge/Render-Live_App-brightgreen?logo=render)](https://slothsort-ai-latest.onrender.com)
[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org/)

---

## 🔗 Quick Links

* **Live Web App:** [https://slothsort-ai-latest.onrender.com](https://slothsort-ai-latest.onrender.com)
* **Source Code:** [https://github.com/GouravGC/tinysteps-ai](https://github.com/GouravGC/tinysteps-ai)
* **CI/CD Pipeline Runs:** [https://github.com/GouravGC/tinysteps-ai/actions](https://github.com/GouravGC/tinysteps-ai/actions)
* **Published Packages:** [https://github.com/GouravGC?tab=packages](https://github.com/GouravGC?tab=packages)

---

## 🌟 Key Features

* **Dual-Backend AI Engine (`TinyStepsEngine`):**
  * **Ollama (Local):** Run models locally for privacy and offline usage.
  * **OpenRouter (Cloud):** Access scalable, cloud-hosted open-source models seamlessly.
* **Structured Roadmap Generation:** Breaks down complex, high-level engineering tasks into clear, step-by-step execution phases with estimated time allocations.
* **Automated Fallback Mechanism:** Includes built-in expert fallback logic to ensure uninterrupted execution roadmaps even during model downtime or API errors.
* **Streamlit UI:** An intuitive dashboard for selecting backends, inputting tasks, and viewing roadmaps in real time.
* **Production-Ready CI/CD:** Fully automated testing (`pytest`), Docker containerization, publishing to GitHub Container Registry (GHCR), and continuous deployment on Render.

---

## 🏗 Project Architecture

```text
tinysteps-ai/
├── .github/
│   └── workflows/
│       └── deploy.yml          # Automated CI/CD pipeline (Test -> Build -> Publish -> Deploy)
├── src/
│   ├── __init__.py             # Exposes TinyStepsEngine for clean imports
│   └── tinysteps_engine.py     # Core engine supporting dual AI backends
├── tests/
│   └── test_tinysteps.py       # Automated unit tests for engine logic
├── app.py                      # Streamlit frontend application
├── Dockerfile                  # Production container definition
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation