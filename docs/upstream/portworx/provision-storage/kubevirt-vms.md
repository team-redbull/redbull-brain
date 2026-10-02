# Manage KubeVirt VMs with Portworx

Source: https://docs.portworx.com/portworx-enterprise/provision-storage/kubevirt-vms (Portworx Enterprise 3.6)

Manage KubeVirt VMs with Portworx | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx by Everpure integrates with KubeVirt to provide Kubernetes native persistent storage for virtual machines (VMs), enabling shared access, high availability, and live migration on OpenShift and other supported distributions.

KubeVirt allows you to run virtual machine workloads alongside containerized applications within a Kubernetes cluster using the same storage constructs such as `StorageClass`, `PersistentVolumeClaim` (PVC), and Container Storage Interface (CSI).

For information on how to deploy KubeVirt on a Kubernetes cluster, see KubeVirt documentation.

note

Portworx supports KubeVirt VMs with IPv6 networking.

Portworx supports the following types of ReadWriteMany (RWX) volumes for KubeVirt virtual machines, enabling a balance between portability and performance:

- Shared raw block volumes for streamlined live migration.
 For information on how to manage shared raw block volumes for KubeVirt VMs, see Manage Shared Block Device (RWX Block) for KubeVirt VMs.

- FlashArray Direct Access (FADA) shared raw block volumes for high-performance workloads, and reduced file system overhead.
 For information on how to manage FADA volumes for KubeVirt VMs, see Manage FlashArray Direct Access Shared Block Device (RWX Block) for KubeVirt VMs.

- Shared file system volumes, such as `sharedv4` or NFS, for portability and multi-node access.
 For information on how to manage shared filesystem storage for KubeVirt VMs, see Manage Shared File System for KubeVirt VMs.

important

A KubeVirt VM must use a single RWX volume type for all its disks, including any hot-plugged disks. Mixing volume types on the same VM, for example, attaching a Portworx RWX block (raw block) PVC to a VM that uses SharedV4 (sv4) volumes, or vice versa is not supported. This configuration can cause OpenShift node drains to stall during OCP or Portworx upgrades.
