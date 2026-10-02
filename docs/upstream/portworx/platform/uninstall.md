# Uninstall Portworx Enterprise

Source: https://docs.portworx.com/portworx-enterprise/platform/uninstall (Portworx Enterprise 3.6)

Uninstall Portworx Enterprise | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

The topics below provide instructions for uninstalling Portworx Enterprise from Kubernetes or OpenShift. You can choose to uninstall Portworx Enterprise from the entire cluster or a particular node.

-
Removing Portworx from a Specific Node: Use these instructions to decommission a node from the Portworx cluster without affecting the rest of the cluster. This method is useful when you need to replace or remove a node for maintenance or scaling down. For more information, see Decommission a node.

-
Removing Portworx from the Entire Cluster: Use these instructions to uninstall Portworx from all nodes in the cluster. Use this when you need to completely remove Portworx for reasons such as migration to a different storage solution, cluster decommissioning, etc. For more information, see Uninstall Portworx using the Operator.

-
Using DaemonSet for Uninstallation: If you installed Portworx Enterprise using the DaemonSet method, see Uninstall using DaemonSet.

-
Using Helm Uninstallation: For clusters where Portworx Enterprise was installed on FlashArray and OpenShift vSphere platforms via Helm, see Uninstall using Helm.

-
Platform-Specific Uninstall Methods:

- AWS Marketplace: For uninstalling Portworx Enterprise from AWS EKS clusters where it was installed through the marketplace, see Uninstall using AWS Marketplace.

- OpenShift Console: For uninstalling Portworx Enterprise from OpenShift using the graphical console interface for operator management, see Uninstall using OpenShift console.

- IBM Clusters: For uninstalling from IBM Cloud Kubernetes Service (IKS) and OpenShift IBM clusters, including cleanup of storage objects from the IBM dashboard, see Uninstall from IBM cluster.

-
Special Scenarios:

- Air-gapped Environments: Instructions for wiping Portworx Enterprise from clusters without internet access, including steps for managing container images, see Wipe Portworx from an air-gapped cluster.

-
Removing the Portworx MultiCluster Operator: If you use ACM-based disaster recovery, see Uninstall the Portworx MultiCluster Operator to remove the Portworx MultiCluster Operator from the ACM hub cluster.
