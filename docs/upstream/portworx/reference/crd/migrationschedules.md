# MigrationSchedule CRD reference

Source: https://docs.portworx.com/portworx-enterprise/reference/crd/migrationschedules (Portworx Enterprise 3.6)

MigrationSchedule CRD reference | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

MigrationSchedule represents a scheduled migration object.

## MigrationSchedule​

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

`spec`MigrationScheduleSpec is the spec used to schedule migrations`object`

`status`MigrationScheduleStatus is the status of a migration schedule`object`

### `spec` fields​

FieldDescriptionType

`spec.autoSuspend`AutoSuspend enables automatic suspension of DR migration schedules on the source cluster in case of a disaster`boolean`

`spec.suspend`Suspend will suspend the schedule upon creation`boolean`

`spec.template`Template is the migration spec template`object`

`spec.template.spec`MigrationSpec is the spec used to migrate apps between clusterpairs`object`

`spec.template.spec.adminClusterPair`AdminClusterPair is the name of the admin cluster pair used for managing the migration.`string`

`spec.template.spec.clusterPair`ClusterPair is the name of the cluster pair using which the migration will be performed.`string`

`spec.template.spec.excludeResourceTypes`ExcludeResourceTypes is a list of resource types that should be excluded from the migration.`array`

`spec.template.spec.excludeSelectors`ExcludeSelectors is a set of label-based selectors used to filter out specific objects from the migration.`object`

`spec.template.spec.ignoreOwnerReferencesCheck`IgnoreOwnerReferencesCheck specifies whether the migration should ignore checks related to owner references.`boolean`

`spec.template.spec.includeNetworkPolicyWithCIDR`IncludeNetworkPolicyWithCIDR determines whether network policies with CIDR-based rules should be included in the migration.`boolean`

`spec.template.spec.includeOptionalResourceTypes`IncludeOptionalResourceTypes is a list of optional Kubernetes resource types that should be included in the migration.`array`

`spec.template.spec.includeResources`IncludeResources specifies whether Kubernetes resources (such as Deployments, ConfigMaps, etc.) should be included in the migration.`boolean`

`spec.template.spec.includeVolumes`IncludeVolumes specifies whether underlying volumes should be included in the migration.`boolean`

`spec.template.spec.namespaceSelectors`NamespaceSelectors is a set of label-based selectors used to filter which namespaces should be migrated.`object`

`spec.template.spec.namespaces`Namespaces is a list of namespaces that should be migrated to the destination cluster.`array`

`spec.template.spec.postExecRule`PostExecRule is the name of the rule that should be executed after migration completes.`string`

`spec.template.spec.preExecRule`PreExecRule is the name of the rule that should be executed before migration starts.`string`

`spec.template.spec.purgeDeletedResources`PurgeDeletedResources specifies whether deleted resources (that existed before but no longer exist) should be removed from the destination cluster.`boolean`

`spec.template.spec.selectors`Selectors is a set of label-based selectors used to filter the objects that should be included in the migration.`object`

`spec.template.spec.skipDeletedNamespaces`SkipDeletedNamespaces determines whether namespaces that have been deleted should be skipped during migration.`boolean`

`spec.template.spec.skipServiceUpdate`SkipServiceUpdate determines whether service updates should be skipped during migration.`boolean`

`spec.template.spec.startApplications`StartApplications determines whether the migrated applications should be started on the destination cluster after migration.`boolean`

`spec.template.spec.transformSpecs`TransformSpecs is a list of transformation specifications that should be applied to Kubernetes resources before they are migrated.`array`

In this topic:
