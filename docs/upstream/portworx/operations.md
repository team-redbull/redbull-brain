# Keep your Portworx Deployment Up and Running

Source: https://docs.portworx.com/portworx-enterprise/operations (Portworx Enterprise 3.6)

Keep your Portworx Deployment Up and Running | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

You can maintain a reliable and high-performing Portworx environment by following operational best practices that help you monitor, scale, protect, and optimize your cluster throughout its lifecycle. The following day-2 operations helps you to maintain the performance, availability, and resilience of your cluster.

-
Observe your Portworx cluster using Prometheus, Grafana, and Portworx dashboards. Track storage and performance metrics such as health, latency, IOPS, and throughput to maintain visibility and detect issues early.

-
Create snapshots of your volumes on demand or on a schedule. You can clone these snapshots to PVCs and use them with your applications.

-
Provision and manage storage pools built from local disks or cloud drives.

-
Scale your cluster automatically or manually using Autopilot. Adjust capacity and storage pool size based on usage thresholds and operational needs.

-
Migrate workloads between Kubernetes clusters with Stork. Use ClusterPair objects and migration schedules to move volumes and applications safely and consistently.

-
Set up disaster recovery using synchronous (Metro DR) or asynchronous methods.

-
Tune performance by configuring a dedicated data interface, enabling LACP bonding, adjusting runtime parameters, and optimizing topology, StorageClasses, and volume placement.

-
Troubleshoot your environment by collecting diagnostics, resolving common errors (including vSphere-specific issues), using systemd integration, and enabling telemetry with Pure1.
