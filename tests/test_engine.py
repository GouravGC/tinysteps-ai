import pytest
from src.tinysteps_engine import TinyStepsEngine

def test_expert_fallback_mechanism():
    """Verify that the engine fallback generates structured steps correctly."""
    engine = TinyStepsEngine()
    
    # Test offline fallback generation
    fallback = engine._generate_expert_fallback(
        task="Build a test pipeline", 
        total_mins=30, 
        error_msg="Test offline error"
    )
    
    assert "task_summary" in fallback
    assert fallback["total_time_allocated"] == 30
    assert len(fallback["steps"]) == 3
    assert fallback["steps"][0]["step_number"] == 1
    assert "Phase 1" in fallback["steps"][0]["title"]