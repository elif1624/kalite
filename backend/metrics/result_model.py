# backend/metrics/result_model.py

from dataclasses import dataclass

@dataclass
class MetricResult:
    tool_name: str
    critical: int
    high: int
    medium: int
    low: int
    total_issues: int
    scan_duration: float
