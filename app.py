from flask import Flask, jsonify, send_file, request
import os
from pathlib import Path
from snyk_runner import run_and_return, REPORT_DIR
from metric_runner import run_code_scan_and_save
from deepsource_runner import run_deepsource_scan_and_save

app = Flask(__name__)

# Mevcut test projeleri
AVAILABLE_PROJECTS = ["flask_demo", "nodejs-goof"]

@app.route("/scan", methods=["POST"])
def scan():
    """Container taraması (eski endpoint - geriye dönük uyumluluk için)"""
    summary, file_path = run_and_return()
    if not summary:
        return jsonify({"error": "scan failed"}), 500

    return jsonify({
        "message": "scan completed",
        "summary": summary,
        "report_file": file_path
    })


@app.route("/scan/code", methods=["POST"])
def scan_code():
    """
    Code taraması endpoint'i
    
    Request body (JSON):
    {
        "project": "flask_demo" veya "nodejs-goof" (opsiyonel, default: flask_demo)
    }
    
    veya query parameter:
    ?project=flask_demo
    """
    # Proje adını al (body'den veya query'den)
    project = None
    
    if request.is_json and request.json:
        project = request.json.get("project")
    
    if not project:
        project = request.args.get("project", "flask_demo")
    
    # Proje geçerli mi kontrol et
    if project not in AVAILABLE_PROJECTS:
        return jsonify({
            "error": f"Invalid project. Available projects: {AVAILABLE_PROJECTS}",
            "available_projects": AVAILABLE_PROJECTS
        }), 400
    
    # Tarama yap
    result = run_code_scan_and_save(project)
    
    if not result["success"]:
        return jsonify({
            "error": result.get("error", "Scan failed"),
            "project": project
        }), 500
    
    return jsonify({
        "message": "code scan completed",
        "project": result["project"],
        "file_path": result["file_path"],
        "metrics": result["metric_result"]
    }), 200


@app.route("/scan/code/all", methods=["POST"])
def scan_code_all():
    """
    Tüm test projeleri için code taraması yapar
    
    Returns:
        Her proje için tarama sonuçları
    """
    results = []
    
    for project in AVAILABLE_PROJECTS:
        result = run_code_scan_and_save(project)
        results.append(result)
    
    success_count = sum(1 for r in results if r["success"])
    
    return jsonify({
        "message": f"Scanned {success_count}/{len(AVAILABLE_PROJECTS)} projects",
        "results": results
    }), 200 if success_count > 0 else 500


@app.route("/projects", methods=["GET"])
def list_projects():
    """Mevcut test projelerini listeler"""
    projects_info = []
    
    for project in AVAILABLE_PROJECTS:
        project_path = Path(f"../test_projects/{project}")
        exists = project_path.exists()
        
        projects_info.append({
            "name": project,
            "exists": exists,
            "path": str(project_path)
        })
    
    return jsonify({
        "available_projects": AVAILABLE_PROJECTS,
        "projects": projects_info
    })


@app.route("/scan/latest", methods=["GET"])
def latest():
    files = os.listdir(REPORT_DIR)
    if not files:
        return jsonify({"error": "no reports found"}), 404

    latest = sorted(files)[-1]
    return send_file(os.path.join(REPORT_DIR, latest))


@app.route("/scan/file/<name>", methods=["GET"])
def file(name):
    return send_file(os.path.join(REPORT_DIR, name))


# ============================================
# DEEPSOURCE ENDPOINT'LERİ
# ============================================

@app.route("/scan/deepsource", methods=["POST"])
def scan_deepsource():
    """
    DeepSource code taraması endpoint'i
    
    Request body (JSON):
    {
        "project": "flask_demo" veya "nodejs-goof" (opsiyonel, default: flask_demo)
    }
    
    veya query parameter:
    ?project=flask_demo
    """
    # Proje adını al (body'den veya query'den)
    project = None
    
    if request.is_json and request.json:
        project = request.json.get("project")
    
    if not project:
        project = request.args.get("project", "flask_demo")
    
    # Proje geçerli mi kontrol et
    if project not in AVAILABLE_PROJECTS:
        return jsonify({
            "error": f"Invalid project. Available projects: {AVAILABLE_PROJECTS}",
            "available_projects": AVAILABLE_PROJECTS
        }), 400
    
    # Tarama yap
    result = run_deepsource_scan_and_save(project)
    
    if not result["success"]:
        return jsonify({
            "error": result.get("error", "Scan failed"),
            "project": project
        }), 500
    
    return jsonify({
        "message": "deepsource scan completed",
        "project": result["project"],
        "file_path": result["file_path"],
        "metrics": result["metric_result"]
    }), 200


@app.route("/scan/deepsource/all", methods=["POST"])
def scan_deepsource_all():
    """
    Tüm test projeleri için DeepSource taraması yapar
    
    Returns:
        Her proje için tarama sonuçları
    """
    results = []
    
    for project in AVAILABLE_PROJECTS:
        result = run_deepsource_scan_and_save(project)
        results.append(result)
    
    success_count = sum(1 for r in results if r["success"])
    
    return jsonify({
        "message": f"DeepSource scanned {success_count}/{len(AVAILABLE_PROJECTS)} projects",
        "results": results
    }), 200 if success_count > 0 else 500


if __name__ == "__main__":
    app.run(port=5001, debug=True)
