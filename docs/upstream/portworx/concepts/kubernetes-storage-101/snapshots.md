# Kubernetes Snapshots and Backups

Source: https://docs.portworx.com/portworx-enterprise/concepts/kubernetes-storage-101/snapshots (Portworx Enterprise latest)

Kubernetes Snapshots and Backups | Portworx Enterprise Documentation

## Snapshots​

Snapshots can be used to capture the state of a PVC at a given point of time.

important

For FlashArray and FlashBlade Direct Access volumes, use the CSI snapshot method page for creating and restoring snapshots.

Following objects are important when working with snapshots:

### VolumeSnapshot​

A VolumeSnapshot defines a users request to snapshot a PVC. Let's take an example:

```

apiVersion: volumesnapshot.external-storage.k8s.io/v1

kind: VolumeSnapshot

metadata:

  name: mysql-snapshot

  namespace: default

spec:

  persistentVolumeClaimName: mysql-data

```

In above spec,

- persistentVolumeClaimName: mysql-data indicates that user wants to snapshot the mysql-data PVC.

### GroupVolumeSnapshot​

A GroupVolumeSnapshot defines a users request to snapshot a group of PVCs. Portworx will quiesce IO on all volumes in the group and then trigger the snapshot.

Let's take an example:

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: GroupVolumeSnapshot

metadata:

  name: mysql-group-snap

spec:

  pvcSelector:

    matchLabels:

      app: mysql

```

In above spec,

- pvcSelector specifies a label selector which will match all PVCs that have the label app=mysql.

note

For single or group snapshots, it is possible to backup the volumes to a cloud S3 endpoint instead of disks on the local cluster. The Create snapshots page has details on taking snapshots of Portworx volumes.

### Application consistency when taking snapshots​

For each of the snapshot types, Portworx supports specifying pre and post rules that are run on the application pods using the volumes. This allows users to quiesce the applications before the snapshot is taken and resume I/O after the snapshot is taken. The commands will be run in pods which are using the PVC being snapshotted.

Read Configuring 3DSnaps for further details on 3DSnaps.

## Restore snapshots​

You can restore both single and group volume snapshots by creating a VolumeSnapshotRestore spec.

- Create a VolumeSnapshotRestore YAML file, specifying the following:

- name The name of this VolumeSnapshotRestore object

- namespace The namespace this VolumeSnapshotRestore object will be located in

- spec

-
groupSnapshot Specifies whether or not the source is a group snapshot

-
sourceName The name of the VolumeSnapshot or groupVolumeSnapshot object you want to restore

-
sourceNamespace The namespace the source VolumeSnapshot or groupVolumeSnapshot object exists in

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: VolumeSnapshotRestore

metadata:

  name: mysql-snap-inrestore

  namespace: default

spec:

  groupSnapshot: true

  sourceName: mysql-snapshot

  sourceNamespace: mysql-snap-restore-splocal

```

-
Apply the YAML file:

```

kubectl apply -f volSnap.yaml

```

## Migration​

Migration is referred to the operation of transferring application workloads (e.g Deployments, Statefulsets, Jobs, ConfigMaps etc) and their data (PVCs) across Kubernetes clusters.

Common use cases for this would be:

- Augment capacity: Free capacity on critical clusters by evacuating lower priority applications to secondary clusters.

- Blue-green test: Validate new versions of Kubernetes and/or Portworx using both application and its data. This is the same blue-green approach used by cloud-native application teams– now available for your infrastructure.

- Dev/test: Promote workloads from dev to staging clusters in an automated manner. Thereby, eliminate the manual steps for data preparation that hurt fidelity of tests.

- Lift/Shift: Move applications and data from an on-prem cluster to a hosted AWS EKS or Google GKE. The reverse is also supported to repatriate, move applications on-prem.

- Maintenance: Decommission a cluster in order to perform hardware-level upgrades.

Portworx uses Stork for migration. The Migration page detailed documentation on this.

## Related topics​

- Create and use snapshots

## Related videos​

### Create a local snapshot of a running MongoDB cluster on GKE and restore it to a new POD​

### Create a cloud snapshot of a running MongoDB cluster on GKE and restore it to a new POD​

### Create group snapshots of multiple volumes with Portworx on OpenShift​

In this topic:
