# SlothSort AI — project plan

## MVP
1. Scan direct child files in a user-selected folder.
2. Extract short text from supported text, PDF, and DOCX files.
3. Classify and propose filenames using local Ollama Gemma or OpenRouter.
4. Review/edit suggestions before applying.
5. Move approved files into category folders; preserve extensions and avoid overwrite.
6. Keep an undo record.
7. Run tests locally and through GitHub Actions.

## Explicit non-goals for the MVP
- No automatic deletion.
- No recursive folder traversal.
- No silent cloud fallback.
- No uploading files to a hosted server.
- No external database.

## Manual verification checklist
- Test with a disposable folder containing a PDF, text file, image, and duplicate filename.
- Verify cloud mode blocks until consent is checked.
- Verify missing OpenRouter key produces a readable error.
- Verify local mode works with Ollama running and the selected model pulled.
- Apply a plan and use undo.
- Run `pytest -q`.
- Build Docker image and verify the UI starts.
