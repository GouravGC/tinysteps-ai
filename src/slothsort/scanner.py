from pathlib import Path

TEXT_EXTENSIONS = {".txt", ".md", ".csv", ".json", ".py", ".yaml", ".yml", ".log"}
SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".txt", ".md", ".csv", ".json", ".py", ".yaml", ".yml", ".log",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg",
    ".mp4", ".mov", ".avi", ".mkv", ".mp3", ".wav", ".flac", ".m4a",
    ".zip", ".rar", ".7z", ".tar", ".gz",
    ".xls", ".xlsx", ".ods", ".ppt", ".pptx", ".odp",
    ".html", ".css", ".js", ".ts", ".sql", ".ipynb",
}
MAX_TEXT_CHARS = 1800

def _extract_text(path: Path) -> str:
    ext = path.suffix.lower()
    try:
        if ext in TEXT_EXTENSIONS:
            return path.read_text(encoding="utf-8", errors="ignore")[:MAX_TEXT_CHARS]
        if ext == ".pdf":
            from pypdf import PdfReader
            reader = PdfReader(str(path))
            text = "\n".join((page.extract_text() or "") for page in reader.pages[:3])
            return text[:MAX_TEXT_CHARS]
        if ext == ".docx":
            from docx import Document
            doc = Document(str(path))
            return "\n".join(p.text for p in doc.paragraphs)[:MAX_TEXT_CHARS]
    except Exception:
        return ""
    return ""

def scan_folder(folder: Path, limit: int = 30, include_content: bool = True):
    try:
        root = folder.expanduser().resolve(strict=True)
    except Exception:
        return [], "The selected folder could not be resolved."
    if not root.is_dir():
        return [], "The selected path is not a directory."
    results = []
    try:
        children = sorted(root.iterdir(), key=lambda p: p.name.lower())
        for path in children:
            if len(results) >= limit:
                break
            if not path.is_file() or path.is_symlink() or path.name.startswith("."):
                continue
            if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            snippet = _extract_text(path) if include_content else ""
            results.append({
                "path": str(path.resolve()),
                "original_name": path.name,
                "extension": path.suffix.lower(),
                "size_bytes": path.stat().st_size,
                "snippet": snippet,
            })
    except PermissionError:
        return [], "Permission denied while scanning this folder."
    return results, None
