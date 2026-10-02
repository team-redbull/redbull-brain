# Storage pools

Source: https://docs.portworx.com/portworx-enterprise/concepts/storage-pools (Portworx Enterprise latest)

Storage pools | Portworx Enterprise Documentation

A storage pool is a logical grouping of a node's physical drives. Portworx uses the space in a storage pool to dynamically create virtual volumes on containers.

## Storage pool composition​

Storage pools consist of a collection of drives with the same capacity and type. When you create a pool, Portworx categorizes it based on its latency and performance in random and sequential IOPS.

When a drive is allocated to Portworx, a benchmark process evaluates its performance. Based on the drive's throughput and throughput thresholds, it is categorized into one of three IO priorities: low, medium, or high.

Drives that share the same IO priority and size within the same node are grouped together into a pool. The assigned IO priority can be used in the StorageClass to align various applications with the appropriate tier of storage based on their performance requirements. For example, database applications can be placed on SSDs, and applications that manage logging data can be placed on traditional spinning disks. For more precise control over the placement of Portworx volumes, use the Volume Placement Strategies.

## Interact with storage pools​

You can form and manage storage pools using the `pxctl` command-line utility. You can also assign them labels, which allow you to specify them in provisioning rules you write. A storage pool's performance category is one such label.

You can form a maximum of 32 storage pools on a single node. You may also have nodes with no storage at all in your cluster; nodes with no storage are storageless.

You can monitor your storage pools using Prometheus or the `pxctl` command-line utility. The Alerts using pxctl page provides details about monitoring the status of your cluster with the `pxctl` command-line utility.

## Related topics​

- Storage pool caching

- Considerations for PX-StoreV2 pools

- Provision storage pool

In this topic:
