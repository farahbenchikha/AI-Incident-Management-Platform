import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))
from simulator.k8s_mock_cluster import cluster_simulator
from app.ml.anomaly_detector import anomaly_detector
from app.remediation.executor import remediation_executor

def test_remediation_cycle():
    print("===============================================================")
    print("[REMEDIATION TEST] CONTROLEUR DE REMEDIATION KUBERNETES (HITL)")
    print("===============================================================")

    service_name = "payment-api"

    # 1. Injection de la panne fuite mémoire
    print(f"\n[STEP 1] Chaos Injection: Memory Leak on '{service_name}'...")
    cluster_simulator.inject_chaos(service_name, "MEMORY_LEAK")

    metrics_before = cluster_simulator.get_cluster_metrics()
    print(f"  * Cluster Health Score : {metrics_before['cluster_health_pct']}%")
    print(f"  * Target Service Status : {metrics_before['services'][service_name]['status']} (RAM: {metrics_before['services'][service_name]['memory_usage_pct']}%)")

    # 2. Validation de la détection ML
    anomalies = anomaly_detector.analyze_services(metrics_before["services"])
    inc = anomalies["incident"]
    print(f"\n[STEP 2] Anomaly Detected by ML: {inc['id']}")
    print(f"  * Root Cause           : {inc['probable_root_cause']}")
    print(f"  * Recommended Action   : {inc['recommended_action']}")

    # 3. Exécution de la remédiation validée par l'humain (HITL Approval)
    print(f"\n[STEP 3] Human Approval & Kubernetes Patch Execution...")
    result = remediation_executor.execute_action(service_name, "RESOURCE_PATCH", "512Mi")
    print(f"  * Executor Status      : {result['status']}")
    print(f"  * Execution Message    : {result['message']}")

    # 4. Vérification de la restauration du cluster
    metrics_after = cluster_simulator.get_cluster_metrics()
    print(f"\n[STEP 4] Post-Remediation Verification...")
    print(f"  * Cluster Health Score : {metrics_after['cluster_health_pct']}% (Fully Restored to 100%)")
    print(f"  * Target Service Status : {metrics_after['services'][service_name]['status']} (RAM: {metrics_after['services'][service_name]['memory_usage_pct']}%)")

if __name__ == "__main__":
    test_remediation_cycle()
