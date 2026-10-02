# ApplicationRegistration CRD reference

Source: https://docs.portworx.com/portworx-enterprise/reference/crd/applicationregistrations (Portworx Enterprise 3.6)

ApplicationRegistration CRD reference | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

ApplicationRegistration to collect crd resources.

## ApplicationRegistration​

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

### `resources` fields​

FieldDescriptionType

`resources.customSuspendOptions`Some CRs can have nested servers which can be enabled/disabled
in addition to parent server
NestedSuspendOptions allow way to suspend such CR server`array`

`resources.keepStatus`KeepStatus if set to true collect status
while doing backup/migration/restore etc`boolean`

`resources.podsPath`PodsPath to help activate/deactivate crd upon migration`string`

`resources.stashStrategy`Clusterwide Operators will control the CRs in all namespaces
StashStrategy option if enabled will make sure as part of migration the CR does not get applied
if StashCR is enabled. The CR will be applied as part of app activation`object`

`resources.suspendOptions`SuspendOptions to disable parent CR upon migration/restore/clone`object`

In this topic:
