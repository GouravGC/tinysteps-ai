import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class TinyStepsEngine:
    def __init__(self, provider: str = "Ollama (Local)"):
        self.provider = provider
        
        if "OpenRouter" in provider:
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_API_KEY")
            )
            # Use OpenRouter's built-in free multi-model auto-router
            self.model = os.getenv("OPENROUTER_MODEL", "openrouter/free")
        else:
            self.client = OpenAI(
                base_url=os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1"),
                api_key=os.getenv("OPENAI_API_KEY", "ollama")
            )
            self.model = os.getenv("LOCAL_MODEL_NAME", "gemma3:4b")

    def breakdown_task(self, task_description: str, available_minutes: int, energy_level: str = "Medium") -> dict:
        system_prompt = (
            "You are an elite Lead Software Engineering Guide and Technical Mentor. "
            "Take a developer's project objective and time budget, then break it down "
            "into an actionable, multi-phase technical roadmap. Each step must be rich, descriptive, "
            "and span 5 to 10 lines of precise technical guidance covering tech stack selection, "
            "implementation details, testing, and execution."
        )

        user_prompt = f"""
        Developer Objective: "{task_description}"
        Total Time Budget: {available_minutes} minutes.
        Energy Level: {energy_level}

        Return ONLY a valid JSON object matching this exact schema, with no markdown formatting outside the JSON block:
        {{
          "task_summary": "Comprehensive architectural overview of the objective",
          "total_time_allocated": {available_minutes},
          "steps": [
            {{
              "step_number": 1,
              "title": "Phase title",
              "duration_mins": <integer>,
              "actionable_instruction": "Detailed 5 to 10 line technical guide explaining tools, frameworks, and script logic."
            }}
          ]
        }}
        """

        try:
            # Note: Optional headers for OpenRouter rankings can be passed via extra_headers if desired
            extra_headers = {}
            if "OpenRouter" in self.provider:
                extra_headers = {
                    "HTTP-Referer": "https://github.com/tinysteps-ai",
                    "X-Title": "TinySteps AI"
                }

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"},
                extra_headers=extra_headers if extra_headers else None
            )
            
            raw_content = response.choices[0].message.content.strip()
            if raw_content.startswith("```json"):
                raw_content = raw_content[7:-3].strip()
            return json.loads(raw_content)

        except Exception as e:
            return self._generate_expert_fallback(task_description, available_minutes, str(e))

    def _generate_expert_fallback(self, task: str, total_mins: int, error_msg: str) -> dict:
        m1 = int(total_mins * 0.2)
        m2 = int(total_mins * 0.6)
        m3 = total_mins - (m1 + m2)
        return {
            "task_summary": f"Engineering Blueprint for: {task} (Expert Offline Guide)",
            "total_time_allocated": total_mins,
            "steps": [
                {
                    "step_number": 1,
                    "title": "Phase 1: Architecture, Scoping & Environment Setup",
                    "duration_mins": m1,
                    "actionable_instruction": f"Define scope and tech stack for '{task}'. Initialize workspace, virtual environment, configure `.env`, and check your requirements."
                },
                {
                    "step_number": 2,
                    "title": "Phase 2: Core Implementation & Script Development",
                    "duration_mins": m2,
                    "actionable_instruction": f"Write primary modular logic for '{task}'. Build core services, hook up local APIs, and ensure data flows correctly."
                },
                {
                    "step_number": 3,
                    "title": "Phase 3: Verification, Testing & Deployment",
                    "duration_mins": m3,
                    "actionable_instruction": "Execute local testing, patch immediate bugs, and prepare container configurations for your deployment pipeline."
                }
            ],
            "warning": f"API connection error ({error_msg}). Loaded expert fallback blueprint."
        }