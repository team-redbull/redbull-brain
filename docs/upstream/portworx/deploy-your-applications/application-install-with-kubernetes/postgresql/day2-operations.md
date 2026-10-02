# Day 2 operations and reliability

Source: https://docs.portworx.com/portworx-enterprise/deploy-your-applications/application-install-with-kubernetes/postgresql/day2-operations (Portworx Enterprise 3.6)

Day 2 operations and reliability | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Once your PostgreSQL environment is up and running, the real work of maintaining reliability, security, and efficiency begins. Effective Day 2 operations focus on everything from rolling upgrades to backup and restore strategies, ensuring your data remains protected and recoverable. By proactively monitoring system health and setting meaningful alerts, you can catch issues before they escalate, reducing the chance of downtime. Should problems arise, having a solid troubleshooting framework in place enables quick resolution and keeps your critical workloads running smoothly.

## Day 2 operations​

Keeping your PostgreSQL and Portworx environments up-to-date is crucial for maintaining a secure, high-performing, and feature-rich deployment. By planning and executing regular upgrades, whether they involve PostgreSQL itself, Portworx, or the underlying Kubernetes cluster, you can quickly benefit from new capabilities, address security patches, and minimize the risk of unexpected outages.

Scenarios

- PostgreSQL version upgrades: Validate extensions and perform rolling restarts.

- Portworx upgrades: Use the Operator or Helm to ensure seamless storage updates.

- Kubernetes upgrades: Check Portworx compatibility; maintain node health checks.

Key benefits

- Continuous innovation: Quickly adopt new PostgreSQL features.

- Safe rolling upgrades: Maintain availability at each step.

- Minimal overhead: Operator-driven processes handle complexity.

## Backups and restores​

A robust backup and restore strategy is more than just an insurance policy, it is a foundational element of any mission-critical system. By combining PostgreSQL‑specific techniques like WAL archiving with Portworx snapshots and Portworx Backup, you can confidently recover from failures or data corruption, minimizing downtime and safeguarding your organization’s most valuable asset: its data.

Approaches

- Local snapshots: For quick, point-in-time recovery.

- Portworx Backup: A dedicated solution for backing up Portworx volumes and Kubernetes resources.

- WAL archiving: PostgreSQL‑specific point-in-time recovery (PITR).

Key benefits

- Short RPO: Frequent snapshots for near real-time recoveries.

- Fast restores: Minimize downtime with volume-level revert operations.

- Offsite DR: Replicate snapshots to S3, Azure, or GCP

For more information, refer to:

- Portworx snapshots

- Portworx Backup

## Monitoring and alerts​

Real-time insights into both your PostgreSQL database and the underlying Portworx storage are critical for detecting issues before they impact users. By correlating metrics such as I/O latency, replication status, and resource utilization, you can swiftly identify bottlenecks, optimize performance, and address potential failures early. This proactive approach saves time, reduces the risk of downtime, and helps maintain a seamless user experience.

Key benefits

- Single-pane visibility: Aggregate metrics from Portworx, Kubernetes, and PostgreSQL.

- Early detection: Spot replication lag, node failures, or volume saturation.

- Actionable intelligence: Correlate DB and storage metrics for root-cause analysis.

Recommended metrics

- Portworx: `px_node_status`, `px_volume_used_bytes`, `px_pool_available_bytes`, `px_volume_latency`

- PostgreSQL: `pg_stat_activity`, `pg_database_size`, `pg_stat_replication`, WAL lag

## Alerts and thresholds​

Timely and targeted alerts enable you to address issues such as escalating resource usage or abnormal latency, before they become user-facing problems. By configuring custom thresholds and integrating notifications into your on-call workflow, you can prioritize critical events, rapidly pinpoint root causes, and maintain continuous availability for your PostgreSQL on Portworx environment.

Key benefits

- Reduced downtime: Quick responses to performance or capacity issues.

- Integrated on‑call: Connect to PagerDuty, Slack, or email.

- Customizable thresholds: Tailor usage, latency, or replication-lag alerts per environment.

Common alert examples

- Volume/Pool usage: 80% warning, 90% critical.

- Node offline: Immediate alert if unreachable.

- Replication lag: Alert if standby lags beyond a set threshold.

## Troubleshooting tips​

Having a structured troubleshooting approach ensures that you can quickly diagnose and address issues, whether they are related to PVC pending states, performance bottlenecks, or node failures, before they significantly affect your end-users. By proactively documenting common scenarios and their resolutions, you will minimize downtime and maintain confidence in your overall PostgreSQL on Portworx deployment.

Common scenarios

- PVC pending: Validate correct StorageClass, node resources, Portworx health.

- Low performance: Check CPU/memory, network conditions, replication overhead.

- Failing node: Rely on storage replication and Stork scheduling for auto-recovery.

Key benefits

- Confidence under pressure: Clear, step-by-step procedures.

- Faster MTTR: Less downtime with standardized playbooks.

- Post-incident analysis: Incorporate lessons learned for future prevention.

In this topic:
