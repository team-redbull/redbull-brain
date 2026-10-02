# VolumeSnapshotSchedule CRD reference

Source: https://docs.portworx.com/portworx-enterprise/reference/crd/volumesnapshotschedules (Portworx Enterprise latest)

VolumeSnapshotSchedule CRD reference | Portworx Enterprise Documentation

VolumeSnapshotSchedule represents a scheduled VolumeSnapshot object.

Starting with Stork 26.4.0, VolumeSnapshotSchedules for PVCs provisioned by the Portworx CSI driver (`pxd.portworx.com`) automatically use CSI VolumeSnapshots. See Associate a schedule policy using a CSI VolumeSnapshotClass for configuration details.

## VolumeSnapshotSchedule​

FieldDescriptionType

`apiVersion`APIVersion defines the versioned schema of this representation of an object.
Servers should convert recognized schemas to the latest internal value, and
may reject unrecognized values.
More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources`string`

`kind`Kind is a string value representing the REST resource this object represents.
Servers may infer this from the endpoint the client submits requests to.
Cannot be updated.
In CamelCase.
More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds`string`

`spec`VolumeSnapshotScheduleSpec is the spec used to schedule volumesnapshots`object`

`status`VolumeSnapshotScheduleStatus is the status of a volumesnapshot schedule`object`

### `metadata.annotations` fields​

AnnotationDescription

`stork.libopenstorage.org/volume-snapshot-class-name`Name of an existing `VolumeSnapshotClass` to use for CSI snapshots (Stork 26.4.0 and later). When set, Stork uses this class as-is for all CSI VolumeSnapshots created by this schedule. When absent, Stork auto-creates a VolumeSnapshotClass from the `portworx/snapshot-type` and `portworx/cloud-cred-id` annotations.

`portworx/snapshot-type`Snapshot type: `cloud` for cloud backups, `local` for in-cluster snapshots. Used to auto-create the VolumeSnapshotClass when `volume-snapshot-class-name` is not set.

`portworx/cloud-cred-id`UUID of the Portworx cloud credential. Used to auto-create the VolumeSnapshotClass when `volume-snapshot-class-name` is not set. Required only when multiple cloud credentials are configured.

`stork.libopenstorage.org/snapshot-restore-namespaces`Comma-separated list of namespaces to which snapshots created by this schedule can be restored.

`openstorage.io/auth-secret-namespace`Namespace of the Kubernetes Secret holding the auth token. Required when PX-Security is enabled.

`openstorage.io/auth-secret-name`Name of the Kubernetes Secret holding the auth token. Required when PX-Security is enabled.

### `spec` fields​

FieldDescriptionType

`spec.postExecRule`PostExecRule is the name of the rule that will be executed after taking a snapshot.`string`

`spec.preExecRule`PreExecRule is the name of the rule that will be executed before taking a snapshot.`string`

`spec.reclaimPolicy`ReclaimPolicy determines what happens to the snapshots when the VolumeSnapshotSchedule is deleted.`string`

`spec.schedulePolicyName`SchedulePolicyName is the name of the schedule policy that determines when snapshots are taken.`string`

`spec.suspend`Suspend, if set to true, suspends the snapshot schedule`boolean`

`spec.template`Template specifies the configuration of the volume snapshot that will be created.`object`

`spec.template.spec`VolumeSnapshotSpec is the desired state of the volume snapshot`object`

`spec.template.spec.persistentVolumeClaimName`PersistentVolumeClaimName is the name of the PVC being snapshotted`string`

`spec.template.spec.snapshotDataName`SnapshotDataName binds the VolumeSnapshot object with the VolumeSnapshotData`string`

In this topic:
