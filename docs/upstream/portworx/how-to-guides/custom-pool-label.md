# How to assign custom labels to device pools

Source: https://docs.portworx.com/portworx-enterprise/how-to-guides/custom-pool-label (Portworx Enterprise 3.6)

How to assign custom labels to device pools | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Assign custom labels to local storage devices during Portworx installation to control the placement of volumes and replicas. Labels applied to individual devices propagate to the storage pool that contains them. These labels serve as scheduling hints, enabling intelligent placement of volumes and replicas based on pool-level characteristics.

## Why use pool labels?​

- Control placement of volumes and replicas based on environmental or workload requirements.

- Improve operational awareness by associating pools with environments (for example, `env:prod`) or performance classes (for example, `perf:high`).

- Ensure consistent labeling by controlling behavior at the device level while applying labels at the pool level.

## Labeling guidelines​

- Labels must follow the `key:value` format.

- Label keys and values:

- Must not be empty.

- Must not contain colons (:) or whitespace. The colon is used as a separator between key and value (for example, `poolLabels=env:prod`).

- You can label only data devices.

- The pool label specified on the device applies to the pool to which the device belongs.

- All devices in the same pool must use the same label.

- You can assign only one label to a data device during installation. Later, you can use the `pxctl service pool update` command to assign multiple labels to the device.

- The following label keys are reserved for Portworx internal use and must not be used:

- `medium`

- `iopriority`

## Configure pool labels​

You can define labels during initial deployment or apply them to existing pools using the `pxctl` CLI. This section describes both methods.

### During initial installation​

To assign labels during installation, define them in the StorageCluster specification for each data device. Append the label using the `poolLabels=key:value` format to the device path.

```

spec:

  nodes:

    - selector:

        nodeName: <node-name-1>

      storage:

        devices:

          - <data-device-path-1>,poolLabels=env:prod

          - <data-device-path-2>,poolLabels=env:prod

```

### On an existing cluster​

To add a label to an existing pool, run one of the following pxctl commands:

```

# Using pool ID

pxctl service pool update <pool-id> --labels "key=value"

# Using pool UID

pxctl service pool update --uid <pool-uid> --labels "key=value"

```

You can specify the pool using either:

- The pool ID (numeric ID shown in `pxctl service pool show` output)

- The pool UID (UUID shown in `pxctl service pool show` output)

Note: If both pool ID and --uid are specified, the pool ID takes precedence and the --uid is ignored.

## Verify the labels​

To confirm that labels are correctly applied to pools, run the following command:

```

pxctl service pool show

```

```

Pool ID: 0

Type: SSD

UUID: a5d2b5...

IO Priority: HIGH

Labels: kubernetes.io/arch=amd64,env=prod

```

In this topic:
