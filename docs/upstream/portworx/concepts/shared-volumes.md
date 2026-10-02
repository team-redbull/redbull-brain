# Sharedv4 Volumes

Source: https://docs.portworx.com/portworx-enterprise/concepts/shared-volumes (Portworx Enterprise 3.6)

Sharedv4 Volumes | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Through sharedv4 volumes (also known as a global namespace), a single volume’s filesystem is concurrently available to multiple containers running on multiple hosts.

note

- There is no inherent limit imposed by Portworx on the number of pods that can be attached to a sharedv4 service-based volume. However, the actual limit is dependent on factors such as cluster size and available resources. Pod scaling may also be constrained by the maximum number of pods allowed per node, as dictated by Kubernetes. It is important to monitor and optimize cluster resources to ensure stable performance at higher pod counts.

- Portworx does not support Kerberos with sharedv4 volumes.

- You do not need to use sharedv4 volumes to have your data accessible on any host in the cluster. Any Portworx volumes can be exclusively accessed from any host as long as they are not simultaneously accessed. Sharedv4 volumes are for providing simultaneous (concurrent or shared) access to a volume from multiple hosts at the same time.

- You do not necessarily need a replication factor of greater than 1 on your volume in order for it to be shared. Even a volume with a replication factor of 1 can be shared on as many nodes as there are in your cluster.

- IOPS might be misleading when using sharedv4 volumes due to batching of small blocksize I/Os into a larger one before I/O reaches the `pxd` device. Bandwidth is more consistent.

- When multiple pods on the same node mount the same Sharedv4 (NFS) volume, Portworx traditionally performs a separate NFS mount for each pod. This can lead to several issues, including redundant NFS connections, an increased number of mount table entries, higher kernel overhead, and more complex unmount operations. To address these limitations, Portworx uses sentinel mounts which creates a single, shared NFS mount per volume per node. For more information, see Configure sentinel mount cleanup interval and timeout.

A typical pattern is for a single container to have one or more volumes. Conversely, many scenarios would benefit from multiple containers being able to access the same volume, possibly from different hosts. Accordingly, the shared volume feature enables a single volume to be read/write accessible by multiple containers. Example use cases include:

- A technical computing workload sourcing its input and writing its output to a sharedv4 volume.

- Scaling a number of Wordpress containers based on load while managing a single sharedv4 volume.

- Collecting logs to a central location.

note

Usage of sharedv4 volumes for databases is not recommended because they have a small metadata overhead. Additionally, typical databases do not support concurrent writes to the underlying database at the same time.

## Sharedv4 failover and failover strategy​

When the node which is exporting the sharedv4 or sharedv4 service volume becomes unavailable, there is a sharedv4 failover. After failover, the volume is exported from another node which has a replica of the volume.

Failover is handled slightly differently for sharedv4 volumes than for sharedv4 service volumes:

- When a sharedv4 volume fails over, all of the application pods are restarted.

- For sharedv4 service volumes, only a subset of the pods need to be restarted. These are the pods that were running on the 2 nodes involved in failover: the node that became unavailable, and the node that started exporting the replica of the volume. The pods running on the other nodes do not need to be restarted.

The failover strategy determines how quickly the failover will start after detecting that the node exporting the volume has become unavailable. The `normal` strategy waits for a longer duration than the `aggressive` strategy.

### Sharedv4 volumes​

The default failover strategy for sharedv4 volumes is `normal`. This gives the unavailable node more time to come back up after a transient issue. If the node comes back up during the grace period allowed by the `normal` failover strategy, there is no need to restart the application pods.

If an application with a sharedv4 volume is able to recover quickly after a restart, it may be more appropriate to use the `aggressive` failover strategy even for a sharedv4 volume.

### Sharedv4 service volumes​

A sharedv4 service volume is mounted through a Kubernetes service (ClusterIP) rather than through the address of a specific node. The ClusterIP is a stable front end: Portworx maps it to the data IP of the node that is currently exporting the volume. Because the ClusterIP itself does not change when the export moves to a different node, application pods keep their mounts across a failover.

This seamless failover depends on NFS version 4.0, which is the default protocol version for sharedv4 service volumes. NFS 4.1 and 4.2 clients consolidate connections to the same server: if two sharedv4 service volumes have two different ClusterIPs that currently resolve to the data IP of the same exporting node, a 4.1 or 4.2 client collapses both mounts into a single connection to that one server. NFS 4.0 does not apply this optimization; it resolves each ClusterIP independently.

That consolidation breaks during a failover. If the exporting node becomes unavailable and the two volumes fail over to two different nodes, their ClusterIPs must now resolve to two different data IPs, but the client is still using the single consolidated connection. For this reason, seamless failover is not possible over NFS 4.1 or 4.2.

The default failover strategy for sharedv4 service volumes is `aggressive`, because these volumes are able to fail over without restarting all the application pods.

These defaults can be changed in the following ways:

-
Setting a value for `sharedv4_failover_strategy` in StorageClass before provisioning a volume.

-
Using a `pxctl volume update` command if a volume has been provisioned already. For example:

```

pxctl volume update --sharedv4_failover_strategy=normal <volume_ID>

```

### Sharedv4 service volume hyperconvergence​

When you set the `stork.libopenstorage.org/preferRemoteNode` parameter in the StorageClass as `false`, Stork will deactivate anti-hyperconvergence for sharedv4 service volumes generated with this StorageClass, and the value of the `stork.libopenstorage.org/preferRemoteNodeOnly` parameter will be ignored.

note

- The `stork.libopenstorage.org/preferRemoteNode` parameter is supported from the Stork 23.11.0 and newer versions, and the default setting for this parameter is `true`.

- If you want to update the `stork.libopenstorage.org/preferRemoteNode` parameter after creating sharedv4 PVCs, you can update the volume labels using `pxctl volume update --label` command.

### Sharedv4 service pod anti-hyperconvergence​

If you want to prevent pods from needing to bounce upon NFS server failover for `sharedv4` service volumes, you would have to use NFS mountpoints on nodes instead of having pods running on the node with the volume attached as a direct bind mount.

By default, the Stork scheduler places application pods on nodes where `sharedv4` volume replicas do not exist, if such nodes are available. This configuration is known as anti-hyperconvergence, meaning that pods are positioned on different nodes from their volume replicas. In other words, this can be described as the pods using `sharedv4` volumes being anti-hyperconverged with respect to their volume replicas.

note

- You can force a pod using sharedV4 service volumes to be scheduled only on non replica nodes by specifying `stork.libopenstorage.org/preferRemoteNodeOnly: "true"` as a StorageClass parameter. This parameter will strictly enforce this behavior, and application pods will not come up if a valid node is not found.

- If you want to update the `stork.libopenstorage.org/preferRemoteNodeOnly` parameter after creating sharedv4 PVCs, you can update the volume labels using `pxctl volume update --label` command.

In this topic:
