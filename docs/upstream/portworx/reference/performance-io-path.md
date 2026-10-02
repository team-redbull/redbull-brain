# Portworx performance optimization options in the IO path

Source: https://docs.portworx.com/portworx-enterprise/reference/performance-io-path (Portworx Enterprise latest)

Portworx performance optimization options in the IO path | Portworx Enterprise Documentation

Portworx provides the following configurable features to ensure data integrity on the entire I/O path. They are designed to protect against memory corruption, corruption over the network, and bit rot.

### In-memory checksum​

Portworx maintains a per block checksum of all data blocks coming into and going out of the system:

- For write requests, checksums are computed as soon as data arrives in the storage process.

- For read requests, checksums are computed as soon as data is read from the local pool.

- For remote reads, both data and checksums are sent over the wire to the remote node.

Checksum verification takes place before the data is written to stable media or returned to the application.

This feature is turned On by default. It protects against in-memory corruption as well as corruption over the network.

### On-disk checksum and repair on read operations​

This feature detects media errors (bit rot and bad blocks). Portworx uses a copy-on-write filesystem on the backing storage pool which stores the virtual volumes. All writes arriving at the pool are checksummed and are stored separate from data blocks. In the read path, the data is read along with checksums. If the checksum mismatches, it is treated as an IO error from the pool and a recovery mechanism is triggered. In this case, Portworx reads the block from a good replica when possible, and writes it to the bad replica.

note

The checksum feature is not supported with PX-StoreV2 datastore.

While the space overhead is very small (~0.1%), there is a performance overhead to this option. Checksum needs copy-on-write to be enabled, which has the following implications:

- All writes are treated as new writes. Filesystem has to take the entire block allocation path which can be avoided for in-place overwrites.

- All blocks directly or indirectly involved in a write get modified (direct data blocks, indirect data blocks, metadata blocks). The extra modification causes high write amplification and fragmentation.

- Additional background work is required to maintain block reference counting because each write goes through allocate new block and free old block processing.

Although it depends on the workload (small block versus large block, random versus sequential, sync versus async), around 20-30% overhead is expected in a general purpose use-case.

This feature is Off by default. For information on how to implement this feature, see Understand copy-on-write feature.

### IO Profiles​

Portworx volumes can be configured with IO profiles based on the data workload. Database workloads typically have small block sizes with frequent syncs. The software supports `io_profiles` for such IO patterns. Portworx implements synchronous replication for HA. All writes are synchronously mirrored across all replicas. The replica placement is failure domain aware. Replicas are placed across failure domains (Rack, DC, AZ) when possible.

- The `db_remote io_profile` implements a write-back flush coalescing algorithm that attempts to coalesce multiple syncs that occur within a 100 ms window into a single sync. Coalesced syncs are acknowledged only after being copied to memory on all replicas. In order to do this, this algorithm requires a minimum replication (HA factor) of 2 preferably with replicas spread across availability zones. This mode assumes all replicas do not fail simultaneously in a 100 ms window.

- The `auto` profile enables this feature by default as long as there are at least 2 healthy replicas. The behavior can be disabled per volume by using the `--io_profile=none` volume update flag or by using the `--default-io-profile=none` cluster update flag for all volumes, cluster-wide. The `journal io_profile` does stable writes to the journal and commits writes in batches to the backing pool, amortizing the cost associated with syncs at the small block sizes associated with a database payload. This assumes that the journal has higher performance than the backing pool.

### Tune volume performance with pxctl​

Portworx optimizes performance for specific application access patterns using IO profiles. You can set these IO profiles by providing the `io_profile` option while creating the volume. For example:

```

pxctl volume create --size=10 --repl=3 --io_profile=journal demovolume

```

This command will assign `journal` io_profile to the `demovolume` volume.

#### Change the default IO profile using pxctl​

You can change the default IO profile for volumes created without the `io_profile` annotation using the cluster option `--default-io-profile`. For example, using the following command will assign the `none` IO profile to any volumes created within the cluster that do not have the `io_profile` StorageClass annotation:

```

pxctl cluster options update --default-io-profile none

```

For information on how to apply these IO profiles, see:

- Configure IO profiles for Portworx volumes on Kubernetes

In this topic:
