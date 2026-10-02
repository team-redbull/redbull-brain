# How to use Velero with Portworx Enterprise

Source: https://docs.portworx.com/portworx-enterprise/how-to-guides/velero (Portworx Enterprise 3.6)

How to use Velero with Portworx Enterprise | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Velero is a utility for managing disaster recovery, specifically for your Kubernetes cluster resources and persistent volumes. To take snapshots of Portworx volumes through Velero you need to install and configure the Portworx plugin.

note

These instructions are for Velero v1.0 and higher. For older versions of Ark (previous name for the Velero project), please click here.

## Install Velero Plugin​

Portworx needs to be added as a plugin to your existing Velero installation. Run the following command to install the Portworx plugin:

```

velero plugin add portworx/velero-plugin:1.0.3

```

This should add an init container to your Velero deployment to install the plugin.

- Kubernetes

- Openshift

## Configure Velero to use Portworx snapshots​

Once the plugin is installed, you need to create VolumeSnapshotLocation objects for Velero to use when taking volume snapshots. These specify whether you want to take local or cloud snapshots.

Run the following command to create a VolumeSnapshotLocation for local snapshots.

```

velero snapshot-location create portworx-local --provider portworx.io/portworx --config type=local

```

Run the following command to create a VolumeSnapshotLocation for cloud snapshots.

```

velero snapshot-location create portworx-cloud --provider portworx.io/portworx --config type=cloud,credId=<UUID>

```

After applying the above specs you should see them when you list the VolumeSnapshotLocations

```

kubectl get volumesnapshotlocation -n velero

```

```

NAME             AGE

portworx-cloud   54m

portworx-local   54m

```

The valid configuration parameters that can be given through the `--config` argument in the above commands are:

- type: Defines the type of snapshot. Valid values: [cloud | local]

- credID: Defines the credential Portworx should use when triggering a cloud snapshot.

- PX_NAMESPACE: Specify the namespace in which Portworx is installed. This parameter is not required if Portworx is installed in `kube-system` namespace. This option is similar to what is specified in other Portworx components like Stork.

- portworx.io/cloudsnap-incremental-count: Specify the number of incremental cloud snapshots Portworx should take before triggering a full backup. This option is similar to what is specified in other Portworx components like Stork.

Here is a sample command that uses all the available config parameters:

```

velero snapshot-location create portworx-cloud --provider portworx.io/portworx --config type=cloud,credId=<UUID>,PX_NAMESPACE=portworx,portworx.io/cloudsnap-incremental-count=7

```

## Configure Velero to use Portworx snapshots​

Once the plugin is installed, you need to create VolumeSnapshotLocation objects for Velero to use when taking volume snapshots. These specify whether you want to take local or cloud snapshots.

Run the following command to create a VolumeSnapshotLocation for local snapshots.

```

velero snapshot-location create portworx-local --provider portworx.io/portworx --config type=local

```

Run the following command to create a VolumeSnapshotLocation for cloud snapshots.

```

velero snapshot-location create portworx-cloud --provider portworx.io/portworx --config type=cloud,credId=<UUID>

```

After applying the above specs you should see them when you list the VolumeSnapshotLocations

```

oc get volumesnapshotlocation -n velero

```

```

NAME             AGE

portworx-cloud   54m

portworx-local   54m

```

The valid configuration parameters that can be given through the `--config` argument in the above commands are:

- type: Defines the type of snapshot. Valid values: [cloud | local]

- credID: Defines the credential Portworx should use when triggering a cloud snapshot.

- PX_NAMESPACE: Specify the namespace in which Portworx is installed. This parameter is not required if Portworx is installed in `kube-system` namespace. This option is similar to what is specified in other Portworx components like Stork.

- portworx.io/cloudsnap-incremental-count: Specify the number of incremental cloud snapshots Portworx should take before triggering a full backup. This option is similar to what is specified in other Portworx components like Stork.

Here is a sample command that uses all the available config parameters:

```

velero snapshot-location create portworx-cloud --provider portworx.io/portworx --config type=cloud,credId=<UUID>,PX_NAMESPACE=portworx,portworx.io/cloudsnap-incremental-count=7

```

## Creating backups​

Once you have installed and configured the plugin, every time you take backups using Velero and include PVCs, it will also take Portworx snapshots of your volumes.

### Local Backups​

To backup all your apps in the default namespace and also create local snapshots of the volumes, you would use `portworx-local` for the snapshot location:

```

velero backup create default-ns-local-backup --include-namespaces=default --snapshot-volumes \

     --volume-snapshot-locations portworx-local

```

```

Backup request "default-ns-local-backup" submitted successfully.

Run `velero backup describe default-ns-local-backup` for more details.

```

### Cloud Backups​

To backup all your apps in the default namespace and also create cloud backups of the volumes, you would use `portworx-cloud` for the snapshot location:

```

velero backup create default-ns-cloud-backup --include-namespaces=default --snapshot-volumes \

     --volume-snapshot-locations portworx-cloud

```

```

Backup request "default-ns-cloud-backup" submitted successfully.

Run `velero backup describe default-ns-cloud-backup` for more details.

```

## Listing backups​

Once the specs and volumes have been backed up you should see the backup marked as `Completed` in velero.

```

velero get backup

```

```

NAME                      STATUS      CREATED                         EXPIRES   STORAGE LOCATION    SELECTOR

default-ns-local-backup   Completed   2018-11-11 20:10:45 +0000 UTC   29d       default             <none>

default-ns-cloud-backup   Completed   2018-11-11 20:15:45 +0000 UTC   29d       default             <none>

```

## Restoring from backups​

When restoring from backups, a clone volume will be created from the snapshot and bound to the restored PVC. To restore from the backup created above you can run the following command:

```

velero restore create --from-backup default-ns-local-backup

```

```

Restore request "default-ns-local-backup-20181111201245" submitted successfully.

Run `velero restore describe default-ns-local-backup-20181111201245` for more details.

```

In this topic:
