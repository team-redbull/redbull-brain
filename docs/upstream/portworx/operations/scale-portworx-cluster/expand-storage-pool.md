# Expand your Storage Pool Size

Source: https://docs.portworx.com/portworx-enterprise/operations/scale-portworx-cluster/expand-storage-pool (Portworx Enterprise 3.6)

Expand your Storage Pool Size | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

As your cluster usage increases and the data on your storage pools grows, you may start to run out of capacity. In order to correct this, you must determine the most efficient way to expand your storage pool size.

Portworx allows you to expand your storage pools completely online (with a few exceptions) with the following two methods:

-
resize-drive: Using this method, you can vertically expand the storage pool size by increasing the size of the existing drives. All drives in the pool need to be resized to the same size for this operation. If the underlying infrastructure or the cloud provider supports resizing drives, this is the preferred option, as resizing disks involves no data movement and ensures zero downtime.

Limitation

On Azure platforms, online pool expansion is not supported if your Azure disk size is equal to or less than 4 TiB and you want to expand it beyond 4 TiB.

-
add-drive: Using this mode, you can horizontally expand the storage pool by adding drives. The new drive(s) will need to match the existing drives in size and IOPS properties (if available). This operation might involve a significant amount of data movement, since the existing data needs to be restriped. This operation can also be performed online and requires no downtime. Note that the pool runs in degraded mode during the `add-drive` operation.

Limitations

- If the pool is at or greater than 90% of its capacity, this operation can only be performed in pool maintenance mode.

- If you have installed Portworx with the PX-StoreV2 datastore:

- You can increase the size of the pool up to 15 TB.

- Portworx does not support the `add-drive` operations.

important

-
If a pool to be resized contains an auto journal device, Portworx automatically performs data partition resizing as part of the expansion operation.

-
If you disable non-disruptive pool resize, PX-StoreV2 pool expansion uses pool maintenance mode, which restarts Portworx on the node. During the restart, a volume with a single replica (repl=1) might experience I/O loss. In some cases, the volume file system might require a full file system check.

To recover the affected volume:

- Scale down any applications that use the affected volume.

- Attach the volume to a node:

```

pxctl host attach <volumeID>

```

- On the same node, run a volume check:

```

pxctl  volume check start --mode fix_all <volumeID>

```

## Non-disruptive pool resize for PX-StoreV2 pools​

Portworx expands eligible PX-StoreV2 pools without entering pool maintenance mode or restarting Portworx. It automatically uses non-disruptive resize for eligible resize-drive operations, including expansions triggered by Autopilot. For information about how non-disruptive resize works, its requirements, and how to configure it, see Non-Disruptive Pool Resize.

## Expand storage pool size​

Depending on the drives you want to use to expand a pool, proceed to one of the following sections:

## 📄️Non-disruptive pool resize

Learn how Portworx expands eligible PX-StoreV2 pools without entering pool maintenance mode and how to manage non-disruptive pool resize.

## 📄️Disks managed by Portworx

Explore different methods for expanding your storage pool size with disks managed by Portworx.

## 📄️Disks not managed by Portworx

Explore different methods for expanding your storage pool size with disks not managed by Portworx.

## 📄️Pre-provisioned Disks in a PX-StoreV2 Storage Pool

Expand a pre-provisioned LUN or disk backed by PX-StoreV2 and have Portworx recognize the new capacity through an OS rescan and maintenance mode cycle.

In this topic:
