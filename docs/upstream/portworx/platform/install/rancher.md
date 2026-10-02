# Install Portworx on SUSE Rancher

Source: https://docs.portworx.com/portworx-enterprise/platform/install/rancher (Portworx Enterprise 3.6)

Install Portworx on SUSE Rancher | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

You can install Portworx Enterprise on a Rancher Kubernetes Engine 2 (RKE2) cluster to enable enterprise-grade, cloud-native storage for your Kubernetes workloads. Portworx integrates natively with RKE2, providing highly available, persistent storage for mission-critical applications. It supports both non-air-gapped and air-gapped environments, allowing deployment flexibility across diverse infrastructure setups. The installation process includes preparing the server, configuring the Kubernetes cluster, and deploying Portworx with a generated specification.

## Prerequisites​

In addition to the System Requirements, ensure that your RKE2 cluster meets the following requirements before installing Portworx Enterprise:

- The cluster must use one of the following storage backends:

- vSphere cloud drives

- FlashArray cloud drives (supported only on Ubuntu)

- Local drives (pre-provisioned disks)

- Attach the backing storage disks to each worker node.

- Allocate a dedicated disk for KVDB (internal or external) on at least three nodes. Each disk must have a unique device name across all KVDB nodes. For more information, see KVDB for Portworx.

- Disable kernel auto-updates on your cluster.

## Limitations​

- Portworx does not support the `RancherOS` distro.

- PX-Fast functionality is not supported on SUSE Linux Micro 6.x distro.

## Installation Options for Portworx Enterprise on RKE2 Clusters​

To install Portworx Enterprise on an RKE2 cluster, see the following topics:

-
To install Portworx Enterprise on an RKE2 cluster using the SUSE Rancher console Catalogs (previously known as SUSE Rancher Apps & Marketplace), see Installation using Rancher Console.

-
To install Portworx Enterprise on an RKE2 cluster with vSphere cloud drives, see Installation on VMware vSphere.

-
To install Portworx Enterprise on an RKE2 cluster with FlashArray cloud drives (supported only on Ubuntu), see Portworx with FlashArray and FlashBlade.

-
To install Portworx Enterprise on an RKE2 cluster with Local drives (pre-provisioned disks), see Installation on Bare Metal Server.

In this topic:
