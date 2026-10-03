import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))
from app.ml.anomaly_detector import anomaly_detector

def test_ml_detection():
    print("===============================================================")
    print("[ML TEST] DETECTEUR D'ANOMALIES MACHINE LEARNING (Isolation Forest)")
    print("===============================================================")

    # Jeux de données de test de métriques K8s
    sample_cluster_data = {
        "payment-api": {
            "cpu_usage_pct": 97.0,
            "memory_usage_pct": 94.0,
            "latency_ms": 2800.0,
            "error_rate_pct": 18.0
        },
        "checkout-service": {
            "cpu_usage_pct": 18.2,
            "memory_usage_pct": 38.5,
            "latency_ms": 85.0,
            "error_rate_pct": 0.1
        },
        "auth-service": {
            "cpu_usage_pct": 88.0,
            "memory_usage_pct": 40.0,
            "latency_ms": 1950.0,
            "error_rate_pct": 1.2
        }
    }

    results = anomaly_detector.analyze_services(sample_cluster_data)

    print(f"\n[STATUT] Anomalies Detectees : {results['detected']}")
    for anomaly in results.get("all_anomalies", results.get("anomalies", [])):
        print(f"\n-> Service : {anomaly['service']}")
        print(f"   Severite : {anomaly.get('status', 'Critical')}")
        print(f"   Cause Racine Probable : {anomaly['probable_root_cause']}")
        print(f"   Score de Confiance : {anomaly.get('confidence', anomaly.get('confidence_pct'))}%")
        print(f"   Metriques : CPU={anomaly.get('cpu', anomaly.get('cpu_usage_pct'))}%, RAM={anomaly.get('memory', anomaly.get('memory_usage_pct'))}%, Latence={anomaly.get('latency', anomaly.get('latency_ms'))}ms, Erreurs={anomaly.get('errors', anomaly.get('error_rate_pct'))}%")

if __name__ == "__main__":
    test_ml_detection()
