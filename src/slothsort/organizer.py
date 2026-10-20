from pathlib import Path
import re

ALLOWED_CATEGORIES = {"Documents", "Images", "Videos", "Audio", "Archives", "Code", "Spreadsheets", "Presentations", "Other"}

def _clean_name(name, original_name):
    candidate = Path(str(name or original_name)).name
    candidate = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", candidate).strip(" .")
    if not candidate:
        candidate = original_name
    ext = Path(original_name).suffix
    stem = Path(candidate).stem.strip(" .") or Path(original_name).stem or "file"
    return f"{stem[:100]}{ext}"

def _unique_path(path: Path):
    if not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    counter = 2
    while True:
        candidate = path.with_name(f"{stem}_{counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1

def build_plan(root: Path, scanned, classified):
    root = root.expanduser().resolve()
    classified_by_name = {x["original_name"]: x for x in classified}
    plan = []
    for item in scanned:
        result = classified_by_name.get(item["original_name"], item)
        category = result.get("category", "Other")
        if category not in ALLOWED_CATEGORIES:
            category = "Other"
        plan.append({
            **item,
            "category": category,
            "new_name": _clean_name(result.get("new_name", item["original_name"]), item["original_name"]),
            "reason": result.get("reason", ""),
        })
    return plan

def apply_plan(root: Path, plan):
    root = root.expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Selected root is not a directory.")
    moves = []
    try:
        for item in plan:
            source = Path(item["path"]).resolve(strict=True)
            if source.parent != root or not source.is_file() or source.is_symlink():
                raise ValueError(f"Refusing to move a file outside the selected folder: {source.name}")
            category = item.get("category", "Other")
            if category not in ALLOWED_CATEGORIES:
                raise ValueError(f"Invalid category: {category}")
            dest_dir = root / category
            # Never treat an existing symlink directory as a destination.
            if dest_dir.exists() and (dest_dir.is_symlink() or not dest_dir.is_dir()):
                raise ValueError(f"Unsafe destination path: {dest_dir}")
            dest_dir.mkdir(exist_ok=True)
            new_name = _clean_name(item.get("new_name", source.name), source.name)
            destination = _unique_path(dest_dir / new_name)
            source.replace(destination)
            moves.append({"source": str(source), "destination": str(destination)})
    except Exception:
        # Best-effort rollback of changes already made in this operation.
        for move in reversed(moves):
            src, dest = Path(move["source"]), Path(move["destination"])
            try:
                if dest.exists() and not src.exists():
                    src.parent.mkdir(parents=True, exist_ok=True)
                    dest.replace(src)
            except Exception:
                pass
        raise
    return moves

def undo_moves(moves):
    restored = 0
    warnings = []
    for move in reversed(moves):
        source = Path(move["source"])
        destination = Path(move["destination"])
        if not destination.exists():
            warnings.append(f"Missing organized file: {destination.name}")
            continue
        if source.exists():
            warnings.append(f"Original path already exists; skipped {destination.name}")
            continue
        source.parent.mkdir(parents=True, exist_ok=True)
        destination.replace(source)
        restored += 1
    return restored, warnings
