import time
import random
from typing import Dict, List, Any

class K8sMockCluster:
    """
    Simulates a live Kubernetes cluster telemetry data stream (Prometheus metrics, Loki logs, K8s events).
    Supports injecting real-world incident scenarios for testing AIOps anomaly detection & LLM agent.
    """
    def __init__(self):
        self.services = {
            "payment-api": {
                "namespace": "default",
                "replicas": 3,
                "target_replicas": 3,
                "cpu_usage_pct": 24.5,
                "memory_usage_pct": 42.0,
                "memory_limit": "256Mi",
                "latency_ms": 120.0,
                "error_rate_pct": 0.2,
                "status": "Healthy",
                "chaos_active": False,
                "chaos_type": None
            },
            "checkout-service": {
                "namespace": "default",
                "replicas": 4,
                "target_replicas": 4,
                "cpu_usage_pct": 18.2,
                "memory_usage_pct": 38.5,
                "memory_limit": "512Mi",
                "latency_ms": 85.0,
                "error_rate_pct": 0.1,
                "status": "Healthy",
                "chaos_active": False,
                "chaos_type": None
            },
            "frontend-web": {
                "namespace": "default",
                "replicas": 5,
                "target_replicas": 5,
                "cpu_usage_pct": 15.0,
                "memory_usage_pct": 30.0,
                "memory_limit": "512Mi",
                "latency_ms": 45.0,
                "error_rate_pct": 0.05,
                "status": "Healthy",
                "chaos_active": False,
                "chaos_type": None
            },
            "auth-service": {
                "namespace": "default",
                "replicas": 2,
                "target_replicas": 2,
                "cpu_usage_pct": 12.0,
                "memory_usage_pct": 25.0,
                "memory_limit": "256Mi",
                "latency_ms": 30.0,
                "error_rate_pct": 0.0,
                "status": "Healthy",
                "chaos_active": False,
                "chaos_type": None
            }
        }
        # Add additional healthy placeholder services to reach 23 total services as in UI
        for i in range(1, 20):
            svc_name = f"microservice-app-{i:02d}"
            self.services[svc_name] = {
                "namespace": "prod",
                "replicas": 2,
                "target_replicas": 2,
                "cpu_usage_pct": round(random.uniform(5.0, 25.0), 1),
                "memory_usage_pct": round(random.uniform(15.0, 45.0), 1),
                "memory_limit": "256Mi",
                "latency_ms": round(random.uniform(20.0, 60.0), 1),
                "error_rate_pct": 0.0,
                "status": "Healthy",
                "chaos_active": False,
                "chaos_type": None
            }

        self.events_log: List[Dict[str, Any]] = []

    def inject_chaos(self, service_name: str, chaos_type: str = "MEMORY_LEAK"):
        if service_name not in self.services:
            return False
        
        svc = self.services[service_name]
        svc["chaos_active"] = True
        svc["chaos_type"] = chaos_type
        svc["status"] = "Critical"

        if chaos_type == "MEMORY_LEAK":
            svc["cpu_usage_pct"] = 97.0
            svc["memory_usage_pct"] = 94.0
            svc["replicas"] = 12
            svc["latency_ms"] = 2800.0
            svc["error_rate_pct"] = 18.0
            
            # Cascading impact on checkout-service
            if "checkout-service" in self.services:
                chk = self.services["checkout-service"]
                chk["status"] = "Warning"
                chk["latency_ms"] = 1450.0
                chk["error_rate_pct"] = 6.5

            self.events_log.append({
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "service": service_name,
                "type": "Warning",
                "reason": "OOMKilled",
                "message": f"Container payment-api in pod payment-api-7d9bf-x8k92 exceeded memory limit {svc['memory_limit']}. Memory working set 240Mi / 256Mi."
            })
        return True

    def resolve_chaos(self, service_name: str, new_memory_limit: str = "512Mi"):
        if service_name not in self.services:
            return False
        
        svc = self.services[service_name]
        svc["chaos_active"] = False
        svc["chaos_type"] = None
        svc["status"] = "Healthy"
        svc["memory_limit"] = new_memory_limit
        svc["cpu_usage_pct"] = 22.0
        svc["memory_usage_pct"] = 35.0
        svc["replicas"] = 3
        svc["latency_ms"] = 115.0
        svc["error_rate_pct"] = 0.1

        if "checkout-service" in self.services:
            chk = self.services["checkout-service"]
            chk["status"] = "Healthy"
            chk["latency_ms"] = 85.0
            chk["error_rate_pct"] = 0.1

        self.events_log.append({
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "service": service_name,
            "type": "Normal",
            "reason": "ResourcePatched",
            "message": f"Successfully updated memory limit to {new_memory_limit} and scaled replicas to 3. Pod health restored."
        })
        return True

    def get_cluster_metrics(self) -> Dict[str, Any]:
        total_apps = len(self.services)
        healthy = sum(1 for s in self.services.values() if s["status"] == "Healthy")
        warning = sum(1 for s in self.services.values() if s["status"] == "Warning")
        critical = sum(1 for s in self.services.values() if s["status"] == "Critical")
        
        # Calculate cluster health score
        health_pct = round((healthy / total_apps) * 100, 1)

        return {
            "cluster_health_pct": health_pct,
            "total_applications": total_apps,
            "healthy_count": healthy,
            "warning_count": warning,
            "critical_count": critical,
            "services": self.services
        }

    def get_service_logs(self, service_name: str, limit: int = 50) -> List[str]:
        if service_name == "payment-api" and self.services["payment-api"]["chaos_active"]:
            return [
                f"[{time.strftime('%H:%M:%S')}] [INFO] Processing request /api/v1/payment/charge amount=89.99",
                f"[{time.strftime('%H:%M:%S')}] [WARN] Memory consumption elevated: 241MB / 256MB allocated heap",
                f"[{time.strftime('%H:%M:%S')}] [ERROR] java.lang.OutOfMemoryError: Java heap space - Failed to allocate 16384 bytes",
                f"[{time.strftime('%H:%M:%S')}] [ERROR] Connection pool timeout waiting for available buffer thread",
                f"[{time.strftime('%H:%M:%S')}] [CRITICAL] Pod payment-api-7d9bf-x8k92 terminated with exit code 137 (OOMKilled)"
            ]
        return [
            f"[{time.strftime('%H:%M:%S')}] [INFO] GET /healthz HTTP/1.1 200 OK",
            f"[{time.strftime('%H:%M:%S')}] [INFO] Request processed in 12ms"
        ]

# Global singleton instance for local simulator
cluster_simulator = K8sMockCluster()
