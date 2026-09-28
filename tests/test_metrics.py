from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from transition_metrics import calculate, load  # noqa: E402

def test_seven_request_types():
    assert calculate(load())["request_types"] == 7

def test_all_synthetic_types_transitioned():
    assert calculate(load())["transition_completion_pct"] == 100.0

def test_cycle_time_improves():
    metrics = calculate(load())
    assert metrics["weighted_after_hours"] < metrics["weighted_before_hours"]
    assert metrics["cycle_time_reduction_pct"] > 0

def test_volume_is_positive():
    assert calculate(load())["monthly_volume"] > 0
