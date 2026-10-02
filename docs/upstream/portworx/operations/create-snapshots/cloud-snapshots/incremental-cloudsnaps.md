# Incremental Cloud Snapshots

Source: https://docs.portworx.com/portworx-enterprise/operations/create-snapshots/cloud-snapshots/incremental-cloudsnaps (Portworx Enterprise 3.6)

Incremental Cloud Snapshots | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

When Portworx takes and uploads backups for cloud snapshots (CloudSnaps), it first takes and uploads a full backup to your cloud provider. After the initial upload, Portworx uploads a series of incremental backups punctuated by an occasional full backup. By default, Portworx uploads a full backup every 7th cloud backup it performs. You can control the frequency with which Portworx uploads a full backup by configuring cluster options.

note

This is a cluster-wide setting.

## View full backup frequency​

You can view the currently set frequency by searching for it in the `pxctl cluster options list` output:

```

pxctl cluster options list | grep frequency

```

```

Cloudsnap full backup frequency                         : 7

```

## Change full backup frequency​

To modify the frequency with which Portworx uploads full backups for CloudSnaps, enter the following `pxctl cluster options update` command with the `--cloudsnap-full-backup-frequency` flag and a valid frequency range. The following example updates the frequency to every 4 CloudSnaps:

```

pxctl cluster options update --cloudsnap-full-backup-frequency 4

```

note

- The `--cloudsnap-full-backup-frequency` cluster option applies only to CloudSnap schedules created by Stork.

- If you set the `--cloudsnap-full-backup-frequency` to a very high value, Portworx may take longer to restore your CloudSnaps since there's a large number of incremental snapshot data to piece together before reaching a full backup. Additionally, these CloudSnaps may be larger, as they hold more incremental snapshots.

- If you set the frequency to a very low value, Portworx will send full backups more often.

In this topic:
