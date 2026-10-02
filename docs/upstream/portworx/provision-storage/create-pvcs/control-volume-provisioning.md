# Manage Provisioning of PVCs

Source: https://docs.portworx.com/portworx-enterprise/provision-storage/create-pvcs/control-volume-provisioning (Portworx Enterprise latest)

Manage Provisioning of PVCs | Portworx Enterprise Documentation

Portworx provisions volumes with little configuration from you. By default, Portworx thin provisions volumes and balances them according to current usage and load within the cluster.

An advantage to this approach is that your apps can provision volumes uninterrupted for as long as your pools have enough backing storage for volume usage. However, if the volume usage exceeds your available backing storage, your apps will encounter capacity problems.

Your use-case may dictate a stricter allocation of resources than thin-provisioning, or you may wish to stop new volumes from being provisioned onto a node or pool without removing existing pools and risking disruption to apps and users.

In each of these cases, you can modify how Portworx provisions volumes with the `--provisioning-commit-labels` flag in the `pxctl cluster options update` command.

## Disable thin provisioning for your cluster​

If you want to ensure that each volume in your cluster has enough backing storage when it's provisioned, enter the `pxctl cluster options update` command with the `--provisioning-commit-labels` flag, specifying the following fields in JSON:

-
`OverCommitPercent` with the maximum storage percentage volumes can provision against backing storage set to `100`

-
`SnapReservePercent` with the percent of the previously specified maximum storage percent that is reserved for snapshots

```

pxctl cluster options update  --provisioning-commit-labels '[{"OverCommitPercent": 100, "SnapReservePercent": 30} ]'

```

```

Successfully updated cluster-wide options

```

## Disable thin provisioning for portions of your cluster​

If you want to disable thin provisioning for portions of your cluster, enter the `pxctl cluster options update` command with the `--provisioning-commit-labels` flag, specifying the following fields in JSON:

-
`LabelSelector` with the key values for labels and the `node` key with a comma separated list of the node IDs you wish to apply this rule to

-
`OverCommitPercent` with the maximum storage percentage volumes can provision against backing storage set to `100`

-
`SnapReservePercent` with the percent of the previously specified maximum storage percent that is reserved for snapshots

```

pxctl cluster options update  --provisioning-commit-labels '[{"LabelSelector": {"medium": "STORAGE_MEDIUM_MAGNETIC"}, "OverCommitPercent": 100, "SnapReservePercent":30} ]'

```

```

Successfully updated cluster-wide options

```

## Configure thin provisioning for your cluster​

If you want to limit thin provisioning for your cluster, as well as set different limits for portions of your cluster, enter the `pxctl cluster options update` command with the `--provisioning-commit-labels` flag, specifying the following fields in JSON:

- `OverCommitPercent` with the maximum storage percentage volumes can provision against backing storage

- `SnapReservePercent` with the percent of the previously specified maximum storage percent that is reserved for snapshots

- `LabelSelector` with the key values for labels or node IDs you wish to apply this rule to

Set the `OverCommitPercent` and `SnapReservePercent` limits for each label:

```

pxctl cluster options update  --provisioning-commit-labels '[{"LabelSelector": {"medium": "STORAGE_MEDIUM_MAGNETIC"}, "OverCommitPercent": 100, "SnapReservePercent":30} ]'

```

```

Successfully updated cluster-wide options

```

## Reset thin provisioning for your cluster​

You can reset thin provisioning entirely for your cluster by entering the `pxctl cluster options update` command with the `--provisioning-commit-labels` flag with empty brackets:

```

pxctl cluster options update  --provisioning-commit-labels '[]'

```

## Disable provisioning entirely​

You can disable provisioning entirely by specifying the `pxctl cluster options update` command with the `--disable-provisioning-labels` flag and the `node` key with a comma separated list of the node IDs you wish to disable provisioning for:

```

pxctl cluster options update  --disable-provisioning-labels "node=xxxxxxxx-xxxx-xxxx-xxxx-19a2e71fed14"

```

In this topic:
