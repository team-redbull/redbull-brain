# Manage Shared Block Device (RWX Block) for KubeVirt VMs

Source: https://docs.portworx.com/portworx-enterprise/provision-storage/kubevirt-vms/manage-kubevirt-vms-rwx-block (Portworx Enterprise 3.6)

Manage Shared Block Device (RWX Block) for KubeVirt VMs | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx supports volumes for KubeVirt virtual machines (VMs) as storage disks in various configurations. To enable features such as live migration, these volumes must support the ReadWriteMany (RWX) access mode. Portworx supports the RWX block volume type, which offers improved performance in certain scenarios, and also supports the RWX file system (FS) volume type.

important

- Portworx RWX block volumes are designed and qualified only for use with KubeVirt VMs. For other scenarios, contact support before deployment.

- For ReadWriteMany (RWX) volumes, Portworx supports up to 1,024 attachments per node, which can increase virtual machine (VM) density on a single node if resources permit. SharedV4 and FADA RWX volumes support up to 256 attachments per node. For more details, see Features and configurations supported with different license types.

- Portworx ReadWriteMany (RWX) block volumes do not support encryption or fast-path.

- When you import or clone a VM disk image onto an RWX block volume, for example, during a Forklift migration from VMware vSphere or a CDI DataVolume import, you can use Write Zeroes support to speed up the operation and reduce capacity consumption. For more information, see Write Zeroes Support for RWX Block Volumes.

Portworx supports volume co-location for KubeVirt VMs using RWX block volumes. Portworx ensures that multiple volumes used by a single VM running on KubeVirt are placed on the same set of replica nodes. This automatic co-location simplifies achieving hyperconvergence and improves performance, reliability, and I/O efficiency.

note

By default, co-location is enabled for newly created VMs in Portworx Enterprise 3.5.0 or later.

Co-location behavior differs depending on whether a volume is cloned with the `cloneStrategy: csi-clone` setting.

-
When volumes are cloned from a template PVC using the `cloneStrategy: csi-clone` setting, the volume replicas are initially placed on the same nodes as the source volume. This improves provisioning speed but may cause multiple VMs to share the same replica nodes if they are cloned from the same template. To avoid potential node overload, Portworx automatically relocates the cloned volume replicas after the VM starts, aligning them with the non-cloned volumes associated with that VM.
If your VMs have only a single disk cloned from the template PVC and no non-cloned volume, Portworx has no target to align to, and provisioning a large batch of such VMs can create I/O hot spots. For approaches to distribute replicas evenly in this case, see Storage hot spots when cloning many VMs from a single template PVC.

-
For blank volumes or those created with the `cloneStrategy: copy` setting, Portworx automatically selects replica nodes to co-locate the volumes of the same VM during creation. Replica placement takes node capacity and current replica distribution into account. Portworx recommends including at least one such data volume in each VM to help balance replica placement across nodes.

-
For existing VMs upgraded to 3.5.0, Portworx adds a `vps.portworx.io/volume-affinity-mode: "disable"` annotation to the corresponding VM object in Kubernetes to prevent replica movement after the upgrade. This prevents unexpected replica migrations that could temporarily impact I/O performance. To enable co-location for an existing VM, you must manually remove the annotation from the VM and restart the VM. Portworx will then trigger background co-location adjustments using its scheduled reconciliation job (`vps-fix`), which runs every 15 minutes.

## Select your platform​

Use the platform-specific guide below to manage Portworx RWX block volumes with KubeVirt VMs:

- Manage RWX block volumes on OpenShift

- Manage RWX block volumes on SUSE Virtualization

In this topic:
