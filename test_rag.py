import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))
from app.agent.rag_engine import rag_engine

def test_rag_queries():
    print("===============================================================")
    print("[RAG TEST] BASE DE CONNAISSANCES SRE (ChromaDB Vector Engine)")
    print("===============================================================")

    queries = [
        "payment-api memory high OOMKilled heap space",
        "CPU throttling latency P99 2000ms",
        "Database connection pool timeout 500 error"
    ]

    for q in queries:
        print(f"\n[QUERY] Incident Search: '{q}'")
        results = rag_engine.search_similar_runbook(q, top_k=1)
        if results:
            res = results[0]
            print(f"[FOUND] Runbook Matched: {res['filename']} (Score: {res['score']})")
            print("--- Content Snippet ---")
            lines = res['content'].split('\n')[:8]
            print('\n'.join(lines))
            print("-----------------------")
        else:
            print("[NOT FOUND] No matching runbook found.")

if __name__ == "__main__":
    test_rag_queries()
