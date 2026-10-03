# SRE Runbook: CPU Throttling & High Latency Incident Response

## Overview
CPU throttling occurs when a Kubernetes container exceeds its allocated CPU quota (`resources.limits.cpu`), causing the kernel CFS (Completely Fair Scheduler) to freeze container threads for periods within a quota period.

## Symptoms & Detection Signals
- **Prometheus Metrics**:
  - `container_cpu_cfs_throttled_periods_total` / `container_cpu_cfs_periods_total` > 25%.
  - `node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate` approaching `limits.cpu`.
  - HTTP Request Latency P99 spiking from 120ms to > 2.0s.
- **Loki Logs**:
  - Timeout exceptions (`ClientTimeoutException`, `Gateway Timeout 504`).
- **K8s Events**:
  - `HorizontalPodAutoscaler` scaling events or pod CPU saturation warnings.

## Recommended Remediation Actions
1. Remove or increase container CPU limits (`resources.limits.cpu`).
2. Scale HorizontalPodAutoscaler (HPA) target CPU utilization threshold or increase min/max replicas.
