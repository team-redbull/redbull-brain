# Observability

Source: https://docs.portworx.com/portworx-enterprise/operations/observability (Portworx Enterprise latest)

Observability | Portworx Enterprise Documentation

Portworx Enterprise provides built-in observability features to help you monitor the health of your cluster deployment, collect metrics, and send diagnostic information to Everpure support. Observability ensures that both cluster operators and Everpure can detect issues quickly and maintain system reliability. Observability varies depending on your deployment environment.

-
For the majority of setups, Portworx Enterprise's integrated Prometheus and Grafana deployment runs by default. For more information about configuring the Portworx monitoring solution for clusters on Kubernetes, see Monitor Portworx Clusters on Kubernetes.

-
If you are operating Portworx Enterprise on OCP, you must configure components to work with the OCP Prometheus deployment for monitoring, since the native Portworx Prometheus support is not available on newer OCP versions. For more information about configuring the Portworx monitoring solution for clusters on OpenShift, see Configure Portworx Monitoring on OpenShift.

-
You can use the Portworx OpenShift Dynamic plugin in the OpenShift console to:

- Monitor the health, performance, and configuration of your Portworx storage cluster from the Portworx dashboard. For more information, see Monitor Portworx Clusters on Openshift.

- Monitor your PVCs or Disks for KubeVirt VMs directly within the OpenShift Container Platform (OCP), providing actionable insights. For more information, see Monitor Portworx Clusters on Openshift.

-
If you manage multiple Portworx clusters with Red Hat Advanced Cluster Management (ACM), you can collect and centralize Portworx Prometheus metrics from your managed clusters into the ACM hub cluster using MultiCluster Observability. For more information, see Configure ACM Multicluster Observability for Portworx metrics.

-
You can also use the Portworx extension in the Rancher UI to monitor your cluster directly within the Rancher platform, simplifying cluster management and providing actionable insights. For more information, see Monitor Portworx Cluster in Rancher UI.

-
If you enable the FA/FB driver, Portworx Enterprise provides the following observability capabilities for FlashArray and FlashBlade Direct Access volumes:

- Monitor per-volume usage and capacity, and per-node iSCSI, NVMe, Fibre Channel, and multipath connectivity by using Prometheus metrics. For more information, see Monitor FlashArray and FlashBlade volumes.

- Visualize FlashArray and FlashBlade metrics in Grafana. For more information, see Grafana dashboards.

- Send logs and diagnostic information to Pure1 through Portworx Enterprise telemetry. For more information, see Telemetry.
