# Fix volume errors using Filesystem Check

Source: https://docs.portworx.com/portworx-enterprise/operations/troubleshooting/volume-check (Portworx Enterprise 3.6)

Fix volume errors using Filesystem Check | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Over the course of normal operation, the filesystems on volumes can accrue damage and errors. Filesystem Check or `fsck` is a tool that reports and fixes filesystem issues. This feature allows you to do the following:

- Report issues found on the filesystem

- Fix only issues that `fsck` deems safe to fix

- For expert users, fix all reported issues

In order to mitigate data loss due to incorrect `fsck` fixes to the filesystem, Portworx creates a snapshot of the volume before attempting any fixes. If unintended changes occur, you can use this snapshot to recover your volume to its original state. Portworx does not automatically delete this snapshot, you should manually validate your data in the filesystem and delete the snapshot only when you're sure everything is as expected.

In addition to running when manually requested, Portworx runs `fsck` transparently before mounting volumes and fixes safe-to-fix errors. This can happen when the volume has a deferred volume resize operation pending during mount or the previous volume resize failed due errors in the filesystem.

caution

When Filesystem Check fixes errors, it modifies the filesystem metadata and can sometimes lead to unexpected changes to the filesystem. Pay close attention to the issues reported by `fsck` and ensure you understand the impact of proceeding before letting it fix unsafe issues.

note

- This feature is currently available only for ext4 filesystems.

- Filesystem check can be performed only on unmounted volume

- You cannot detach a volume when filesystem check is running on it.

- You can only run 1 instance of Filesystem check on a volume at-a-time

- You can only run 1 instance of Filesystem check per system. This is to reduce the impact on IO performance for user workloads running on that node.

- You must start filesystem check operations from the node on which the volume's storage is mounted

You can use `fsck` by entering `pxctl` commands on the node which contains your volume and mounted block storage.

The following collection of tasks describes how to perform health check on the filesystem and then repair it based on the result:

- Perform repair on clone volume

- Perform repair on original volume

It is recommended to first perform the filesystem check and repair on clone volume. If the filesystem repair completes successfully on cloned, then perform the same in original volume.

## Perform repair on clone volume​

-
Take a clone of the original volume.

```

pxctl volume clone <original-volume> --name <name-for-new-clone-vol>

```

-
Attach the cloned volume to a node.

```

pxctl host attach <new-cloned-vol>

```

note

Do not mount the clone volume at this stage.

-
Check for errors on the attached clone volume using the following `pxctl` command.

```

pxctl v check start --mode check_health <cloned-volume-name>

```

```

status code : FS_CHECK_STARTED] msg : Filesystem Check initiated

VolName      : test_ext4 (1106348497266600329)

devpath      : /dev/pxd/pxd1106348497266600329

```

Upon starting, you will receive the above confirmation message.

-
Monitor the progress and status of the check.

```

pxctl v check status <cloned-volume-name>

```

-
Inspect the cloned volume to check for `LAST_SCAN_STATUS`.

Status code descriptions

- FS_HEALTH_STATUS_HEALTHY: No problems detected with the filesystem.

- FS_HEALTH_STATUS_SAFE_TO_FIX: Issues were found that are safe to fix.

- FS_HEALTH_STATUS_NEEDS_INSPECTION: Filesystem problems require further inspection and possibly the involvement of a development engineer.

-
Repair the errors found on the attached clone volume using `fix_safe` mode.

```

pxctl v check start --mode fix_safe <cloned-volume-name>

```

note

Portworx creates a snapshot of the volume while executing repair in `fix_safe` mode.

-
Inspect the cloned volume again to check for LAST_SCAN_STATUS and verify the status of the repair.

```

pxctl v check status <cloned-volume-name>

```

If the health_status_code is FS_HEALTH_STATUS_HEALTHY, the errors have been successfully fixed.

## Perform repair on original volume​

The following steps can be performed on original volume only if you have repair the clone volume. The original volume should be in unmounted state (i.e. not being consumed by any application pod). This can be done by scaling down the application pod consuming this volume.

-
Inspect the original volume where it should not be any consumers.

```

pxctl volume inspect <original-volume>

```

-
Attach to a node if it is in detached state.

```

pxctl host attach <original-volume>

```

-
Take a fresh clone of the volume as a precautionary measure.

```

pxctl volume clone <original-volume> --name <fresh-clone-for-orginal-vol>

```

-
Repeat the steps from 3 to 7 mentioned in Perform repair on clone volume.

-
Scale up the application to see if the volumes gets unmounted.

Once the filesystem is repaired, delete the cloned volumes and auto-snapshot created by Portworx to avoid space consumption.

## pxctl volume check reference​

### pxctl volume check start​

`pxctl volume check start --mode [check_health | fix_all | fix_safe] <volume_name>`

DescriptionArgumentsFlags

Start a filesystem check operation on the block device and volume you specify`<volume_name>`: The name of the volume on which you want to perform a filesystem check operation`--mode`: Determines which mode filesystem check operates in.

Values: `check_health`, `fix_all`, `fix_safe`

:::note `fix_all` is a risky operation and may result in data loss on the volume. Ensure you understand the impact of using this flag and make appropriate backups before attempting to run it.:::

#### Examples​

-
Check an example volume's health:

```

pxctl volume check start --mode check_health exampleVolume

```

-
Fix an example volume's safe issues:

```

pxctl volume check start --mode fix_safe exampleVolume

```

### pxctl volume check status​

`pxctl volume check status <volume_name>`

DescriptionArgumentsFlags

Show the status of a Filesystem Check operation currently running on a volume you specify.`<volume_name>` : The name of the volume you want to check the status Filesystem Check operation status for

#### Examples​

-
Check an example volume's health:

```

pxctl volume check status exampleVolume

```

### pxctl volume check stop​

`pxctl volume check stop <volume_name>`

caution

This operation may lead to partially fixed filesystem errors and potentially cause further corruption.

DescriptionArgumentsFlags

Stop a Filesystem Check operation currently running on a volume you specify.`<volume_name>`: The name of the volume you want to stop Filesystem Check operations on

#### Examples​

-
Stop Filesystem Check operations an example volume:

```

pxctl volume check stop exampleVolume

```

In this topic:
