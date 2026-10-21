import os
import streamlit as st

# Ensure PYTHONPATH or direct src import works smoothly
try:
    from tinysteps_engine import TinyStepsEngine
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
    from tinysteps_engine import TinyStepsEngine

# --- Page Configuration ---
st.set_page_config(
    page_title="TinySteps AI",
    page_icon="⚡",
    layout="centered"
)

# --- Header Section ---
st.title("⚡ TinySteps AI: Technical Guide & Assistant")
st.caption("Turn overwhelming engineering tasks into structured execution roadmaps.")

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Configuration")
provider_choice = st.sidebar.radio(
    "Select AI Execution Backend:",
    ["Ollama (Local)", "OpenRouter (Cloud)"]
)

# --- User Inputs ---
task_input = st.text_area(
    "What project or programming task are you tackling?",
    placeholder="e.g., Build and deploy a Machine Learning model pipeline with MLOps tracking..."
)

col1, col2 = st.columns(2)

with col1:
    time_limit = st.slider(
        "Total Time Available (Minutes)",
        min_value=10,
        max_value=240,
        value=120,
        step=5
    )

with col2:
    energy_level = st.select_slider(
        "Your Current Energy Level",
        options=["Low", "Medium", "High"],
        value="High"
    )

generate_btn = st.button("🚀 Generate Actionable Roadmap", type="primary")

# --- Engine Execution & Output ---
if generate_btn:
    if not task_input.strip():
        st.warning("Please enter a task description before generating the roadmap.")
    else:
        with st.spinner("Analyzing task scope, allocating time buffers, and building execution phases..."):
            # Initialize engine with selected backend provider
            engine = TinyStepsEngine(provider=provider_choice)
            
            # Generate task breakdown
            result = engine.breakdown_task(
                task=task_input,
                time_limit=time_limit,
                energy_level=energy_level
            )

        st.success("Roadmap generated successfully!")
        st.divider()

        # Display Objective Summary Card
        st.markdown(
            f"### 🎯 Objective: {result.get('task_summary', task_input)}\n"
            f"**⏳ Time Budget:** {result.get('total_time_allocated', time_limit)} mins | "
            f"**Backend:** {result.get('provider_used', provider_choice)} | "
            f"**Energy Level:** {result.get('energy_level', energy_level)}"
        )

        st.divider()

        # Render Steps
        steps = result.get("steps", [])
        for step in steps:
            step_num = step.get("step_number", "")
            title = step.get("title", f"Step {step_num}")
            
            # Fallback checks across key name variants
            mins = (
                step.get("duration_mins") or 
                step.get("estimated_minutes") or 
                step.get("minutes") or 
                0
            )
            guidance = (
                step.get("guidance") or 
                step.get("instructions") or 
                step.get("details") or 
                "No guidance provided."
            )

            st.markdown(f"#### Step {step_num}: {title} ({mins} mins)")
            st.markdown(f"**Guidance & Actions:**\n{guidance}")
            st.divider()