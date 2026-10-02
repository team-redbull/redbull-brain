# Portworx MultiCluster Operator Release Notes

Source: https://docs.portworx.com/portworx-enterprise/multicluster-operator-release-notes (Portworx Enterprise 3.6)

Portworx MultiCluster Operator Release Notes | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## 26.1.0​

August 03, 2026

The Portworx MultiCluster Operator provides disaster recovery (DR) and multi-cluster management for Portworx Enterprise clusters. It includes the Portworx ACM Dynamic Console Plugin, which integrates with Red Hat Advanced Cluster Management (RHACM) to enable disaster recovery between OpenShift clusters running Portworx. From a single OpenShift hub cluster, you can manage disaster recovery across multiple Portworx clusters, configure application protection, orchestrate failover and failback, and monitor cluster health.

For information on how to install the operator, see Install Portworx MultiCluster Operator.

### New features​

Multi-cluster disaster recovery orchestration
 The Portworx MultiCluster Operator orchestrates asynchronous DR across workload clusters from a single RHACM hub cluster. It automates cluster pairing, protection group creation, and failover and failback operations, eliminating the standalone Stork-based cluster pairing workflow and its associated CLI steps. For more information, see Multi Cluster Disaster Recovery with Red Hat Advanced Cluster Management.

Asynchronous disaster recovery from the OpenShift console
 The Portworx ACM Dynamic Console Plugin integrates asynchronous DR into the OpenShift console. It provides guided workflows to create disaster recovery pairs between clusters, manage protection groups, and perform failover and failback without using the command line. For more information, see Manage a Disaster Recovery Pair, Manage Protection Groups, Failover, and Failback.

Centralized cluster fleet dashboards
 The Portworx ACM Dynamic Console Plugin provides dashboards in the OpenShift console that let you monitor disaster recovery from a single OpenShift interface. You can view cluster health, disaster recovery readiness, and the status of Disaster Recovery Pairs, Protection Groups, and Disaster Recovery Actions across workload clusters. For more information, see Portworx ACM Dynamic Console Plugin Dashboards.

In this topic:
