from slothsort.classifier import fallback_category, _safe_filename

def test_pdf_defaults_to_documents():
    assert fallback_category({"extension": ".pdf"}) == "Documents"

def test_image_defaults_to_images():
    assert fallback_category({"extension": ".png"}) == "Images"

def test_unknown_extension_defaults_to_other():
    assert fallback_category({"extension": ".xyz"}) == "Other"

def test_filename_keeps_original_extension_and_removes_path():
    assert _safe_filename("../My report.exe", "report.pdf") == "My report.pdf"
