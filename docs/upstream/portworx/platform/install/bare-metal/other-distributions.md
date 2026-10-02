# Installation on Google Anthos, Rancher, or vSphere Kubernetes Service Clusters (Air-Gapped and Non-Air-Gapped)

Source: https://docs.portworx.com/portworx-enterprise/platform/install/bare-metal/other-distributions (Portworx Enterprise 3.6)

Installation on Google Anthos, Rancher, or vSphere Kubernetes Service Clusters (Air-Gapped and Non-Air-Gapped) | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx Enterprise can be deployed on a variety of Kubernetes platforms including Google Anthos, Rancher Kubernetes Engine (RKE2), and VMware vSphere Kubernetes Service (VKS) running on bare metal clusters.

Ensure that your cluster meets all the prerequisites before installing Portworx Enterprise.

The deployment process for these environments, whether in air-gapped or non-air-gapped setups, is identical to deploying Portworx on a vanilla Kubernetes bare metal cluster. The only difference is that when generating the Portworx specification, you must select the appropriate distribution-specific options in the Portworx Spec Generator (See Step 5 in Generate Portworx Specification). This ensures that the deployment manifest is correctly tailored for RKE, VKS, or Anthos.

-
For information on how to deploy Portworx Enterprise on Anthos, RKE2, or VKS in a non-air-gapped bare metal cluster, follow the same steps in Installation on a Non-Air-Gapped Bare Metal Kubernetes Cluster.

-
For information on how to deploy Portworx Enterprise on Anthos, RKE2, or VKS in an air-gapped bare metal cluster, follow the same steps in Installation on Air-Gapped Bare Metal Kubernetes Cluster.
