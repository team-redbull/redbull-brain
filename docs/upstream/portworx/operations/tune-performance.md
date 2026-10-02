# Tune performance

Source: https://docs.portworx.com/portworx-enterprise/operations/tune-performance (Portworx Enterprise 3.6)

Tune performance | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

In its default configuration, Portworx attempts to provide good performance across a wide range of situations. However, you can improve your storage performance in your environment by configuring a number of settings and leveraging features Portworx offers. To get the most out of Portworx, follow the guidance provided in this article.

## Configure the network data interface​

You can provide Portworx with a specific network interface for data when you generate the spec as part of your installation. Portworx by Everpure recommends a network interface with a bandwidth of at least 10Gb/s and network latency below 5 milliseconds. If multiple NICs are present on the host, provide a bonded interface to Portworx.

note

If you've already installed Portworx, you can update the `network.dataInterface` value of the install spec and reapply it.

### Configure multiple NICs with LACP NIC Bonding​

Portworx uses a single network interface for data traffic, which you define as the `network.dataInterface` in the StorageCluster spec. This interface handles all data traffic between Portworx nodes and applications. The interface can be either a single NIC or a bonded interface when multiple NICs are present on a node or host.

important

For optimal performance with bonded interfaces, ensure your Linux bonding configuration has the `xmit_hash_policy` set to `layer3+4`. The default value of `layer2` does not effectively distribute traffic across multiple links. Without this setting, traffic between two hosts only utilizes a single network link, even when multiple links are available in the bond. This setting is critical to achieve the full bandwidth benefits of LACP bonding with Portworx.

For more information about bonding configuration options, refer to the Linux bonding documentation.

In earlier releases, Portworx used a single connection over the interface, which caused all network threads to contend for the single connection. This contention restricts load distribution and prevents full utilization of available bandwidth. With LACP (Link Aggregation Control Protocol) NIC bonding support, Portworx now creates multiple parallel connections over the same interface, which significantly increases throughput by transmitting multiple data streams concurrently.

#### How to define a data network interface​

You can define the interface either during initial installation or by updating your existing storage cluster spec.
 Option 1: During installation​
When generating the specs using the Portworx Central UI, select the Customize option. Under the Network tab, you provide the network data interface as shown below.

Specify an interface name. If `auto` is specified, Portworx selects the first routable interface for management and network data interface.

 Option 2: Updating an existing StorageCluster​
On an already installed Portworx cluster, you can update the `network.dataInterface` value of the install spec and reapply it.

```

---

spec:

  network:

    dataInterface: eth0

---

```

#### Configure runtime option for parallel connections​

Portworx creates multiple connections on the single address (i.e. interface). The number is defined by the cluster runtime options parameter `net_connections`, by default the value is 4.

This parameter is useful:

- When your nodes have only one NIC, and you want to reduce network contention.

- When using bonded interfaces that expose only one logical NIC.

- Or when you're running I/O-intensive workloads that generate a high volume of storage traffic.

To update the number of connections, use the following command.

warning

Only tune this parameter under guidance from Portworx Support or when you’ve identified a performance bottleneck via monitoring tools.

```

pxctl cluster options update --runtime-options "net_connections=2"

```

Note that a restart is required after you edit this parameter for Portworx to reinitialize connections.

Retain the values previously defined in `--runtime-options` along with the above parameter. For more information, see Set runtime options.

## Configure FUSE driver thread count​

Starting with Portworx Enterprise version 3.5.0, you can configure the number of threads used by the FUSE driver by using the runtime option `percentage_num_fpthreads`. This option improves fast-path volume performance by adjusting thread count based on available CPU resources.

note

The `percentage_num_fpthreads` setting controls kernel threads created by the FUSE driver for fast-path volumes. These threads are not pinned to specific CPUs. By default, the FUSE driver creates these threads on all nodes in the cluster, even if fast-path volumes are not in use. If no fast-path volumes are present, the threads remain idle and do not affect system performance.

### Prerequisites​

Ensure that Portworx Enterprise version 3.5.0 or later is installed. If your cluster is running an earlier version, upgrade to 3.5.0 and update the px-fuse module:

- Backup the existing directory:

```

 cp -r /var/lib/osd/pxfs/latest /var/lib/osd/pxfs/latest_backup

```

- Move the existing px-fuse module:

```

mv -f /var/lib/osd/pxfs/latest /var/lib/osd/pxfs/latest_backup

```

- Reboot the node.
After the reboot, the node automatically pulls the latest px-fuse module compatible with the kernel.

note

In air-gapped environments, run the `pxfs-lib` update DaemonSet to ensure the latest kernel module archives are available on Portworx nodes.

### Configure thread count​

To update the number of threads used for fast-path I/O, run:

```

pxctl cluster options update --runtime-options percentage_num_fpthreads=<value>

```

Replace `<value>` with a number between 0 and 100.

Retain the values previously defined in `--runtime-options` along with the above parameter. For more information, see Set runtime options.

Alternatively, set the value in the `StorageCluster` specification:

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  name: portworx

  namespace: <px-namespace>

annotations:

  portworx.io/misc-args: "-rt_opts percentage_num_fpthreads=50”

```

### Verify thread count​

To verify the number of threads used for fast-path I/O, run:

```

cat /sys/devices/pxd/pxd_num_fpthreads

```

## Enable hyperconvergence​

Use Stork to ensure your Pod is running on the same node in which the data resides.

## Configure your cluster topology​

When configured to be aware of your cluster topology, Portworx places replicas for high availability. Configure your cluster topology.

## Define a VolumePlacementStrategy​

StatefulSets and distributed NoSQL databases, such as Cassandra, require PVCs to be distributed across the cluster. Use Affinity/Anti Affinity rules along with topology labels to define relationships between PVCs.Define a VolumePlacementStrategy using affinity and anti-affinity labels to distribute volumes.

## Adjust storage classes​

To improve performance, adjust storage class parameters in the following ways:

-
Prioritize volume traffic by setting the `priority_io:` field to `high`

-
Choose the replication factor best suited to your high availability needs

```

kind: StorageClass

apiVersion: storage.k8s.io/v1beta1

metadata:

 name: px-storage-class

provisioner: pxd.portworx.com

allowVolumeExpansion: true

parameters:

 repl: "2"

 priority_io: "high"

 nodiscard: "true"

```

## Modify Portworx resource consumption​

By default, Portworx consumes as little CPU and memory resources as possible. You can potentially improve performance by allocating more resources, allowing Portworx to use more CPU threads and memory. Do this by modifying the spec used to install Portworx based on your cluster architecture.

### Disaggregated architecture​

In disaggregated deployments with dedicated storage nodes, enable higher resource consumption by specifying the `rt_opts_conf_high` runtime option:

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  name: px-cluster

  namespace: <px-namespace>

spec:

  image: portworx/oci-monitor:3.1.6

  ...

  runtimeOptions:

    rt_opts_conf_high: "1"

```

### Hyperconverged architecture​

In a non-disaggregated/hyperconverged architecture, where applications are running on the same host as storage, set threads based on the number of cores that can be allocated to Portworx. For example, if your host has 16 cores:

- `num_threads=16` sets the total number of threads performing storage operations.

- `num_io_threads=12` sets the number of threads that can do IO operations out of the total `num_threads`. In general, IO threads should be 75% of total threads.

- `num_cpu_threads=16` sets the number threads that can do operations other than IO out of the total num_threads.

Configure these values as runtime options:

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  name: px-cluster

  namespace: <px-namespace>

spec:

  image: portworx/oci-monitor:3.1.6

  ...

  runtimeOptions:

    rt_opts_conf_high: "1"

    num_threads: "16"

    num_io_threads: "12"

    num_cpu_threads: "16"

```

To see more StorageCluster examples, visit the StorageCluster section of the documentation.

In this topic:
