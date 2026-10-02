# Create and Manage PVCs with Portworx

Source: https://docs.portworx.com/portworx-enterprise/provision-storage/create-pvcs (Portworx Enterprise 3.6)

Create and Manage PVCs with Portworx | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

A PersistentVolumeClaim (PVC) is used to request persistent storage for your Kubernetes workloads. When using Portworx as your storage provider, creating a PVC enables your applications to dynamically or statically consume storage backed by Portworx volumes. This section explains the different ways to create and manage PVCs with Portworx.

Portworx Enterprise supports dynamic provisioning of volumes that can be attached to a single pod using the ReadWriteOnce (RWO) access mode, or shared across multiple pods using ReadWriteMany (RWX).

This topic provides instructions for creating and managing PVCs for Portworx-based workloads. The table below lists topics on how to create a PVC, advanced use cases such as integrating with an Everpure backend, enabling read-only or shared access modes, proxying external data, and leveraging PX-Fast for accelerated storage performance. The table also lists topics that cover key day-2 operations, such as dynamically provisioning PVCs, accessing volumes as non-root users, resizing volumes, controlling replica placement, using pre-provisioned volumes, and opening NFS ports for Sharedv4 workloads.

TopicDescription

Create your first PVC Describes how to create and use your first Portworx-backed PVC, including defining a claim and verifying that your application can read and write data through it.

Pure FlashArray PVCsDescribes how to configure PVCs that use Pure FlashArray as a direct access block volume backend through Portworx.

Pure FlashBlade PVCsDescribes how to configure PVCs that use Pure FlashBlade as a direct access file system backend through Portworx.

Create ReadOnlyMany access mode PVCsDescribes how to create PVCs with the `ReadOnlyMany` access mode so multiple pods can mount the same Portworx volume in read-only mode.

Create proxy volume PVCsDescribes how to create proxy volumes that present an external data source (such as an NFS share) as a Portworx-managed volume, so applications can consume external data.

Create PX‑Fast PVCsDescribes how to create PX‑Fast PVCs and enable PX‑Fast functionality on volumes to take advantage of Portworx’s accelerated I/O path on supported configurations.

Create Sharedv4 PVCsDescribes how to create PVCs backed by Sharedv4 (NFS-based) Portworx volumes, enabling `ReadWriteMany` access across multiple pods and nodes.

Create a PVC from a snapshotDescribes how to take a snapshot of a Portworx volume from an existing PVC using annotations, then create a new PVC from that snapshot for cloning or recovery scenarios.

Manage provisioning of PVCsIntroduces strategies for controlling how Portworx provisions volumes for PVCs, aligning provisioning behavior with storage policies and operational requirements.

Dynamic provisioning of PVCsDescribes how to use dynamically provisioned Portworx volumes with Kubernetes `StorageClass` objects, so PVCs automatically create backing volumes on demand.

Access a PVC as non-root userDescribes how to configure access so Portworx-backed PVCs can be used by non‑root users, supporting security and compliance requirements.

Resize PVCsProvides a step‑by‑step procedure for expanding an existing Portworx-backed PVC when your application needs more capacity.

Create and use VolumePlacementStrategiesDescribes how to create and apply a VolumePlacementStrategy custom resource (CR) in your cluster.

Using pre-provisioned volumesDescribes how to use pre‑provisioned Portworx volumes with Kubernetes PVCs when storage is created ahead of time rather than dynamically provisioned.

Using pre-provisioned FlashArray Direct Access volumesDescribes how to import and use existing FlashArray volumes as FlashArray Direct Access (FADA) PVCs in Kubernetes.

Open NFS portsLists the NFS ports that must be opened in your environment so Sharedv4 (NFS-based) Portworx volumes and the workloads that use them function correctly.
