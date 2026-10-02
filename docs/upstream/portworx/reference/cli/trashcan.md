# Volume trash can

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/trashcan (Portworx Enterprise 3.6)

Volume trash can | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

The trash can feature provides protection against accidental or inadvertent volume deletions which could result in loss of data. In a clustered environment such as Kubernetes, unintended deletion of a PV or a namespace will cause volumes to be lost. This feature is recommended in any environment which is prone to such inadvertent deletions, as it can help to prevent data loss.

## Enable the trash can​

To enable the trash can feature on a cluster, run the following command:

```

pxctl cluster options update --volume-expiration-minutes <minutes>

```

`<minutes>` is an integer that represents the number of minutes a volume snapshot is retained after you delete a volume.

## Check trash can settings​

To check a cluster's options to see if the trash can is enabled, and what the retention period is, run the following command:

```

pxctl cluster options list | grep expiration

```

```

Volume expiration minutes                               : 0s

```

## Restore a volume​

When the trash can is enabled, you can list volumes in the trash can with the following command:

```

pxctl volume list --trashcan

```

```

DELETE TIME                   ID                  NAME                  SIZE   HA  SHARED  ENCRYPTED  IO_PRIORITY  STATUS         DELETE_TIMER

Tue Mar 29 21:51:16 UTC 2022  780196670250220779  newvol-tc-1648590676  1 GiB  1   no      no         LOW          up - detached  9m33s

```

In the sample output above, the trash can volume name is in the format `<original-vol-name>-tc-<original-vol-id>`.

To restore a volume, use the following command:

```

pxctl volume restore --trashcan <trashcan-vol-id> <desired-vol-name>

```

```

Successfully restored: <desired-vol-name> from <trashcan-vol-id>

```

This removes the volume from the trash can as well.

To use the restored volume with your application, follow the steps for using the Portworx volume.

## Disable the trash can​

To disable the trash can feature on a cluster, set `volume-expiration-minutes` equal to `0`:

```

pxctl cluster options update --volume-expiration-minutes 0

```

In this topic:
