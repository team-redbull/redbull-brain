# Rule CRD reference

Source: https://docs.portworx.com/portworx-enterprise/reference/crd/rules (Portworx Enterprise latest)

Rule CRD reference | Portworx Enterprise Documentation

Rule denotes an object to declare a rule that performs actions on pods.

## Rule​

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

### `rules` fields​

FieldDescriptionType

`rules.actions`Actions are actions to be performed on the pods selected using the selector`array`

`rules.actions.background`Background indicates that the action needs to be performed in the background`boolean`

`rules.actions.runInSinglePod`RunInSinglePod indicates that the action needs to be performed in a single pod
 from the list of pods that match the selector`boolean`

`rules.actions.type`Type is a type of the stork rule action`string`

`rules.actions.value`Value is the actual action value for e.g the command to run`string`

`rules.container`Container Name of the container in which to run the rule if there are
multiple containers in the pod`string`

`rules.podSelector`PodSelector is a map of key value pairs that are used to select the pods using their labels`object`

In this topic:
