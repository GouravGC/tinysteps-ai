import streamlit as st
from src.tinysteps_engine import TinyStepsEngine

st.set_page_config(page_title="TinySteps AI", page_icon="⚡", layout="centered")

st.title("⚡ TinySteps AI: Technical Guide & Assistant")
st.markdown("*Turn overwhelming engineering tasks into structured execution roadmaps.*")

# Sidebar or Top Control for Provider Selection
provider_choice = st.radio(
    "Select AI Execution Backend:",
    ["Ollama (Local)", "OpenRouter (Cloud)"],
    horizontal=True,
    help="Choose whether to run locally using Ollama Gemma or via OpenRouter cloud APIs."
)

# Initialize Engine with selected provider
engine = TinyStepsEngine(provider=provider_choice)

with st.form("tinysteps_guide_form"):
    task_input = st.text_area("What project or programming task are you tackling?", placeholder="e.g., Build a data science pipeline with custom feature engineering")
    
    col1, col2 = st.columns(2)
    with col1:
        time_limit = st.slider("Total Time Available (Minutes)", 10, 240, 60, 10)
    with col2:
        energy_level = st.selectbox("Your Current Energy Level", ["Low", "Medium", "High"], 1)
        
    submitted = st.form_submit_button("Generate Engineering Blueprint")

if submitted:
    if not task_input.strip():
        st.warning("Please enter a valid task description.")
    else:
        spinner_msg = f"🧠 Processing blueprint via {provider_choice}..."
        with st.spinner(spinner_msg):
            result = engine.breakdown_task(task_input, time_limit, energy_level)
            
            if "warning" in result:
                st.warning(result["warning"])
                
            st.success(f"🎯 **Objective:** {result.get('task_summary')}")
            st.info(f"⏳ **Time Budget:** {result.get('total_time_allocated')} mins | **Backend:** {provider_choice} | **Energy:** {energy_level}")
            
            for step in result.get("steps", []):
                with st.expander(f"Step {step.get('step_number')}: {step.get('title')} ({step.get('duration_mins')} mins)", expanded=True):
                    st.markdown(f"**Guidance & Actions:**\n\n{step.get('actionable_instruction')}")