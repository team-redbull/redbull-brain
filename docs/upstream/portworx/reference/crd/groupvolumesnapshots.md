# GroupVolumeSnapshot CRD reference

Source: https://docs.portworx.com/portworx-enterprise/reference/crd/groupvolumesnapshots (Portworx Enterprise 3.6)

GroupVolumeSnapshot CRD reference | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

GroupVolumeSnapshot represents a group snapshot.

## GroupVolumeSnapshot​

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

`spec`GroupVolumeSnapshotSpec represents the spec for a group snapshot`object`

`status`GroupVolumeSnapshotStatus is status for the group snapshot`object`

### `spec` fields​

FieldDescriptionType

`spec.maxRetries`MaxRetries is the number of times to retry the groupvolumesnapshot on failure. default: 0`integer`

`spec.options`Options are pass-through parameters that are passed to the driver handling the group snapshot`object`

`spec.postExecRule`PreExecRule is the name of rule applied after taking the snapshot. The rule needs to be
in the same namespace as the group volumesnapshot`string`

`spec.preExecRule`PreExecRule is the name of rule applied before taking the snapshot. The rule needs to be
in the same namespace as the group volumesnapshot`string`

`spec.pvcSelector`PVCSelector selects the PVCs that are part of the group snapshot`object`

`spec.pvcSelector.matchExpressions`matchExpressions is a list of label selector requirements. The requirements are ANDed.`array`

`spec.pvcSelector.matchExpressions.key`key is the label key that the selector applies to.`string`

`spec.pvcSelector.matchExpressions.operator`operator represents a key's relationship to a set of values.
Valid operators are In, NotIn, Exists and DoesNotExist.`string`

`spec.pvcSelector.matchExpressions.values`values is an array of string values. If the operator is In or NotIn,
the values array must be non-empty. If the operator is Exists or DoesNotExist,
the values array must be empty. This array is replaced during a strategic
merge patch.`array`

`spec.pvcSelector.matchLabels`matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels
map is equivalent to an element of matchExpressions, whose key field is "key", the
operator is "In", and the values array contains only "value". The requirements are ANDed.`object`

`spec.restoreNamespaces`RestoreNamespaces is a list of namespaces to which the snapshots can be restored to`array`

### `status` fields​

FieldDescriptionType

`status.stage`GroupVolumeSnapshotStageType is the stage of the group snapshot`string`

`status.status`GroupVolumeSnapshotStatusType is types of statuses of a group snapshot operation`string`

`status.volumeSnapshots.conditions.lastTransitionTime`The last time the condition transitioned from one status to another.`string`

`status.volumeSnapshots.conditions.message`A human readable message indicating details about the transition.`string`

`status.volumeSnapshots.conditions.reason`The reason for the condition's last transition.`string`

`status.volumeSnapshots.conditions.status`Status of the condition, one of True, False, Unknown.`string`

`status.volumeSnapshots.conditions.type`Type of replication controller condition.`string`

`status.volumeSnapshots.dataSource`VolumeSnapshotDataSource represents the actual location and type of the snapshot. Only one of its members may be specified.`object`

`status.volumeSnapshots.dataSource.awsElasticBlockStore`AWSElasticBlockStoreVolumeSnapshotSource is AWS EBS volume snapshot source`object`

`status.volumeSnapshots.dataSource.awsElasticBlockStore.fsType`Original volume file system type. The volume created from the snapshot would be pre-formatted
using the same file system, so it has to be saved along with the AWS snapshot ID`string`

`status.volumeSnapshots.dataSource.awsElasticBlockStore.snapshotId`Unique id of the persistent disk snapshot resource. Used to identify the disk snapshot in AWS`string`

`status.volumeSnapshots.dataSource.cinderVolume`CinderVolumeSnapshotSource represents Cinder snapshot resource`object`

`status.volumeSnapshots.dataSource.cinderVolume.snapshotId`Unique id of the cinder volume snapshot resource. Used to identify the snapshot in OpenStack`string`

`status.volumeSnapshots.dataSource.gcePersistentDisk`GCEPersistentDiskSnapshotSource represents an GCE PD snapshot resource`object`

`status.volumeSnapshots.dataSource.gcePersistentDisk.snapshotId`Unique id of the persistent disk snapshot resource. Used to identify the disk snapshot in GCE`string`

`status.volumeSnapshots.dataSource.glusterSnapshotVolume`AWSElasticBlockStore represents an AWS Disk resource that is attached to a
kubelet's host machine and then exposed to the pod.
More info: https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore
GlusterSnapshotSource represents a gluster snapshot resource`object`

`status.volumeSnapshots.dataSource.glusterSnapshotVolume.snapshotId`UniqueID represents a snapshot resource.`string`

`status.volumeSnapshots.dataSource.hostPath`HostPath represents a directory on the host.
Provisioned by a developer or tester.
This is useful for single-node development and testing only!
On-host storage is not supported in any way and WILL NOT WORK in a multi-node cluster.
More info: https://kubernetes.io/docs/concepts/storage/volumes#hostpath`object`

`status.volumeSnapshots.dataSource.hostPath.snapshot`Path represents a tar file that stores the HostPath volume source`string`

`status.volumeSnapshots.dataSource.portworxVolume`PortworxVolumeSnapshotSource represents Portworx snapshot resource`object`

`status.volumeSnapshots.dataSource.portworxVolume.snapshotCloudCredID`SnapshotCloudCredID is an optional credentials ID for the snapshot. This is used for cloud snaps.`string`

`status.volumeSnapshots.dataSource.portworxVolume.snapshotData`SnapshotData stores the name of VolumeSnapshotData for this snapshot. This is populated only for group snapshots.`string`

`status.volumeSnapshots.dataSource.portworxVolume.snapshotId`Unique id of the Portworx snapshot.`string`

`status.volumeSnapshots.dataSource.portworxVolume.snapshotTaskID`SnapshotTaskID stores the task ID used for the snapshot`string`

`status.volumeSnapshots.dataSource.portworxVolume.snapshotType`SnapshotType is the type of the snapshot`string`

`status.volumeSnapshots.dataSource.portworxVolume.volumeProvisioner`VolumeProvisioner is either the intree or CSI driver name`string`

In this topic:
