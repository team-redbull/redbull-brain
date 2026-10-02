# Manage Portworx RWX Block Volumes on SUSE Virtualization for KubeVirt VMs

Source: https://docs.portworx.com/portworx-enterprise/provision-storage/kubevirt-vms/manage-kubevirt-vms-rwx-block/suse-virtualization (Portworx Enterprise latest)

Manage Portworx RWX Block Volumes on SUSE Virtualization for KubeVirt VMs | Portworx Enterprise Documentation

Portworx enables the seamless integration of KubeVirt virtual machines (VMs) within Kubernetes clusters, leveraging the high performance of ReadWriteMany (RWX) volumes on SUSE Virtualization. This approach supports raw block devices, which provide direct block storage access instead of a mounted filesystem. This is particularly beneficial for applications that demand low-latency and high-performance storage.

RWX block volumes allow shared access to raw block devices, enabling features such as live migration, high availability, and persistent VM storage across SUSE Virtualization nodes.

Portworx does not support the following configurations when using shared raw block volumes for KubeVirt VMs on Portworx raw block volumes that were migrated from another environment, such as VMware:

- Synchronous disaster recovery

- Asynchronous disaster recovery

This section provides step-by-step instructions for managing Portworx RWX block volumes with KubeVirt virtual machines on SUSE Virtualization.

## Prerequisites​

- An operational SUSE Virtualization cluster.

- Portworx Enterprise version 3.3.0 or later.

- Portworx Operator version 25.2.1 or later.

- Portworx Stork version 25.2.0 or later.

- Administrative access to the SUSE Virtualization dashboard and the underlying Kubernetes cluster.

- Review the known issues before proceeding.

## Create a StorageClass​

If you are running Portworx Enterprise version 3.4.0 or later with Portworx Operator version 25.5.0 or later, the Portworx Operator creates the following StorageClasses by default when the `HyperConverged` custom resource is detected:

- `px-rwx-block-kubevirt`: RWX block volume class, and is annotated as the default KubeVirt StorageClass (only if no other default exists).

- `px-rwx-file-kubevirt`: Shared file system RWX class used for features like vTPM.

- `px-cdi-scratch`: Scratch space required for CDI image operations.

You can control the creation of these StorageClasses using the `spec.csi.kubeVirtStorageClasses` section in the `StorageCluster` custom resource.

Create a StorageClass if one does not already exist. The following is an example StorageClass.

-
Create the `px-kubevirt-sc.yaml` file:

StorageClass

```

apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:

  name: px-rwx-block-kubevirt

provisioner: pxd.portworx.com

parameters:

  cdi.kubevirt.io/storage.contentType: kubevirt

  repl: "3"

  nodiscard: "true" # Disables discard operations on the block device

volumeBindingMode: WaitForFirstConsumer

allowVolumeExpansion: true

```

note

- The `volumeBindingMode=WaitForFirstConsumer` flag enables Portworx to intelligently place the volumes. For more information, see the KubeVirt page.

- Note that the PVCs used by the VMs directly, should not include the annotation `cdi.kubevirt.io/storage.bind.immediate.requested=true`. This is because such an annotation overrides the `WaitForFirstConsumer` setting in the StorageClass.

- When migrating Forklift from vSphere to OpenShift Container Platform with Migration Toolkit for Virtualization, use `volumeBindingMode=immediate` for a successful migration.

-
Run the following command to apply your StorageClass:

```

kubectl apply -f px-kubevirt-sc.yaml

```

Portworx optimizes volume placement and ensures that multiple volumes used by a single KubeVirt VM are placed on the same set of replica nodes. This automatic co-location simplifies achieving hyperconvergence.

## Create a PVC​

-
Using the above StorageClass, define a PVC with the following configuration:

- `accessModes`: `ReadWriteMany` for shared volume access.

- `volumeMode`: `Block` to create a raw block device volume

PersistentVolumeClaim

```

apiVersion: v1

kind: PersistentVolumeClaim

metadata:

  name: rwx-disk-1

  labels:

    portworx.io/app: kubevirt

spec:

  accessModes:

  - ReadWriteMany

  resources:

    requests:

      storage: 100Gi

  storageClassName: px-rwx-block-kubevirt

  volumeMode: Block

```

-
Apply this PVC to your cluster:

```

kubectl apply -f pvc.yaml

```

When deploying KubeVirt VMs, reference the PVC created in the previous step to attach the Portworx RWX raw block volume to the VM. Ensure the VM configuration specifies the correct StorageClass and volume.

