# ⚡ TinySteps AI

> Turn overwhelming engineering tasks into structured, actionable execution roadmaps with dual-backend AI support.

[![CI/CD Pipeline](https://github.com/GouravGC/tinysteps-ai/actions/workflows/deploy.yml/badge.svg)](https://github.com/GouravGC/tinysteps-ai/actions)
[![GitHub Repository](https://img.shields.io/badge/GitHub-tinysteps--ai-blue?logo=github)](https://github.com/GouravGC/tinysteps-ai)
[![Live Demo](https://img.shields.io/badge/Render-Live_App-brightgreen?logo=render)](https://slothsort-ai-latest.onrender.com)
[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org/)

---

## 🔗 Quick Links & Submission Proofs

* **🎥 Video Demo (YouTube):** [Watch Demonstration Link Here](https://www.youtube.com/watch?v=znfbmLAjET8)
* **🌐 Live Web App (Render):** [https://slothsort-ai-latest.onrender.com](https://slothsort-ai-latest.onrender.com)
* **💻 Source Code (GitHub):** [https://github.com/GouravGC/tinysteps-ai](https://github.com/GouravGC/tinysteps-ai)
* **⚙️ CI/CD Pipeline Runs:** [https://github.com/GouravGC/tinysteps-ai/actions](https://github.com/GouravGC/tinysteps-ai/actions)
* **📦 Published Container Packages:** [https://github.com/GouravGC?tab=packages](https://github.com/GouravGC?tab=packages)

---

## 🌟 Key Features

* **Dual-Backend AI Engine (`TinyStepsEngine`):**
  * **Ollama (Local):** Run models locally for absolute privacy and offline capability.
  * **OpenRouter (Cloud):** Access scalable, cloud-hosted open-source models seamlessly.
* **Dynamic Time & Energy Adaptation:** Automatically sizes and paces execution phases based on your available time budget and energy level (Low, Medium, High).
* **Streamlit UI Dashboard:** An intuitive, responsive interface for selecting backends, inputting tasks, and viewing structured phases instantly.
* **Production-Ready CI/CD Pipeline:** Fully automated testing (`pytest`), Docker containerization, publishing to GitHub Container Registry (GHCR), and continuous deployment on Render.

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
```