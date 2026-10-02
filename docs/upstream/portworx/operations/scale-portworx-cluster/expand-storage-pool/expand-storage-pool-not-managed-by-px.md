# Expand your storage pool size with disks not managed by Portworx

Source: https://docs.portworx.com/portworx-enterprise/operations/scale-portworx-cluster/expand-storage-pool/expand-storage-pool-not-managed-by-px (Portworx Enterprise 3.6)

Expand your storage pool size with disks not managed by Portworx | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

If you are running Portworx in an environment where you need or want to manually resize a pool using drives that are not managed by Portworx, then follow these steps:

### Add drives​

-
Identify a storage pool that's running low on capacity.

-
Add drives to your node that are similar in size, type, and performance to the drives already in the pool you need to expand.

-
Add the drive by running the `pxctl service drive add` command with the following options:

- The `--drive` flag followed by the name of the drive you want to add.

- The `--operation` start flag.

```

pxctl sv drive add --drive /dev/sde --operation start

```

```

Adding drives may make storage offline for the duration of the operation.

Are you sure you want to proceed ? (Y/N): y

Drive add done: Storage rebalance is in progress

```

After adding the drive, Portworx starts restriping the pool to include the new drive.

note

For cloud-based pools, use this method for creating a new pool instead of expanding an existing pool. To add a drive to an existing cloud-based pool, use the `pxctl service pool expand --operation add-drive --uid <pool-ID> --size <new-storage-pool-size-in-GiB>` command.

-
Monitor the drive add operation status by entering the `pxctl service drive add` command, specifying the following:

- The `--drive` flag and the name of the drive you added

- The `--operation status` flag

```

pxctl service drive add --drive /dev/sde --operation status

```

When the status shows as `Drive /dev/sde already in use by PX.`, storage will be brought online automatically when this operation completes.

### Expand a pool size to consume the added drive capacity​

Follow the instructions in this section to expand the capacity of your storage pool and make use of the available capacity from added drives or existing drives that are not managed by Portworx:

-
Run the following command to identify a storage pool that's in need of expansion:

```

pxctl service pool show

```

-
Resize your drive and drive partition, if required.

-
On the node containing your target drive, enter the `pxctl service pool update` command, specifying the `--resize` option and the ID of the pool you want to resize:

```

pxctl service pool update --resize <pool-id>

```

```

Pool properties updated

```

In this topic:
