# DataExport CRD reference

Source: https://docs.portworx.com/portworx-enterprise/reference/crd/dataexports (Portworx Enterprise latest)

DataExport CRD reference | Portworx Enterprise Documentation

DataExport defines a spec for importing of application data from a non Portworx PVC (source) to a PVC backed by Portworx..

## DataExportList​

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

`spec`DataExportSpec defines configuration parameters for DataExport.`object`

`status`ExportStatus indicates a current state of the data transfer.`object`

### `spec` fields​

FieldDescriptionType

`spec.destination`DataExportDestination defines a backend for data transfer.`object`

`spec.destination.persistentVolumeClaim`PersistentVolumeClaim defines a PVC backend for data transfer. If provided PVC doesn't exist
a new one will be created using the spec configuration.`object`

`spec.destination.persistentVolumeClaim.apiVersion`APIVersion defines the versioned schema of this representation of an object.
Servers should convert recognized schemas to the latest internal value, and
may reject unrecognized values.
More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources`string`

`spec.destination.persistentVolumeClaim.kind`Kind is a string value representing the REST resource this object represents.
Servers may infer this from the endpoint the client submits requests to.
Cannot be updated.
In CamelCase.
More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds`string`

`spec.destination.persistentVolumeClaim.metadata`Standard object's metadata.
More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata`object`

`spec.destination.persistentVolumeClaim.spec`spec defines the desired characteristics of a volume requested by a pod author.
More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims`object`

`spec.destination.persistentVolumeClaim.spec.accessModes`accessModes contains the desired access modes the volume should have.
More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#access-modes-1`array`

`spec.destination.persistentVolumeClaim.spec.dataSource`dataSource field can be used to specify either:
* An existing VolumeSnapshot object (snapshot.storage.k8s.io/VolumeSnapshot)
* An existing PVC (PersistentVolumeClaim)
If the provisioner or an external controller can support the specified data source,
it will create a new volume based on the contents of the specified data source.
When the AnyVolumeDataSource feature gate is enabled, dataSource contents will be copied to dataSourceRef,
and dataSourceRef contents will be copied to dataSource when dataSourceRef.namespace is not specified.
If the namespace is specified, then dataSourceRef will not be copied to dataSource.`object`

`spec.destination.persistentVolumeClaim.spec.dataSource.apiGroup`APIGroup is the group for the resource being referenced.
If APIGroup is not specified, the specified Kind must be in the core API group.
For any other third-party types, APIGroup is required.`string`

`spec.destination.persistentVolumeClaim.spec.dataSource.kind`Kind is the type of resource being referenced`string`

`spec.destination.persistentVolumeClaim.spec.dataSource.name`Name is the name of resource being referenced`string`

`spec.destination.persistentVolumeClaim.spec.dataSourceRef`dataSourceRef specifies the object from which to populate the volume with data, if a non-empty
volume is desired. This may be any object from a non-empty API group (non
core object) or a PersistentVolumeClaim object.
When this field is specified, volume binding will only succeed if the type of
the specified object matches some installed volume populator or dynamic
provisioner.
This field will replace the functionality of the dataSource field and as such
if both fields are non-empty, they must have the same value. For backwards
compatibility, when namespace isn't specified in dataSourceRef,
both fields (dataSource and dataSourceRef) will be set to the same
value automatically if one of them is empty and the other is non-empty.
When namespace is specified in dataSourceRef,
dataSource isn't set to the same value and must be empty.
There are three important differences between dataSource and dataSourceRef:
* While dataSource only allows two specific types of objects, dataSourceRef
 allows any non-core object, as well as PersistentVolumeClaim objects.
* While dataSource ignores disallowed values (dropping them), dataSourceRef
 preserves all values, and generates an error if a disallowed value is
 specified.
* While dataSource only allows local objects, dataSourceRef allows objects
 in any namespaces.
(Beta) Using this field requires the AnyVolumeDataSource feature gate to be enabled.
(Alpha) Using the namespace field of dataSourceRef requires the CrossNamespaceVolumeDataSource feature gate to be enabled.`object`

`spec.destination.persistentVolumeClaim.spec.dataSourceRef.apiGroup`APIGroup is the group for the resource being referenced.
If APIGroup is not specified, the specified Kind must be in the core API group.
For any other third-party types, APIGroup is required.`string`

`spec.destination.persistentVolumeClaim.spec.dataSourceRef.kind`Kind is the type of resource being referenced`string`

`spec.destination.persistentVolumeClaim.spec.dataSourceRef.name`Name is the name of resource being referenced`string`

`spec.destination.persistentVolumeClaim.spec.dataSourceRef.namespace`Namespace is the namespace of resource being referenced
Note that when a namespace is specified, a gateway.networking.k8s.io/ReferenceGrant object is required in the referent namespace to allow that namespace's owner to accept the reference. See the ReferenceGrant documentation for details.
(Alpha) This field requires the CrossNamespaceVolumeDataSource feature gate to be enabled.`string`

`spec.destination.persistentVolumeClaim.spec.resources`resources represents the minimum resources the volume should have.
If RecoverVolumeExpansionFailure feature is enabled users are allowed to specify resource requirements
that are lower than previous value but must still be higher than capacity recorded in the
status field of the claim.
More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#resources`object`

`spec.destination.persistentVolumeClaim.spec.resources.limits`Limits describes the maximum amount of compute resources allowed.
More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/`object`

`spec.destination.persistentVolumeClaim.spec.resources.requests`Requests describes the minimum amount of compute resources required.
If Requests is omitted for a container, it defaults to Limits if that is explicitly specified,
otherwise to an implementation-defined value. Requests cannot exceed Limits.
More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/`object`

`spec.destination.persistentVolumeClaim.spec.selector`selector is a label query over volumes to consider for binding.`object`

`spec.destination.persistentVolumeClaim.spec.selector.matchExpressions`matchExpressions is a list of label selector requirements. The requirements are ANDed.`array`

`spec.destination.persistentVolumeClaim.spec.selector.matchExpressions.key`key is the label key that the selector applies to.`string`

`spec.destination.persistentVolumeClaim.spec.selector.matchExpressions.operator`operator represents a key's relationship to a set of values.
Valid operators are In, NotIn, Exists and DoesNotExist.`string`

`spec.destination.persistentVolumeClaim.spec.selector.matchExpressions.values`values is an array of string values. If the operator is In or NotIn,
the values array must be non-empty. If the operator is Exists or DoesNotExist,
the values array must be empty. This array is replaced during a strategic
merge patch.`array`

`spec.destination.persistentVolumeClaim.spec.selector.matchLabels`matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels
map is equivalent to an element of matchExpressions, whose key field is "key", the
operator is "In", and the values array contains only "value". The requirements are ANDed.`object`

`spec.destination.persistentVolumeClaim.spec.storageClassName`storageClassName is the name of the StorageClass required by the claim.
More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#class-1`string`

`spec.destination.persistentVolumeClaim.spec.volumeAttributesClassName`volumeAttributesClassName may be used to set the VolumeAttributesClass used by this claim.
If specified, the CSI driver will create or update the volume with the attributes defined
in the corresponding VolumeAttributesClass. This has a different purpose than storageClassName,
it can be changed after the claim is created. An empty string value means that no VolumeAttributesClass
will be applied to the claim but it's not allowed to reset this field to empty string once it is set.
If unspecified and the PersistentVolumeClaim is unbound, the default VolumeAttributesClass
will be set by the persistentvolume controller if it exists.
If the resource referred to by volumeAttributesClass does not exist, this PersistentVolumeClaim will be
set to a Pending state, as reflected by the modifyVolumeStatus field, until such as a resource
exists.
More info: https://kubernetes.io/docs/concepts/storage/volume-attributes-classes/
(Alpha) Using this field requires the VolumeAttributesClass feature gate to be enabled.`string`

`spec.destination.persistentVolumeClaim.spec.volumeMode`volumeMode defines what type of volume is required by the claim.
Value of Filesystem is implied when not included in claim spec.`string`

`spec.destination.persistentVolumeClaim.spec.volumeName`volumeName is the binding reference to the PersistentVolume backing this claim.`string`

`spec.destination.persistentVolumeClaim.status`status represents the current information/status of a persistent volume claim.
Read-only.
More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims`object`

`spec.destination.persistentVolumeClaim.status.accessModes`accessModes contains the actual access modes the volume backing the PVC has.
More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#access-modes-1`array`

`spec.destination.persistentVolumeClaim.status.allocatedResourceStatuses`allocatedResourceStatuses stores status of resource being resized for the given PVC.
Key names follow standard Kubernetes label syntax. Valid values are either:
 * Un-prefixed keys:
 - storage - the capacity of the volume.
 * Custom resources must use implementation-defined prefixed names such as "example.com/my-custom-resource"
Apart from above values - keys that are unprefixed or have kubernetes.io prefix are considered
reserved and hence may not be used.

ClaimResourceStatus can be in any of following states:
 - ControllerResizeInProgress:
 State set when resize controller starts resizing the volume in control-plane.
 - ControllerResizeFailed:
 State set when resize has failed in resize controller with a terminal error.
 - NodeResizePending:
 State set when resize controller has finished resizing the volume but further resizing of
 volume is needed on the node.
 - NodeResizeInProgress:
 State set when kubelet starts resizing the volume.
 - NodeResizeFailed:
 State set when resizing has failed in kubelet with a terminal error. Transient errors don't set
 NodeResizeFailed.
For example: if expanding a PVC for more capacity - this field can be one of the following states:
 - pvc.status.allocatedResourceStatus['storage'] = "ControllerResizeInProgress"
 - pvc.status.allocatedResourceStatus['storage'] = "ControllerResizeFailed"
 - pvc.status.allocatedResourceStatus['storage'] = "NodeResizePending"
 - pvc.status.allocatedResourceStatus['storage'] = "NodeResizeInProgress"
 - pvc.status.allocatedResourceStatus['storage'] = "NodeResizeFailed"
When this field is not set, it means that no resize operation is in progress for the given PVC.

A controller that receives PVC update with previously unknown resourceName or ClaimResourceStatus
should ignore the update for the purpose it was designed. For example - a controller that
only is responsible for resizing capacity of the volume, should ignore PVC updates that change other valid
resources associated with PVC.

This is an alpha field and requires enabling RecoverVolumeExpansionFailure feature.`object`

`spec.destination.persistentVolumeClaim.status.allocatedResources`allocatedResources tracks the resources allocated to a PVC including its capacity.
Key names follow standard Kubernetes label syntax. Valid values are either:
 * Un-prefixed keys:
 - storage - the capacity of the volume.
 * Custom resources must use implementation-defined prefixed names such as "example.com/my-custom-resource"
Apart from above values - keys that are unprefixed or have kubernetes.io prefix are considered
reserved and hence may not be used.

Capacity reported here may be larger than the actual capacity when a volume expansion operation
is requested.
For storage quota, the larger value from allocatedResources and PVC.spec.resources is used.
If allocatedResources is not set, PVC.spec.resources alone is used for quota calculation.
If a volume expansion capacity request is lowered, allocatedResources is only
lowered if there are no expansion operations in progress and if the actual volume capacity
is equal or lower than the requested capacity.

A controller that receives PVC update with previously unknown resourceName
should ignore the update for the purpose it was designed. For example - a controller that
only is responsible for resizing capacity of the volume, should ignore PVC updates that change other valid
resources associated with PVC.

This is an alpha field and requires enabling RecoverVolumeExpansionFailure feature.`object`

`spec.destination.persistentVolumeClaim.status.capacity`capacity represents the actual resources of the underlying volume.`object`

`spec.destination.persistentVolumeClaim.status.conditions`conditions is the current Condition of persistent volume claim. If underlying persistent volume is being
resized then the Condition will be set to 'Resizing'.`array`

`spec.destination.persistentVolumeClaim.status.conditions.lastProbeTime`lastProbeTime is the time we probed the condition.`string`

`spec.destination.persistentVolumeClaim.status.conditions.lastTransitionTime`lastTransitionTime is the time the condition transitioned from one status to another.`string`

`spec.destination.persistentVolumeClaim.status.conditions.message`message is the human-readable message indicating details about last transition.`string`

`spec.destination.persistentVolumeClaim.status.conditions.reason`reason is a unique, this should be a short, machine understandable string that gives the reason
for condition's last transition. If it reports "Resizing" that means the underlying
persistent volume is being resized.`string`

`spec.destination.persistentVolumeClaim.status.conditions.type`PersistentVolumeClaimConditionType is a valid value of PersistentVolumeClaimCondition.Type`string`

`spec.destination.persistentVolumeClaim.status.currentVolumeAttributesClassName`currentVolumeAttributesClassName is the current name of the VolumeAttributesClass the PVC is using.
When unset, there is no VolumeAttributeClass applied to this PersistentVolumeClaim
This is an alpha field and requires enabling VolumeAttributesClass feature.`string`

`spec.destination.persistentVolumeClaim.status.modifyVolumeStatus`ModifyVolumeStatus represents the status object of ControllerModifyVolume operation.
When this is unset, there is no ModifyVolume operation being attempted.
This is an alpha field and requires enabling VolumeAttributesClass feature.`object`

`spec.destination.persistentVolumeClaim.status.modifyVolumeStatus.status`status is the status of the ControllerModifyVolume operation. It can be in any of following states:
 - Pending
 Pending indicates that the PersistentVolumeClaim cannot be modified due to unmet requirements, such as
 the specified VolumeAttributesClass not existing.
 - InProgress
 InProgress indicates that the volume is being modified.
 - Infeasible
 Infeasible indicates that the request has been rejected as invalid by the CSI driver. To
 resolve the error, a valid VolumeAttributesClass needs to be specified.
Note: New statuses can be added in the future. Consumers should check for unknown statuses and fail appropriately.`string`

`spec.destination.persistentVolumeClaim.status.modifyVolumeStatus.targetVolumeAttributesClassName`targetVolumeAttributesClassName is the name of the VolumeAttributesClass the PVC currently being reconciled`string`

`spec.destination.persistentVolumeClaim.status.phase`phase represents the current phase of PersistentVolumeClaim.`string`

`spec.source`DataExportSource defines a PVC name and namespace that should be processed.`object`

`spec.source.persistentVolumeClaim`PersistentVolumeClaim is a user's request for and claim to a persistent volume`object`

`spec.source.persistentVolumeClaim.apiVersion`APIVersion defines the versioned schema of this representation of an object.
Servers should convert recognized schemas to the latest internal value, and
may reject unrecognized values.
More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources`string`

`spec.source.persistentVolumeClaim.kind`Kind is a string value representing the REST resource this object represents.
Servers may infer this from the endpoint the client submits requests to.
Cannot be updated.
In CamelCase.
More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds`string`

`spec.source.persistentVolumeClaim.metadata`Standard object's metadata.
More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata`object`

`spec.source.persistentVolumeClaim.spec`spec defines the desired characteristics of a volume requested by a pod author.
More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims`object`

`spec.source.persistentVolumeClaim.spec.accessModes`accessModes contains the desired access modes the volume should have.
More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#access-modes-1`array`

`spec.source.persistentVolumeClaim.spec.dataSource`dataSource field can be used to specify either:
* An existing VolumeSnapshot object (snapshot.storage.k8s.io/VolumeSnapshot)
* An existing PVC (PersistentVolumeClaim)
If the provisioner or an external controller can support the specified data source,
it will create a new volume based on the contents of the specified data source.
When the AnyVolumeDataSource feature gate is enabled, dataSource contents will be copied to dataSourceRef,
and dataSourceRef contents will be copied to dataSource when dataSourceRef.namespace is not specified.
If the namespace is specified, then dataSourceRef will not be copied to dataSource.`object`

`spec.source.persistentVolumeClaim.spec.dataSource.apiGroup`APIGroup is the group for the resource being referenced.
If APIGroup is not specified, the specified Kind must be in the core API group.
For any other third-party types, APIGroup is required.`string`

`spec.source.persistentVolumeClaim.spec.dataSource.kind`Kind is the type of resource being referenced`string`

`spec.source.persistentVolumeClaim.spec.dataSource.name`Name is the name of resource being referenced`string`

`spec.source.persistentVolumeClaim.spec.dataSourceRef`dataSourceRef specifies the object from which to populate the volume with data, if a non-empty
volume is desired. This may be any object from a non-empty API group (non
core object) or a PersistentVolumeClaim object.
When this field is specified, volume binding will only succeed if the type of
the specified object matches some installed volume populator or dynamic
provisioner.
This field will replace the functionality of the dataSource field and as such
if both fields are non-empty, they must have the same value. For backwards
compatibility, when namespace isn't specified in dataSourceRef,
both fields (dataSource and dataSourceRef) will be set to the same
value automatically if one of them is empty and the other is non-empty.
When namespace is specified in dataSourceRef,
dataSource isn't set to the same value and must be empty.
There are three important differences between dataSource and dataSourceRef:
* While dataSource only allows two specific types of objects, dataSourceRef
 allows any non-core object, as well as PersistentVolumeClaim objects.
* While dataSource ignores disallowed values (dropping them), dataSourceRef
 preserves all values, and generates an error if a disallowed value is
 specified.
* While dataSource only allows local objects, dataSourceRef allows objects
 in any namespaces.
(Beta) Using this field requires the AnyVolumeDataSource feature gate to be enabled.
(Alpha) Using the namespace field of dataSourceRef requires the CrossNamespaceVolumeDataSource feature gate to be enabled.`object`

`spec.source.persistentVolumeClaim.spec.dataSourceRef.apiGroup`APIGroup is the group for the resource being referenced.
If APIGroup is not specified, the specified Kind must be in the core API group.
For any other third-party types, APIGroup is required.`string`

`spec.source.persistentVolumeClaim.spec.dataSourceRef.kind`Kind is the type of resource being referenced`string`

`spec.source.persistentVolumeClaim.spec.dataSourceRef.name`Name is the name of resource being referenced`string`

`spec.source.persistentVolumeClaim.spec.dataSourceRef.namespace`Namespace is the namespace of resource being referenced
Note that when a namespace is specified, a gateway.networking.k8s.io/ReferenceGrant object is required in the referent namespace to allow that namespace's owner to accept the reference. See the ReferenceGrant documentation for details.
(Alpha) This field requires the CrossNamespaceVolumeDataSource feature gate to be enabled.`string`

`spec.source.persistentVolumeClaim.spec.resources`resources represents the minimum resources the volume should have.
If RecoverVolumeExpansionFailure feature is enabled users are allowed to specify resource requirements
that are lower than previous value but must still be higher than capacity recorded in the
status field of the claim.
More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#resources`object`

`spec.source.persistentVolumeClaim.spec.resources.limits`Limits describes the maximum amount of compute resources allowed.
More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/`object`

`spec.source.persistentVolumeClaim.spec.resources.requests`Requests describes the minimum amount of compute resources required.
If Requests is omitted for a container, it defaults to Limits if that is explicitly specified,
otherwise to an implementation-defined value. Requests cannot exceed Limits.
More info: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/`object`

`spec.source.persistentVolumeClaim.spec.selector`selector is a label query over volumes to consider for binding.`object`

`spec.source.persistentVolumeClaim.spec.selector.matchExpressions`matchExpressions is a list of label selector requirements. The requirements are ANDed.`array`

`spec.source.persistentVolumeClaim.spec.selector.matchExpressions.key`key is the label key that the selector applies to.`string`

`spec.source.persistentVolumeClaim.spec.selector.matchExpressions.operator`operator represents a key's relationship to a set of values.
Valid operators are In, NotIn, Exists and DoesNotExist.`string`

`spec.source.persistentVolumeClaim.spec.selector.matchExpressions.values`values is an array of string values. If the operator is In or NotIn,
the values array must be non-empty. If the operator is Exists or DoesNotExist,
the values array must be empty. This array is replaced during a strategic
merge patch.`array`

`spec.source.persistentVolumeClaim.spec.selector.matchLabels`matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels
map is equivalent to an element of matchExpressions, whose key field is "key", the
operator is "In", and the values array contains only "value". The requirements are ANDed.`object`

`spec.source.persistentVolumeClaim.spec.storageClassName`storageClassName is the name of the StorageClass required by the claim.
More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#class-1`string`

`spec.source.persistentVolumeClaim.spec.volumeAttributesClassName`volumeAttributesClassName may be used to set the VolumeAttributesClass used by this claim.
If specified, the CSI driver will create or update the volume with the attributes defined
in the corresponding VolumeAttributesClass. This has a different purpose than storageClassName,
it can be changed after the claim is created. An empty string value means that no VolumeAttributesClass
will be applied to the claim but it's not allowed to reset this field to empty string once it is set.
If unspecified and the PersistentVolumeClaim is unbound, the default VolumeAttributesClass
will be set by the persistentvolume controller if it exists.
If the resource referred to by volumeAttributesClass does not exist, this PersistentVolumeClaim will be
set to a Pending state, as reflected by the modifyVolumeStatus field, until such as a resource
exists.
More info: https://kubernetes.io/docs/concepts/storage/volume-attributes-classes/
(Alpha) Using this field requires the VolumeAttributesClass feature gate to be enabled.`string`

`spec.source.persistentVolumeClaim.spec.volumeMode`volumeMode defines what type of volume is required by the claim.
Value of Filesystem is implied when not included in claim spec.`string`

`spec.source.persistentVolumeClaim.spec.volumeName`volumeName is the binding reference to the PersistentVolume backing this claim.`string`

`spec.source.persistentVolumeClaim.status`status represents the current information/status of a persistent volume claim.
Read-only.
More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims`object`

`spec.source.persistentVolumeClaim.status.accessModes`accessModes contains the actual access modes the volume backing the PVC has.
More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#access-modes-1`array`

`spec.source.persistentVolumeClaim.status.allocatedResourceStatuses`allocatedResourceStatuses stores status of resource being resized for the given PVC.
Key names follow standard Kubernetes label syntax. Valid values are either:
 * Un-prefixed keys:
 - storage - the capacity of the volume.
 * Custom resources must use implementation-defined prefixed names such as "example.com/my-custom-resource"
Apart from above values - keys that are unprefixed or have kubernetes.io prefix are considered
reserved and hence may not be used.

ClaimResourceStatus can be in any of following states:
 - ControllerResizeInProgress:
 State set when resize controller starts resizing the volume in control-plane.
 - ControllerResizeFailed:
 State set when resize has failed in resize controller with a terminal error.
 - NodeResizePending:
 State set when resize controller has finished resizing the volume but further resizing of
 volume is needed on the node.
 - NodeResizeInProgress:
 State set when kubelet starts resizing the volume.
 - NodeResizeFailed:
 State set when resizing has failed in kubelet with a terminal error. Transient errors don't set
 NodeResizeFailed.
For example: if expanding a PVC for more capacity - this field can be one of the following states:
 - pvc.status.allocatedResourceStatus['storage'] = "ControllerResizeInProgress"
 - pvc.status.allocatedResourceStatus['storage'] = "ControllerResizeFailed"
 - pvc.status.allocatedResourceStatus['storage'] = "NodeResizePending"
 - pvc.status.allocatedResourceStatus['storage'] = "NodeResizeInProgress"
 - pvc.status.allocatedResourceStatus['storage'] = "NodeResizeFailed"
When this field is not set, it means that no resize operation is in progress for the given PVC.

A controller that receives PVC update with previously unknown resourceName or ClaimResourceStatus
should ignore the update for the purpose it was designed. For example - a controller that
only is responsible for resizing capacity of the volume, should ignore PVC updates that change other valid
resources associated with PVC.

This is an alpha field and requires enabling RecoverVolumeExpansionFailure feature.`object`

`spec.source.persistentVolumeClaim.status.allocatedResources`allocatedResources tracks the resources allocated to a PVC including its capacity.
Key names follow standard Kubernetes label syntax. Valid values are either:
 * Un-prefixed keys:
 - storage - the capacity of the volume.
 * Custom resources must use implementation-defined prefixed names such as "example.com/my-custom-resource"
Apart from above values - keys that are unprefixed or have kubernetes.io prefix are considered
reserved and hence may not be used.

Capacity reported here may be larger than the actual capacity when a volume expansion operation
is requested.
For storage quota, the larger value from allocatedResources and PVC.spec.resources is used.
If allocatedResources is not set, PVC.spec.resources alone is used for quota calculation.
If a volume expansion capacity request is lowered, allocatedResources is only
lowered if there are no expansion operations in progress and if the actual volume capacity
is equal or lower than the requested capacity.

A controller that receives PVC update with previously unknown resourceName
should ignore the update for the purpose it was designed. For example - a controller that
only is responsible for resizing capacity of the volume, should ignore PVC updates that change other valid
resources associated with PVC.

This is an alpha field and requires enabling RecoverVolumeExpansionFailure feature.`object`

`spec.source.persistentVolumeClaim.status.capacity`capacity represents the actual resources of the underlying volume.`object`

`spec.source.persistentVolumeClaim.status.conditions`conditions is the current Condition of persistent volume claim. If underlying persistent volume is being
resized then the Condition will be set to 'Resizing'.`array`

`spec.source.persistentVolumeClaim.status.conditions.lastProbeTime`lastProbeTime is the time we probed the condition.`string`

`spec.source.persistentVolumeClaim.status.conditions.lastTransitionTime`lastTransitionTime is the time the condition transitioned from one status to another.`string`

`spec.source.persistentVolumeClaim.status.conditions.message`message is the human-readable message indicating details about last transition.`string`

`spec.source.persistentVolumeClaim.status.conditions.reason`reason is a unique, this should be a short, machine understandable string that gives the reason
for condition's last transition. If it reports "Resizing" that means the underlying
persistent volume is being resized.`string`

`spec.source.persistentVolumeClaim.status.conditions.type`PersistentVolumeClaimConditionType is a valid value of PersistentVolumeClaimCondition.Type`string`

`spec.source.persistentVolumeClaim.status.currentVolumeAttributesClassName`currentVolumeAttributesClassName is the current name of the VolumeAttributesClass the PVC is using.
When unset, there is no VolumeAttributeClass applied to this PersistentVolumeClaim
This is an alpha field and requires enabling VolumeAttributesClass feature.`string`

`spec.source.persistentVolumeClaim.status.modifyVolumeStatus`ModifyVolumeStatus represents the status object of ControllerModifyVolume operation.
When this is unset, there is no ModifyVolume operation being attempted.
This is an alpha field and requires enabling VolumeAttributesClass feature.`object`

`spec.source.persistentVolumeClaim.status.modifyVolumeStatus.status`status is the status of the ControllerModifyVolume operation. It can be in any of following states:
 - Pending
 Pending indicates that the PersistentVolumeClaim cannot be modified due to unmet requirements, such as
 the specified VolumeAttributesClass not existing.
 - InProgress
 InProgress indicates that the volume is being modified.
 - Infeasible
 Infeasible indicates that the request has been rejected as invalid by the CSI driver. To
 resolve the error, a valid VolumeAttributesClass needs to be specified.
Note: New statuses can be added in the future. Consumers should check for unknown statuses and fail appropriately.`string`

`spec.source.persistentVolumeClaim.status.modifyVolumeStatus.targetVolumeAttributesClassName`targetVolumeAttributesClassName is the name of the VolumeAttributesClass the PVC currently being reconciled`string`

`spec.source.persistentVolumeClaim.status.phase`phase represents the current phase of PersistentVolumeClaim.`string`

`spec.type`DataExportType defines a method of achieving data transfer.`string`

### `status` fields​

FieldDescriptionType

`status.stage`DataExportStage defines different stages for DataExport when its Status changes
from Initial to Failed/Successful.`string`

`status.status`DataExportStatus defines a status of DataExport.`string`

In this topic:
