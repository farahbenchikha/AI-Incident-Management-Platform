import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))
from app.agent.sre_copilot import copilot_agent
from app.ml.anomaly_detector import anomaly_detector

def test_sre_agent():
    print("===============================================================")
    print("[AGENT TEST] AGENT LLM SRE COPILOT & CHAIN-OF-THOUGHT (ReAct)")
    print("===============================================================")

    # 1. Métriques d'entrée simulant l'alerte sur payment-api
    telemetry_input = {
        "memory_pct": 94.0,
        "cpu_pct": 97.0,
        "latency_ms": 2800.0,
        "error_rate_pct": 18.0
    }

    service_name = "payment-api"
    print(f"\n[TRIGGER] Lancement de l'investigation agentique sur '{service_name}'...")

    # 2. Exécution de l'investigation Copilot avec RAG + Chain of Thought
    rca_report = copilot_agent.investigate_incident(service_name, telemetry_input)

    print("\n--- [AGENT REASONING] CHAIN-OF-THOUGHT STEP BY STEP ---")
    for step in rca_report["chain_of_thought"]:
        print(f"\n[Step {step['step']}] {step['title']}")
        print(f"  |-- Detail : {step['detail']}")

    print("\n---------------------------------------------------------------")
    print("[RCA REPORT] FINAL ROOT CAUSE ANALYSIS REPORT")
    print("---------------------------------------------------------------")
    print(f"* Target Service     : {rca_report['service']}")
    print(f"* Root Cause         : {rca_report['root_cause']}")
    print(f"* Confidence Score   : {rca_report['confidence_score']}%")
    print(f"* Impacted Dep       : {', '.join(rca_report['impacted_dependencies'])}")
    print("* Evidence Collected :")
    for ev in rca_report['evidence']:
        print(f"  - {ev}")
    print(f"\n* Recommended Action : {rca_report['recommended_action']['description']}")

if __name__ == "__main__":
    test_sre_agent()
