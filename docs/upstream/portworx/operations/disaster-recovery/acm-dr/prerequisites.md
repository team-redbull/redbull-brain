# Prerequisites for ACM Disaster Recovery

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/acm-dr/prerequisites (Portworx Enterprise latest)

Prerequisites for ACM Disaster Recovery | Portworx Enterprise Documentation

Before you configure ACM-based disaster recovery, ensure your environment meets the following requirements.

## Hub cluster​

Ensure that the hub cluster meets the following prerequisites:

- The Portworx MultiCluster Operator is installed on the hub cluster. For more information, see Install the Portworx MultiCluster Operator.

- The `governance-policy-framework`, `config-policy-controller`, and `search-collector` ACM add-ons are enabled. These add-ons provide policy management, cluster configuration monitoring, and resource discovery capabilities required by the Portworx MultiCluster Operator.
You enable these add-ons through the `KlusterletAddonConfig` resource. The `policyController` setting enables both the `governance-policy-framework` and `config-policy-controller` add-ons, and the `searchCollector` setting enables the `search-collector` add-on. For more information, see the Red Hat ACM documentation on enabling klusterlet add-ons.

## Workload clusters​

Each cluster participating in a DR pair must meet the following requirements:

- Portworx Enterprise version 3.5.0 or later is installed.

- Portworx Operator version 26.2.0 or later is installed.

- OpenShift version 4.18 or later is installed.

- Portworx OpenShift Dynamic Plugin 2.3.0 or later is enabled on the workload cluster. For more information, see Enable Portworx OpenShift Dynamic Plugin.

- Portworx Cache Agent version 1.1.0 or later is installed.
For information about the Cache Agent, see Openshift Dynamic Plugin Support Policy.

- An active Portworx Enterprise license with the Disaster Recovery entitlement is available.

- Stork version 26.1.0 or later is installed with the required RBAC permissions to enable disaster recovery with MultiCluster Manager.

- The `StorageCluster` has load balancing enabled.
Load balancing ensures that the Stork processes on the source and destination clusters can communicate with each other.

- The same admin namespace name is configured on both the source and destination clusters.
The Multi-Cluster Operator uses this namespace to create and manage migrations. If the namespace names differ, DR pair creation pre-checks fail.

- All standard Async DR prerequisites mentioned here are met, including network connectivity between clusters and access to a supported object store (NFS, AWS S3, Google Cloud Object Storage, Azure Blob Storage, or any S3-compatible storage).

In this topic:
