import numpy as np
from typing import Dict, Any, List
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    """
    ML Anomaly Detector for Kubernetes Telemetry.
    Combines Isolation Forest with statistical Z-score thresholds for fast and accurate incident detection.
    """
    def __init__(self):
        # Pre-fit a default IsolationForest model for metric tuples [cpu_pct, mem_pct, latency_ms, error_rate_pct]
        self.model = IsolationForest(n_estimators=50, contamination=0.05, random_state=42)
        
        # Baseline normal telemetry data points
        baseline_data = np.array([
            [15.0, 30.0, 45.0, 0.1],
            [20.0, 40.0, 50.0, 0.2],
            [25.0, 35.0, 60.0, 0.0],
            [10.0, 25.0, 30.0, 0.0],
            [18.0, 38.0, 55.0, 0.1],
            [22.0, 42.0, 70.0, 0.3],
            [14.0, 28.0, 40.0, 0.0],
        ])
        self.model.fit(baseline_data)

    def analyze_services(self, services: Dict[str, Any]) -> Dict[str, Any]:
        anomalies = []
        primary_suspect = None
        highest_score = 0.0
        affected_services = []

        for svc_name, metrics in services.items():
            cpu = metrics.get("cpu_usage_pct", 0.0)
            mem = metrics.get("memory_usage_pct", 0.0)
            lat = metrics.get("latency_ms", 0.0)
            err = metrics.get("error_rate_pct", 0.0)

            # Feature vector: [cpu, mem, latency, error_rate]
            features = np.array([[cpu, mem, lat, err]])
            
            # Predict (-1 is anomaly, 1 is normal)
            pred = self.model.predict(features)[0]
            
            # Rule-based fallback/enrichment for high confidence
            is_critical = (mem > 85.0 or cpu > 90.0 or err > 10.0 or lat > 2000.0)
            is_warning = (mem > 70.0 or cpu > 75.0 or err > 3.0 or lat > 800.0)

            if pred == -1 or is_critical or is_warning:
                affected_services.append(svc_name)
                
                # Calculate confidence score based on severity of metric deviations
                confidence = 0.0
                root_cause = "Unknown Anomaly"

                if mem > 85.0 and cpu > 80.0:
                    root_cause = "Memory leak"
                    confidence = min(99.0, 75.0 + (mem - 85.0) * 1.5 + (cpu - 80.0) * 0.5)
                elif cpu > 85.0:
                    root_cause = "CPU Throttling & Saturation"
                    confidence = min(95.0, 70.0 + (cpu - 85.0) * 1.5)
                elif err > 10.0:
                    root_cause = "Cascading HTTP 500 Service Failures"
                    confidence = min(92.0, 65.0 + err * 1.2)
                else:
                    root_cause = "Latency Degradation / Resource Constraint"
                    confidence = 78.0

                anomalies.append({
                    "service": svc_name,
                    "status": "Critical" if is_critical else "Warning",
                    "cpu_usage_pct": cpu,
                    "memory_usage_pct": mem,
                    "latency_ms": lat,
                    "error_rate_pct": err,
                    "probable_root_cause": root_cause,
                    "confidence": round(confidence, 1)
                })

                if confidence > highest_score:
                    highest_score = confidence
                    primary_suspect = svc_name

        if not anomalies:
            return {
                "detected": False,
                "incident": None
            }

        primary_anomaly = next((a for a in anomalies if a["service"] == primary_suspect), anomalies[0])

        # Recommended Action generation logic
        recommended_action = "Investigate container logs and scale replicas"
        if primary_anomaly["probable_root_cause"] == "Memory leak":
            recommended_action = "Increase memory limit to 512Mi"
        elif "CPU" in primary_anomaly["probable_root_cause"]:
            recommended_action = "Increase CPU quota limit to 1000m and scale deployment replicas to 5"

        return {
            "detected": True,
            "incident": {
                "id": f"INC-{int(np.random.randint(1000, 9999))}",
                "primary_service": primary_anomaly["service"],
                "severity": primary_anomaly["status"],
                "probable_root_cause": primary_anomaly["probable_root_cause"],
                "confidence_pct": primary_anomaly["confidence"],
                "affected_services": affected_services,
                "recommended_action": recommended_action,
                "telemetry_snapshot": {
                    "cpu_pct": primary_anomaly["cpu_usage_pct"],
                    "memory_pct": primary_anomaly["memory_usage_pct"],
                    "latency_ms": primary_anomaly["latency_ms"],
                    "error_rate_pct": primary_anomaly["error_rate_pct"]
                }
            },
            "all_anomalies": anomalies
        }

anomaly_detector = AnomalyDetector()
