# Group Snaps using pxctl

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/group-snaps (Portworx Enterprise 3.6)

Group Snaps using pxctl | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This document explains how to take group snapshots of your container data with Portworx. Run the `pxctl volume snapshot group` command with the `--help` flag to list the available subcommands and flags.

To take a group snapshot of the volumes labelled with `v1=x1`, use this command:

```

pxctl volume snapshot group --label v1=x1

```

```

Volume 549285969696152595 : Snapshot 1026872711217134654

Volume 952350606466932557 : Snapshot 218459942880193319

```

You can easily group volumes by IDs and take a group snapshot with the `--volume_ids` flag:

```

pxctl volume snapshot group --volume_ids 83958335106174418,874802361339616936

```

```

Volume 83958335106174418 : Snapshot 362408823552094597

Volume 874802361339616936 : Snapshot 895516478416742770

```

## Related topics​

- For more information about creating group snapshots of Portworx volumes through Kubernetes, refer to the Snapshot group of PVCs page.

In this topic:
