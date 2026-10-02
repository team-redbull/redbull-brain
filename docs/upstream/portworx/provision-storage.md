# Provision storage for Applications

Source: https://docs.portworx.com/portworx-enterprise/provision-storage (Portworx Enterprise latest)

Provision storage for Applications | Portworx Enterprise Documentation

You can provision persistent storage for both containerized workloads and KubeVirt virtual machines using Portworx Enterprise on Kubernetes. The following topics describe how to create and manage PersistentVolumeClaims (PVCs) for your applications, manage your CSI volume lifecycle, and configure shared RWX storage for KubeVirt VMs, including support for live migration and high availability.

- Create and Manage PVCs with Portworx

- Manage Volume Lifecycle with CSI Driver

- Manage KubeVirt VMs with Portworx

## Provision FlashArray and FlashBlade storage​

When the FA/FB driver is enabled, Portworx Enterprise provisions your FlashArray and FlashBlade Direct Access volumes, and you can use the following provisioning capabilities for FlashArray and FlashBlade storage.

TopicDescription

Dynamic provisioning of FlashArray File ServicesProvisions shared NFS volumes from FlashArray File Services with `ReadWriteMany` (RWX) access.

Dynamic provisioning of FlashArray block volumesProvisions FlashArray Direct Access (FADA) block volumes, including volumes in a synchronously replicated ActiveCluster pod.

Dynamic provisioning of FlashBlade file systemsProvisions FlashBlade Direct Access (FBDA) NFS file systems, including FlashBlade//EXA file systems assigned to a data node group.

Static provisioningMakes an existing FlashArray volume, FlashArray File Services directory, or FlashBlade file system available through a Kubernetes PVC without provisioning new storage.

Raw block volumes for live migrationMakes a FADA volume available as a read-write raw block device on multiple nodes to support KubeVirt live migration.

FlashArray File for live migration with vTPMUses FlashArray File Services volumes to store persistent state for virtual machines that use a virtual Trusted Platform Module (vTPM), supporting VM live migration.

Control volume placement using array IDPlaces volumes created from a `StorageClass` on a specific FlashArray by using its array ID.

Enable CSI topologyRestricts volume provisioning and attachment based on the nodes and zones that can access a storage backend.

Use FlashArray ActiveClusterProvisions FADA volumes in an ActiveCluster pod and provides paths to the volumes through both member FlashArrays.

In this topic:
