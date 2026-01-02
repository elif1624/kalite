# backend/metrics/deepsource_metrics.py

from .base_metric import BaseMetric
from .result_model import MetricResult

class DeepSourceMetrics(BaseMetric):
    """
    DeepSource çıktılarını Snyk ile aynı metrik formatına normalize eder.
    DeepSource'un çıktı formatına göre uyarlanmalıdır.
    """
    
    def calculate(self, raw_data: dict) -> MetricResult:
        """
        DeepSource çıktısını standart MetricResult formatına çevirir.
        
        DeepSource çıktı formatı örneği (tahmini):
        {
            "issues": [
                {
                    "severity": "critical" | "high" | "medium" | "low",
                    ...
                }
            ],
            "scan_duration": 12.5
        }
        
        veya farklı bir format olabilir - DeepSource API dokümantasyonuna göre güncellenmeli
        """
        # DeepSource çıktı formatına göre issues'ları al
        # Format DeepSource API'sine göre değişebilir
        issues = raw_data.get("issues", [])
        
        # Eğer farklı bir key kullanıyorsa (örn: "results", "findings", "violations")
        if not issues:
            issues = raw_data.get("results", [])
        if not issues:
            issues = raw_data.get("findings", [])
        if not issues:
            issues = raw_data.get("violations", [])
        
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        
        for issue in issues:
            # DeepSource severity formatına göre normalize et
            severity = issue.get("severity", "").lower()
            
            # DeepSource'un severity formatı farklı olabilir (örn: "BLOCKER", "CRITICAL", "MAJOR", "MINOR")
            # Bu mapping DeepSource'un gerçek formatına göre güncellenmeli
            if severity in ["critical", "blocker", "error"]:
                counts["critical"] += 1
            elif severity in ["high", "major"]:
                counts["high"] += 1
            elif severity in ["medium", "minor", "warning"]:
                counts["medium"] += 1
            elif severity in ["low", "info", "suggestion"]:
                counts["low"] += 1
            else:
                # Bilinmeyen severity'leri medium olarak say
                counts["medium"] += 1
        
        # Scan duration - DeepSource formatına göre
        scan_duration = raw_data.get("scan_duration", 0.0)
        if scan_duration == 0.0:
            scan_duration = raw_data.get("duration", 0.0)
        if scan_duration == 0.0:
            scan_duration = raw_data.get("time", 0.0)
        
        return MetricResult(
            tool_name="DeepSource",
            critical=counts["critical"],
            high=counts["high"],
            medium=counts["medium"],
            low=counts["low"],
            total_issues=len(issues),
            scan_duration=float(scan_duration) if scan_duration else 0.0
        )

