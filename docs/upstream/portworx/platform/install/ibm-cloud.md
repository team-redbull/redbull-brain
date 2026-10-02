# Install Portworx on IBM Cloud

Source: https://docs.portworx.com/portworx-enterprise/platform/install/ibm-cloud (Portworx Enterprise 3.6)

Install Portworx on IBM Cloud | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

You can install Portworx Enterprise on IBM Cloud using the IBM Catalog or a Terraform module. The installation process typically includes preparing the IBM Cloud environment, configuring the Kubernetes cluster, and deploying Portworx.

## Prerequisites​

In addition to the System Requirements, ensure that your cluster meets the following requirements before installing Portworx Enterprise:

- IBM Catalog

- IKS using Terraform

- An IBM Cloud account with administrator privileges.
Portworx does not support using a service ID.

- A Kubernetes or OpenShift cluster deployed on IBM Cloud with at least 3 worker nodes.

- Cluster configuration that meets the following requirements for IKS clusters:

- CPU: 16

- Memory: 32 GB

- Disk: 100 GB

- The ability to provision cloud storage for each worker node.

- Use Terraform version 0.13 or later.

- Ensure that the following utilities are installed and configured on your client:

- IBM Cloud Kubernetes Service CLI

- kubectl

- HashiCorp Terraform CLI

- Helm CLI

- The latest versions of the `jq`, `curl`, and `wget` libraries

## Installation Options for Portworx Enterprise on IBM Cloud​

Depending on whether you want to deploy Portworx with IBM Cloud Kubernetes Service or Red Hat OpenShift on IBM Cloud, proceed to one of the following topics:

- Installation on IBM Cloud using IBM Catalog

- Installation on IBM Cloud Kubernetes Service (IKS) using Terraform

Each distribution might require specific steps to prepare the cluster before you deploy Portworx Enterprise.

In this topic:
