# SRE Runbook: Database Connection Pool Exhaustion & Cascading 500 Errors

## Overview
Database Connection Pool Exhaustion occurs when downstream application workers consume all available pool connections, causing incoming requests to block, queue up, and eventually time out with HTTP 500 or 504 Gateway Timeout responses.

## Symptoms & Detection Signals
- **Prometheus Metrics**:
  - `hikaricp_pending_threads` or `db_pool_active_connections` at 100% capacity.
  - Spikes in HTTP 500 error rates across dependent microservices (`checkout-service`, `payment-api`).
  - Average latency surging > 3.5 seconds.
- **Loki Logs**:
  - `ConnectionPoolTimeoutException: Timeout waiting for connection from pool`.
  - `PSQLException: FATAL: remaining connection slots are reserved for non-replication superuser connections`.

## Recommended Remediation Actions
1. **Immediate Action**:
   - Temporarily increase max connection pool size (`SPRING_DATASOURCE_HIKARI_MAXIMUM_POOL_SIZE` or `DB_POOL_SIZE`).
   - Restart idle worker pods to release hung database sockets (`kubectl rollout restart deployment <service-name>`).
2. **Permanent Fix**:
   - Tune database query execution time, add missing DB indexes, and set strict query timeout limits.
