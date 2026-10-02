# What is Portworx Enterprise

Source: https://docs.portworx.com/portworx-enterprise/what-is-portworx-enterprise (Portworx Enterprise latest)

What is Portworx Enterprise | Portworx Enterprise Documentation

Portworx Enterprise is a cloud native storage and data management platform for Kubernetes that is designed to enable enterprises manage storage for their containerized stateful applications across various infrastructure environments.

Storage Automation for Kubernetes with Portworx Enterprise

## Key Features and Components of Portworx Enterprise​

Portworx Enterprise provides storage automation for containerized applications on any Kubernetes distribution, across all cloud platforms and infrastructures. Portworx Enterprise offers the following benefits through its key components and features:

#### Zero RPO Disaster Recovery with PX-DR​

Portworx Enterprise provides a comprehensive disaster recovery suite with synchronous and asynchronous replication. Synchronous PX-DR replication creates a stretched StorageCluster between Kubernetes clusters for zero RPO. Asynchronous PX-DR replication ensures reliable data replication between geographically separated StorageClusters. For more information, see Disaster Recovery.

#### High-Performance Storage with PX-StoreV2​

Portworx Enterprise offers PX-StoreV1, a full-featured filesystem as a storage backend, and PX-StoreV2 that uses block storage for metadata management. PX-StoreV2 is a Portworx datastore optimized for supporting IO intensive workloads for configurations utilizing high performance NVMe class devices. For more information about PX-StoreV2, see Portworx Datastores.

#### Integration with FlashArray and FlashBlade​​

The combination of Portworx Enterprise’s data management capabilities and the high-performance FlashArray and FlashBlade storage solutions enhances overall application performance and reduces operational overhead. This native integration with CSI allows for automated provisioning and management of storage directly from the Kubernetes environments, ensuring that deployments maintain optimal performance while leveraging Flash storage capabilities.

#### Modern virtualization capability to support KubeVirt virtual machines​

Portworx offers support for KubeVirt, which allows Kubernetes to manage virtual machines. Portworx enables live migration of virtual machines (VMs) within Kubernetes without downtime, which is essential for maintaining service continuity during maintenance or infrastructure changes. KubeVirt VMs benefit from Portworx Enterprise's capabilities to manage persistent volumes, providing storage classes optimized for VM workloads. Templates can define VMs with specific configurations, streamlining deployment and management in Kubernetes environments.

#### Automated capacity management with Portworx Autopilot and Cloud Drives​

Portworx Autopilot automates storage management using a rule-based engine that dynamically responds to scaling needs by continuous monitoring. It resizes PVCs, scales Portworx storage pools, and rebalances volumes when required. Cloud Drives simplify disk provisioning during installation and scaling by automatically provisioning disks in cloud environments for Portworx consumption.

#### Intelligent pod scheduling and data locality with Portworx Stork​

Portworx Stork (Storage Orchestrator Runtime for Kubernetes) enhances Kubernetes with dynamic volume placement and intelligent scheduling based on volume locality. It uses Kubernetes scheduler extenders to ensure pods run on nodes where the requested volume replicas reside, improving data access performance. Portworx Stork also supports pod rescheduling, snapshots, and migration capabilities.

## What to do next​

-
Based on your storage infrastructure, understand how to Install Portworx Enterprise for a Kubernetes environment. See, Install and Run Portworx Enterprise.

-
To understand more about Portworx, see Portworx Concepts.

In this topic:
