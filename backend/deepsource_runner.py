# backend/deepsource_runner.py

import json
import subprocess
import os
import requests
from datetime import datetime
from pathlib import Path
from metrics.deepsource_metrics import DeepSourceMetrics

RESULTS_DIR = "../results"


def _get_mock_deepsource_output(target_path: str) -> dict:
    """
    Test için mock DeepSource çıktısı döner.
    Gerçek DeepSource API formatını öğrendikten sonra bu fonksiyon kaldırılabilir.
    """
    # Mock format - DeepSource'un gerçek formatına göre güncellenmeli
    return {
        "issues": [
            {
                "severity": "high",
                "issue_code": "DS-PY-001",
                "message": "Mock DeepSource issue - High severity",
                "file": "app.py",
                "line": 10
            },
            {
                "severity": "medium",
                "issue_code": "DS-PY-002",
                "message": "Mock DeepSource issue - Medium severity",
                "file": "app.py",
                "line": 20
            }
        ],
        "scan_duration": 5.2,
        "total_issues": 2
    }

# DeepSource yapılandırması
DEEPSOURCE_API_TOKEN = os.getenv("DEEPSOURCE_API_TOKEN", "")
DEEPSOURCE_API_URL = os.getenv("DEEPSOURCE_API_URL", "https://api.deepsource.io/graphql/")
DEEPSOURCE_CLI_PATH = os.getenv("DEEPSOURCE_CLI_PATH", "deepsource")

# Repository bilgileri (environment variable'dan veya default)
DEEPSOURCE_REPO_OWNER = os.getenv("DEEPSOURCE_REPO_OWNER", "elif1624")
DEEPSOURCE_REPO_NAME = os.getenv("DEEPSOURCE_REPO_NAME", "kalite")
DEEPSOURCE_VCS_PROVIDER = os.getenv("DEEPSOURCE_VCS_PROVIDER", "GITHUB")  # GITHUB, GITLAB, BITBUCKET

def run_deepsource_scan(target_path: str) -> dict:
    """
    DeepSource taraması yapar ve JSON çıktısı döner.
    
    DeepSource'un nasıl çalıştırıldığına göre bu fonksiyon güncellenmelidir:
    - API üzerinden: requests ile API çağrısı
    - CLI üzerinden: subprocess ile CLI komutu
    - Python SDK: DeepSource Python kütüphanesi
    
    Args:
        target_path: Taranacak proje yolu
    
    Returns:
        DeepSource'un JSON çıktısı (dict)
    """
    # YÖNTEM 1: DeepSource CLI kullanımı (eğer CLI varsa)
    try:
        result = subprocess.run(
            [DEEPSOURCE_CLI_PATH, "analyze", target_path, "--format", "json"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300  # 5 dakika timeout
        )
        
        if result.returncode == 0 and result.stdout:
            return json.loads(result.stdout)
        elif result.stdout:
            # Bazı durumlarda hata olsa bile stdout'ta JSON olabilir
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                raise RuntimeError(f"DeepSource CLI error: {result.stderr}")
        else:
            raise RuntimeError(f"DeepSource CLI failed: {result.stderr}")
    
    except FileNotFoundError:
        # CLI bulunamadı, API kullanmayı dene
        pass
    except subprocess.TimeoutExpired:
        raise RuntimeError("DeepSource scan timeout (exceeded 5 minutes)")
    
    # YÖNTEM 2: DeepSource GraphQL API kullanımı
    if DEEPSOURCE_API_TOKEN:
        try:
            # DeepSource GraphQL API endpoint'ine istek at
            headers = {
                "Authorization": f"Bearer {DEEPSOURCE_API_TOKEN}",
                "Content-Type": "application/json"
            }
            
            # GraphQL query: Repository issues'ları al
            # Not: DeepSource repository-based çalışır, local path yerine repository bilgisi kullanılır
            query = {
                "query": """
                query {
                    repository(login: "%s", name: "%s", vcsProvider: %s) {
                        name
                        issues(first: 100) {
                            totalCount
                            edges {
                                node {
                                    issue {
                                        shortcode
                                        title
                                        severity
                                        category
                                    }
                                }
                            }
                        }
                    }
                }
                """ % (DEEPSOURCE_REPO_OWNER, DEEPSOURCE_REPO_NAME, DEEPSOURCE_VCS_PROVIDER)
            }
            
            response = requests.post(
                DEEPSOURCE_API_URL,
                headers=headers,
                json=query,
                timeout=300
            )
            
            if response.status_code == 200:
                result = response.json()
                if "errors" in result:
                    raise RuntimeError(f"DeepSource GraphQL error: {result['errors']}")
                return result
            else:
                raise RuntimeError(f"DeepSource API error: {response.status_code} - {response.text}")
        
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"DeepSource API request failed: {str(e)}")
    
    # YÖNTEM 3: Mock/Test verisi (geliştirme aşaması için)
    # Gerçek DeepSource entegrasyonu yapılana kadar test için kullanılabilir
    print("WARNING: DeepSource CLI/API bulunamadi. Test modu kullaniliyor...")
    return _get_mock_deepsource_output(target_path)


def save_scan_result(raw_output: dict, tool_name: str, project_name: str) -> str:
    """
    Tarama sonucunu results/ klasörüne kaydeder.
    
    Args:
        raw_output: DeepSource'ten gelen ham JSON çıktısı
        tool_name: Kullanılan araç adı (örn: "deepsource")
        project_name: Test projesi adı
    
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


def run_deepsource_scan_and_save(project_name: str) -> dict:
    """
    Belirli bir proje için DeepSource taraması yapar ve sonucu kaydeder.
    API'den çağrılabilir fonksiyon.
    
    Args:
        project_name: Test projesi adı
    
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
        raw_output = run_deepsource_scan(target_path)
        
        # Sonucu kaydet
        saved_path = save_scan_result(raw_output, "deepsource", project_name)
        
        # Metrik hesapla
        metric = DeepSourceMetrics()
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
    """Test için main fonksiyonu"""
    target_path = "../test_projects/flask_demo"
    project_name = Path(target_path).name
    
    raw_output = run_deepsource_scan(target_path)
    
    # Sonucu kaydet
    saved_path = save_scan_result(raw_output, "deepsource", project_name)
    
    # Metrik hesapla
    metric = DeepSourceMetrics()
    result = metric.calculate(raw_output)

    print("\n=== SMARTTESTAI METRIC OUTPUT (DEEPSOURCE) ===")
    print(result)
    print("================================")

if __name__ == "__main__":
    main()

