# Disaster Recovery with Red Hat Advanced Cluster Management

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/acm-dr (Portworx Enterprise 3.6)

Disaster Recovery with Red Hat Advanced Cluster Management | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Red Hat Advanced Cluster Management (ACM) for Kubernetes is a Red Hat operator that allows you to manage multiple OpenShift Kubernetes clusters from a single hub cluster. After you install ACM, the OpenShift console provides a single-cluster view for managing the local cluster and a multicluster management view for managing common operations across all registered clusters from a centralized interface.

The Portworx MultiCluster Operator integrates with ACM to provide asynchronous disaster recovery (DR) for Portworx Enterprise clusters directly from the OpenShift console. For more information on Portworx Multi-Cluster Operator, see Install Portworx MultiCluster Operator.
This integration removes the need to perform the manual DR cluster pairing workflow through CLI.

## Features of ACM-based disaster recovery with Portworx​

The Async DR workflow requires multiple manual prerequisite steps, including generating and exchanging kubeconfigs, creating object store credentials, generating cluster pair specifications, and applying configurations on both clusters before Stork can start scheduled migrations.

The MultiCluster Operator simplifies the asynchronous DR and multi-cluster management by:

- Automating cluster pairing: Handles kubeconfig exchange, cluster pair creation, and backup location configuration internally.

- Running preflight checks automatically: Validates `StorageCluster` annotations, Stork privileges, supported Portworx and Stork versions, security settings, and admin namespace consistency on both clusters. The DR pair creation workflow is enabled only after all checks pass.

- Supporting disaster recovery orchestration: Automates disaster recovery migration schedule creation (using DR Protection Groups), failover, and failback operations across paired clusters.

- Providing centralized DR posture: Displays cluster health, Portworx installation status, DR readiness, and replication status from a single interface.

- Allowing independent operator upgrades: Supports independent Multi-Cluster Operator releases while remaining compatible with supported versions of Portworx Enterprise running on workload clusters.

## How ACM-based disaster recovery works​

In an ACM-based disaster recovery deployment, you designate one OpenShift cluster as the hub cluster and install the following operators on it:

- The Red Hat Advanced Cluster Management operator, which provides multi-cluster management capabilities.

- The Portworx MultiCluster Operator, which includes an OpenShift console plugin and provides disaster recovery orchestration.

The hub cluster manages one or more workload clusters where Portworx Enterprise is installed and where application workloads run. The hub cluster itself does not require Portworx Enterprise.

The high-level workflow to configure ACM-based disaster recovery is as follows:

- Install the Portworx MultiCluster Operator on the ACM hub cluster.

- Import OpenShift clusters running Portworx Enterprise into ACM as workload clusters. For more information, see the Red Hat ACM cluster import documentation.

- Create a Disaster Recovery Pair to establish a replication channel between two workload clusters.

- Create a Protection Group to protect applications and namespaces on the source cluster.

- Failover to the destination cluster when the source cluster is unavailable.

- Failback to the source cluster when it is available again.

You can perform the configuration steps, such as creating the DR pair and protection groups, through the OpenShift console or declaratively through GitOps. For more information about the declarative approach, see Manage ACM Disaster Recovery using GitOps.

The MultiCluster Operator introduces the following Kubernetes custom resource definitions (CRDs) to provide centralized disaster recovery management:

CRDPurpose

`Cluster`Represents a workload cluster and exposes DR readiness, Portworx installation status, cluster health status, platform, and capacity information.

`DisasterRecoveryPair`Represents a DR relationship between clusters. Internally manages `ClusterPair` creation, and backup location configuration.

`ProtectionGroup`Manages DR configuration, including `MigrationSchedule`, `SchedulePolicy`, migrations, and migration specifications. Supports both forward and reverse migration workflows.

`DisasterRecoveryAction`Represents DR operations such as failover and failback and maps directly to Stork actions.

For the full schema and example manifests of these CRDs, see ACM DR CRD Reference.

## Supported configurations​

Portworx qualifies ACM-based disaster recovery on OpenShift Container Platform (OCP) version 4.18 or later with the following hub cluster and workload cluster configurations.

### Same-platform combinations​

You can perform disaster recovery when the hub cluster and both workload clusters (the source and the destination) run on the same platform, using the following combinations:

- OCP on VMware

- OCP on Bare Metal

- OCP cluster hosted on Google Cloud Platform (GCP)

- OCP with IPv6 configuration

### Cross-platform combinations​

You can perform disaster recovery between a source workload cluster and a destination workload cluster that run on different platforms, using the following combination:

- OCP on Bare Metal and Red Hat OpenShift Service on AWS (ROSA)

## Limitations​

- Supports asynchronous DR pairs only.

- You can fail over or fail back a protection group only once. Select all the namespaces that you want to include in the first operation. After the operation starts, migration for the protection group stops, and you cannot fail over or fail back any namespaces that were excluded.

- Only one DR pair can exist between the same source and destination clusters for a specific backup location. For example, if a pair already exists between cluster A and cluster B, you cannot create another A-to-B pair. However, you can create pairs between A and C or A and D.

- The cluster admin namespace must have the same name on both workload clusters. By default, Portworx uses the `kube-system` namespace as the cluster admin namespace. You can optionally configure a custom cluster admin namespace, but you must use the same namespace name on both clusters. If the namespace names differ, DR pair creation fails. For more information about configuring the cluster admin namespace, see Configure the Cluster Admin namespace.

- The Portworx Multi-Cluster Operator requires a hub cluster managed by Red Hat Advanced Cluster Management (ACM). Standalone OpenShift clusters without ACM cannot use this workflow.

- Resource transformation specs are not supported. When you create a migration schedule through ACM-based DR, the MultiCluster Operator does not apply `ResourceTransformation` specs, unlike the `storkctl create migrationschedule` command, which supports transformation specs through the `--transform-spec` flag. For more information, see Create MigrationSchedule.

- All limitations of the standalone Async DR workflow continue to apply. For more information, see Asynchronous Disaster Recovery.

In this topic:
