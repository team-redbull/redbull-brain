# Storage configuration and performance

Source: https://docs.portworx.com/portworx-enterprise/deploy-your-applications/application-install-with-kubernetes/postgresql/storage-configuration (Portworx Enterprise 3.6)

Storage configuration and performance | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## Choosing storage classes​

Different database workloads have unique storage demands. Portworx StorageClasses let you define replication factors, I/O priorities, and volume parameters to meet your business SLAs.

Key benefits

- Optimized performance: Control replication factor (`repl`) and `io_priority`.

- Easy provisioning: Dynamically provision volumes for new PostgreSQL instances.

- Customizable policies: Fine-tune parameters for various environment needs, such as development, testing, and production.

Example StorageClass configuration

```

apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:

  name: px-postgres-sc

provisioner: pxd.portworx.com

parameters:

  repl: "2"

  io_priority: "high"

allowVolumeExpansion: true

```

where:

- `repl=2`: Offers high availability with minimal write overhead.

- `allowVolumeExpansion=true`: Enables online resizing without downtime.

## Further configuration​

- `aggregation_level`: Stripes data for higher throughput.

- `snap_interval`: Sets snapshot intervals if using Portworx periodic snapshots.

- `encryption`: Encrypts volumes for enhanced security.

## Replication​

PostgreSQL commonly uses a primary-standby model for application-level replication. In parallel, Portworx provides storage-level replication (using the repl parameter) to protect against hardware or node failures.

- Combining PostgreSQL standbys with Portworx replicas: Consider both the number of PostgreSQL secondaries and the Portworx volume replica count to achieve the desired redundancy.

- Recommended baseline: A storage replication factor of 2 is often sufficient for most workloads.

- PX-Fast Volumes (`repl=1`): If your application-level replication is robust, you can use PX-Fast volumes with repl=1 for optimal performance—assuming environment-specific prerequisites are met.

For more information, refer to:

- Portworx StorageClass parameters

- Portworx volume encryption

## Adaptive storage scaling​

Proactive capacity planning is essential to avoid running out of storage at critical moments. By anticipating data growth, replication overhead, and backup requirements, you ensure that your PostgreSQL cluster can scale smoothly without sacrificing performance or availability. This approach not only prevents service disruptions but also helps manage costs by striking the right balance between allocation and utilization.

Considerations

- Initial data size + Growth rate

- Replication overhead (for example, `RF=2` or `RF=3`)

- Backup retention (local snapshots, offsite backups)

Benefits

- Predictable scaling: Size your cluster for current and future needs.

- Optimized costs: Prevent overprovisioning while avoiding shortages.

- Seamless growth: Dynamically expand volumes as needed.

## Performance budget and planning​

When running production databases, speed and reliability often define the user experience. By focusing on an effective performance budget and plan such as tuning for low latency, optimizing throughput, and leveraging the right replication strategies, you can maintain consistent response times even under heavy loads. This ensures your PostgreSQL deployment remains agile enough to meet changing demands while delivering the high performance that modern applications and customers expect.

Key benefits

- Low latency: Hyperconvergence places data near PostgreSQL pods.

- High throughput: I/O priority and volume striping for intensive workloads.

- Scalable performance: Add more nodes or disks without disruption.

Recommended best practices

- Use SSD/NVMe for production databases.

- Carefully configure the replication factor (more replicas = higher write overhead).

- Benchmark with pgBench, fio, or Portworx FIO to validate performance.

In this topic:
