# ⚡ TinySteps AI

> Turn overwhelming engineering tasks into structured, actionable execution roadmaps with dual-backend AI support.

[![CI/CD Pipeline](https://github.com/GouravGC/tinysteps-ai/actions/workflows/deploy.yml/badge.svg)](https://github.com/GouravGC/tinysteps-ai/actions)
[![GitHub Repository](https://img.shields.io/badge/GitHub-tinysteps--ai-blue?logo=github)](https://github.com/GouravGC/tinysteps-ai)
[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org/)

---

## 🔗 Quick Links & Submission Proofs

- **🎥 Video Demo:** [Watch the demonstration on YouTube](https://www.youtube.com/watch?v=znfbmLAjET8)
- **💻 Source Code:** [GitHub Repository](https://github.com/GouravGC/tinysteps-ai)
- **⚙️ CI/CD Pipeline:** [GitHub Actions](https://github.com/GouravGC/tinysteps-ai/actions)
- **📦 Published Container Packages:** [GitHub Packages](https://github.com/GouravGC?tab=packages)

> **Live demo:** The existing Render URL below belongs to the previous SlothSort deployment. Do not treat it as a verified TinySteps AI demo until the correct application is deployed and tested.
>
> Previous deployment: https://slothsort-ai-latest.onrender.com

---

## 🌟 Key Features

- **Dual-Backend AI Engine (`TinyStepsEngine`)**
  - **Ollama (Local):** Supports local model execution, keeping prompts on your machine when using a local Ollama model.
  - **OpenRouter (Cloud):** Connects to cloud-hosted models through OpenRouter, subject to model availability, network access, and provider limits.
- **Dynamic Time & Energy Adaptation:** Adjusts execution phases according to the user's available time and energy level (Low, Medium, or High).
- **Streamlit Dashboard:** Provides an interface for entering a task, choosing an AI backend, and viewing a structured execution plan.
- **Automated CI/CD:** Uses GitHub Actions to run tests and automate the configured container build, publishing, and deployment workflow.

---

## 🏗️ Project Architecture

```text
tinysteps-ai/
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD workflow
├── src/
│   ├── __init__.py              # Package initialization
│   └── tinysteps_engine.py      # Core engine and AI backends
├── tests/
│   └── test_tinysteps.py        # Automated tests
├── app.py                       # Streamlit application
├── Dockerfile                   # Container configuration
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

*The tree above documents the intended project structure. Verify filenames against the repository before relying on it as an exact inventory.*

---

## 🚀 Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/GouravGC/tinysteps-ai.git
cd tinysteps-ai
```

### 2. Create and activate a Python environment

```bash
conda create -n tinysteps python=3.11 -y
conda activate tinysteps
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Launch the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal.

**Backend requirements:**
- For local inference, install and start Ollama and pull a model supported by your application configuration.
- For cloud inference, configure the OpenRouter API key using the environment-variable name expected by the project. Never commit API keys or other secrets.

---

## 🧪 Testing

Run the test suite from the repository root:

```bash
python -m pytest -q
```

Check that the tests pass in your environment before reporting test results.

---

## 🐳 Docker

Build the image:

```bash
docker build -t tinysteps-ai .
```

Run the container:

```bash
docker run --rm -p 8501:8501 tinysteps-ai
```

Open `http://localhost:8501` if the Docker configuration exposes Streamlit on port `8501`.

---

## ⚙️ CI/CD Workflow

The GitHub Actions workflow is configured for the following pipeline:

1. Run automated tests.
2. Build the Docker image.
3. Publish the image to GitHub Container Registry (GHCR).
4. Trigger the configured Render deployment.

The exact behavior depends on the workflow configuration, repository secrets, and deployment settings. See the [workflow file](https://github.com/GouravGC/tinysteps-ai/blob/main/.github/workflows/deploy.yml) and [recent workflow runs](https://github.com/GouravGC/tinysteps-ai/actions).

---

## 🔒 Privacy & Reliability

- Local inference can keep task prompts on the local machine when Ollama is used and the application does not send data to external services.
- Cloud inference sends prompts to the selected provider; review that provider's privacy terms before using sensitive information.
- AI-generated roadmaps should be reviewed and adapted to real constraints. Model output can be incomplete or incorrect.
- Backend availability, API limits, and network connectivity can affect response generation.

---

## 🎯 Intended Use

TinySteps AI helps turn a large or intimidating engineering task into smaller, more manageable execution phases. It is intended as a planning aid, not a substitute for technical review or project-specific decision-making.

---

## 📜 License

Add the license used by this repository here. If the project has no license file yet, choose and add an appropriate open-source license before describing the project as open source.

---

**Built by [GouravGC](https://github.com/GouravGC)**
