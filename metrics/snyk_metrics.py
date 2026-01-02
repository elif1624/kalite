# backend/metrics/snyk_metrics.py

from .base_metric import BaseMetric
from .result_model import MetricResult
import time

class SnykMetrics(BaseMetric):
    def calculate(self, raw_data: dict) -> MetricResult:
        # SARIF format desteği
        if "runs" in raw_data and len(raw_data.get("runs", [])) > 0:
            # SARIF formatı: runs[0].results[]
            results = raw_data["runs"][0].get("results", [])
            
            counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
            
            for result in results:
                level = result.get("level", "error").lower()
                priority_score = result.get("properties", {}).get("priorityScore", 0)
                
                # Priority score'a göre severity belirleme
                if priority_score > 0:
                    if priority_score >= 900:
                        counts["critical"] += 1
                    elif priority_score >= 700:
                        counts["high"] += 1
                    elif priority_score >= 500:
                        counts["medium"] += 1
                    else:
                        counts["low"] += 1
                else:
                    # Eğer priority score yoksa, level'a göre belirle
                    if level == "error":
                        counts["high"] += 1
                    elif level == "warning":
                        counts["medium"] += 1
                    else:
                        counts["low"] += 1
            
            # Scan duration SARIF'te farklı yerde olabilir
            scan_duration = 0.0
            if "runs" in raw_data and len(raw_data["runs"]) > 0:
                automation_details = raw_data["runs"][0].get("automationDetails", {})
                # Duration bilgisi genelde automationDetails'te yok, 0.0 olarak bırakıyoruz
            
            return MetricResult(
                tool_name="Snyk Code",
                critical=counts["critical"],
                high=counts["high"],
                medium=counts["medium"],
                low=counts["low"],
                total_issues=len(results),
                scan_duration=scan_duration
            )
        
        # Eski format desteği (geriye dönük uyumluluk)
        vulns = raw_data.get("vulnerabilities", [])

        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}

        for v in vulns:
            sev = v.get("severity")
            if sev in counts:
                counts[sev] += 1

        return MetricResult(
            tool_name="Snyk Code",
            critical=counts["critical"],
            high=counts["high"],
            medium=counts["medium"],
            low=counts["low"],
            total_issues=len(vulns),
            scan_duration=raw_data.get("scanDuration", 0.0)
        )
