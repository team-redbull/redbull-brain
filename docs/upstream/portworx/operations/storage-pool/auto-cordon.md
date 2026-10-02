# Recover Storage Nodes with Auto Cordon

Source: https://docs.portworx.com/portworx-enterprise/operations/storage-pool/auto-cordon (Portworx Enterprise 3.6)

Recover Storage Nodes with Auto Cordon | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Auto Cordon limits the impact of a storage pool failure by returning the affected node and its healthy storage pools to service while isolating the failed pool. This allows the node's remaining healthy storage capacity to stay available until you repair the underlying disk or pool failure.

When a disk failure takes a storage pool offline, the node can enter the `StorageDown` state even when its remaining pools are healthy. While the node is in this state, replicas on its healthy pools are also unavailable for I/O. If the node remains in this state for the configured timeout, Auto Cordon migrates eligible replicas from the offline pool, marks the failed pool as `Cordoned`, and restarts Portworx Enterprise. The node then returns to the `Up` state with its healthy pools online, while the failed pool remains cordoned until you recover it.

Auto Cordon is disabled by default. Enabling or disabling Auto Cordon applies to the entire cluster. To enable Auto Cordon, set the `auto-cordon-pool-timeout` cluster option to a nonzero value.

Auto Cordon is supported with both the PX-StoreV1 and PX-StoreV2 datastores.

important

Auto Cordon supports only the following drive configurations:

- Local drives on bare-metal nodes

- FlashArray pre-provisioned drives

- vSphere pre-provisioned drives

Do not enable Auto Cordon on clusters that use FlashArray cloud drives or vSphere cloud drives.

## Prerequisites​

All nodes in the cluster must run a Portworx Enterprise version that supports Auto Cordon.

## When Portworx Enterprise triggers Auto Cordon​

A disk failure can take a storage pool offline and cause the node to enter the `StorageDown` state. If the node remains in this state for the configured `auto-cordon-pool-timeout`, Portworx Enterprise triggers Auto Cordon.

If pool failures affect multiple nodes, each affected node runs Auto Cordon independently.

## How Auto Cordon recovers a node​

Auto Cordon performs the following operations on the affected node:

- Moves replicas of `repl=2` and `repl=3` volumes from the offline pool to healthy pools on other nodes.

- Sets the offline pool status to `Cordoned` and the status of the remaining healthy pools on the node to `Up`.

- Restarts Portworx Enterprise.

After the restart, the node returns to the `Up` state with its healthy pools available. If the node restarts while Auto Cordon is running, Portworx Enterprise resumes the operation from where it stopped.

To move the replicas, Auto Cordon performs an HA reduction for each `repl=2` and `repl=3` volume on the offline pool to remove its replica from that pool. Auto Cordon then performs a best-effort HA increase for each of these volumes to restore the configured replication level.

## Enable Auto Cordon​

To enable Auto Cordon, set `auto-cordon-pool-timeout` to the number of minutes that a node can remain in the `StorageDown` state before Portworx Enterprise starts Auto Cordon. Choose a timeout that provides enough time to investigate the pool failure while minimizing how long healthy storage capacity remains unavailable.

-
Set the timeout.
The following example sets it to 10 minutes:

```

pxctl cluster options update --auto-cordon-pool-timeout 10

```

```

Successfully updated cluster wide options

```

-
Verify the setting:

```

pxctl cluster options list

```

```

AutoCordonPool timeout                                  : 10m0s

```

## Disable Auto Cordon​

To disable Auto Cordon, set `auto-cordon-pool-timeout` to `0`:

```

pxctl cluster options update --auto-cordon-pool-timeout 0

```

Verify that the timeout is disabled:

```

pxctl cluster options list

```

```

AutoCordonPool timeout                                  : off

```

## Monitor Auto Cordon​

Portworx Enterprise generates the following pool alerts during an Auto Cordon operation:

AlertSeverityDescription

`AutoCordonPoolStarted`NOTIFYThe `autoCordonPool` background task has started.

`AutoCordonPoolSuccess`NOTIFYThe `autoCordonPool` background task has completed.

`AutoCordonPoolFailed`WARNINGThe `autoCordonPool` background task has failed.

For information about the corresponding metrics, see Portworx alerts reference.

To view alerts, run the following command:

```

pxctl alerts show

```

Example output:

```

NODE    AutoCordonPoolStarted    45xxxxe9-6xx9-4xx9-axx8-fxxxbx79xxx6    NOTIFY    1    Aug 31 20:54:46 UTC 2023    Aug 31 20:54:46 UTC 2023    Started repl-move for all replicas on pool 0

```

After Auto Cordon completes, verify the results on the affected node:

- Run `pxctl status` and verify that the node has returned from `StorageDown` to `Up` state.

- Run `pxctl service pool show` and verify that the failed pool is listed with the `Cordoned` status.

If Auto Cordon fails to complete, check the journal logs on the node in the `StorageDown` state for Auto Cordon-related entries.

## Limitations​

- Auto Cordon is supported only for non-metadata storage pools.

- Auto Cordon cannot cordon a pool that contains `repl=1` volumes. The node remains in the `StorageDown` state. Auto Cordon still moves replicas of `repl=2` and `repl=3` volumes from the offline pool.

- Auto Cordon processes one failed pool at a time. If multiple pools fail on the same node, Portworx Enterprise processes each failed pool through a separate `StorageDown` and Auto Cordon cycle.

- Auto Cordon does not delete or repair a cordoned pool or restore its capacity. You must recover the pool manually.

- Auto Cordon runs only if all nodes in the cluster run a version of Portworx Enterprise that supports the feature.

- Auto Cordon makes a best-effort attempt to restore each volume to its configured replication level. In some scenarios, a volume might remain at a reduced replication level.

## Recover a cordoned pool​

Auto Cordon does not recover a cordoned pool. To restore the capacity of the cordoned pool, delete the pool, repair or replace the failed disks, and then add the disks back to the node as a new pool.

caution

Deleting a pool is a destructive operation, and you cannot recover the deleted data. Before you delete a pool, ensure that it contains no volume replicas that you need.

-
Verify that the cordoned pool contains no volume replicas:

```

pxctl volume list --pool-uid <pool-uuid>

```

Auto Cordon moves the replicas of `repl=2` and `repl=3` volumes off the offline pool. If the pool still contains replicas, reduce the replication factor of each remaining volume to remove its replica from the pool.

-
Enter pool maintenance mode:

```

pxctl service pool maintenance --enter

```

-
Delete the cordoned pool by specifying its pool ID:

```

pxctl service pool delete <pool-id>

```

note

You can delete a pool only if the node has more than one pool.

-
Exit pool maintenance mode:

```

pxctl service pool maintenance --exit

```

-
Repair or replace the failed disks.

-
Add the disks back to the node as a new pool by specifying the drive paths:

```

pxctl service drive add --drive /dev/sdc,/dev/sdd --newpool

```

## Related topics​

- Manage your storage pool capacity

- PX-StoreV2

- Remove or replace a failed drive

- Portworx alerts reference

- pxctl cluster options

- pxctl service pool delete

In this topic:
