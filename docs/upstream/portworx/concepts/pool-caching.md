# Storage Pool Caching

Source: https://docs.portworx.com/portworx-enterprise/concepts/pool-caching (Portworx Enterprise latest)

Storage Pool Caching | Portworx Enterprise Documentation

PX-Cache improves storage pool performance by building a small caching layer with higher-performance drives over individual Portworx storage pools. This tiered storage approach uses fast drives (SSD or NVMe) as a cache tier to accelerate I/O operations for slower storage pools, improving both latency and IOPS.

## Key Concepts​

- Tiered Architecture: PX-Cache requires two classes of drives - a small capacity of high-performance drives for caching (local to the node) and larger capacity drives for the storage pool

- Cache Capacity: For optimal results, cache drive capacity should be 10-20% of the storage pool capacity. Larger cache sizes may not provide proportionally better performance

- Burst Absorption: Caching is designed to absorb I/O bursts by offloading the storage pool. Workloads requiring sustained I/O bandwidth may see performance degradation if the cache is constantly full

## Deployment Requirements​

-
PX-Cache is only supported with on-premises deployments, and not supported with Cloud deployments.

-
For on-prem deployments, if your storage pool drives are connected via SAN, the cache drive must be local to the node and capable of higher performance than the SAN drives for caching to be effective.

## Drive Type Requirements​

The cache drive performance must be higher than the backing storage pool drives:

Storage Pool TypeSupported Cache DrivesNotes

HDD (Magnetic)SSD or NVMePX-StoreV2 does not support HDD pools

SSDNVMe onlyCache must be faster than pool drives

NVMeNot supportedNo performance benefit from caching

## PX-Store Version Differences​

VersionPX-Cache Support

PX-StoreV2Natively supports PX-Cache. No special installation configuration required.

PX-StoreV1Requires at least one cache drive to be configured at installation time using the `-cache` option. You must enable pool caching at installation time for PX-StoreV1 by providing at least one cache drive. Migration from non-cached to cached configuration is not supported for PX-StoreV1.

## Install Portworx with Caching Enabled for PX-StoreV1​

### Prerequisites​

Before you can enable pool caching, you must meet the following prerequisites:

- An NVMe or SSD drive attached to the same node as your storage pool (with higher performance than pool drives)

- Linux kernel 4.20.13 or later

- The following packages must be installed on your node:

- `thin-provisioning-tools`

- `device mapper`

- `lvm2`

- `mdadm`

For PX-StoreV1, you must enable caching when you first install Portworx by running `px-runc` with the `-cache` option:

```

px-runc install -name portworx \

  -c doc-cluster-caching \

  -k etcd:http://127.0.0.1:4001 \

  -s /dev/sdf \

  -cache /dev/sdc \

  -v /mnt:/mnt:shared

```

note

Do not provide the same storage device as both a cache and a data storage device. If you run `px-runc` with the `-A` argument, Portworx forms storage pools on all unmounted drives except for drives specified using the `-cache` argument.

## Migration threshold​

The `migration_threshold` parameter controls how aggressively data migrates between cache and origin:

- Represents the number of 512-byte sectors allowed to migrate at any time

- Default is automatically computed based on cache capacity (100× the cache block size)

- For a 1MB block size, default is 100MB = 204800 sectors

You can either manually tune `migration_threshold` by configuring storage pool caching or consider using the auto-tune cache migration threshold feature which automatically adjusts its value based on cache utilization.

## Auto-tune storage pool cache​

Portworx can automatically adjust the cache migration threshold based on cache utilization. This feature monitors the percentage of dirty blocks in the cache and adjusts the migration settings to optimize cache performance.

When running cache in `writeback` mode, dirty blocks (modified data not yet written to backing storage) accumulate in the cache. If too many dirty blocks accumulate, cache performance degrades. If they are too few, you're not fully utilizing the cache's performance benefits.

The auto-tune feature monitors dirty block percentage and automatically adjusts:

- Migration threshold: How aggressively data migrates between cache and backing storage

- Cache policy: Temporarily switches to "cleaner" mode when cache is too full

### How auto-tune storage pool cache works​

Auto-tune monitors the dirty block percentage and takes action based on three states:

#### DirtyState: Low (< min_dirty%)​

When dirty blocks are below the minimum threshold:

- Cache is underutilized

- Original cache settings are restored

- No special action needed

#### DirtyState: Optimal (between min_dirty% and max_dirty%)​

When dirty blocks are within the optimal range:

- Cache is performing well

- Policy is set to default (`smq`)

- No intervention needed

#### DirtyState: High (> max_dirty%)​

When dirty blocks exceed the maximum threshold:

- Cache is filling up with dirty data

- Migration threshold is increased to maximum to flush faster

- Policy is temporarily switched to `cleaner` mode

- Once dirty blocks return to optimal range, settings are restored

## Related topics​

- Storage pools

- Configure storage pool cache

- Troubleshooting storage pool cache configuration

In this topic:
