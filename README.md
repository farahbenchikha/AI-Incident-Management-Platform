# 🧠 AIOps Copilot — Intelligent Kubernetes Incident Management Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Native-326CE5.svg?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-ff6600.svg)](https://www.trychroma.com/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Isolation%20Forest-F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)

An autonomous **AI-powered Cloud Operations & Incident Management Platform** for Kubernetes environments. 
It ingests multi-source telemetry (Prometheus metrics, Loki logs, K8s cluster events), detects metric anomalies using ML (*Isolation Forest*), performs Agentic Root Cause Analysis (RCA) via RAG-enhanced SRE Runbooks, and executes safe Human-in-the-Loop (HITL) automated remediations.

---

## 🏛️ System Architecture

```
                    Kubernetes Cluster (Pods, Deployments, Events)
                                          │
                   ┌──────────────────────┼──────────────────────┐
                   ▼                      ▼                      ▼
             Prometheus                Loki                   Jaeger / OTel
           (Metrics Engine)        (Logs Engine)          (Distributed Traces)
                   │                      │                      │
                   └──────────────────────┼──────────────────────┘
                                          ▼
                                AIOps Telemetry Engine
                                          │
                     ┌────────────────────┼────────────────────┐
                     ▼                    ▼                    ▼
             Anomaly Detection    Event Correlation    RAG Runbook VectorDB
             (Isolation Forest)    (K8s Graph Topology)     (ChromaDB / SRE Docs)
                     │                    │                    │
                     └────────────────────┼────────────────────┘
                                          ▼
                               Agentic LLM Incident Copilot
                               (FastAPI + ReAct SRE Agent)
                                          │
                     ┌────────────────────┼────────────────────┐
                     ▼                    ▼                    ▼
             Root Cause Analysis    Remediation Engine    Notifications
             (RCA & Confidence)    (Kubectl Actions)    (Slack / Email / Webhook)
                                          │
                                          ▼
                             AI Operations Center Dashboard
                               (Next.js / React Frontend)
```

---

## ✨ Key Features

- **📊 Multi-Source Telemetry Aggregation**: Seamless ingestion of live container metrics (CPU, RAM, Latency, Error rates), Loki logs, and Kubernetes cluster events.
- **⚡ ML Anomaly Detection**: Real-time statistical and Machine Learning anomaly detection (*Isolation Forest*) to calculate incident severity and confidence scores.
- **🧠 Agentic SRE Copilot & RAG**: ReAct agent with tool execution capabilities (`promql`, `loki_query`, `kubectl`) backed by a **ChromaDB** vector store containing SRE Postmortems and Runbooks.
- **🛡️ Human-in-the-Loop Safe Remediation**: Automated recommendation engine supporting one-click resource patching (e.g. memory limit scaling, pod rollbacks).
- **🖥️ AI Cloud Operations Center UI**: Real-time executive & SRE dashboard featuring live cluster health scores, telemetry graphs, log terminal, and step-by-step Chain-of-Thought reasoning.

---

## 📂 Project Structure

```text
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI REST Endpoints (health, incidents, investigate, remediate)
│   │   ├── ml/           # Machine Learning Anomaly Detector (Isolation Forest)
│   │   ├── agent/        # Agentic SRE Copilot & RAG Vector Engine
│   │   └── remediation/  # Kubernetes Action Execution Controller
│   ├── main.py           # Core FastAPI Application Server
│   └── requirements.txt  # Python Dependencies
├── simulator/
│   └── k8s_mock_cluster.py # K8s Telemetry & Chaos Injection Simulator (23 Microservices)
├── rag_docs/
│   └── runbooks/         # SRE Incident Runbooks (Memory Leak, CPU Throttling, DB Timeout)
├── frontend/
│   └── index.html        # AI Cloud Operations Center Dashboard UI
├── run_demo.py           # One-click Launcher (API Server + Web Dashboard)
└── test_rag.py           # RAG Vector Search CLI Verification Script
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- `git`

### 1. Clone the Repository
```bash
git clone https://github.com/farahbenchikha/AI-Incident-Management-Platform.git
cd AI-Incident-Management-Platform
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv backend/venv
# On Windows:
.\backend\venv\Scripts\activate
# On Linux/macOS:
source backend/venv/bin/activate

pip install -r backend/requirements.txt
```

### 3. Verify RAG Engine Vector Retrieval
```bash
python test_rag.py
```

### 4. Launch AI Cloud Operations Center (One-Click Demo)
```bash
python run_demo.py
```
This command will:
1. Start the FastAPI backend API engine on `http://127.0.0.1:8000`.
2. Automatically launch the **AI Cloud Operations Center Dashboard** in your default web browser.

---

## 🧪 Interactive Chaos & Incident Flow Demo

1. Open the Dashboard UI (`frontend/index.html`).
2. Click **[ INJECT MEMORY LEAK CHAOS ]** to trigger a simulated memory leak on `payment-api`.
3. Observe live metric degradation (CPU 97%, RAM 94%, Latency 2.8s, Errors 18%, Cluster Health 91.3%).
4. Click **[ INVESTIGATE ]** to inspect the Agentic SRE Copilot's 4-step Chain-of-Thought reasoning.
5. Click **[ REMEDIATE ]** to apply the recommended resource patch (`memory: 512Mi`), restoring cluster health to **100%**.

---

## ☁️ Deployment Strategy

- **Development Environment**: Local Python execution with K8s Telemetry Simulator / Minikube via WSL2 (100% Free).
- **Production Demo**: Cloud deployment on **Oracle Cloud Always Free Tier** (Arm Ampere A1, 4 OCPUs, 24GB RAM) using Docker & K3s.

---

## 📄 License
Licensed under the [MIT License](LICENSE).
