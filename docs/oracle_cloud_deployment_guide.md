# ☁️ Oracle Cloud "Always Free" Deployment Guide

This guide walks through deploying the **AIOps Copilot Platform** onto an Oracle Cloud Always Free K3s/Kubernetes cluster.

---

## 📌 Prerequisites

1. An **Oracle Cloud Free Tier Account** ([oracle.com/cloud/free](https://www.oracle.com/cloud/free/)).
2. An **Ampere A1 Compute Instance** (Always Free: 4 OCPUs, 24GB RAM, Ubuntu 22.04 LTS).
3. Docker & `kubectl` installed on the instance.

---

## 🛠️ Step 1: Install K3s (Lightweight Kubernetes) on Oracle VPS

Connect to your Oracle VPS via SSH and run:
```bash
curl -sfL https://get.k3s.io | sh -
sudo chmod 644 /etc/rancher/k3s/k3s.yaml
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
kubectl get nodes
```

---

## 🛠️ Step 2: Build & Push Docker Image

On your local machine or build server:
```bash
docker build -t farahbenchikha/aiops-copilot:latest .
docker push farahbenchikha/aiops-copilot:latest
```

---

## 🛠️ Step 3: Apply Kubernetes Manifests

On your Oracle Cloud K3s instance:
```bash
git clone https://github.com/farahbenchikha/AI-Incident-Management-Platform.git
cd AI-Incident-Management-Platform

kubectl apply -f k8s_manifests/configmap.yaml
kubectl apply -f k8s_manifests/deployment.yaml
kubectl apply -f k8s_manifests/service.yaml
```

---

## 🛠️ Step 4: Verify Deployment & Public Access

Check pod status:
```bash
kubectl get pods -w
kubectl get svc aiops-copilot-service
```

Access the AI Operations Center Dashboard at:
`http://<YOUR_ORACLE_PUBLIC_IP>:8000/dashboard`
