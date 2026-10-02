# Portworx Datastores

Source: https://docs.portworx.com/portworx-enterprise/concepts/px-store-v2 (Portworx Enterprise 3.6)

Portworx Datastores | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx supports two types of datastores:

- PX-StoreV1

- PX-StoreV2

These storage backends provide different capabilities and are used in distinct deployment scenarios.

PX-StoreV1 is the legacy storage backend for Portworx Enterprise. As a full-featured filesystem backend, PX-StoreV1 manages volumes with enhanced metadata and supports RAID and device management features.

PX-StoreV2 data store is optimized for I/O-intensive workloads that use high-performance NVMe-class devices. PX-StoreV2 efficiently manages and balances workloads across nodes by dynamically assigning tasks to the most suitable nodes based on available resources, thereby improving the overall performance and scalability of the cluster.

PX-StoreV2 focuses on volume management with optimized metadata handling and enhanced performance metrics, making it well suited for high-performance environments.

## Advantages of PX-StoreV2 over PX-StoreV1​

- Simplicity: PX-StoreV2 focuses on volume management only, which simplifies the architecture by managing blocks with minimal metadata, unlike PX-StoreV1, which operates as a complete filesystem. This reduces the complexity in handling RAID or device management.

- Stability: PX-StoreV2 is designed with lower metadata and refcount overhead compared to PX-StoreV1. By avoiding recursive refcounts and extent backreferences, PX-StoreV2 offers improved stability and simplicity in environments where block management is key.

- Performance:

- Low Performance Overhead: PX-StoreV2 ensures low write amplification and predictable latencies, which provides better performance consistency for users, especially in scenarios with high throughput demands.

- Userspace Bypass (PX fastpath): PX-StoreV2 enables the fastpath, which further improves performance by bypassing certain userspace operations.

## Minimum Requirements​

For information on the minimum requirements for deploying a cluster on PX-StoreV1 or PX-StoreV2, see System Requirements.

## Volume limits​

Starting with Portworx Enterprise 3.6.0, each PX-StoreV2 storage pool supports a maximum of 1,024 volumes. Volumes, replicas, and snapshots in the pool all count toward this limit. In earlier versions, the limit applied per node rather than per pool.

Portworx Enterprise enforces the limit during volume provisioning. When a pool reaches 1,024 volumes, Portworx Enterprise no longer selects that pool for new volume provisioning and returns an error. Snapshot creation on a pool that has reached the limit also fails with an error.

Portworx Enterprise does not support increasing the 1,024-volume limit for a PX-StoreV2 storage pool. To support more than 1,024 volumes on a node, provision additional storage pools. For more information, see Provision a storage pool.

note

For pools that use PX-StoreV2, the 1,024-volume limit applies per pool. For pools that use PX-StoreV1, the limit applies per node.

## Limitations​

PX-StoreV2 has the following limitations:

- Does not support `add-disk` pool expansion operation.

- Does not support upgrading from a previous Portworx version to deploy PX-StoreV2 with cloud drives.

- Does not support checksum of data blocks.

## Supported Platforms and Distributions​

- PX-StoreV2

- PX-StoreV1

PX-StoreV2 is supported on the following platforms and distributions:

PlatformKubernetes DistributionStorage Backend

AWSElastic Kubernetes Service (EKS)IO1 and GP3

OpenShift 4+IO1 and GP3

Red Hat OpenShift Service on AWS (ROSA)IO1 and GP3

Google CloudGoogle Kubernetes Engine (GKE)PD_SSD and PD_Balanced

OpenShift 4+PD_SSD and PD_Balanced

AnthosPD_SSD and PD_Balanced

AzureAzure Kubernetes Service (AKS)Standard SSD, Premium SSD, Premium SSD v2, Ultra Disk

Azure Red Hat OpenShift (ARO)Standard SSD, Premium SSD, Premium SSD v2, Ultra Disk

OpenShift 4+Standard SSD, Premium SSD, Premium SSD v2, Ultra Disk

DAS/SANAnthosPreprovisioned SSD or NVMe

OpenShift 4+Preprovisioned SSD or NVMe

Rancher Kubernetes Engine (RKE2)Preprovisioned SSD or NVMe

vSphereAnthosLazy-Zeroed Thick, Eager-Zeroed Thick, Thin

OpenShift 4+Lazy-Zeroed Thick, Eager-Zeroed Thick, Thin

Rancher Kubernetes Engine (RKE2)Lazy-Zeroed Thick, Eager-Zeroed Thick, Thin

VMware vSphere Kubernetes Service (VKS)VKSStorage Class based configuration

FlashArrayAnthosThin (iSCSI, Fibre Channel, NVMe-oF RDMA, NVMe-oF TCP)

OpenShift 4+Thin (iSCSI, Fibre Channel, NVMe-oF RDMA, NVMe-oF TCP)

Rancher Kubernetes Engine (RKE2)Thin (iSCSI, Fibre Channel, NVMe-oF RDMA, NVMe-oF TCP)

PX-StoreV1 is supported on the following platforms and distributions:

PlatformKubernetes DistributionStorage Backend

AWSElastic Kubernetes Service (EKS)IO1, GP2, and GP3

OpenShift 4+IO1, GP2, and GP3

Red Hat OpenShift Service on AWS (ROSA)IO1, GP2, and GP3

Google CloudGoogle Kubernetes Engine (GKE)PD_Standard, PD_SSD, and PD_Balanced

OpenShift 4+PD_Standard, PD_SSD, and PD_Balanced

AnthosPD_Standard, PD_SSD, and PD_Balanced

AzureAzure Kubernetes Service (AKS)Standard HDD, Standard SSD, Premium SSD, Premium SSD v2, Ultra Disk

Azure Red Hat OpenShift (ARO)Standard HDD, Standard SSD, Premium SSD, Premium SSD v2, Ultra Disk

OpenShift 4+Standard HDD, Standard SSD, Premium SSD, Premium SSD v2, Ultra Disk

OracleOracle Kubernetes Engine (OKE)Volume Processing Units (VPUs) based configuration

DAS/SANAnthosPreprovisioned SSD or NVMe

OpenShift 4+Preprovisioned SSD or NVMe

Rancher Kubernetes Engine (RKE2)Preprovisioned SSD or NVMe

Tanzu Kubernetes Grid Integrated Edition (TKGI)Preprovisioned SSD or NVMe

vSphereAnthosLazy-Zeroed Thick, Eager-Zeroed Thick, Thin

OpenShift 4+Lazy-Zeroed Thick, Eager-Zeroed Thick, Thin

Rancher Kubernetes Engine (RKE2)Lazy-Zeroed Thick, Eager-Zeroed Thick, Thin

Tanzu Kubernetes Grid Integrated Edition (TKGI)Lazy-Zeroed Thick, Eager-Zeroed Thick, Thin

VKSVKSStorage Class based configuration

FlashArrayOpenShift 4+Thin (iSCSI, Fibre Channel, NVMe-oF RDMA, NVMe-oF TCP)

AnthosThin (iSCSI, Fibre Channel, NVMe-oF RDMA, NVMe-oF TCP)

Tanzu Kubernetes Grid Integrated Edition (TKGI)Thin (iSCSI, Fibre Channel, NVMe-oF RDMA, NVMe-oF TCP)

Rancher Kubernetes Engine (RKE2)Thin (iSCSI, Fibre Channel, NVMe-oF RDMA, NVMe-oF TCP)

In this topic:
