# Configure Multicluster Observability for Portworx metrics on ACM

Source: https://docs.portworx.com/portworx-enterprise/operations/observability/acm-multicluster-observability (Portworx Enterprise latest)

Configure Multicluster Observability for Portworx metrics on ACM | Portworx Enterprise Documentation

Red Hat Advanced Cluster Management (ACM) Multicluster Observability (MCO) collects and centralizes Prometheus metrics from workload clusters into a central ACM hub cluster. MCO stores these metrics in Thanos and makes them available through the built-in ACM Grafana dashboard. When you manage multiple Portworx clusters with ACM, you can use MCO to collect Portworx metrics from each workload cluster through OpenShift User Workload Monitoring and view them from a centralized interface on the hub cluster.

This topic explains how to configure ACM Multicluster Observability to collect Portworx metrics from workload clusters and make them available on the ACM hub cluster.

## Prerequisites​

Ensure that your cluster meets the following prerequisites:

- An ACM hub cluster with one or more imported workload clusters running Portworx Enterprise.

- Cluster administrator access to the hub cluster and each workload cluster.

- Object storage required by MCO to store metrics is available. For more information, see the Red Hat ACM documentation.

## Procedure​

### Step 1. Enable Multicluster Observability on the hub cluster​

Enable the MCO service on the ACM hub cluster. For more information, see the Red Hat ACM procedure for enabling the observability service.

### Step 2. Export Portworx metrics to OpenShift Prometheus​

On each workload cluster, configure Portworx to export its metrics to the OpenShift Prometheus deployment. For more information, see How to export Portworx metrics to OpenShift Prometheus.

### Step 3. Enable User Workload Monitoring on workload clusters​

MCO collects application metrics, such as Portworx metrics, through OpenShift User Workload Monitoring. On each workload cluster, enable User Workload Monitoring by setting `enableUserWorkload: true` in the `cluster-monitoring-config` ConfigMap. For more information, see Configure the OpenShift Prometheus deployment.

### Step 4. Add Portworx metrics to the MCO allowlist​

By default, MCO does not forward Portworx metrics from the workload clusters to the hub cluster. Add the Portworx metrics to the MCO custom allowlist so that the metrics collector forwards them.

warning

Use the `observability-metrics-custom-allowlist` ConfigMap, not `observability-metrics-allowlist`. The standard `observability-metrics-allowlist` ConfigMap is operator-managed, and any direct edits are overwritten during reconciliation.

On the hub cluster, apply a ConfigMap to define the Portworx metrics that MCO should collect from workload clusters. The following example includes a representative set of Portworx metrics. Modify the entries under `names` to add or remove metrics based on your monitoring requirements:

```

oc apply -f - <<'EOF'

apiVersion: v1

kind: ConfigMap

metadata:

  name: observability-metrics-custom-allowlist

  namespace: open-cluster-management-observability

data:

  uwl_metrics_list.yaml: |

    names:

      - px_pool_stats_pool_status

      - px_cluster_disk_utilized_bytes

      - px_volume_capacity_bytes

      - px_pool_stats_used_bytes

      - px_node_stats_cpu_usage

EOF

```

After you apply the ConfigMap, the `endpoint-observability-operator` on each workload cluster detects the change and redeploys the `uwl-metrics-collector-deployment` with the updated `--match=` arguments, typically within about 60 seconds. For more information, see the Red Hat ACM procedure for adding custom metrics.

### Step 5. Verify the metrics on the hub cluster​

Verify that the Portworx metrics from the workload clusters are available on the hub:

-
From the OpenShift console on the ACM hub cluster, open the built-in ACM Grafana dashboard.

-
Run the following PromQL query:

```

px_node_stats_cpu_usage{cluster="<cluster-name>"}

```

Replace `<cluster-name>` with the name of a workload cluster.

-
Confirm that the query returns data for the specified workload cluster.

In this topic:
