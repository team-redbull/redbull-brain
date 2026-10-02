# Expand a Pre-Provisioned LUN or Disk in a PX-StoreV2 Storage Pool

Source: https://docs.portworx.com/portworx-enterprise/operations/scale-portworx-cluster/expand-storage-pool/expand-preprovisioned-lun-storev2 (Portworx Enterprise latest)

Expand a Pre-Provisioned LUN or Disk in a PX-StoreV2 Storage Pool | Portworx Enterprise Documentation

When you expand a pre-provisioned LUN or disk at the storage backend (for example, by resizing a Pure FlashArray LUN or a vSphere virtual disk), PX-StoreV2 does not detect the change automatically. You must rescan the device at the OS level and then cycle Portworx Enterprise through maintenance mode for the storage pool to reflect the new capacity.

### Prerequisites​

- Portworx Enterprise 3.6.0 or later with PX-StoreV2 datastore running on your cluster

- Pre-provisioned disks (DAS/SAN, Pure FlashArray, or vSphere-based)

- Root access to the node where the pool resides

### Procedure​

To expand a pre-provisioned LUN or disk in a storage pool, perform the following steps on the node that hosts the pool.

-
Identify the drive paths in use on the node:

```

pxctl service drive show

```

Note the device paths (for example, `/dev/mapper/<wwid>` for multipath-connected FlashArray LUNs or `/dev/sd<x>` for direct-attached disks) and the pool ID of the pool to expand.

-
Resize the LUN from your storage backend (for example, FlashArray UI or vCenter). If the pool contains more than one LUN, you must resize all LUNs in the pool to the same new size.

-
Rescan the underlying block device on the OS to make the kernel detect the new LUN size:

```

echo 1 > /sys/class/block/<device>/device/rescan

```

Replace `<device>` with the name of the underlying SCSI block device (for example, `sda`).

important

For multipath-connected LUNs (FlashArray), rescan all SCSI hosts that maps to the expanded LUN.

```

for host in /sys/class/scsi_host/host*; do

echo "- - -" > $host/scan

done

```

-
Verify that the underlying SCSI device size has increased:

```

lsblk

```

-
Resize the multipath device map:

```

multipathd resize map <dm-device>

```

Replace `<dm-device>` with the device mapper name for your LUN (for example, the `dm-X` device that corresponds to the `/dev/mapper/<wwid>` path shown in `pxctl service drive show`).

-
Verify that the multipath device reflects the new size:

```

multipath -ll

lsblk

```

-
Enter Portworx maintenance mode:

```

pxctl service maintenance --enter

```

```

This is a disruptive operation, PX will restart in maintenance mode.

Are you sure you want to proceed ? (Y/N): y

Entering maintenance mode...

```

-
Exit maintenance mode:

```

pxctl service maintenance --exit

```

```

Exiting maintenance mode...

```

note

Alternatively, you can restart Portworx instead of using the maintenance mode cycle:

```

systemctl restart portworx

```

Allow Portworx a few minutes to start before proceeding to the next step.

-
Verify that the pool reflects the new capacity:

```

pxctl status

```

In the output, confirm that the USABLE value for the target pool has increased to the expected size.

## Related topics​

- Non-Disruptive Pool Resize for PX-StoreV2 Pools

- Expand your storage pool size with disks not managed by Portworx

- Expand your storage pool size with disks managed by Portworx

- Portworx Datastores

- Maintenance Commands

In this topic:
