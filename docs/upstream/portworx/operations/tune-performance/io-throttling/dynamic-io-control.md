# Dynamic App I/O Control with Autopilot

Source: https://docs.portworx.com/portworx-enterprise/operations/tune-performance/io-throttling/dynamic-io-control (Portworx Enterprise 3.6)

Dynamic App I/O Control with Autopilot | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx with Autopilot enables dynamic updates to the I/O throttle limits, when the volume size changes. You can dynamically configure the throttling limits for IOPS and Bandwidth by providing scaling factors and a range for the throttle limits (floor and ceiling limit) in the `StorageClass`.

When the volume size changes, then depending on the scaling factor provided, the IOPS and bandwidth raw throttle limits also change. The throttle limits for IOPS and Bandwidth are dynamically set, only if it lies within the range of the throttle limits.

Based on whether you want to configure dynamic application I/O control for Portworx volume or FlashArray Direct Access volume, complete all the steps in one of the section:

- Configure Dynamic App I/O Control for Portworx Volume

- Configure Dynamic App I/O Control for FADA Volume

You can also Disable Dynamic I/O Throttle for StorageClass and PVCs if you do not want it to inherit the throttling configurations.

## Prerequisites​

- Portworx Enterprise 3.5.0 or later is running on your cluster.

- Autopilot version 1.4.0 or later is enabled on your Portworx cluster.

## Configure Dynamic App I/O Control for Portworx Volume​

To configure Dynamic App I/O Control, provide the following parameters for Portworx volumes in the `StorageClass`:

- `io_throttle_iops_scale_factor`: IOPS throttling scaling factor, interpreted as IOPS per GiB of volume.

- `io_throttle_bw_scale_factor`: Bandwidth throttling scaling factor that ranges between 0 and 1, interpreted as GiB/s per GiB of volume.

- `io_throttle_min_iops`: minimum IOPS throttle (floor value)

- `io_throttle_rd_iops`: maximum read IOPS throttle (ceiling value)

- `io_throttle_wr_iops`: maximum write IOPS throttle (ceiling value)

- `io_throttle_min_bw`: minimum bandwidth throttle (floor value) - MegaBytes/s

- `io_throttle_rd_bw`: maximum read bandwidth throttle (ceiling value) - MegaBytes/s

- `io_throttle_wr_bw`: maximum write bandwidth throttle (ceiling value) - MegaBytes/s

The scaling factor parameters `io_throttle_iops_scale_factor` and `io_throttle_bw_scale_factor` that you set in the `StorageClass`, and the volume size detected by Autopilot, will determine the IOPS and bandwidth raw throttle values for the Portworx volumes.

For example, if `S_GiB` is volume size in GiB, the `IOPS_throttle_raw` and `BW_throttle_raw` value is determined in the following way:

```

IOPS_throttle_raw = S_GiB * io_throttle_iops_scale_factor

BW_throttle_raw = S_GiB * io_throttle_bw_scale_factor * 1024 (MegaBytes/s)

```

The maximum throttle limits for Portworx volumes is then determined in the following way using the IOPS and bandwidth raw throttle values:

-
`MaxReadIOPS`: Maximum read IOPS throttle limit

MaxReadIOPS = clamp(IOPS_throttle_raw, io_throttle_min_iops, io_throttle_rd_iops)

-
`MaxWriteIOPS`: Maximum write IOPS throttle limit

MaxWriteIOPS = clamp(IOPS_throttle_raw, io_throttle_min_iops,io_throttle_wr_iops)

-
`MaxReadBW`: Maximum read bandwidth throttle limit

MaxReadBW = clamp(BW_throttle_raw, io_throttle_min_bw, io_throttle_rd_bw)

-
`MaxWriteBW`: Maximum write bandwidth throttle limit

MaxWriteBW = clamp(BW_throttle_raw, io_throttle_min_bw, io_throttle_wr_bw)

The `clamp` function here sets the maximum throttle limits to be within the range mentioned in each computation.

For example:

```

MaxReadIOPS = clamp(IOPS_throttle_raw, io_throttle_min_iops, io_throttle_rd_iops)

```

The value of `MaxReadIOPS` is determined by the scaled value `IOPS_throttle_raw`. Where the `IOPS_throttle_raw` is determined by volume size detected by Autopilot and the `io_throttle_iops_scale_factor` provided.

- If `IOPS_throttle_raw` is within the range of `io_throttle_min_iops` and `io_throttle_rd_iops`, then the `IOPS_throttle_raw` value is set as `MaxReadIOPS`.

- If `IOPS_throttle_raw` is lesser than `io_throttle_min_iops`, then `io_throttle_min_iops` is set as `MaxReadIOPS`.

- If `IOPS_throttle_raw` is greater than `io_throttle_rd_iops`, then `io_throttle_rd_iops` is set as `MaxReadIOPS`.

### Sample `StorageClass` for Dynamic App I/O Control for Portworx Volume​

Here is an example `StorageClass` that defines all the required to set up Dynamic App I/O Control for a Portworx volume.

```

apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:

  name: qos-params-example

provisioner: pxd.portworx.com

parameters:

  repl: "1"

  # Scale factors (per GiB of volume)

  io_throttle_iops_scale_factor: "400"

  io_throttle_bw_scale_factor: "0.1"

  # Minimum limits (floors)

  io_throttle_min_iops: "1500"

  io_throttle_min_bw: "1000"

  # Maximum limits (ceilings)

  io_throttle_rd_bw: "1500"

  io_throttle_wr_bw: "1500"

  io_throttle_rd_iops: "6000"

  io_throttle_wr_iops: "3000"

allowVolumeExpansion: true

```

For a 10GiB volume, Portworx will compute the values as shown below:

-
Raw IOPS value is calculated as:

```

IOPS_throttle_raw = S_GiB * io_throttle_iops_scale_factor

IOPS_throttle_raw = 10 * 400 = 4000

```

-
Maximum read IOPS scaled value is calculated as:

```

MaxReadIOPS = clamp(IOPS_throttle_raw, io_throttle_min_iops, io_throttle_rd_iops)

MaxReadIOPS = clamp(4000, 1500, 6000)

```

As the Raw IOPS value 4000 is less than the ceiling value 6000, the value for `MaxReadIOPS` will be set to 4000.

-
Maximum write IOPS scaled value is calculated as:

```

MaxWriteIOPS = clamp(IOPS_throttle_raw, io_throttle_min_iops,io_throttle_wr_iops)

MaxWriteIOPS = clamp(4000, 1500, 3000)

```

As the Raw IOPS value 4000 is more than the ceiling value of 3000, the value for `MaxWriteIOPS` will be set to 3000.

Similarly, the value for `MaxReadBW` and `MaxWriteBW` will be computed using the computational method mentioned above.

## Configure Dynamic App I/O Control for FADA Volume​

To configure Dynamic App I/O Control, provide the following parameters for FADA volumes in the `StorageClass`:

- `io_throttle_iops_scale_factor`: IOPS scaling factor, interpreted as IOPS per GiB of volume.

- `io_throttle_bw_scale_factor`: Bandwidth scaling factor that ranges between 0 and 1, interpreted as GiB/s per GiB of volume.

- `io_throttle_min_iops`: minimum IOPS throttle (floor).

- `max_iops`: maximum IOPS throttle (ceiling).

- `io_throttle_min_bw`: minimum bandwidth throttle (floor) - MegaBytes/s

- `max_bandwidth`: maximum bandwidth throttle (ceiling) - KiloBytes/s, MegaBytes/s and GigaBytes/s

The scaling factor parameters `io_throttle_iops_scale_factor` and `io_throttle_bw_scale_factor` that you set in the `StorageClass`, and the volume size detected by Autopilot, will determine the IOPS and bandwidth raw value for FADA volumes.

For example, if `S_GiB` is volume size in GiB, the `IOPS_throttle_raw` and `BW_throttle_raw` value is determined in the following way:

```

IOPS_throttle_raw = S_GiB * io_throttle_iops_scale_factor

BW_throttle_raw = S_GiB * io_throttle_bw_scale_factor * 1024 (MegaBytes/s)

```

The maximum throttle limits for FADA volumes is then determined in the following way using the IOPS and bandwidth raw throttle values:

-
`Max_IOPS`: Maximum IOPS for FADA volume Max_IOPS = clamp(IOPS_throttle_raw, io_throttle_min_iops, max_iops)

-
`Max_BW`: Maximum bandwidth for FADA volume Max_BW = clamp(BW_throttle_raw, io_throttle_min_bw, max_bandwidth)

The `clamp` function here adjusts the final value within the range mentioned in each computation. For example:

```

Max_IOPS = clamp(IOPS_throttle_raw, io_throttle_min_iops, max_iops)

```

The value of `Max_IOPS` is determined by the scaled value `IOPS_throttle_raw`.

- If `IOPS_throttle_raw` is within the range of `io_throttle_min_iops` and `max_iops` then the same value is set as `Max_IOPS`.

- If `IOPS_throttle_raw` is less than `io_throttle_min_iops` then `io_throttle_min_iops` is set as `Max_IOPS`.

- If `IOPS_throttle_raw` is greater than `max_iops` then `max_iops` is set as `Max_IOPS`.

### Sample `StorageClass` for Dynamic App I/O Control for FADA Volume​

Here is an example `StorageClass` that defines all the required parameters for a FADA volume.

```

apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:

  name: qos-params-example

provisioner: pxd.portworx.com

parameters:

  backend: "pure-block"

  repl: "1"

  # Scale factors (per GiB of volume)

  io_throttle_iops_scale_factor: "500"

  io_throttle_bw_scale_factor: "0.1"

  # Minimum limits (floors)

  io_throttle_min_iops: "1500"

  io_throttle_min_bw: "1000"

  # Maximum limits (ceilings)

  max_iops: "7000"

  max_bandwidth: "2000M"

allowVolumeExpansion: true

```

For a 10GiB volume, Portworx will compute the values as shown below:

-
Raw bandwidth value is calculated as:

```

BW_throttle_raw = S_GiB * io_throttle_bw_scale_factor (GiB/s)

BW_throttle_raw = 10 * 0.1 * 1024 = 1024M

```

-
Maximum bandwidth value is calculated as:

```

Max_BW = clamp(BW_throttle_raw, io_throttle_min_bw, max_bandwidth)

Max_BW = clamp(1024, 1000, 2000)

```

The scaled value 1024 is within the range so `Max_BW` is set as 1024M.

Similarly, the value for `Max_IOPS` can be calculated using the computational method mentioned above.

## Autopilot Dynamic I/O Throttle Metrics​

Autopilot exposes the following metrics to analyze the total number of dynamic throttle applied by Portworx on volumes.

MetricTypeDescription

autopilot_dynamic_throttle_applied_totalCountTotal number of successful dynamic throttle applied on volumes

autopilot_dynamic_throttle_skipped_totalCountTotal number of skipped dynamic throttle applied on volumes

autopilot_dynamic_throttle_failed_totalCountTotal number of failed dynamic throttle applied on volumes

## Disable Dynamic I/O Throttle for StorageClass and PVCs​

The PVCs that are bound to the `StorageClass` that are configured with throttle parameters to enable dynamic IO throttle will inherit the same throttle settings for IOPS and bandwidth using Autopilot.

To disable a PVC from not inheriting the I/O throttle behavior from the bound `StorageClass`, add the following annotation to the PVCs manifest.

```

portworx.io/throttle-auto-update: "false"

```

This annotation will skip that PVC from dynamic I/O throttle.

To disable all the PVCs that are bound to a `StorageClass` from using the dynamic I/O throttle, add the following annotation to the `StorageClass`:

```

portworx.io/throttle-auto-update: "false"

```

This annotation will skip all the PVCs from dynamic I/O throttle in that `StorageClass`.

## References​

- Application I/O Control

- Portworx Enterprise StorageClass

In this topic:
