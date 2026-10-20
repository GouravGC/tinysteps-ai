import json
import re
from pathlib import Path
from .providers import get_model_text
from .config import Settings

CATEGORIES = {"Documents", "Images", "Videos", "Audio", "Archives", "Code", "Spreadsheets", "Presentations", "Other"}
EXTENSION_CATEGORY = {
    ".pdf": "Documents", ".docx": "Documents", ".txt": "Documents", ".md": "Documents", ".rtf": "Documents",
    ".png": "Images", ".jpg": "Images", ".jpeg": "Images", ".gif": "Images", ".webp": "Images", ".bmp": "Images", ".svg": "Images",
    ".mp4": "Videos", ".mov": "Videos", ".avi": "Videos", ".mkv": "Videos",
    ".mp3": "Audio", ".wav": "Audio", ".flac": "Audio", ".m4a": "Audio",
    ".zip": "Archives", ".rar": "Archives", ".7z": "Archives", ".tar": "Archives", ".gz": "Archives",
    ".xls": "Spreadsheets", ".xlsx": "Spreadsheets", ".ods": "Spreadsheets", ".csv": "Spreadsheets",
    ".ppt": "Presentations", ".pptx": "Presentations", ".odp": "Presentations",
    ".py": "Code", ".js": "Code", ".ts": "Code", ".html": "Code", ".css": "Code", ".sql": "Code", ".json": "Code", ".yaml": "Code", ".yml": "Code", ".ipynb": "Code",
}

def fallback_category(file_info):
    return EXTENSION_CATEGORY.get(file_info.get("extension", "").lower(), "Other")

def _parse_json(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("["), text.rfind("]")
        if start < 0 or end <= start:
            raise ValueError("The AI response was not a JSON array.")
        data = json.loads(text[start:end + 1])
    if isinstance(data, dict):
        data = data.get("files", data.get("results", []))
    if not isinstance(data, list):
        raise ValueError("The AI response must contain a JSON array.")
    return data

def _safe_filename(name, original_name):
    original_ext = Path(original_name).suffix
    candidate = Path(str(name or original_name)).name.strip()
    candidate = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", candidate).strip(" .")
    if not candidate:
        candidate = original_name
    # Preserve original extension, regardless of model output.
    stem = Path(candidate).stem.strip(" .") or Path(original_name).stem or "file"
    return f"{stem[:100]}{original_ext}"

def classify_files(files, provider: str, settings: Settings):
    if not files:
        return []
    try:
        raw = get_model_text(files, provider, settings)
        outputs = _parse_json(raw)
    except Exception:
        # Keep app usable if model output is malformed, but surface fallback results.
        outputs = []
    by_name = {}
    for item in outputs:
        if not isinstance(item, dict):
            continue
        name = str(item.get("original_name", "")).strip()
        if name:
            by_name[name] = item
    results = []
    for file_info in files:
        item = by_name.get(file_info["original_name"], {})
        category = item.get("category")
        if category not in CATEGORIES:
            category = fallback_category(file_info)
        reason = str(item.get("reason", "")).strip()[:240] or f"Suggested from file type: {file_info['extension'] or 'unknown'}"
        new_name = _safe_filename(item.get("new_name", file_info["original_name"]), file_info["original_name"])
        results.append({
            **file_info,
            "category": category,
            "new_name": new_name,
            "reason": reason,
        })
    return results
