# Rejoin a decommissioned Portworx node back to the cluster in Kubernetes

Source: https://docs.portworx.com/portworx-enterprise/operations/k8s-node-rejoin (Portworx Enterprise 3.6)

Rejoin a decommissioned Portworx node back to the cluster in Kubernetes | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This document provides instructions for rejoining a previously decommissioned node with its original Portworx cluster.

## Ensure the node is decommissioned from Portworx​

If the node was previously part of a Portworx cluster, you must first ensure you followed steps to decommission it from the cluster. The Decommission a Node page has detailed steps for this.

## Ensure the following labels are removed from the node​

Remove these labels from the node before rejoining it back to the cluster after you decommission it.

To rejoin the node back as a storage-less node, remove both labels `portworx.io/provision-storage-node-handled=”true”` and `portworx.io/provision-storage-node=”true”`.

Portworx automatically adds the label `portworx.io/provision-storage-node-handled="true"` when it processes a node for storage-less or storage mode. During rejoin, Portworx checks this label and ignores nodes where it is present.

To rejoin the node back as a storage node, remove only the `portworx.io/provision-storage-node-handled=”true”` label and ensure that `portworx.io/provision-storage-node=”true”` label is present on the node.

## Ensure the Portworx services are no longer running​

You must ensure that the Portworx services are completely disabled from your system. You can check the status of the Portworx `systemd` service using the following `systemctl` command:

```

sudo systemctl status portworx

```

If the `systemd` service is still running, enter the following commands to stop and disable it:

```

sudo systemctl stop portworx

sudo systemctl disable portworx

sudo rm -f /etc/systemd/system/portworx*

grep -q '/opt/pwx/oci /opt/pwx/oci' /proc/self/mountinfo && sudo umount /opt/pwx/oci

```

note

Do not remove `/opt/pwx` or `/etc/pwx` at this stage if you want to use `pxctl` to clean up metadata in the next step. If you've already removed these directories, skip to the Remove metadata using wipefs section.

## Clean up Portworx metadata on the node​

Portworx also stores local metadata on the node to fingerprint its identity. The method you used to decommission the node determines the steps you must follow to clean up local Portworx metadata.

### Remove metadata using pxctl​

If pxctl is still on your node, enter the following `pxctl service` command to remove local metadata using pxctl:

```

pxctl service node-wipe --all

```

After running the above command, clean up the Portworx installation directories:

```

sudo umount /opt/pwx/oci

sudo rm -rf /etc/pwx /opt/pwx

```

### Remove metadata using wipefs​

If you've already removed pxctl from your node (or removed `/opt/pwx` in the previous step), you must manually find and wipe Portworx disks:

-
Enter the following `blkid` and `grep` command to list the disks that Portworx used:

```

blkid | grep pxpool

```

-
For each disk listed in step 1, enter the `wipefs` command with the `-af` options and the disk name `<disk-name>` to wipe Portworx metadata:

```

wipefs -af <disk-name>

```

Example

```

wipefs -af /dev/sdf

```

## Restart the Portworx pod on your node by applying labels​

- Kubernetes

- OpenShift

Once you have completely decommissioned your node and wiped it of Portworx data, you're ready to re-add it to your cluster. Enter the following `kubectl label nodes` commands, replacing `<node>` with the name of your Kubernetes node:

```

kubectl label node <node-name> px/service=restart --overwrite

kubectl label node <node-name> px/enabled=true --overwrite

```

Once you've entered these commands, Portworx starts on this node and rejoins the cluster as a new node.

Once you have completely decommissioned your node and wiped it of Portworx data, you're ready to re-add it to your cluster. Enter the following `oc label nodes` commands, replacing `<node>` with the name of your cluster node:

```

oc label node <node-name> px/service=restart --overwrite

oc label node <node-name> px/enabled=true --overwrite

```

Once you've entered these commands, Portworx starts on this node and rejoins the cluster as a new node.

caution

Decommissioning a node destroys its storage pools. When the node rejoins the cluster, Portworx recreates the pools with new pool IDs, so any custom pool labels used by Volume Placement Strategy (VPS) rules are lost and must be re-applied to the new pools. Until you restore these labels, volumes governed by VPS rules may not perform automatic HA updates.

Once the node has rejoined and its pools are recreated, re-apply each pool label using the following command:

```

pxctl service pool update <pool-id> --labels "<label-key>=<label-value>"

```

In this topic:
