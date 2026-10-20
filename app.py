from pathlib import Path
import pandas as pd
import streamlit as st

from slothsort.config import Settings
from slothsort.scanner import scan_folder
from slothsort.classifier import classify_files
from slothsort.organizer import apply_plan, undo_moves, build_plan

st.set_page_config(page_title="SlothSort AI", page_icon="🦥", layout="wide")
settings = Settings.from_env()

st.title("🦥 SlothSort AI")
st.caption("A calm, local-first file organizer powered by open-weight AI.")
st.write("Scan a folder, review suggested categories and filenames, then approve the changes yourself.")

with st.sidebar:
    st.header("AI provider")
    default_provider = settings.default_provider if settings.default_provider in ("Local Gemma (Ollama)", "OpenRouter (Cloud)") else "Local Gemma (Ollama)"
    provider = st.selectbox(
        "Choose where AI runs",
        ["Local Gemma (Ollama)", "OpenRouter (Cloud)"],
        index=["Local Gemma (Ollama)", "OpenRouter (Cloud)"].index(default_provider),
    )
    if provider == "Local Gemma (Ollama)":
        st.info(f"Local model: `{settings.ollama_model}`")
        st.caption("File names and text stay on this machine, unless another app or service is configured to transmit them.")
    else:
        st.info(f"OpenRouter model: `{settings.openrouter_model}`")
        st.warning("Cloud mode sends file names and extracted text snippets to OpenRouter for classification.")
        cloud_consent = st.checkbox("I understand and approve sending these snippets to OpenRouter.")
    st.divider()
    st.caption("Safety: nothing is moved until you review the plan and click Apply.")

folder_text = st.text_input(
    "Folder to organize",
    value=str(Path.home() / "Downloads"),
    help="Use a folder you own and test with sample files first. Only files directly inside this folder are scanned.",
)
max_files = st.slider("Maximum files to scan", min_value=5, max_value=100, value=30, step=5)
include_content = st.checkbox("Read short text snippets from supported documents", value=True)

if "plan" not in st.session_state:
    st.session_state.plan = []
if "last_moves" not in st.session_state:
    st.session_state.last_moves = []
if "scan_root" not in st.session_state:
    st.session_state.scan_root = ""

col1, col2 = st.columns([1, 1])
with col1:
    scan_clicked = st.button("🔎 Scan and suggest", type="primary", use_container_width=True)
with col2:
    undo_clicked = st.button("↩️ Undo last organization", use_container_width=True, disabled=not bool(st.session_state.last_moves))

if scan_clicked:
    root = Path(folder_text).expanduser()
    if not root.exists() or not root.is_dir():
        st.error("That folder does not exist or is not a directory.")
    elif provider == "OpenRouter (Cloud)" and not cloud_consent:
        st.error("Please confirm cloud-data sharing before using OpenRouter.")
    else:
        with st.spinner("Scanning files and preparing suggestions..."):
            scanned, error = scan_folder(root, limit=max_files, include_content=include_content)
            if error:
                st.error(error)
            elif not scanned:
                st.warning("No eligible files found directly inside that folder.")
            else:
                provider_key = "ollama" if provider == "Local Gemma (Ollama)" else "openrouter"
                try:
                    classified = classify_files(scanned, provider_key, settings)
                    st.session_state.plan = build_plan(root, scanned, classified)
                    st.session_state.scan_root = str(root.resolve())
                    st.success(f"Prepared suggestions for {len(st.session_state.plan)} file(s). Nothing has been changed yet.")
                except Exception as exc:
                    st.error(f"AI classification failed: {exc}")
                    st.caption("Check that Ollama is running and the model is downloaded, or verify your OpenRouter key/model configuration.")

if st.session_state.plan:
    st.subheader("Review your proposed changes")
    st.caption("Edit the category or new filename before applying. Categories are created as subfolders.")
    editable = []
    for i, item in enumerate(st.session_state.plan):
        editable.append({
            "original_name": item["original_name"],
            "category": item["category"],
            "new_name": item["new_name"],
            "reason": item.get("reason", ""),
        })
    edited = st.data_editor(
        pd.DataFrame(editable),
        use_container_width=True,
        hide_index=True,
        disabled=["original_name", "reason"],
        column_config={
            "category": st.column_config.SelectboxColumn("Category", options=[
                "Documents", "Images", "Videos", "Audio", "Archives", "Code",
                "Spreadsheets", "Presentations", "Other"
            ], required=True),
            "new_name": st.column_config.TextColumn("New filename", required=True),
            "reason": st.column_config.TextColumn("Why", width="large"),
        },
        key="plan_editor",
    )
    st.caption("Tip: keep the original filename if you are unsure. Duplicate destination names are handled safely.")
    if st.button("✅ Apply approved changes", type="primary"):
        root = Path(st.session_state.scan_root)
        final_plan = []
        for row in edited.to_dict(orient="records"):
            original = next((x for x in st.session_state.plan if x["original_name"] == row["original_name"]), None)
            if original:
                final_plan.append({**original, "category": row["category"], "new_name": row["new_name"]})
        try:
            moved = apply_plan(root, final_plan)
            st.session_state.last_moves = moved
            st.session_state.plan = []
            st.success(f"Organized {len(moved)} file(s). A record is available for undo.")
            st.rerun()
        except Exception as exc:
            st.error(f"Could not safely apply the full plan: {exc}")

if undo_clicked and st.session_state.last_moves:
    try:
        restored, warnings = undo_moves(st.session_state.last_moves)
        st.session_state.last_moves = []
        if warnings:
            st.warning("Undo completed with some skipped items: " + "; ".join(warnings))
        else:
            st.success(f"Restored {restored} file(s).")
        st.rerun()
    except Exception as exc:
        st.error(f"Undo failed: {exc}")

st.divider()
st.caption("SlothSort AI · Review first, move only with permission. Use a test folder before organizing important files.")
