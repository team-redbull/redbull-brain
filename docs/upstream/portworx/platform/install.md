# Install Portworx Enterprise

Source: https://docs.portworx.com/portworx-enterprise/platform/install (Portworx Enterprise 3.6)

Install Portworx Enterprise | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

You can install Portworx Enterprise on a wide range of Kubernetes platforms to support various on-premises and cloud environments. You can install Portworx Enterprise using either Portworx Central, Helm charts, or from a supported cloud marketplace.

Before you begin, review the prerequisites and choose the installation method that aligns with your deployment scenario. Each section linked below contains step-by-step instructions, and configuration examples required to deploy Portworx in your environment.

### Portworx Central-based installation​

Portworx Central provides a guided user interface where you can select your storage platform and Kubernetes distribution to generate a customized installation specification. You can then use the generated manifest to deploy Portworx Enterprise on your Kubernetes cluster.

Portworx Central allows you to configure and deploy Portworx Enterprise with the following supported storage platforms and Kubernetes distributions:

Everpure platforms:
FlashArray, FlashBlade, and Everpure Cloud Dedicated for Azure

Other supported platforms/infrastructure:

PlatformRed Hat OpenShift DistributionKubernetes Distribution

Amazon Web ServicesPortworx Enterprise on Red Hat OpenShift Service on AWS (ROSA)Portworx Enterprise on Amazon Elastic Kubernetes Service (EKS)
 Installation on an Amazon EKS Cluster with Hybrid Nodes
 Portworx Enterprise on an AWS Gardener Cluster

Microsoft AzurePortworx Enterprise on Azure Red Hat OpenShift (ARO)Portworx Enterprise on Azure Kubernetes Service (AKS)
 Portworx Enterprise on an Azure Gardener Cluster

Bare MetalPortworx Enterprise on OpenShift Container Platform on Bare MetalPortworx Enterprise on Kubernetes Bare Metal

Google Cloud PlatformPortworx Enterprise on OpenShift running on GCPPortworx Enterprise on Google Kubernetes Engine (GKE)
 Portworx Enterprise on Google Cloud Anthos
 Portworx Enterprise on a GCP Gardener Cluster

vSpherePortworx Enterprise on vSphere OpenShift ClusterPortworx Enterprise on vSphere Kubernetes Cluster

VMware VKSPortworx Enterprise on VMware vSphere Kubernetes Service

Oracle Cloud InfrastructurePortworx Enterprise on Oracle Cloud Infrastructure

IBM CloudPortworx Enterprise on IBM Cloud Kubernetes Service (IKS)

SUSE VirtualizationPortworx Enterprise on SUSE Virtualization

SUSE RancherPortworx Enterprise on SUSE Rancher

Spectro CloudPortworx Enterprise on Spectro Cloud

Mirantis Kubernetes EnginePortworx Enterprise on Mirantis Kubernetes Engine

Charmed KubernetesPortworx Enterprise on Charmed Kubernetes

### Marketplace-based installation​

You can install Portworx Enterprise directly from a supported cloud marketplace using native deployment tools and templates provided by the cloud provider. Portworx Enterprise supports the following marketplace based installations:

- AWS Marketplace

- Google Cloud Marketplace

- SUSE Rancher Marketplace

- IBM Cloud

note

For information on availability across marketplaces, the latest listings and versions, see Portworx Releases on Supported Marketplaces.

### Helm Chart-based installation​

You can install Portworx Enterprise using Helm in Kubernetes environments.

- FlashArray

- vSphere

- Azure Gardener

- AWS Gardener

- GCP Gardener

note

For information on the Helm versions compatible with Portworx Enterprise, see the Helm Chart compatibility matrix.

In this topic:
