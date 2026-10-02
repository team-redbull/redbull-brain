# ReverseProtectionGroup CRD reference

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/acm-dr/crd-reference/reverse-protection-group (Portworx Enterprise latest)

ReverseProtectionGroup CRD reference | Portworx Enterprise Documentation

The `ReverseProtectionGroup` CRD represents the reverse direction configuration for a ProtectionGroup, allowing users to override settings for the reverse DR direction (secondary to primary). This CRD has a 1:1 mapping with ProtectionGroup and is managed by the ProtectionGroup controller.

## Example​

```

apiVersion: multicluster.portworx.com/v1alpha1

kind: ReverseProtectionGroup

metadata:

  name: <name>            # Name of the ReverseProtectionGroup

  namespace: <namespace>  # Namespace for the ReverseProtectionGroup

spec: {}                  # No required fields under spec

```

## ReverseProtectionGroup​

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

`spec`ReverseProtectionGroupSpec defines the configuration for reverse direction disaster recovery.
This contains the settings needed to protect data in the opposite direction (from secondary back to primary).
This type is shared between the ProtectionGroup subresource and the standalone ReverseProtectionGroup CRD.`object`

`status`ReverseProtectionGroupStatus defines the observed state of ReverseProtectionGroup.`object`

### spec fields​

FieldDescriptionType

`advanceConfiguration`AdvanceConfiguration provides fine-grained migration control options for reverse direction.
If not specified, the AdvanceConfiguration from the main ProtectionGroup is used.`object`

`advanceConfiguration.applicationLifecycleHooks`ApplicationLifecycleHooks defines the hooks that should be executed before and after application migration.`object`

`advanceConfiguration.applicationLifecycleHooks.postMigrationHook`PostMigrationHook is the list of hooks that should be executed after application migration completes.`object`

`advanceConfiguration.applicationLifecycleHooks.preMigrationHook`PreMigrationHook is the list of hooks that should be executed before application migration starts.`object`

`advanceConfiguration.ignoreDeletedNamespacesAtSource`SkipDeletedNamespaces determines whether namespaces that have been deleted should be skipped during migration.`boolean`

`advanceConfiguration.ignoreOwnerReferencesValidation`IgnoreOwnerReferencesValidation specifies whether the migration should ignore checks related to owner references.`boolean`

`advanceConfiguration.purgeDeletedResourcesAtSource`PurgeDeletedResources specifies whether deleted resources (that existed before but no longer exist) should be removed from destination cluster.`boolean`

`advanceConfiguration.resourceTransformations`ResourceTransformations is a list of transformation specifications that should be applied to Kubernetes resources before they are migrated.`array`

`advanceConfiguration.skipServiceUpdate`SkipServiceUpdate determines whether service updates should be skipped during migration.`boolean`

`namespaceSelection`NamespaceSelection controls which namespaces are in the reverse protection group.
If not specified, the NamespaceSelection from the main ProtectionGroup is used.`object`

`namespaceSelection.namespaceSelectors`NamespaceSelectors selects namespaces by label.`array`

`namespaceSelection.namespaceSelectors.label`Key is the label key to match.`string`

`namespaceSelection.namespaceSelectors.operator`Operator is the label operator to use.`string`

`namespaceSelection.namespaceSelectors.value`Value is the label value to match.`string`

`namespaceSelection.namespaces`Namespaces is the explicit list of namespaces that are part of this`array`

`replicationSchedulePolicy`ReplicationSchedulePolicy defines the replication schedule for the reverse direction.
If not specified, the ReplicationSchedulePolicy from the main ProtectionGroup is used.`object`

`replicationSchedulePolicy.interval`Interval policy that will be triggered at the specified interval`object`

`replicationSchedulePolicy.interval.intervalMinutes`IntervalMinutes specifies the interval in minutes between triggers.`integer`

`replicationSchedulePolicy.interval.retain`Retain specifies the number of backups to retain.`integer`

`replicationSchedulePolicy.suspend`Suspend indicates whether the migrations for the protection group are to be suspended.`boolean`

`resourceConfiguration`ResourceConfiguration for the reverse direction.
If not specified, the ResourceConfiguration from the main ProtectionGroup is used.`object`

`resourceConfiguration.customSelection`ResourceSelector controls which resources and volumes within the selected namespaces are protected.`object`

`resourceConfiguration.customSelection.excludeLabelSelectors`ExcludeFilters is a set of label-based selectors used to filter the objects that should be excluded from the migration.`array`

`resourceConfiguration.customSelection.excludeLabelSelectors.label`Key is the label key to match.`string`

`resourceConfiguration.customSelection.excludeLabelSelectors.operator`Operator is the label operator to use.`string`

`resourceConfiguration.customSelection.excludeLabelSelectors.value`Value is the label value to match.`string`

`resourceConfiguration.customSelection.includeApplicationVolumes`IncludeApplicationVolumes specifies whether application volumes (PVCs) should be included in the protection group.`boolean`

`resourceConfiguration.customSelection.includeCIDRBasedNetworkPolicies`IncludeCIDRBasedNetworkPolicies specifies whether network policies with CIDR-based rules should be included in the migration.`boolean`

`resourceConfiguration.customSelection.includeLabelSelectors`IncludeLabelSelectors is a set of label-based selectors used to filter the objects that should be included in the migration.`array`

`resourceConfiguration.customSelection.includeLabelSelectors.label`Key is the label key to match.`string`

`resourceConfiguration.customSelection.includeLabelSelectors.operator`Operator is the label operator to use.`string`

`resourceConfiguration.customSelection.includeLabelSelectors.value`Value is the label value to match.`string`

`resourceConfiguration.customSelection.resourceTypeSelector`ResourceTypeSelector controls which resource kinds are included or excluded from protection.`object`

`resourceConfiguration.customSelection.resourceTypeSelector.exclude`Exclude is a list of resource types that should be excluded from the migration.`array`

`resourceConfiguration.customSelection.resourceTypeSelector.include`Include is a list of optional Kubernetes resource types that should be included in the migration.`array`

`resourceConfiguration.customSelection.startApplicationsAfterFailover`StartApplicationsAfterFailover determines whether migrated applications should be started after failover.`boolean`

`resourceConfiguration.includeAllResources`IncludeAllResources specifies whether all resources in the selected namespaces should be included in the protection group.`boolean`

### status fields​

FieldDescriptionType

`phase`Phase represents the current phase of the reverse protection group.`string`

In this topic:
