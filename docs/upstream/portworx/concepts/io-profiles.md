# IO profiles

Source: https://docs.portworx.com/portworx-enterprise/concepts/io-profiles (Portworx Enterprise latest)

IO profiles | Portworx Enterprise Documentation

You can optimize the performance of your Portworx volumes by matching the type of workload you're running with a suitable IO profile. IO profiles change how a Portworx volume interacts with the underlying storage disks to improve traffic for different workloads. If you don't provide an IO profile, Portworx will use the IO profile specified by the `default-io-profile` setting in the cluster. During Portworx spec generation, the `default-io-profile` option in the StorageCluster spec is set to `auto` by default. To change the default IO profile after installing Portworx, see the Change the default IO profile using pxctl section.

## Understand the different IO profiles​

The following are various IO profiles you can configure using the `default-io-profile` option:

- `auto`

- `db_remote`

- `journal`

- `none`

- `use_cluster_default`

### The `auto` profile​

This profile dynamically selects the optimal IO profile based on volume configuration, switching between `none` and `db_remote` for efficient IO handling. Portworx selects `db_remote` when a volume's replication factor is 2 or more; otherwise, it defaults to `none`. For single-replica (`repl 1`) volumes, `auto` applies internal optimizations to enhance performance without requiring manual adjustments.

### The `db_remote` profile​

This profile utilizes a write-back flush coalescing algorithm, reducing the number of sync operations by consolidating multiple `syncs` within a 100 ms window into a single operation. The coalesced syncs are acknowledged only after being copied to memory across all replicas, improving performance for highly available (HA) volumes. It is designed for `repl 2+` volumes, effectively managing sync rates through periodic flushes.

note

- If there are not enough nodes online, Portworx will automatically disable this algorithm.

- The `db_remote` profile only applies if you have a repl count of 2 or more.

### The `journal` profile​

note

To configure this profile for a volume, it is required to have a specific journal device or a dedicated partition allocated on the node. Follow the instructions on the Add a dedicated journal device to a node page to set up a journal device.

The `journal` IO profile ensures stable writes to a dedicated journal, batching commit operations to the backing pool. This reduces the overhead associated with frequent sync operations, making it ideal for database-class applications with high sync IO rates. It is particularly beneficial for single-replica (`repl 1`) volumes, efficiently handling high sync IO workloads by journaling both data and metadata.

### The `none` profile​

This profile disables all IO profile optimizations, processing all IO requests as they arrive without additional modifications. It is useful for workloads that do not require specialized IO handling.

### The `use_cluster_default` profile​

This profile allows the cluster-wide default setting to determine IO behavior, ensuring flexibility and consistency across multiple volumes. By default, the cluster is set to `auto`, but this setting can be overridden based on workload requirements.

### Deprecated IO profiles​

The following profiles are deprecated in the newer versions of Portworx.

#### The db profile​

Databases typically result in a large number of flush operations on the disk. Because a flush forces Portworx to wait until the data is synched on the disk, it can slow down traffic. When the `db` profile is active, Portworx batches flush operations for a quicker write response time.

note

Legacy volumes will still show up as having db profile but internally they will be treated as auto profile volumes.

#### The sequential profile​

This profile optimizes the read-ahead algorithm for sequential workloads, such as backup operations.

note

Legacy volumes will still show up as having sequential profile but internally they will be treated as auto profile volumes.

#### The `auto_journal` profile​

The `auto_journal` profile continuously monitors incoming IO patterns and dynamically determines whether enabling the `journal` profile can improve performance. It evaluates write IO patterns over a 24-second window and automatically switches between the `none` and `journal` profiles based on detected workload behavior.

note

Legacy volumes will still show up as having the `auto_journal` profile. Use the `journal` or `auto` profile for new volumes.

## Configure profiles​

You can configure IO profiles through Kubernetes specs or at the Portworx level, depending on your needs and what operator you're running with.

For information about how to configure IO profiles for volumes on Kubernetes clusters either manually or using `pxctl`, follow this link:
 Configure IO profiles for Portworx volumes on Kubernetes

## Related topics​

- Performance optimization options in the IO path

In this topic:
