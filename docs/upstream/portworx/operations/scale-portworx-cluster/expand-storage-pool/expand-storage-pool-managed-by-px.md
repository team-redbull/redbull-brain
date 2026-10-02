# Expand your storage pool size with disks managed by Portworx

Source: https://docs.portworx.com/portworx-enterprise/operations/scale-portworx-cluster/expand-storage-pool/expand-storage-pool-managed-by-px (Portworx Enterprise 3.6)

Expand your storage pool size with disks managed by Portworx | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

If you are running on the cloud, consider automation into your decision for which pool resize approach you use. The `pxctl service pool expand` command allows you to perform resize operations without manually adding new drives or increasing drive capacity on your cluster.

When you enter the `pxctl service pool expand` command, Portworx uses your cloud provider's API to create new drives and attach them or to expand the existing drives with no further input from you.

You can control the pool expand operation by specifying which operation you want to use: `resize-drive` or `add-drive`, or you can specify `auto` to let Portworx determine the best way to resize your storage pools based on your cloud provider.

By default, each pool can have a maximum of 6 drives. If required, you can use the runtime option `limit_drives_per_pool` to change this value.

note

- You cannot add a new drive to the pool if your Portworx deployment is using PX-StoreV2 backend.

- On PX-StoreV2 pools, Portworx performs eligible `resize-drive` expansions non-disruptively by briefly pausing I/O to the pool instead of restarting Portworx in pool maintenance mode. For more information, see Non-Disruptive Pool Resize for PX-StoreV2 Pools.

The following table shows the maximum number of drives (which includes boot drives, Portworx cloud drives, and any other drives) for various platforms:

PlatformMaximum number of drives

AWS, Azure, GCP, and IBM8

vSphere12

Pure FlashArray32

### Limitations​

- For an EBS volume converted from gp2 to gp3, Portworx does not update with the latest metadata such as IOPS, even after completing a pool maintenance cycle. As a result, you continue to see gp2 related details in the output of `pxctl` commands.

- Performing back-to-back pool expansions may cause AWS cloud drives to enter an Optimizing state. In this state, it may take up to 24 hours for AWS to permit further resizing. You can expand your pools again once drives are out of this state. This state can be monitored via the EBS volume UI or the `aws cli`. For more information, see the AWS documentation.

### Prerequisites​

You must be running Portworx on one of the following cloud providers:

- AWS

- Azure

- GCP

- vSphere (cloud drives)

- Oracle

- IBM VPC Gen2 Platform (Portworx 2.11.0 or newer)

- Pure FlashArray (FACD)

note

For IBM, you must have the IBM Block CSI driver version 4.4 or newer. To check your version, run the following command:

```

ibmcloud ks cluster addon ls --cluster <cluster-id>

```

If you need to update the IBM CSI driver on your cluster, perform the following steps:

-
Remove the current version using the following command:

```

ibmcloud ks cluster addon disable vpc-block-csi-driver --cluster <cluster-id>

```

-
Enable `cluster addon` with `--version 4.4`:

```

ibmcloud ks cluster addon enable vpc-block-csi-driver --cluster <cluster-id> --version 4.4

```

-
Check that the correct version is present:

```

ibmcloud ks cluster addon ls --cluster <cluster-id>

```

```

OK

Name Version Health State Health Status

vpc-block-csi-driver 4.4* (4.3 default) - Enabling

```

### Automatically expand a cloud-based pool​

-
Run the following command to find the UUID for a pool:

```

pxctl service pool show

```

```

PX drive configuration:

Pool ID: 0

        UUID:  xxxxxxxx-xxxx-xxxx-xxxx-aef346e61d89

        IO Priority:  HIGH

        Labels:  iopriority=HIGH,medium=STORAGE_MEDIUM_SSD

        Size: 384 GiB

        Status: Online

        Has metadata:  Yes

        Balanced:  Yes

        Drives:

        1: /dev/sde, Total size 128 GiB, Online

        2: /dev/sdf, Total size 128 GiB, Online

        3: /dev/sdg, Total size 128 GiB, Online

        Cache Drives:

        No Cache drives found in this pool

Journal Device:

        1: /dev/sdc1, STORAGE_MEDIUM_SSD

```

```

PX drive configuration:

Pool ID: 0

        UUID:  46f7e68b-3892-xxxx-xxxx-xxxxxxxxxxxx

        IO Priority:  HIGH

        Labels:  iopriority=HIGH,medium=STORAGE_MEDIUM_SSD

        Size: 384 GiB

        Status: Online

        Has metadata:  Yes

        Balanced:  Yes

        Drives:

        1: /dev/sde, Total size 128 GiB, Online

        2: /dev/sdf, Total size 128 GiB, Online

        3: /dev/sdg, Total size 128 GiB, Online

        Cache Drives:

        No Cache drives found in this pool

Journal Device:

        1: /dev/sdc1, STORAGE_MEDIUM_SSD

```

-
Expand a cloud-based pool by entering the `pxctl service pool expand` command with the following options:

- The `--operation` option to specify the desired operation

- The `--size` option to set the minimum new size of the pool in GiB

- The `--uid` option to provide the ID of the pool you want to resize

```

pxctl service pool expand --operation auto --size 1000 --uid <pool-UUID>

```

For example:

```

pxctl service pool expand --operation auto --size 1000 --uid xxxxxxxx-xxxx-xxxx-xxxx-aef346e61d89

```

For example:

```

pxctl service pool expand --operation auto --size 1000 --uid 46f7e68b-3892-xxxx-xxxx-xxxxxxxxxxxx

```

-
Once you submit the command, Portworx expands the storage pool in the background. You can list the storage pools periodically to check if they have finished expansion.

```

pxctl cluster provision-status

```

-
When invoked on the Portworx node where the storage pool resides, the following command provides detailed information about the status of the pool expand process.

```

pxctl service pool show

```

### Resize or add a new drive to a cloud-based pool​

The `auto` operation automatically expands your pool capacity by increasing the pool size or adding the new drives to it. To perform a specific operation, replace `auto` with `add-drive` or `resize-drive`:

```

pxctl service pool expand --operation add-drive --uid <pool-ID> --size <new-storage-pool-size-in-GiB>

```

To use `resize-drive` instead:

```

pxctl service pool expand --operation resize-drive --uid <pool-ID> --size <new-storage-pool-size-in-GiB>

```

note

When running the command `pxctl service pool expand --operation resize-drive --size <new-storage-pool-size-in-GiB> --uid <pool-ID>` for specific nodes, you may encounter the following warning message in the output of `kubectl describe pvc <name-of-px-cloud-drive-pvc>`:

`Waiting for user to (re-)start a pod to finish file system resize of volume on node.`

This warning indicates that the file system resize process on the volume is pending until the pod is restarted. However, it does not impact any Portworx operations, as the storage pool reflects the correct size, and you can further expand the pool if necessary. Portworx continues to function normally, and you can safely ignore this warning.

## Azure disk expansion with PremiumV2_LRS and UltraSSD_LRS disk types​

When using PremiumV2_LRS or UltraSSD_LRS disk types, a dedicated metadata device partition must be configured on the storage pool. This configuration is required to support disk expansion operations and to ensure metadata is preserved independently of the data pool.

To avoid losing metadata during the disk expansion process of PremiumV2_LRS and UltraSSD_LRS disk types, ensure the following conditions are met:

- A dedicated metadata device must be available on the node.

- The metadata device must be separate from the data drives used in the pool.

- Each data pool must report `Has metadata: No` to confirm that metadata is not stored within the pool's data devices.

The following example shows a correctly configured storage pool with a dedicated metadata device:

```

[root@aks-nodepool1-3xx24542-vmss000001 /]# pxctl sv pool show

PX drive configuration:

Pool ID: 0

	Type:  Default

	UUID:  101103aa-1xxd-45c1-8dcc-059ee039fxxx

	IO Priority:  MEDIUM

	Labels:  kubernetes.azure.com/xxxxxx/xxxxxxx

	Size: 147 GiB

	Status: Online

	Has metadata:  No                        # Indicates metadata is stored separately

	Drives:

	1: /dev/sdf2, Total size 147 GiB, Online

	Cache Drives:

	No Cache drives found in this pool

Journal Device:

	1: /dev/sdf1, STORAGE_MEDIUM_SSD

Metadata Device:

	1: /dev/sde, STORAGE_MEDIUM_SSD          # Dedicated metadata device

```

In this configuration:

- The `Metadata Device` is listed separately (`/dev/sde`).

- The `Has metadata` field is set to `No`, confirming that metadata is not stored on the main data drives.

In this topic:
