# SlothSort AI 🦥

A local-first file organizer that uses open-weight AI to suggest file categories and clearer filenames. It scans a folder, prepares a reviewable plan, and only moves files after explicit approval.

## Features

- **Two AI providers:** Gemma through local Ollama, or OpenRouter for hosted/cloud use.
- **Privacy choice:** local inference is the default. Cloud mode requires an explicit in-app confirmation before snippets are sent.
- **Review before action:** edit suggested categories and filenames before applying.
- **Safe file handling:** scans only direct files in the selected folder, skips symlinks, preserves extensions, avoids overwriting files, and never deletes files.
- **Undo:** records moves for a best-effort restore.
- **Engineering:** pytest suite, GitHub Actions CI, and Dockerfile.

## Requirements

- Python 3.11
- Ollama for local mode
- A downloaded Ollama model (default: `gemma3:4b`)
- OpenRouter API key only if using cloud mode

## Local setup (Windows CMD)

```bat
conda create -n slothsort python=3.11.10 -y
conda activate slothsort
cd path\to\slothsort-ai
pip install -r requirements.txt
copy .env.example .env
ollama pull gemma3:4b
streamlit run app.py
```

Edit `.env` to set `OPENROUTER_API_KEY` if using OpenRouter. Never commit `.env`.

## Run tests

```bat
set PYTHONPATH=src
pytest -q
```

## Docker

Build and run the UI:

```bash
docker build -t slothsort-ai .
docker run --rm -p 8501:8501 -e DEFAULT_PROVIDER="OpenRouter (Cloud)" -e OPENROUTER_API_KEY="YOUR_KEY" slothsort-ai
```

For local Ollama from a container, configure `OLLAMA_BASE_URL` to a host-reachable Ollama endpoint. Do not assume `localhost` inside the container points to the host.

## Deployment notes

Set `DEFAULT_PROVIDER=OpenRouter (Cloud)` and `OPENROUTER_API_KEY` in your hosting provider's secret settings. The API key must not be placed in source code or exposed to the browser. Choose a model ID that is currently available to your OpenRouter account.

A hosted deployment cannot access a user's local disk. Cloud-hosted use therefore needs users to upload files or use the local app. The initial version is designed primarily for local folders; treat cloud deployment as a demo unless a separate, secure upload workflow is implemented.

## Privacy and safety

- Cloud mode sends file names and extracted text snippets to OpenRouter after the user checks the consent box.
- Test with a disposable folder first.
- The app never deletes files. Review the plan before applying it.
- Use only folders you own or have permission to organize.

## Challenge theme

**Slow and Steady:** automate the repetitive work of sorting files while keeping the user in control. Open-weight local AI enables private, user-controlled inference and makes the core feature usable without a paid inference API.
