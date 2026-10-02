# ApplicationClone CRD reference

Source: https://docs.portworx.com/portworx-enterprise/reference/crd/applicationclones (Portworx Enterprise latest)

ApplicationClone CRD reference | Portworx Enterprise Documentation

ApplicationClone represents the cloning of application in different namespaces.

## ApplicationClone​

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

`spec`ApplicationCloneSpec defines the spec to create an application clone`object`

`status`ApplicationCloneStatus defines the status of the clone`object`

### `spec` fields​

FieldDescriptionType

`spec.destinationNamespace`DestinationNamespace is a must parameter to tell the cloning object
where to place the application objects`string`

`spec.includeOptionalResourceTypes`IncludeOptionalResourceTypes is a list of optional resource types to include in the cloning`array`

`spec.postExecRule`PostExecRule is the name of the rule to execute after cloning`string`

`spec.preExecRule`PreExecRule is the name of the rule to execute before cloning`string`

`spec.replacePolicy`ReplacePolicy to decide how to react when a object conflict occurs in the cloning process`string`

`spec.selectors`Selectors for label on objects`object`

`spec.sourceNamespace`SourceNamespace can be optional, and we can check in the code that we are using
the same namespace in which we are creating the cloning object`string`

### `status` fields​

FieldDescriptionType

`status.resources.status`ApplicationCloneStatusType defines status of the application being cloned`string`

`status.stage`Stage of the cloning process`string`

`status.status`Status of the cloning process`string`

`status.volumes.status`ApplicationCloneStatusType defines status of the application being cloned`string`

In this topic:
