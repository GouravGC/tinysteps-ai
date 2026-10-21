import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

class TinyStepsEngine:
    """Core execution engine for TinySteps AI with live dual-backend LLM support."""

    def __init__(self, provider: str = "Ollama (Local)"):
        self.provider = provider
        self.local_model = os.getenv("LOCAL_MODEL_NAME", "gemma3:4b")
        self.cloud_model = os.getenv("OPENROUTER_MODEL", "openrouter/free")
        self.ollama_base_url = os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")

    def breakdown_task(self, task: str, time_limit: int = 30, energy_level: str = "Medium"):
        if not task or not str(task).strip():
            task = "Engineering Task Breakdown"

        prompt = f"""
You are TinySteps AI, an expert engineering assistant.
Break down the following engineering task into exactly 3 sequential phases/steps.

Task: {task}
Total Time Available: {time_limit} minutes
Energy Level: {energy_level}

Return your response strictly as a valid JSON object with this exact structure (no markdown code blocks, just raw JSON):
{{
    "task_summary": "{task}",
    "total_time_allocated": {time_limit},
    "energy_level": "{energy_level}",
    "provider_used": "{self.provider}",
    "steps": [
        {{
            "step_number": 1,
            "title": "Phase 1: Environment & Discovery",
            "estimated_minutes": {max(1, int(time_limit * 0.2))},
            "instructions": "Detailed instructions for phase 1..."
        }},
        {{
            "step_number": 2,
            "title": "Phase 2: Core Execution & Implementation",
            "estimated_minutes": {max(1, int(time_limit * 0.6))},
            "instructions": "Detailed instructions for phase 2..."
        }},
        {{
            "step_number": 3,
            "title": "Phase 3: Validation & Delivery",
            "estimated_minutes": {max(1, int(time_limit * 0.2))},
            "instructions": "Detailed instructions for phase 3..."
        }}
    ]
}}
"""

        try:
            if "Ollama" in self.provider:
                url = f"{self.ollama_base_url}/chat/completions"
                payload = {
                    "model": self.local_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "stream": False
                }
                print(f"-> Calling Local Ollama at {url} with model {self.local_model}")
                response = requests.post(url, json=payload, timeout=60)
                print(f"<- Ollama Response Status: {response.status_code}")
                
                if response.status_code == 200:
                    content = response.json()["choices"][0]["message"]["content"]
                    return self._parse_llm_response(content, task, time_limit, energy_level)
                else:
                    print(f"Ollama error body: {response.text}")
            else:
                url = "https://openrouter.ai/api/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {self.openrouter_api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": self.cloud_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3
                }
                print(f"-> Calling OpenRouter with model {self.cloud_model}")
                response = requests.post(url, json=payload, headers=headers, timeout=60)
                print(f"<- OpenRouter Response Status: {response.status_code}")
                
                if response.status_code == 200:
                    content = response.json()["choices"][0]["message"]["content"]
                    return self._parse_llm_response(content, task, time_limit, energy_level)
                else:
                    print(f"OpenRouter error body: {response.text}")

        except Exception as e:
            print(f"❌ LLM Execution Exception: {e}")

        # Fallback if connection fails
        return self._generate_expert_fallback(task, time_limit, energy_level)

    def _parse_llm_response(self, content: str, task: str, time_limit: int, energy_level: str):
        try:
            cleaned = content.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            data = json.loads(cleaned.strip())
            # Ensure provider tag matches current choice
            data["provider_used"] = self.provider
            return data
        except Exception as parse_err:
            print(f"❌ JSON Parse Error: {parse_err} | Raw content: {content}")
            return self._generate_expert_fallback(task, time_limit, energy_level)

    def _generate_expert_fallback(self, task: str, total_mins: int, energy_level: str = "Medium"):
        p1 = int(total_mins * 0.2)
        p3 = int(total_mins * 0.2)
        p2 = total_mins - (p1 + p3)
        return {
            "task_summary": task,
            "total_time_allocated": total_mins,
            "energy_level": energy_level,
            "provider_used": self.provider,
            "steps": [
                {"step_number": 1, "title": "Phase 1: Environment & Discovery", "estimated_minutes": p1, "instructions": f"Fallback: Setup and analyze requirements for: {task}"},
                {"step_number": 2, "title": "Phase 2: Core Execution", "estimated_minutes": p2, "instructions": f"Fallback: Implement core logic for: {task}"},
                {"step_number": 3, "title": "Phase 3: Validation & Deployment", "estimated_minutes": p3, "instructions": f"Fallback: Test and deploy: {task}"}
            ]
        }