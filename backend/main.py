import sys
import os

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BACKEND_DIR, ".."))

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any

from simulator.k8s_mock_cluster import cluster_simulator
from app.ml.anomaly_detector import anomaly_detector
from app.agent.sre_copilot import copilot_agent
from app.remediation.executor import remediation_executor

app = FastAPI(
    title="AIOps Copilot — Kubernetes Incident Management Platform API",
    version="1.0.0",
    description="Intelligent Kubernetes incident detection, RAG-powered RCA, and automated remediation engine."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_INDEX = os.path.abspath(os.path.join(ROOT_DIR, "frontend", "index.html"))

class ChaosInjectRequest(BaseModel):
    service_name: str = "payment-api"
    chaos_type: str = "MEMORY_LEAK"

class InvestigateRequest(BaseModel):
    service_name: str = "payment-api"

class RemediateRequest(BaseModel):
    service_name: str = "payment-api"
    memory_limit: str = "512Mi"

@app.get("/")
def read_root():
    """Redirects root to the visual AI Cloud Operations Center UI Dashboard."""
    return RedirectResponse(url="/dashboard")

@app.get("/dashboard", response_class=FileResponse)
def serve_dashboard():
    """Serves the AI Cloud Operations Center UI Dashboard."""
    if os.path.exists(FRONTEND_INDEX):
        return FileResponse(FRONTEND_INDEX)
    return {"error": "Dashboard HTML not found"}

@app.get("/api/health")
def api_status():
    return {"status": "online", "system": "AIOps Copilot Engine"}

@app.get("/api/cluster/health")
def get_cluster_health():
    return cluster_simulator.get_cluster_metrics()

@app.get("/api/incidents/active")
def detect_active_incidents():
    metrics = cluster_simulator.get_cluster_metrics()
    anomalies = anomaly_detector.analyze_services(metrics["services"])
    return anomalies

@app.post("/api/incidents/investigate")
def investigate_incident(req: InvestigateRequest):
    metrics = cluster_simulator.get_cluster_metrics()
    svc_metrics = metrics["services"].get(req.service_name, {})
    if not svc_metrics:
        raise HTTPException(status_code=404, detail=f"Service '{req.service_name}' not found")
    rca_result = copilot_agent.investigate_incident(req.service_name, svc_metrics)
    return rca_result

@app.post("/api/incidents/remediate")
def execute_remediation(req: RemediateRequest):
    result = remediation_executor.execute_action(req.service_name, "RESOURCE_PATCH", req.memory_limit)
    return result

@app.post("/api/chaos/inject")
def inject_chaos(req: ChaosInjectRequest):
    success = cluster_simulator.inject_chaos(req.service_name, req.chaos_type)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to inject chaos scenario")
    return {
        "status": "CHAOS_INJECTED",
        "service": req.service_name,
        "chaos_type": req.chaos_type,
        "cluster_health": cluster_simulator.get_cluster_metrics()
    }

@app.post("/api/chaos/reset")
def reset_cluster():
    for svc in list(cluster_simulator.services.keys()):
        cluster_simulator.resolve_chaos(svc)
    return {
        "status": "CLUSTER_RESET_HEALTHY",
        "cluster_health": cluster_simulator.get_cluster_metrics()
    }
