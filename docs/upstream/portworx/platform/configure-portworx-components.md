# Configure Portworx Components

Source: https://docs.portworx.com/portworx-enterprise/platform/configure-portworx-components (Portworx Enterprise latest)

Configure Portworx Components | Portworx Enterprise Documentation

This section outlines how to configure essential Portworx components that provide storage orchestration, dynamic volume management, and help with monitoring storage nodes in Kubernetes environments.

Portworx Operator is a primary component that manages the complete Portworx Enterprise deployment in Kubernetes. The operator deploys and manages the complete lifecycle of the Portworx pods. Portworx Operator follows a separate release cycle from Portworx Enterprise. For information about Operator updates, see the Operator Release Notes.

When you install Portworx Enterprise, Portworx Operator deploys the following components in the Portworx stack by default, unless you have customized the installation to disable them.

-
Portworx Autopilot - A rule-based engine that responds to changes based on metric conditions and then automatically takes actions such as adding capacity, rebalancing storage, and so on. Autopilot allows you to specify monitoring conditions along with actions it should take when those conditions occur. For information on Autopilot and how to enable or upgrade Autopilot, see Portworx Autopilot. To know about how Autopilot can be used to scale your clusters, see Automate storage operations with Autopilot. Autopilot has its own release cycle, and the updates are captured in the Autopilot Release Notes.

-
Portworx Stork - Portworx's storage scheduler for Kubernetes that helps achieve tighter integration of Portworx with Kubernetes. Stork allows users to co-locate pods with their data, provides seamless migration of pods in case of storage errors, and makes it easier to create and restore snapshots of Portworx volumes. Stork consists of 2 components, the Stork scheduler and an extender. Both of these components run in HA mode with 3 replicas by default. For information on Stork and how to enable or upgrade Stork, see Portworx Stork. Stork has its own release cycle, and the updates are captured in the Stork Release Notes.

-
Portworx Telemetry - An integration that automatically uploads the diagnostics bundle and real-time Prometheus metrics from your Portworx cluster to Pure1. This enables support teams to proactively monitor and troubleshoot your clusters. For information on how to enable or disable telemetry, see Portworx Telemetry. When telemetry is enabled, you can also use Pure1 AI Copilot to interact with your Portworx storage clusters using natural language. For more information, see Portworx on Pure1 AI Copilot.

-
CSI Driver - A standardized plugin that manages the full Kubernetes volume lifecycle including dynamic provisioning, cloning, expansion, snapshotting (local and cloud), volume restoration, shared (RWX) volumes, raw block volumes, ephemeral storage, and encryption/RBAC-based security via native Kubernetes APIs. For more information, see Manage Volume Lifecycle with CSI Driver.

When you upgrade Portworx Enterprise, these components are automatically upgraded. The updated plugin version is aligned with the Portworx Enterprise version you are upgrading to.

For Portworx Enterprise on OpenShift clusters, the following integrations are available:

-
Portworx OpenShift Dynamic Plugin - An integrated storage observability and management component available directly in the OpenShift console. The plugin provides monitoring and troubleshooting capabilities for Portworx storage clusters, Kubernetes applications, and OpenShift integrations such as KubeVirt.
 For information about enabling or upgrading the plugin, see Enable or Upgrade Portworx OpenShift Dynamic Plugin.
 The Portworx OpenShift Dynamic Plugin follows a separate release cycle from Portworx Enterprise. For information about plugin updates, see the Portworx OCP Release Notes.

-
Portworx MultiCluster Operator - An integration that extends Red Hat Advanced Cluster Management (ACM) to provide asynchronous disaster recovery and centralized multi-cluster management for Portworx Enterprise clusters directly from the OpenShift console. It removes the need to perform the standalone Stork-based Async DR cluster pairing workflow through multiple CLI steps. For information on how to install the operator, see Install Portworx MultiCluster Operator.

For Portworx Enterprise with Everpure FlashArray and FlashBlade, the following integrations are available:

-
FA/FB driver - A Portworx Enterprise component that provides enhanced storage capabilities for FlashArray Direct Access (FADA), FlashBlade Direct Access (FBDA), and FlashArray File volumes. The driver supports Kubernetes-native provisioning, attachment, snapshot, and other volume lifecycle operations. For more information, see FlashArray/FlashBlade Driver.

-
Portworx Fusion Controller (early access) - A unified, application-aware platform that combines Everpure Fusion’s fleet-level management with Portworx’s Kubernetes-native data services. Portworx Fusion Controller connects Kubernetes clusters to Fusion fleets, enabling access to storage presets and workloads. For more information, see Enable Portworx Fusion Controller.
