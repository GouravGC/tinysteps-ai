import os
import json
from dotenv import load_dotenv

load_dotenv()

class TinyStepsEngine:
    """Core execution engine for TinySteps AI supporting dual backends."""
    
    def __init__(self, provider: str = "Ollama (Local)"):
        self.provider = provider
        self.local_model = os.getenv("LOCAL_MODEL_NAME", "gemma3:4b")
        self.cloud_model = os.getenv("OPENROUTER_MODEL", "openrouter/free")
        self.base_url = os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1")

    def generate_roadmap(self, task: str, total_mins: int = 30):
        """Generates the execution roadmap based on the selected provider."""
        # Your execution/generation logic here...
        pass

    def _generate_expert_fallback(self, task, total_mins, error_msg):
        return {
            "task_summary": task,
            "total_time_allocated": total_mins,
            "steps": [
                {
                    "step_number": 1,
                    "title": "Phase 1: Environment & Discovery",
                    "estimated_minutes": int(total_mins * 0.2),
                    "instructions": "Audit baseline project setup and dependencies."
                },
                {
                    "step_number": 2,
                    "title": "Phase 2: Core Execution & Implementation",
                    "estimated_minutes": int(total_mins * 0.6),
                    "instructions": "Implement core domain logic and verify functionality."
                },
                {
                    "step_number": 3,
                    "title": "Phase 3: Validation & Deployment",
                    "estimated_minutes": int(total_mins * 0.2),
                    "instructions": "Run automated test suite and trigger CI/CD pipeline."
                }
            ]
        }