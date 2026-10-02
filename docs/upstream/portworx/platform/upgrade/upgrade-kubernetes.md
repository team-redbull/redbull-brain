# Upgrade Kubernetes using Smart Upgrade

Source: https://docs.portworx.com/portworx-enterprise/platform/upgrade/upgrade-kubernetes (Portworx Enterprise 3.6)

Upgrade Kubernetes using Smart Upgrade | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This document explains how to leverage the smart upgrade feature of Portworx to upgrade multiple Kubernetes nodes in parallel without any disruption.

## Smart upgrade​

The Smart upgrade feature introduces a streamlined, resilient upgrade process for Kubernetes nodes, allowing them to be upgraded in parallel while maintaining volume quorum and without application disruption.

The upgrade process for Kubernetes clusters is streamlined using per-node PodDisruptionBudgets (PDBs). Operator creates a dedicated PDB for each Portworx storage node. These per-node PDBs ensure granular control over node disruptions, allowing parallel upgrades without risking volume quorum.

During upgrades, the Operator dynamically adjusts the PDBs to enable safe draining of nodes selected for upgrade. Nodes are carefully chosen to avoid disrupting volume availability, with volume provisioning disabled on upgrading nodes. This method significantly reduces upgrade times, enhances cluster resilience, and maintains high availability throughout the process.

By default, smart upgrade is disabled, and cluster-wide PDB will be used where `minAvailable` set to `numStorageNodes - 1`, which means one Kubernetes node is upgraded at a time.

You can enable the smart upgrade by setting the `portworx.io/disable-non-disruptive-upgrade` annotation to false. Also, you can configure the minimum number of nodes that must be available at a time using the `portworx.io/storage-pdb-min-available` annotation in the StorageCluster.

note

Smart upgrade is supported only when there is one node group per availability zone, and only one node group is upgraded at a time for AKS and EKS clusters. If the cluster has node groups spread across multiple zones or if multiple node groups are upgraded together, the operator raises a warning event and adds a condition to the `StorageCluster` status.

This check is triggered in the following cases:

- When the operator is upgraded to version 25.1.0 or later

- When a new `StorageCluster` is created

- Each time the operator detects one or more cordoned nodes as part of the upgrade process

The following are the key benefits of using smart upgrades:

- Parallel upgrades: Based on volume distribution, the Portworx Operator tries the best to select multiple nodes for concurrent upgrades, accelerating the upgrade process while eliminating downtime and application disruption.

- Volume quorum maintenance: Ensures volume quorum is maintained throughout the upgrade process.

- Managed node upgrades: You can use the `portworx.io/storage-pdb-min-available` annotation in the StorageCluster CRD to manage the number of nodes upgraded in parallel.

- Automatic reconciliation: The Portworx operator actively monitors and reconciles the storage nodes during upgrades, ensuring smooth progression while preserving quorum integrity.

important

- There will be a downtime for applications using volumes with a replication factor of 1.

- Smart upgrade is not supported for synchronous DR setup.

## Prerequisites​

For smart upgrades, ensure the following prerequisites are met:

- Required Portworx and Operator versions:

- Portworx version 3.1.2 or later

- Operator version 25.1.0 or later. For Anthos, Operator version should be 24.2.0 or later.

- The cluster must be ready and available for upgrade. You can use the `pxctl status` and `kubectl get storagenodes -n portworx` commands to check the cluster status.

- No nodes or pools should be under maintenance.

- No decommissioned nodes should appear in the output of the `kubectl get storagenodes` command.

- No nodes should have the `px/service=stop` or `px/service=disabled` label. If nodes have these labels, remove them and restart the Portworx service or decommission the node before the upgrade.

## Upgrade Kubernetes​

-
To upgrade your Kubernetes cluster using the smart upgrade feature, make the following changes in the StorageCluster:

-
Enable the smart upgrade by setting the `portworx.io/disable-non-disruptive-upgrade` annotation to `false`.

note

When smart upgrade is enabled, the operator uses `quorum` as the `minAvailable` value by default. If you want to override the value, follow the next step.

-
(Optional) Set the minimum number of nodes that must be available during upgrade using the `portworx.io/storage-pdb-min-available` annotation.

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  name: portworx

  namespace: <px-namespace>

  annotations:

    portworx.io/disable-non-disruptive-upgrade: "false"

    # If you want to override the default value of `minAvailable`, uncomment the below line and set a desired value.

    # portworx.io/storage-pdb-min-available: "2"

```

-
Upgrade your Kubernetes cluster.

note

For Anthos clusters, when `storage-pdb-min-availablevalue` is set in StorageCluster during upgrade from version 1.29 to 1.30, you must invoke the user cluster upgrade command with `--skip-validation-all` and `--skip-pre-upgrade-checks=true` flags.

important

To help prevent application downtime and data loss during upgrades, Portworx allows volumes to resync as needed. This behavior can significantly increase upgrade time, particularly under heavy I/O workloads. Upgrades might also fail if pods can’t be evicted in time. Common causes include a short node drain timeout or too few storage nodes for the application workload.

Set the node drain timeout to at least 1 hour, and increase it further if upgrades fail because of pod eviction issues.

In this topic:
