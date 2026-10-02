# Autopilot Use cases

Source: https://docs.portworx.com/portworx-enterprise/operations/scale-portworx-cluster/autopilot/use-cases (Portworx Enterprise 3.6)

Autopilot Use cases | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

The following sections describe common Autopilot use cases and provide end-to-end examples with Kubernetes specs that are Prometheus compatible. Please refer to the AutoPilotRule CRD to see how to configure AutopilotRule with Datadog as a metrics provider.

Use caseDescription

Automatically grow PVCsUse Autopilot to expand PVCs automatically when they begin to run out of space.

Expand all storage pools in your clusterUse Autopilot to expand every storage pool in your cluster until they reach a specified capacity.

Automatically expand storage poolsUse Autopilot to expand storage pools automatically when they begin to run out of space.

Automatically rebalance storage poolsUse Autopilot to rebalance storage pools automatically when they deviate from average provisioned or used space across the cluster.
