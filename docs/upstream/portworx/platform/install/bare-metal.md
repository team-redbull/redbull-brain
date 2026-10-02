# Install Portworx on Bare Metal Server

Source: https://docs.portworx.com/portworx-enterprise/platform/install/bare-metal (Portworx Enterprise latest)

Install Portworx on Bare Metal Server | Portworx Enterprise Documentation

You can install Portworx Enterprise on a bare metal server using either a custom Kubernetes manifest or Helm chart, based on your infrastructure requirement. Portworx Enterprise supports clusters running on major cloud service providers and on-premises data centers in both air-gapped and connected environments. The installation process includes preparing the server, configuring the Kubernetes cluster, and deploying Portworx with a generated specification.

## Prerequisites​

In addition to the System Requirements, ensure that your bare metal cluster meets the following requirements before installing Portworx Enterprise:

- Provide a dedicated disk for KVDB (internal or external) on at least three nodes. Each disk must have a unique device name across all KVDB nodes. For more information, see KVDB for Portworx.

- If you plan to have a disaggregated setup, designate your nodes as storage or storageless (compute) before installing Portworx. Portworx uses the following labels on Kubernetes nodes to determine their roles:

-
`portworx.io/node-type: storage`

-
`portworx.io/node-type: storageless`

- Add labels to the nodes:

- For new node groups: When using a managed Kubernetes cluster, you can add these label pairs when you create the node groups. This ensures that your cloud provider consistently applies the labels to all nodes.

- For existing node groups: If your cluster is already running, add or update the labels on your nodes using a Kubernetes command. For example:

```

kubectl label node <node-name> portworx.io/node-type=storage

# or for storageless nodes

kubectl label node <node-name> portworx.io/node-type=storageless

```

## Installation Options for Portworx Enterprise on Bare Metal Servers​

-
To install Portworx Enterprise on a bare metal server with Directly Attached Storage (DAS) or Storage Area Network (SAN) see the following topics:

- Openshift

- Non-Air-Gapped OpenShift Cluster

- Air-Gapped OpenShift Cluster

- Kubernetes

- Non-Air-Gapped Kubernetes Cluster

- Air-Gapped Kubernetes Cluster

- Other Supported Distributions

- Installation on Rancher, VMware Tanzu, or Google Anthos Clusters (Air-Gapped and Non-Air-Gapped)

-
To install Portworx Enterprise on a bare metal server with FlashArray or FlashBlade, see Installation of Portworx with FlashArray

Each Kubernetes distribution might require specific steps to prepare the bare metal cluster before you deploy Portworx Enterprise.

In this topic:
