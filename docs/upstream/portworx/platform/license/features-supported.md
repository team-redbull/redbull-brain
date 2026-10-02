# Features and configurations supported with different license types

Source: https://docs.portworx.com/portworx-enterprise/platform/license/features-supported (Portworx Enterprise latest)

Features and configurations supported with different license types | Portworx Enterprise Documentation

In the following table, you can see the overview of features that are controlled via licensing.

License featureDescriptionLicense: Portworx CSI for FlashArray and FlashBladeLicense: Portworx EnterpriseLicense: Portworx for Modern Virtualization

Number of nodes maximumDefines the maximum number of nodes in a cluster100010001000

Number of volumes per cluster maximumDefines the maximum number of volumes in a cluster100000 Direct Access volumes100000100000

Provide storage for container workloadsProvision volumes for containersyesyesno

Provide storage for virtual machine workloadsProvision volumes for virtual machinesyesyesyes

Live migration for virtual machine workloadsMigrate your virtual machines from one node to another node without any disruptionsyesyesyes

Volume capacity [TiB] maximumDefines the maximum size of a single volume40 TiB40 TiB40 TiB

Node disk capacity [TiB] maximumDefines the maximum storage capacity of a single node256 TiB256 TiB256 TiB

Node disk capacity extensionDefines whether the storage capacity can be extendedno1yesyes

Number of snapshots per volume maximumNumber of volume snapshots allowed per single volumeno16464

Number of attached volumes per node maximumDefines the maximum number of attached volumes on a single node5121024210242

Number of total volumes per node maximum (PX-StoreV2)The total number of volumes on a single node for PX-StoreV2. This includes volumes, replicas, and snapshots present on the node.102431024310243

Storage aggregationDefines whether volumes can be aggregated across multiple nodesnoyesyes

Shared volumes (RWX)Defines whether volumes can be shared with other nodesyesyes4yes4

BYOK data encryptionDefines whether you can bring your own key (BYOK) for data encryptionno1Per volume and per clusterPer volume and per cluster

Limit BYOK encryption to cluster-wide secretsDefines whether the use of data-encryption keys is restricted to cluster-wide secretslimitedunlimitedunlimited

Resize volumes on demandDefines whether volumes can be resizedyesyesyes

Snapshot to object store [CloudSnap]Defines whether cloud snapshots can be used (for example, volume snapshot to Amazon S3 service)no1yesyes

Number of CloudSnaps daily per volume maximumDefines the maximum number of cloud snapshots per volume, per dayno1unlimitedunlimited

Cluster-level migration [Kube-motion/Data Migration]Defines whether you can use Data Migration. For more information, see Data Migration.noyesyes

Disaster Recovery [PX-DR]Enables synchronous and asynchronous disaster recovery featuresnoyes (add-on license required)yes

Autopilot Capacity ManagementDefines whether you can use Autopilotnoyesyes

PX SecurityProvides a way to secure the communication between Kubernetes and Portworxnoyesyes

Bare-metal hostsDefines whether you can deploy Portworx on commodity hardwareyesyesyes

Virtual machine hostsDefines whether you can deploy Portworx on VMs, including Amazon EC2 and OpenStack Novayesyesno

### Trial License​

The trial license is activated automatically when the Portworx Enterprise license is installed and provides the full product functionality for 30 days.

```

DESCRIPTION                  ENABLEMENT  ADDITIONAL INFO

Number of nodes maximum         1000

Number of volumes maximum     100000

Volume capacity [TB] maximum      40

Storage aggregation              yes

Shared volumes                   yes

Volume sets                      yes

BYOK data encryption             yes

Resize volumes on demand         yes

Snapshot to object store         yes

Bare-metal hosts                 yes

Virtual machine hosts            yes

Product SKU                     Trial    expires in 6 days, 20:40

```

### Trial license expiration​

After the trial period expires, you cannot create new volumes or volume snapshots. You can restore normal functionality by purchasing and installing a Portworx Enterprise license.

## Footnotes​

-
Starting with Portworx version 3.1.0, Portworx volumes are not supported with the Portworx CSI for FlashArray and FlashBlade license, some related features are no longer applicable under this plan. ↩ ↩2 ↩3 ↩4 ↩5

-
FADA and SharedV4 volumes cannot exceed 256 attachments per node. Portworx needs the FUSE driver version v3.5.0 or later to support a higher limit on volume attachments. Ensure that sufficient node resources such as CPU, memory, disks, network, and other resources, are available to support the number of volumes attached to the node. If the node’s resources are overloaded, it could result in the Portworx service restarting or the node becoming unresponsive. ↩ ↩2

-
This is the recommended maximum number of volumes per node for PX-StoreV2. It is not enforced by product licensing and serves as a guideline for optimal performance. You can increase this limit using cluster configuration options, depending on your environment and workload requirements. ↩ ↩2 ↩3

-
Portworx supports RWX file volumes for both container and virtual machine workloads, and RWX block volumes for virtual machine workloads only. RWX block volumes are designed and qualified only for use with KubeVirt VMs, and they do not support encryption or fast-path. For more information, see Manage Shared Block Device (RWX Block) for KubeVirt VMs. ↩ ↩2

In this topic:
