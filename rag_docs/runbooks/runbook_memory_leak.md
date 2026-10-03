# SRE Runbook: Kubernetes Memory Leak & OOMKilled Incident Response

## Overview
Memory leak incidents occur when an application continuously allocates memory without returning it to the operating system, eventually leading to Pod eviction or `OOMKilled` (Exit Code 137) by the Linux Out-Of-Memory Killer.

## Symptoms & Detection Signals
- **Prometheus Metrics**:
  - `container_memory_working_set_bytes` approaching `container_spec_memory_limit_bytes` (> 90%).
  - Gradual upward trend in memory slope over time without stabilization after garbage collection.
  - Pod restarts count increasing (`kube_pod_container_status_restarts_total`).
- **Loki Logs**:
  - `java.lang.OutOfMemoryError`, `JavaScript heap out of memory`, or `MemoryAllocationError`.
  - Garbage collection log pauses exceeding SLA thresholds.
- **K8s Events**:
  - `SystemOOM` or `OOMKilled` events reported by `kubelet`.

## Root Cause Analysis (RCA) Guidelines
1. Check if recent deployments introduced memory-intensive cache layers, unclosed database connections, or unhandled file streams.
2. Inspect if the configured memory limit in `resources.limits.memory` is undersized for current production traffic load.
3. Correlate with downstream services (`checkout-service`, `payment-api`): Memory pressure often degrades HTTP processing speed, causing request queuing.

## Recommended Remediation Actions
1. **Immediate Mitigation (Traffic & Limits)**:
   - Patch container resource limit: Increase `limits.memory` (e.g. from `256Mi` to `512Mi` or `1Gi`).
   - Trigger a rolling restart (`kubectl rollout restart deployment <dep-name>`) to flush process heap memory.
   - Scale out deployment replicas (`kubectl scale deployment <dep-name> --replicas=<N>`) to distribute load.
2. **Permanent Fix**:
   - Profile application memory dump (heap dump) and submit bug fix PR.
