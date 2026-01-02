"""
Snyk Code Runner Modülü

Bu modül, Snyk Code CLI kullanarak kod analizi yapar ve sonuçları
standart metrik formatına normalize eder.

Ana Fonksiyonlar:
- run_snyk_code_scan(): Snyk CLI ile tarama yapar
- save_scan_result(): Sonuçları JSON formatında kaydeder
- run_code_scan_and_save(): Tam tarama ve kaydetme işlemi

Kullanım:
    python metric_runner.py
    veya
    from metric_runner import run_code_scan_and_save
    result = run_code_scan_and_save("flask_demo")
"""

import json
import subprocess
import os
from datetime import datetime
from pathlib import Path
from metrics.snyk_metrics import SnykMetrics

# Snyk CLI yolu (Windows için)
# Not: Bu yol sistemden sisteme değişebilir
SNYK_PATH = r"C:\Users\LOQ\AppData\Roaming\npm\snyk.cmd"

# Sonuç dosyalarının kaydedileceği klasör
RESULTS_DIR = "../results"

def run_snyk_code_scan(target_path: str) -> dict:
    """
    Snyk Code CLI kullanarak kod analizi yapar
    
    Args:
        target_path: Taranacak proje klasörünün yolu
    
    Returns:
        dict: Snyk'ten gelen JSON formatındaki ham sonuç
        (SARIF formatı veya eski vulnerabilities formatı)
    
    Raises:
        RuntimeError: Snyk CLI hatası veya tarama başarısız olduğunda
    """
    # Snyk CLI komutunu çalıştır
    # --json flag'i ile JSON formatında çıktı al
    result = subprocess.run(
        [SNYK_PATH, "code", "test", target_path, "--json"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Hata kontrolü
    if result.returncode != 0 and not result.stdout:
        raise RuntimeError(result.stderr)

    # JSON çıktısını parse et
    return json.loads(result.stdout)

def save_scan_result(raw_output: dict, tool_name: str, project_name: str) -> str:
    """
    Tarama sonucunu results/ klasörüne kaydeder.
    
    Args:
        raw_output: Snyk'ten gelen ham JSON çıktısı
        tool_name: Kullanılan araç adı (örn: "snyk_code")
        project_name: Test projesi adı (örn: "nodejs-goof", "flask_demo")
    
    Returns:
        Kaydedilen dosyanın yolu
    """
    # results klasörünü oluştur
    results_path = Path(RESULTS_DIR)
    results_path.mkdir(parents=True, exist_ok=True)
    
    # Dosya adını oluştur: tool_project_timestamp.json
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"{tool_name}_{project_name}_{timestamp}.json"
    file_path = results_path / filename
    
    # JSON'u kaydet
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(raw_output, f, indent=2, ensure_ascii=False)
    
    print(f"Tarama sonucu kaydedildi: {file_path}")
    return str(file_path)

def run_code_scan_and_save(project_name: str) -> dict:
    """
    Belirli bir proje için code taraması yapar ve sonucu kaydeder.
    API'den çağrılabilir fonksiyon.
    
    Args:
        project_name: Test projesi adı ("flask_demo" veya "nodejs-goof")
    
    Returns:
        {
            "success": bool,
            "project": str,
            "file_path": str,
            "metric_result": MetricResult (dict olarak),
            "error": str (varsa)
        }
    """
    try:
        # Proje yolunu oluştur
        target_path = f"../test_projects/{project_name}"
        
        # Proje var mı kontrol et
        if not Path(target_path).exists():
            return {
                "success": False,
                "project": project_name,
                "error": f"Project '{project_name}' not found in test_projects/"
            }
        
        # Tarama yap
        raw_output = run_snyk_code_scan(target_path)
        
        # Sonucu kaydet
        saved_path = save_scan_result(raw_output, "snyk_code", project_name)
        
        # Metrik hesapla
        metric = SnykMetrics()
        metric_result = metric.calculate(raw_output)
        
        # MetricResult'ı dict'e çevir
        metric_dict = {
            "tool_name": metric_result.tool_name,
            "critical": metric_result.critical,
            "high": metric_result.high,
            "medium": metric_result.medium,
            "low": metric_result.low,
            "total_issues": metric_result.total_issues,
            "scan_duration": metric_result.scan_duration
        }
        
        return {
            "success": True,
            "project": project_name,
            "file_path": saved_path,
            "metric_result": metric_dict
        }
        
    except Exception as e:
        return {
            "success": False,
            "project": project_name,
            "error": str(e)
        }

def main():
    target_path = "../test_projects/flask_demo"
    project_name = Path(target_path).name
    
    raw_output = run_snyk_code_scan(target_path)
    
    # Sonucu kaydet
    saved_path = save_scan_result(raw_output, "snyk_code", project_name)
    
    # Metrik hesapla
    metric = SnykMetrics()
    result = metric.calculate(raw_output)

    print("\n=== SMARTTESTAI METRIC OUTPUT ===")
    print(result)
    print("================================")

if __name__ == "__main__":
    main()
