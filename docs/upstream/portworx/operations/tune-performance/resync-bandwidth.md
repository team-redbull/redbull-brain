# Dynamic Resync Bandwidth Control

Source: https://docs.portworx.com/portworx-enterprise/operations/tune-performance/resync-bandwidth (Portworx Enterprise latest)

Dynamic Resync Bandwidth Control | Portworx Enterprise Documentation

Portworx Enterprise allows you to control the maximum bandwidth used for resync and replica-add (repl-add) operations to prevent resync traffic from affecting application I/O. Use this option when application and resync traffic share the same node and you need to limit resync bandwidth.

Portworx Enterprise dynamically adjusts the resync rate based on application load while ensuring that resync traffic never exceeds the user-configured maximum bandwidth. When application I/O is low, resync operations use more available resources, but Portworx Enterprise ensures that resync bandwidth never exceeds the user-configured maximum. If application traffic increases, Portworx continues to enforce the configured limit and keeps resync traffic below the specified threshold. Portworx Enterprise continuously monitors transfer behavior to balance application performance and resync completion time.

The runtime option used to control resync and repl-add bandwidth is `max_resync_bandwidth_mbps`. The default value is 1024 Mbps. The minimum supported value is 50 Mbps. There is no enforced upper limit. The bandwidth value is specified in Mbps.

Portworx Enterprise dynamically adjusts resync traffic based on application load:

- Application I/O always takes priority over resync I/O.

- The configured value ensures that resync traffic does not exceed the specified maximum bandwidth.

- The configured value specifies the maximum bandwidth reserved for resync traffic. Resync operations can use bandwidth up to this limit, but it does not guarantee that resync traffic runs at this rate continuously.

## Prerequisites​

Ensure that your cluster meets the following prerequisites before you configure maximum resync bandwidth:

- Have Portworx Enterprise version 3.6.0 or later installed.

## Limitations​

Consider the following limitations before you set resync bandwidth:

- Applies only to resync and repl-add traffic.

- The configured setting applies to the node and there is no per-volume rate control.

- The configured setting limits maximum bandwidth but does not guarantee throughput.

## Configure maximum resync bandwidth​

Portworx Enterprise provides multiple methods to configure maximum resync bandwidth.

### Using StorageCluster spec during Portworx installation​

Pass the following annotations to the StorageCluster spec manually and set the value based on the requirement of parameters. There are two options to add the annotations:

-
Option 1: `portworx.io/misc-args: -rt_opts max_resync_bandwidth_mbps=<bandwidth-value>`
Replace `<bandwidth-value>` with the maximum bandwidth limit for resync traffic.

-
Option 2:

```

runtimeOptions:

max_resync_bandwidth_mbps=<bandwidth-value>

```

Replace `<bandwidth-value>` with the maximum bandwidth limit (in Mbps) for resync traffic.

### Using pxctl cluster runtime options post Portworx installation​

Maximum resync bandwidth configuration options are runtime-configurable using cluster settings:

```

pxctl cluster options update --runtime-options max_resync_bandwidth_mbps=<bandwidth-value>

```

Replace `<bandwidth-value>` with the maximum bandwidth limit (in Mbps) for resync traffic.

The following is an example:

```

pxctl cluster options update --runtime-options max_resync_bandwidth_mbps=850

```

Retain the values previously defined in `--runtime-options` along with the above parameter. For more information, see Set runtime options.

In this topic:
