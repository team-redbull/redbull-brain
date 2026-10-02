# Install Portworx on Google Cloud

Source: https://docs.portworx.com/portworx-enterprise/platform/install/google-cloud (Portworx Enterprise 3.6)

Install Portworx on Google Cloud | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

You can install Portworx Enterprise on Google Cloud to run stateful workloads across Kubernetes environments such as Google Kubernetes Engine (GKE), OpenShift on Google Cloud, Google Anthos, or a Gardener cluster on Google Cloud. The installation process typically includes preparing your Google Cloud environment, configuring the Kubernetes cluster, and deploying Portworx with a generated specification.

## Prerequisites​

In addition to the System Requirements, ensure that your cluster meets the following requirements before installing Portworx Enterprise:

- Google Cloud OpenShift

- Google Kubernetes Engine

- Google Cloud Marketplace/CLI

- Anthos

- Install and configure the Google Cloud command-line tool (`gcloud`) to set up the required permissions for deploying Portworx.

- Configure your network settings to allow the following traffic:

- Ports 17001–17021: Required for Portworx node-to-node communication.

- Ports 111, 2049, and 20048: Required to support SharedV4 volumes using NFSv3.

- Port 2049 (NFS server): Required only when using SharedV4 services with NFSv4.

- If you plan to have a disaggregated setup, designate your nodes as storage or storageless (compute) before installing Portworx. Portworx uses the following labels on Kubernetes nodes to determine their roles:

-
`portworx.io/node-type: storage`

-
`portworx.io/node-type: storageless`

- Portworx is supported only on GKE clusters that use Ubuntu node images. Ensure you've created cluster using the right Ubuntu image type and machine type while meeting the hardware requirements.

- For production environments, deploy across three Availability Zones (AZs) with at least one node in each zone.

- Configure the maximum number of storage nodes per availability zone to ensure Portworx maintains the required storage node count in each zone.

- Portworx recommends using a zonal cluster. For instructions, see the GCP documentation.

- If you plan to have a disaggregated setup, designate your nodes as storage or storageless (compute) before installing Portworx. Portworx uses the following labels on Kubernetes nodes to determine their roles:

-
`portworx.io/node-type: storage`

-
`portworx.io/node-type: storageless`

- Install and configure the Google Cloud command-line tool (`gcloud`) to set up the required permissions for deploying Portworx.

- Portworx is supported only on GKE clusters that use Ubuntu node images. Ensure you've created cluster using the right Ubuntu image type and machine type while meeting the hardware requirements.

- For production environments, deploy across three Availability Zones (AZs) with at least one node in each zone.

- Portworx recommends using a zonal cluster. For instructions, see the GCP documentation.

- Portworx requires access to the Google Cloud APIs to provision and manage disks. Ensure that the service account for Portworx has the following roles:

- Compute Admin

- Service Account User

- Kubernetes Engine Cluster Viewer

- If you plan to have a disaggregated setup, designate your nodes as storage or storageless (compute) before installing Portworx. Portworx uses the following labels on Kubernetes nodes to determine their roles:

-
`portworx.io/node-type: storage`

-
`portworx.io/node-type: storageless`

-
Ensure your cluster is using the supported Google Anthos kernel versions.

-
Ensure your cluster have the supported disk types.

-
By default, Google includes Kernel version 5.15 from Anthos version 1.14 for vSphere. Therefore, upgrading to Anthos version 1.14 or newer can result in Kernel performance issues, leading to a drop in the sequential write operations. Avoid using this Anthos version and Kernel version until the issue is fixed. See the bug description for more information.

-
If you plan to have a disaggregated setup, designate your nodes as storage or storageless (compute) before installing Portworx. Portworx uses the following labels on Kubernetes nodes to determine their roles:

- `portworx.io/node-type: storage`

- `portworx.io/node-type: storageless`

-
Best practices to prevent accidental deletion: If your virtualization software has a feature to prevent accidental deletion, you should enable it for the VMs hosting PX nodes. While PX is designed to handle the loss of some nodes without issue, losing a significant number of storage nodes due to VM deletion can result in a loss of quorum and an outage. For more information on how to prevent accidental deletion of VM, refer to Prevent accidental VM deletion on Google cloud compute engine.

## Installation Options for Portworx Enterprise on Google Cloud Clusters​

Depending on whether you want to deploy Portworx with Google Kubernetes Engine, OpenShift, Google Anthos, or a Gardener cluster on Google Cloud, proceed to one of the following topics:

- Installation on Google Kubernetes Engine Cluster

- Installation on Google Cloud Openshift Cluster

- Installation on Anthos Cluster

- Installation on a GCP Gardener Cluster

Each Kubernetes distribution might require specific steps to prepare the cluster before you deploy Portworx Enterprise.

In this topic:
