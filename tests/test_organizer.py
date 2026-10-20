from pathlib import Path
from slothsort.organizer import apply_plan, undo_moves, build_plan

def test_apply_plan_moves_file_into_category_and_undo_restores(tmp_path):
    source = tmp_path / "report.pdf"
    source.write_text("sample", encoding="utf-8")
    scanned = [{
        "path": str(source.resolve()),
        "original_name": "report.pdf",
        "extension": ".pdf",
        "size_bytes": 6,
        "snippet": "",
    }]
    classified = [{
        **scanned[0],
        "category": "Documents",
        "new_name": "annual-report.pdf",
        "reason": "A report",
    }]
    plan = build_plan(tmp_path, scanned, classified)
    moves = apply_plan(tmp_path, plan)
    destination = tmp_path / "Documents" / "annual-report.pdf"
    assert destination.exists()
    assert not source.exists()
    restored, warnings = undo_moves(moves)
    assert restored == 1
    assert warnings == []
    assert source.exists()
    assert not destination.exists()

def test_collision_does_not_overwrite_existing_file(tmp_path):
    source = tmp_path / "photo.jpg"
    source.write_text("source", encoding="utf-8")
    folder = tmp_path / "Images"
    folder.mkdir()
    (folder / "photo.jpg").write_text("existing", encoding="utf-8")
    plan = [{
        "path": str(source.resolve()),
        "original_name": "photo.jpg",
        "category": "Images",
        "new_name": "photo.jpg",
    }]
    moves = apply_plan(tmp_path, plan)
    assert (folder / "photo.jpg").read_text(encoding="utf-8") == "existing"
    assert (folder / "photo_2.jpg").read_text(encoding="utf-8") == "source"
    assert len(moves) == 1

def test_refuses_file_outside_selected_folder(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    elsewhere = tmp_path / "outside.txt"
    elsewhere.write_text("do not move", encoding="utf-8")
    plan = [{
        "path": str(elsewhere.resolve()),
        "original_name": "outside.txt",
        "category": "Documents",
        "new_name": "outside.txt",
    }]
    try:
        apply_plan(root, plan)
        assert False, "Expected a safety exception"
    except ValueError:
        assert elsewhere.exists()