Once the VM is running with the specified PVC, you can perform live migration using SUSE Virtualization’s native functionality. The shared RWX volume ensures data consistency during the migration process by allowing simultaneous read/write operations for the source and destination nodes.

important

If you are manually creating a PVC and attaching it to a VM, ensure the following:

- Add the `portworx.io/app: kubevirt` annotation to the PVC spec. This ensures that Portworx will apply KubeVirt-specific logic when processing the volume.

- Maintain the same HA or replication factor for all volumes associated with a VM.

## VM configuration guidelines for Portworx raw block volumes​

When using Portworx RWX block volumes VMs, specific configurations are required to ensure compatibility and performance. The following guidance outlines considerations for root and data disks, block sizes, and bootloaders.

### Block size and bootloader compatibility​

The VM disk configuration defaults to a 512-byte block size. The hypervisor makes it compatible so that 512-byte operations work over a provisioned Portworx storage disk with a 4096-byte block size. Therefore, no changes are needed because block size compatibility is ensured.

- Portworx block volumes always use a 4096-byte block size.

- VM disks default to a 512-byte block size unless otherwise specified. Specifying a logical block size of 512-byte and a physical block size of 4096-byte in the VM disk specification is an optional configuration detail within the VM that may help applications or file systems optimize performance, if supported.

- VM root disks also contain a bootloader, which can be either EFI or BIOS. BIOS supports booting only from disks with a 512-byte block size. EFI supports booting from disks with either a 4096-byte or 512-byte block size. They are independent bootloading mechanisms. The root disk configuration determines which bootloader is used.

- You can identify the root disk configuration by examining the QCOW2 image or the disk partition table.

- EFI requires an EFI system partition, a GPT partition table, and related components.

- BIOS requires a partition marked as bootable.

- For example, RHEL configures its QCOW2 cloud images to boot using both EFI and BIOS by creating two partitions that contain the required information. Note that not all distributions support this configuration.

### VM spec example with custom block size​

VirtualMachine

```

...

spec:

  domain:

    devices:

      disks:

        - bootOrder: 1

          blockSize:

            custom:

              logical: 512

              physical: 4096

          disk:

            bus: virtio

          name: rootdisk

        - name: fio-data-disk-1

          blockSize:

            custom:

              logical: 4096

              physical: 4096

...

```

- Set `bootOrder: 1` to indicate the root disk.

- If `blockSize` is not specified, the default is 512 for both logical and physical sizes.

- For additional data disks, specifying both logical and physical block sizes as 4096 is recommended for improved performance.

### VM bootloader spec example​

Portworx supports both `UEFI` and `BIOS` bootloader.

- To use UEFI, define the bootloader section with `efi: {}`.

- If no `bootloader` section is present, BIOS is used by default.

VirtualMachine

```

...

spec:

  domain:

    firmware:

      bootloader:

        efi: {}

...

```

### Supported configuration matrix​

#### VM Root disk​

S.NoPortworx block sizeVM physical block sizeVM logical block sizeBootloader (root disk only)Supported

140964096 / 512512BIOSYes

240964096 / 512512EFIYes

3409640964096BIOSNo

4409640964096EFI only (qcow2 with 4K block size)Yes

#### Additional disks​

S.NoPortworx block sizeVM physical block sizeVM logical block sizeSupported

140964096512Yes

2409640964096Yes (Recommended)

## Create a VM​

Refer to the applicable version of the SUSE Virtualization: Create a Virtual Machine guide and KubeVirt user guide to create a KubeVirt VM.

After the VMs are created, each VM will start running in a `virt-launcher` pod.

Portworx ensures that:

- The newly created non-cloned volumes in a VM are co-located during creation.

- The cloned volumes in a VM are automatically relocated after the VM starts, aligning them with the non-cloned volumes created for that VM.

## Manage KubeVirt VMs during Portworx node upgrades​

When upgrading Portworx on a node, the Portworx Operator manages KubeVirt VMs by initiating a live migration before the upgrade begins. Here’s what happens during this process:

-
Eviction notice: As the operator attempts to evict virtual machines (VMs) from a node, it generates the following event if it is unable to migrate the VMs:

```

Warning: UpdatePaused - The update of the storage node <node-name> has been paused because there are 3 KubeVirt VMs running on the node. Portworx will live-migrate the VMs and the storage node will be updated after there are no VMs left on this node.

```

-
Migration failure: If the operator cannot successfully live-migrate a VM, the upgrade is paused, and the following event is recorded:

```

Warning: FailedToEvictVM - Live migration <migration-name> failed for VM <vm-namespace\ß>/<vm-name> on node <node-name>. Please stop or migrate the VM manually to continue the update of the storage node.

```

In this topic:
