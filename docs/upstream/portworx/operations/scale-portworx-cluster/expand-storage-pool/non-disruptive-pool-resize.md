# Non-Disruptive Pool Resize

Source: https://docs.portworx.com/portworx-enterprise/operations/scale-portworx-cluster/expand-storage-pool/non-disruptive-pool-resize (Portworx Enterprise latest)

Non-Disruptive Pool Resize | Portworx Enterprise Documentation

Non-disruptive pool resize allows Portworx Enterprise to expand eligible PX-StoreV2 storage pools without entering pool maintenance mode or restarting Portworx. During the expansion, Portworx briefly pauses I/O to the affected pool, expands the pool, and then resumes I/O.

This behavior is particularly useful for volumes with a replication factor of 1 (`repl=1`), including eligible fast-path volumes, because these volumes do not have another replica that can serve I/O during a Portworx restart.

Non-disruptive pool resize is enabled by default. You expand a pool by using the existing `pxctl service pool expand` command, and Portworx automatically uses the non-disruptive workflow when the pool and requested operation meet the requirements.

## How non-disruptive pool resize works​

When an eligible PX-StoreV2 pool is expanded by using the `resize-drive` operation, Portworx performs the following operations:

-
Validates the request: Portworx verifies that the pool and expansion operation meet the requirements for non-disruptive resize.

-
Quiesces the pool: Portworx moves eligible local fast-path volumes to the native I/O path and temporarily pauses I/O to the pool. Portworx drains pending I/O and flushes data to storage before starting the resize.

-
Resizes the pool: Portworx expands the underlying data and metadata devices and updates the pool size.

-
Resumes I/O: Portworx resumes I/O to the pool. Eligible volumes that were moved from the fast path can return to the fast path.

If the pool does not meet the requirements for non-disruptive resize, Portworx uses the applicable pool expansion workflow instead.

## Prerequisites​

Portworx uses non-disruptive pool resize when all of the following conditions are met:

- All nodes in the cluster run Portworx Enterprise version 3.7.0 or later.

- The pool uses PX-StoreV2.

- The expansion uses the `resize-drive` operation.

- The pool does not host remote fast-path volumes.

- Non-disruptive pool resize is enabled at the cluster level.

The `resize-drive` operation can be selected explicitly with `--operation resize-drive` or automatically when `--operation auto` resolves to `resize-drive`.

## Limitations​

Non-disruptive pool resize has the following limitations:

-
Pools that host remote fast-path volumes are not supported.

-
Pool resize duration increases with the number of drives because Portworx resizes each drive in the pool. If the data pool contains a journal partition, the additional partition refreshes can further increase the resize duration.

-
Portworx blocks a pool resize if any volume in the pool has an HA update in progress. The resize fails and reports the affected volumes, for example:

```

Message: failed to quiesce pool: pool abg7-25-4g4-bd44-05xx2 has 78 volume(s) with an HA update in progress (...). Retry the pool resize operation after HA update operation on pool volumes complete

```

Retry the pool resize after all HA updates on volumes in the pool complete. If appropriate, you can cancel the in-progress HA updates before retrying the resize.

## Considerations​

Review the following before expanding a PX-StoreV2 pool:

-
Portworx temporarily moves eligible local fast-path volumes to the native I/O path during the expansion and returns eligible volumes to the fast path afterward. Pools with many fast-path volumes can take longer to quiesce and resume.

-
Volumes with multiple replicas can continue to serve I/O through other replicas. Workloads might experience a temporary increase in I/O latency during the resize.

-
While the pool is quiesced, some operations that require access to the pool might be temporarily unavailable. Retry unsuccessful operations after the resize completes.

-
A pool resize cannot run concurrently with another operation that requires the same pool to be quiesced, such as a dynamic pool migration.

-
If Portworx or the node restarts during a resize, Portworx detects the interrupted operation during startup and recovers the pool before continuing the resize workflow.

-
Do not enter maintenance mode while a pool resize is in progress.

## Expand a PX-StoreV2 pool​

Portworx automatically selects the non-disruptive workflow when the pool meets all the requirements mentioned in the Prerequisites section.

-
Identify the UUID of the pool that you want to expand:

```

pxctl service pool show

```

-
Expand the pool by using the `resize-drive` operation:

```

pxctl service pool expand --operation resize-drive --uid <pool-UUID> --size <new-size-in-GiB>

```

Replace:

- `<pool-uuid>` with the UUID of the pool.

- `<new-size-in-GiB>` with the new pool size in GiB.

Following is a sample output:

```

Request to expand pool: 256f-97cc-aee1-fa37cba to size: 1500 using operation: resize-drive

Pool resize requested successfully. Please check resize operation status with `pxctl sv pool show`.

```

-
Monitor the pool expansion:

```

pxctl service pool show

```

```

Pool ID: 0

        Type:  PX-StoreV2

        UUID:  256f-97cc-aee1-fa37cba

        ...

        Size: 1.5 TiB

        Status: Online

        LastOperation  OPERATION_RESIZE

                Status:  OPERATION_SUCCESSFUL

                Message: pool expansion to 1500 GiB completed successfully using online resize

```

Verify that:

- The pool status is `Online`.

- The pool reports the requested capacity.

- The last resize operation completed successfully.

note

The `using online resize` text in the `Message` field confirms that Portworx used the non-disruptive resize workflow. If Portworx uses the maintenance-mode resize workflow instead, Portworx restarts on the node in pool maintenance mode, and the Message field does not include `using online resize`.

For detailed expansion procedures and platform-specific requirements, see Expand your storage pool size with disks managed by Portworx.

## Disable or re-enable non-disruptive pool resize​

Non-disruptive pool resize is enabled by default. Disable it only when you need Portworx to use the maintenance-mode resize workflow, such as when troubleshooting with Portworx Support.

To disable non-disruptive pool resize for the cluster:

```

pxctl cluster options update --non-disruptive-pool-resize false

```

```

Non-disruptive pool resize has been disabled. Pool resize will use maintenance mode.

```

To re-enable it:

```

pxctl cluster options update --non-disruptive-pool-resize true

```

```

Non-disruptive pool resize has been enabled. Pool resize will use the online resize flow.

```

To check the current setting:

```

pxctl cluster options list | grep -i "Non-disruptive"

```

```

Non-disruptive pool resize             : true

```

note

This setting is a cluster-wide option and applies to all PX-StoreV2 pools in the cluster. Changing it affects only subsequent expansions, not an expansion that is already in progress.

In this topic:
