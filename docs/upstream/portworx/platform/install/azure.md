# Install Portworx on Microsoft Azure

Source: https://docs.portworx.com/portworx-enterprise/platform/install/azure (Portworx Enterprise latest)

Install Portworx on Microsoft Azure | Portworx Enterprise Documentation

You can install Portworx on an Azure cluster to enable enterprise-grade cloud-native storage for your Kubernetes workloads. Portworx supports both standard Kubernetes deployments and OpenShift-based environments running on Azure. Portworx integrates natively with Azure, leveraging Azure resources for persistent storage management and advanced data services.

Portworx installation on an Azure cluster is managed via Kubernetes manifests, generated through Portworx Central. You can apply a Portworx Operator and StorageCluster manifest to your Azure cluster, which automates and orchestrates the installation across all nodes.

## Prerequisites​

In addition to the System Requirements, ensure that your Azure cluster meets the following requirements before installing Portworx Enterprise:

-
Install the Azure CLI.
For more information, see Microsoft documentation.

-
Use one of the supported Azure managed disk types for persistent volumes.

-
For production environments, Portworx recommends deploying your Azure cluster across three Availability Zones (AZs), with one node per zone to ensure high availability.

-
For existing clusters, make note of the AKS cluster Infrastructure Resource Group name or the initial Resource Group name used during cluster creation.

-
If you are using Azure Disk encryption with customer-managed keys (CMKs), ensure that an Azure Key Vault instance exists in the same region as your Azure cluster.

-
If you plan to have a disaggregated setup, designate your nodes as storage or storageless (compute) before installing Portworx. Portworx uses the following labels on Kubernetes nodes to determine their roles:

-
`portworx.io/node-type: storage`

-
`portworx.io/node-type: storageless`

-
Add labels to the nodes:

- For new node groups: When using a managed Kubernetes cluster, you can add these label pairs when you create the node groups. This ensures that your cloud provider consistently applies the labels to all nodes.

- For existing node groups: If your cluster is already running, add or update the labels on your nodes using a Kubernetes command. For example:

```

kubectl label node <node-name> portworx.io/node-type=storage

# or for storageless nodes

kubectl label node <node-name> portworx.io/node-type=storageless

```

-
If you plan to use the Portworx Helm chart for installation, ensure the following:

- Helm 3.x (3.18.0 or later) installed on the client machine. For information about installing Helm, see Installing Helm.

- Review the Helm compatibility matrix and the configurable parameters.

- Complete the Configure Authentication section. The `px-azure` Kubernetes secret (for Service Principal or Managed Identity) or the federated managed identity (for Workload Identity) must be in place in the namespace where you plan to install Portworx.

## Installation Options for Portworx Enterprise on Azure Clusters​

This topic lists the installation process for each cluster type, helping you integrate Portworx as a cloud-native storage solution. Use the appropriate method based on your Azure cluster configuration.

- Installation on an Azure Red Hat OpenShift Cluster

- Installation on an Azure Kubernetes Service (AKS) Cluster

- Installation on an Azure Gardener Cluster

note

If your workload scales up or down based on demand, consider installing Portworx in disaggregated mode. The installation process follows the same steps as a standard installation, with one addition: Step 2 in Deploy Portworx Operator.

In this topic:
