# Manage FlashArray Direct Access Shared Block Device (RWX Block) for KubeVirt VMs

Source: https://docs.portworx.com/portworx-enterprise/provision-storage/kubevirt-vms/shared-raw-block-for-live-migration (Portworx Enterprise 3.6)

Manage FlashArray Direct Access Shared Block Device (RWX Block) for KubeVirt VMs | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx enables the seamless integration of KubeVirt virtual machines (VMs) within Kubernetes clusters, leveraging the high performance of ReadWriteMany (RWX) volumes backed by FlashArray Direct Access (FADA) shared raw block RWX volumes. This approach supports raw block devices, which provide direct block storage access instead of a mounted filesystem. This is particularly beneficial for applications that demand low-latency and high-performance storage.

Traditional RWX storage using shared NFS filesystem volumes may face performance limitations, especially for workloads requiring high-speed I/O operations. By contrast, raw block devices:

- Eliminate filesystem overhead.

- Provide direct access to the underlying storage for improved performance.

- Enable efficient live migration of VMs using Kubernetes-native tools.

This page explains how to deploy KubeVirt VMs using raw block storage and describes the live migration workflow.

## Prerequisites​

- Portworx Operator version 25.2.1 or later.

- Portworx Stork version 25.2.0 or later.

- Both OpenShift and OpenShift Virtualization (OSV) versions must be 4.15 or higher.

## Workflow for Live migration of KubeVirt VMs​

The live migration workflow for KubeVirt VMs using Portworx involves these steps:

- Use a StorageClass and PVC configured for RWX raw block storage.

- The source VM is attached to an RWX volume hosted on shared raw block storage. Access is controlled to ensure both the source and destination nodes can interact with the volume.

- The source node writes VM data to the RWX volume. The destination node pre-copies VM state and disk contents by reading from the same volume.

- The destination node gains write access to the RWX volume, and the VM is initialized on the destination node, ensuring seamless migration within the Kubernetes environment.

## Create a StorageClass​

-
To provision storage for KubeVirt VMs, create a StorageClass as shown below. This configuration uses the `pure_block` backend to create volumes on FlashArray:

important

If you need the mount path to have 777 permissions, set the `parameters.allow_others` field to `true` in your StorageClass. This setting ensures that all users have read, write, and execute access to the mount point. Use this setting carefully to avoid granting unintended access.

```

apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:

 name: fada-rwx-sc

parameters:

 backend: "pure_block"

 #allow_others: true     # uncomment this line if you need the mount path to have 777 permissions.

provisioner: pxd.portworx.com

volumeBindingMode: WaitForFirstConsumer

allowVolumeExpansion: true

```

-
Apply this StorageClass to your cluster:

```

kubectl apply -f storageclass.yaml

```

## Create a PVC​

note

Starting with OpenShift Container Platform (OCP) version 4.17, the default `StorageProfile` for Portworx-backed `StorageClass` objects sets the access mode to `ReadWriteMany` and the volume mode to `Block`.
When creating or migrating (forklifting) new PX RWX Block volumes, ensure that the corresponding `StorageProfile` has `volumeMode` set to `Block` if it is not already configured by default in your OCP version.
For more information about `StorageProfile` configuration, see Configuring storage profiles.

-
Using the above StorageClass, define a PVC with the following configuration:

- `accessModes`: `ReadWriteMany` for shared volume access.

- `volumeMode`: `Block` to create a raw block device volume

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

 name: fada-rwx-pvc

spec:

 storageClassName: fada-rwx-sc

 accessModes:

  - ReadWriteMany

 resources:

  requests:

   storage: 2Gi

 volumeMode: Block

```

-
Apply this PVC to your cluster:

```

kubectl apply -f pvc.yaml

```

When deploying KubeVirt VMs, reference the PVC created in the previous step to attach the RWX raw block volume to the VM. Ensure the VM configuration specifies the correct StorageClass and volume.

Once the VM is running with the specified PVC, you can perform live migration using OpenShift's native functionality. The shared RWX volume ensures data consistency during the migration process by allowing simultaneous read/write operations for the source and destination nodes.

In this topic:
