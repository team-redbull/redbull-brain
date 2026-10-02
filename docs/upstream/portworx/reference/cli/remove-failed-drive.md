# Remove or replace a failed drive

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/remove-failed-drive (Portworx Enterprise latest)

Remove or replace a failed drive | Portworx Enterprise Documentation

When a drive fails, Portworx continues to operate using available replicas on other nodes. To fully recover from a drive failure, you must replace or remove the failed drive from Portworx, and how you recover depends on the pool which contains the failed drive.

There are two possible scenarios for a failed drive:

- The drive belongs to a pool which hosts Portworx metadata

- The drive belongs to a non-metadata pool

note

- You cannot recover a completely failed drive from a RAID 0 drive.

- You can only recover volumes with a replication factor greater than 1. Refer to the updating volumes page for information on increasing the replication factor of a volume.

Perform the procedures below to determine if your drive failed on a storage pool containing metadata and remove or replace a failed drive:

## Determine if the pool containing your failed drive hosts Portworx metadata​

You must determine if your failed drive belongs to a storage pool containing metadata to choose the appropriate method for replacing it.

-
Identify a failed drive and `ssh` into the node containing that drive.

-
Determine if the pool containing that drive hosts metadata by entering the `pxctl service pool show` command and looking for the `Has metadata` field in the output:

```

pxctl service pool show

```

```

PX drive configuration:

Pool ID: 1

UUID: xxxxxxxx-xxxx-xxxx-xxxx-eca86906c921

IO Priority: LOW

Labels: iopriority=LOW,medium=STORAGE_MEDIUM_MAGNETIC

Size: 20 GiB

Status: Online

Has metadata: Yes

Drives:

1: /dev/sdc, 8.0 GiB allocated of 20 GiB, Online

Cache Drives:

```

In the output above, note the line that reads "Has metadata: Yes".

If your service pool has metadata, follow the procedure to Replace a drive that belongs to a pool which hosts Portworx metadata. If your service pool does not have metadata, follow the procedure to Replace a drive that belongs to a non-metadata pool.

## Remove or replace a drive that belongs to a pool which hosts Portworx metadata​

If the drive belongs to a pool that hosts Portworx metadata, then you must remove the node from the cluster and remove or replace the failed drive.

Perform the following steps to remove or replace the failed drive:

-
Use the Node decommission workflow to remove a node from the cluster. This reduces the HA level for all replicated volumes which reside on the node and restores the volumes if enough storage nodes are available in the cluster.

-
Remove or replace the failed drive and add the node back into the cluster. Note that Portworx runs as a `DaemonSet` in Kubernetes, so when you add a node or a worker to your Kubernetes cluster, you don't need to explicitly run Portworx on it.

## Remove or replace a drive that belongs to a non-metadata pool​

If the drive belongs to a non-metadata pool, then you must delete the affected storage pool.

note

The failed drive must belong to a node that contains more than one storage pool. You cannot transition to a storageless node using this procedure.

Perform the following steps to remove or replace a failed drive by deleting the storage pool:

-
Enter the `pxctl service pool show` command and make a note of both the UID and pool ID for the next steps:

```

pxctl service pool show

```

```

PX drive configuration:

Pool ID: 0

    UUID: xxxxxxxx-xxxx-xxxx-xxxx-91e5108ebba5

    IO Priority:  LOW

    Labels:  iopriority=LOW,medium=STORAGE_MEDIUM_MAGNETIC

    Size: 128 GiB

    Status: Online

    Has metadata:  Yes

    Drives:

    1: /dev/sdc, 38 GiB allocated of 128 GiB, Online

    Cache Drives:

    No Cache drives found in this pool

```

-
Enter the `pxctl volume list` command with the `--pool-uid` option and the pool UID you got from the step above to list the volumes. Look through the output to find the replica sets that match the pool identifier containing the failed drive.

```

pxctl volume list --pool-uid xxxxxxxx-xxxx-xxxx-xxxx-91e5108ebba5

```

```

ID			            NAME					SIZE	   HA SHARED	ENCRYPTED IO_PRIORITY	 STATUS		      SNAP-ENABLED

184362890321734385	exampleVolume	128 GiB  3  no	    no		    LOW		       up - detached	no

```

-
Manually remove all replicas of the volumes in this pool. Refer to the Decreasing the replication factor section for information on how to do this.

-
Run the following command to enter the pool maintenance mode:

```

pxctl service pool maintenance --enter

```

-
To delete the pool, use the `pxctl service pool delete` command and specify the `Pool ID` that you noted in step 1 as the argument:

```

pxctl service pool delete 0

```

-
Run the following command to exit the pool maintenance mode:

```

pxctl service pool maintenance --exit

```

-
Perform the node maintenance cycle for your Portworx node.

-
Optionally, you can replace the failed drive, ensuring it matches the same capacity and type as the original. Alternatively, you can delete the pool and recreate it with fewer drives if needed. Note that drive replacement is not supported when using the PX-StoreV2 backend.

-
To re-add drives, use the `pxctl service drive add` command with the `--drive` option to specify the paths to your drives.

-
On-premises Drives: Use the following command to add multiple drives. For example, this command adds three drives and creates a new storage pool:

```

pxctl service drive add --drive /dev/sdc,/dev/sdd,/dev/sde --newpool

```

-
Cloud Drives: Use the `pxctl service drive add -s` command to add cloud drives. Specify the drive type and size as shown below:

```

pxctl service drive add -s  type=db,size=50 --newpool

```

In this topic:
