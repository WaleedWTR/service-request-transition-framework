#!/usr/bin/env python3
from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "request_types.csv"

def load():
    with DATA.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def weighted_average(rows, field):
    total_volume = sum(int(r["monthly_volume"]) for r in rows)
    return sum(float(r[field]) * int(r["monthly_volume"]) for r in rows) / total_volume

def calculate(rows):
    before = weighted_average(rows, "before_hours")
    after = weighted_average(rows, "after_hours")
    return {
        "request_types": len(rows),
        "monthly_volume": sum(int(r["monthly_volume"]) for r in rows),
        "weighted_before_hours": round(before, 2),
        "weighted_after_hours": round(after, 2),
        "cycle_time_reduction_pct": round((before - after) / before * 100, 1),
        "average_first_time_right_pct": round(
            sum(float(r["first_time_right_pct"]) for r in rows) / len(rows), 1
        ),
        "transition_completion_pct": round(
            sum(r["transitioned"].lower() == "true" for r in rows) / len(rows) * 100, 1
        ),
    }

if __name__ == "__main__":
    for key, value in calculate(load()).items():
        print(f"{key}: {value}")
