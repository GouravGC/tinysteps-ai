import pytest
from tinysteps_engine import TinyStepsEngine

def test_expert_fallback():
    engine = TinyStepsEngine()
    result = engine._generate_expert_fallback("Test Task", 30, "Simulated Error")
    assert result["total_time_allocated"] == 30
    assert len(result["steps"]) == 3
    assert "Test Task" in result["task_summary"]