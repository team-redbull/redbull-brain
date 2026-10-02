# Non-Blocking Device Delete

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/non-blocking-device-delete (Portworx Enterprise 3.6)

Non-Blocking Device Delete | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

The Non-Blocking Device Delete (NBDD) feature in Portworx Enterprise improves the efficiency of volume and snapshot deletions by running background discards at a configurable rate when you delete large snapshots or storage volumes from Portworx clusters. NBDD reduces I/O latency when you delete a volume or snapshot, and helps reclaim space, especially on SAN or FlashArray (FA) storage backends.

note

NBDD is only supported on clusters with the PX-StoreV2 datastore.

NBDD has the following capabilities:

-
Reduced latency during deletion: NBDD minimizes I/O pauses during volume and snapshot deletions by performing background discard operations at a configurable rate before issuing the actual delete. This significantly reduces latency and minimizes the impact on active I/O during deletions.

-
Reclaim space on SAN or FA backends: Reclaims deleted volume space on SAN/FA backends, making it available for other nodes in the cluster.

-
Support for Large Deletion Use Cases: Ideal for managing deletion of large volumes or frequent snapshot chains without I/O disruption.

-
Configurable discard rate: You can configure the discard throughput to balance between latency reduction and backend space reclamation needs.

Recommended discard rate

The default discard rate is 1 GBps, which is suitable for most environments. At this rate, deleting a 1 TiB volume takes approximately 15 minutes (1,000 seconds).

Portworx by Everpure recommends setting `device_delete_max_concurrent` to `1` to maintain a low discard rate. A higher discard rate can increase latency on active volumes, while a lower rate can delay space reclamation. Choose a discard rate that balances space reclamation time with workload performance.

For information about configuring the discard rate, see Configure discard throughput rate.

You are required to set values of two parameters:

- `device_delete_after_discard`: Controls discard rate for large snapshot or storage volume deleted.

- `device_delete_max_concurrent`: Controls the number of parallel volume deletes per pool by NBDD. Ranges from 1 to 5 with default set to 3.

Retain the values previously defined in `--runtime-options` along with the above parameters. For more information, see Set runtime options.

#### Limitations​

- If Portworx restarts or a storage pool becomes unavailable, for example, because of a node reboot or pool failure, pending volume deletions are not processed through NBDD. As a result, their capacity is not reclaimed on the underlying FlashArray or SAN storage. After Portworx returns online, subsequent volume deletions are processed through NBDD and issue discard requests for space reclamation, if NBDD is enabled.

- NBDD reclaims space only for volumes and snapshots deleted after you enable it. To reclaim unused capacity from volumes and snapshots deleted before NBDD was enabled, run a pool trim operation. For more information, see Reclaim Unused Storage with Pool Trim.

## Enabling NBDD​

You can enable NBDD by using runtime options configured through `pxctl` or in the `StorageCluster` specification.

- pxctl

- StorageCluster

```

pxctl cluster options update --runtime-options "device_delete_after_discard=1,device_delete_max_concurrent=1"

```

Retain the values previously defined in `--runtime-options` along with the above parameters. For more information, see Set runtime options.

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  name: portworx

  namespace: <px-namespace>

spec:

  image: portworx/oci-monitor:3.5

  runtimeOptions:

    device_delete_after_discard: 1

    device_delete_max_concurrent: 1

```

## Disabling NBDD​

- pxctl

- StorageCluster

```

pxctl cluster options update --runtime-options "device_delete_after_discard=0,device_delete_max_concurrent=0"

```

```

   apiVersion: core.libopenstorage.org/v1

   kind: StorageCluster

   metadata:

    name: portworx

    namespace: <px-namespace>

   spec:

    image: portworx/oci-monitor:3.5

    runtimeOptions:

    device_delete_after_discard: 0

    device_delete_max_concurrent: 0

```

## Best Practice: Estimating and Configuring Delete Rate per Pool​

To ensure that there are no pending deletes accumulating on a pool, you must calculate the optimal rate at which the system can perform deletions and configure the discard rate limit accordingly.

To calculate the optimal rate and configure the discard rate limit, perform the following steps:

-
Identify the maximum delete rate supported by the system:

```

pxctl cluster options update --runtime-options "device_delete_after_discard=1,device_delete_discard_ratelimit_bytes=<value_in_bytes>"

```

-
Use Prometheus metrics to measure the average discard throughput:

```

px_device_delete_discard_bytes_total

```

For example, if the observed discard rate is 7 GBps, then:

- In one hour: 7 GBps × 60 s × 60 min = 25,200 GiB (≈ 24.6 TiB)

- In 30 minutes: 12.3 TiB of data can be discarded.

-
Estimate the discard capacity for the default discard rate.
 For example, with the `default device_delete_discard_ratelimit_bytes` set to 1 GBps, the system can discard up to:

```

1 GBps × 60 s × 30 min = 1.7578125 TiB

```

This means:

- if the total deletes (snapshots or volumes) within 30 minutes are ≤ 1.7578125 TiB, the system can keep up with deletions and no pending discards will accumulate.

- If delete volume exceeds this threshold, increase the discard rate limit accordingly.

-
Ensure that the discard rate limit must always be greater than the rate at which snapshots and volumes are deleted. For example, the rate of deletes must stay below 1.7578125 TiB per 30 minutes for a default rate limit, or you can tune the limit higher (e.g., 12.3 TiB per 30 minutes) to accommodate faster delete workloads.

## Configure discard chunk size​

To set the size of each discard chunk used during volume or snapshot deletes, run the following command:

```

pxctl cluster options update --runtime-options "device_delete_discard_size_bytes=<value_in_bytes>"

```

For example, to set the discard size to 1 MiB:

```

pxctl cluster options update --runtime-options "device_delete_discard_size_bytes=1048576"

```

note

The minimum value must be 1 MiB (1,048,576 bytes) and the maximum value must be 1 GiB (1,073,741,824 bytes). The configured value must be less than or equal to one-tenth of the discard rate limit specified in Configure discard throughput rate.

## Configure discard throughput rate​

To change the throughput limit for discard operations during volume or snapshot deletes (per pool), use the following command:

```

pxctl cluster options update --runtime-options "device_delete_discard_ratelimit_bytes=<value_in_bytes>"

```

For example, to set the discard rate limit to 100 MiB:

```

pxctl cluster options update --runtime-options "device_delete_discard_ratelimit_bytes=104857600"

```

note

The minimum value must be 50 MiB (52,428,800 bytes). There is no maximum value.

## NBDD metrics and monitoring​

After you enable NBDD, Portworx displays custom metrics in your Prometheus. These metrics allow you to monitor and calculate discard IOPS and throughput for each storage pool. For more information on available NBDD metrics, see device_delete stats in Portworx Metrics documentation.

In this topic:
