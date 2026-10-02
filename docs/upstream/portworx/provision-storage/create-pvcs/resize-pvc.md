# Resize a Portworx PVC

Source: https://docs.portworx.com/portworx-enterprise/provision-storage/create-pvcs/resize-pvc (Portworx Enterprise 3.6)

Resize a Portworx PVC | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This document describes how to dynamically resize a volume (PVC) using Kubernetes or OpenShift and Portworx.

## Pre-requisites​

- The StorageClass must have `allowVolumeExpansion: true`.

- The PVC must be in use by a Pod.

## Example​

To resize a Portworx PVC, you can simply edit the PVC spec and update the size. Let's take an example of resizing a MySQL PVC.

-
Download the MySQL StorageClass spec and apply it. Note that the StorageClass has `allowVolumeExpansion: true`.

-
Download the MySQL PVC spec and apply it. We will start with a 5GB volume.

-
Download the MySQL Deployment spec, specify your own values for the `ACCEPT_EULA` and `SA_PASSWORD`, and apply it. Wait till the pod becomes 1/1 and then proceed to next step.

-
Run `kubectl edit pvc mssql-data` and change the size in the "spec" to 10Gi.

After you save the spec, `kubectl describe pvc mssql-data` should have an entry like below that confirms the volume resize.

```

Normal  VolumeResizeSuccessful  5s    volume_expand                ExpandVolume succeeded for volume default/mssql-data

```

In this topic:
