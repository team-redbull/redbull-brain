# Configure Storage Pool Cache

Source: https://docs.portworx.com/portworx-enterprise/operations/storage-pool/configure-pool-caching (Portworx Enterprise 3.6)

Configure Storage Pool Cache | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Storage pool caching helps with improving IOPS and latency. For more information, see Storage pool caching.

If Pool caching is enabled with your Portworx installation, you can perform the following tasks to add and configure pool caching.

- Add a cache drive to a storage pool

- Configure storage pool caching properties

In case storage pools cache drives are configured and if caching is currently disabled, you can re-enable caching, see Enable Storage Pool Caching.

To forcibly write dirty cache blocks to the backing storage pool, you can flush storage pool cache. This is required before disabling cache on a pool running in `writeback` mode.

## Prerequisites​

-
Pool caching is enabled.

It is enabled by default if Portworx Enterprise is installed with PX-StoreV2. If Portworx Enterprise is installed with PX-StoreV1, you must enable pool caching. See Install Portworx with Caching Enabled for PX-StoreV1.

-
The cache drive must be of higher performance than the storage pool drives.

## Add a Cache Drive to a Storage Pool​

-
Adding a cache drive requires the pool to be in maintenance mode. Enter the pool in maintenance mode by using the `--enter` flag.

```

pxctl service pool maintenance --enter

```

This will restart Portworx and set the pool maintenance mode to active.

note

Adding a cache drive requires pool maintenance mode (not node maintenance mode). This is different from regular drive add operations which can be done online.

-
Add a cache drive using the `--cache` flag.

```

pxctl service drive add --drive <drive_path> --cache <pool_id>

```

For example, to add a caching drive at `/dev/sdc` to pool `0`:

```

pxctl service drive add --drive /dev/sdc --cache 0

```

Wait for the add operation to complete.

-
Verify that the drive has been added.

```

pxctl service drive add --drive <drive_path> --cache <pool_id> --operation status

```

For example, to check status of caching drive at `/dev/sdc` in pool `0`:

```

pxctl service drive add --drive /dev/sdc --cache 0 --operation status

```

-
Exit pool maintenance mode after the cache drive is added.

```

pxctl service pool maintenance --exit

```

## Configure Caching Properties of Storage Pools​

You can configure cache parameters such as mode, block size, policy, and tunables for a storage pool. Before configuring caching properties, you should ensure that a caching drive is added to storage pool, and the pool is online with no pending operations.

info

This operation does not require pool maintenance mode. The pool can remain online during configuration.

Run the `pxctl service pool cache configure` command to configure cache properties as shown below.

```

pxctl service pool cache configure \

  --mode <writeback|writethrough> \

  --blocksize <block_size|auto> \

  --policy <smq|mq> \

  --tunables <tunable_parameters> \

  <pool_id>

```

Set the parameters based on your requirements. Here is the list of all the parameters that can be configured.

ParameterDescription

`mode`Cache operating mode: `writeback` (default, better performance) or `writethrough` (safer, data written to both cache and pool)

`blocksize`Cache block size. Use `auto` to let Portworx optimize this value

`policy`Cache policy: `smq` (default, recommended) or `mq`

`tunables`Comma-separated cache settings like migration threshold can be set as `migration_threshold=2048000`)

caution

Be cautious when modifying tunable arguments. Incorrect values might cause Portworx to behave unexpectedly or perform poorly.

For example, to configure pool `0` with `writeback` mode and custom migration threshold:

```

pxctl service pool cache configure \

  --mode writeback \

  --blocksize auto \

  --policy smq \

  --tunables migration_threshold=2048000 \

  0

```

```

Cache parameters updated, check using 'pxctl service pool cache status 0'

```

You can improve cache performance by using the auto-tune cache migration threshold feature which automatically adjusts migration threshold value based on cache utilization.

## Enable storage pool caching​

To re-enable caching on a storage pool that has cache drives configured but currently disabled:

info

This operation does not require pool maintenance mode. The pool can remain online.

-
Verify that caching is currently disabled:

```

pxctl service pool cache status <pool_id>

```

Caching is disabled if `Enabled: false` is visible in the output.

-
Enable caching with `pxctl service pool cache enable` command:

```

pxctl service pool cache enable <pool_id>

```

For example, to enable caching on pool `0`:

```

pxctl service pool cache enable 0

```

```

Pool 0 attached cache successfully

```

-
Check the pool cache status to verify caching is enabled.

```

pxctl service pool cache status 0

```

```

PX Cache Configuration and Status:

Pool ID:  0

        Enabled:  true

        Members:  [/dev/sdc]

        TotalBlocks: 71660

        UsedBlocks: 10

        DirtyBlocks: 6

        ReadHits: 13

        ReadMisses: 10

        WriteHits: 14

        WriteMisses: 8

        BlockSize: 1048576

        Mode: writeback

        Policy: smq

        Tunables: migration_threshold=20480

```

`Enabled: true` is set in the output verifies that caching is enabled for storage pool 0. Here are the parameter details for all the values that are configured for storage pool cache.

FieldDescription

`Enabled`Whether caching is currently active

`Members`List of cache drive paths

`TotalBlocks`Total number of cache blocks

`UsedBlocks`Number of cache blocks currently in use

`DirtyBlocks`Number of blocks modified but not yet written to backing store

`ReadHits`Number of read requests served from cache

`ReadMisses`Number of read requests that had to be fetched from backing store

`WriteHits`Number of write requests that hit existing cache blocks

`WriteMisses`Number of write requests that required new cache blocks

`Promotions`Number of blocks moved from backing store to cache

`Demotions`Number of blocks moved from cache to backing store

`CacheIOMBps`Current I/O bandwidth between cache and backing store (MB/s)

`BlockSize`Cache block size in bytes

`Mode`Cache mode (`writeback` or `writethrough`)

`Policy`Cache policy (`smq` or `mq`)

`Tunables`Current tunable parameters

`DirtyState`Current dirty block state (`low`, `optimal`, or `high`)

`AutoTune`Whether auto-tuning is enabled for this pool

`MinDirtyPercent`Minimum dirty block percentage threshold (for auto-tune)

`MaxDirtyPercent`Maximum dirty block percentage threshold (for auto-tune)

Alternatively, you can use `pxctl service pool show` command to view the cache status:

```

pxctl service pool show

```

```

Pool ID: 0

        Type:  Dmthin

        ...

        Cache Drives:

        0:0: /dev/sdd2, capacity of 8.4 GiB, Online

                Status:  Active

                TotalBlocks:  8564

                UsedBlocks:  34

                DirtyBlocks:  0

                ...

                DirtyState: low

                AutoTune: true

                MinDirtyPercent: 33

                MaxDirtyPercent: 67

```

The above output shows `Status: Active` and other storage pool caching properties value set. This confirms that storage pool cache is enabled and configured.

## Flush Storage Pool Cache​

To forcibly write dirty cache blocks to the backing storage pool, you need to flush the storage pool cache. This is required before disabling cache on a pool running in `writeback` mode. In `writethrough` mode, flushing of cache is not required.

Prerequisites

The pool must be online with no pending operations

info

This operation does not require pool maintenance mode. The pool can remain online.

-
To flush Cache, use the `pxctl service pool cache flush` command with pool id to flush the cache.

```

pxctl service pool cache flush <pool_id>

```

For example, to flush cache on pool `0`:

```

pxctl service pool cache flush 0

```

Immediate vs Background Flush

Depending on how many dirty blocks are in the cache, the operation executes and gives following outputs:

-
Few dirty blocks: Operation completes immediately

```

Pool 0 has completed flush successfully

```

-
Many dirty blocks: Operation runs in the background

```

Pool 0 flush cache initiated (has 12 dirty blocks)

```

-
Check Flush Status.

For background flush operations, check the status of progress with `status` option.

```

pxctl service pool cache flush <pool_id> -o status

```

For example, to check status of pool `0` :

```

pxctl service pool cache flush 0 -o status

```

```

Pool 0 has completed flush successfully

```

## Disable Pool Caching​

To disable caching on a storage pool without removing the cache drives:

Prerequisites

The pool must be online with no pending operations

info

This operation does not require pool maintenance mode. The pool can remain online.

-
Check current cache status.

Verify caching is enabled and check the cache mode of the storage pool.

```

pxctl service pool cache status <pool_id>

```

If cache is in `writeback` mode, flush storage pool cache before disabling cache.

-
To disable caching, use the `pxctl service pool cache disable` command with pool id to disable cache.

```

pxctl service pool cache disable <pool_id>

```

For example, to disable caching on pool `0`:

```

pxctl service pool cache disable 0

```

```

Pool 0 detached cache successfully

```

-
Verify caching is disabled.

```

pxctl service pool cache status 0

```

```

PX Cache Configuration and Status:

Pool ID:  0

        Enabled:  false

        Members:  [/dev/sdc]

        TotalBlocks: 0

        UsedBlocks: 0

        DirtyBlocks: 0

        ...

```

Caching is disabled if `Enabled: false` is visible in the output.

## Related Topics​

- Storage Pools

- Storage Pool Caching

- Optimize Cache Performance with Auto-Tune Cache Migration Threshold

In this topic:
