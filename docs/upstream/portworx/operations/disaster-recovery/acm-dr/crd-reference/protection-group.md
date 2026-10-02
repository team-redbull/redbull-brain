# ProtectionGroup CRD reference

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/acm-dr/crd-reference/protection-group (Portworx Enterprise 3.6)

ProtectionGroup CRD reference | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

The `ProtectionGroup` CRD represents a protection group consisting of a set of applications and schedules for running DR migrations between clusters.

## Example​

```

apiVersion: multicluster.portworx.com/v1alpha1

kind: ProtectionGroup

metadata:

  name: <protection-group-name>

  namespace: <namespace>

spec:

  disasterRecoveryPairRef: <dr-pair-name>   # Name of the DisasterRecoveryPair resource

  namespaceSelection:                        # Namespaces in this protection group

    namespaces:

      - <namespace-name>

  replicationSchedulePolicy:                 # When DR replications should run

    interval:

      intervalMinutes: <minutes>             # Required within interval

```

## ProtectionGroup​

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

`spec`ProtectionGroupSpec defines the desired state of ProtectionGroup.`object`

`status`ProtectionGroupStatus defines the observed state of ProtectionGroup.`object`

### spec fields​

FieldDescriptionType

`spec.advanceConfiguration`AdvanceConfiguration provides fine-grained migration control options. .`object`

`spec.advanceConfiguration.applicationLifecycleHooks`ApplicationLifecycleHooks defines the hooks that should be executed before and after application migration.`object`

`spec.advanceConfiguration.applicationLifecycleHooks.postMigrationHook`PostMigrationHook is the list of hooks that should be executed after application migration completes.`object`

`spec.advanceConfiguration.applicationLifecycleHooks.preMigrationHook`PreMigrationHook is the list of hooks that should be executed before application migration starts.`object`

`spec.advanceConfiguration.ignoreDeletedNamespacesAtSource`SkipDeletedNamespaces determines whether namespaces that have been deleted should be skipped during migration.`boolean`

`spec.advanceConfiguration.ignoreOwnerReferencesValidation`IgnoreOwnerReferencesValidation specifies whether the migration should ignore checks related to owner references.`boolean`

`spec.advanceConfiguration.purgeDeletedResourcesAtSource`PurgeDeletedResources specifies whether deleted resources (that existed before but no longer exist) should be removed from destination cluster.`boolean`

`spec.advanceConfiguration.resourceTransformations`ResourceTransformations is a list of transformation specifications that should be applied to Kubernetes resources before they are migrated.`array`

`spec.advanceConfiguration.resourceTransformations`InlineResourceTransformation stores a full stork.libopenstorage.org/v1alpha1 ResourceTransformation object inline.`object`

`spec.advanceConfiguration.skipServiceUpdate`SkipServiceUpdate determines whether service updates should be skipped during migration.`boolean`

`spec.disasterRecoveryPairRef`DisasterRecoveryPairRef is the name of the DisasterRecoveryPair resource
that defines the source/destination clusters and backup location.`string`

`spec.namespaceSelection`NamespaceSelection controls which namespaces are in this protection group.
At least one of namespaces or namespaceSelector must be provided.`object`

`spec.namespaceSelection.namespaceSelectors`NamespaceSelectors selects namespaces by label.`array`

`spec.namespaceSelection.namespaceSelectors.label`Key is the label key to match.`string`

`spec.namespaceSelection.namespaceSelectors.operator`Operator is the label operator to use.`string`

`spec.namespaceSelection.namespaceSelectors.value`Value is the label value to match.`string`

`spec.namespaceSelection.namespaces`Namespaces is the explicit list of namespaces that are part of this`array`

`spec.replicationSchedulePolicy`ReplicationSchedulePolicy defines when DR replications for this protection group should run.
At least one schedule policy (interval) should be specified.`object`

`spec.replicationSchedulePolicy.interval`Interval policy that will be triggered at the specified interval`object`

`spec.replicationSchedulePolicy.interval.intervalMinutes`IntervalMinutes specifies the interval in minutes between triggers.`integer`

`spec.replicationSchedulePolicy.interval.retain`Retain specifies the number of backups to retain.`integer`

`spec.replicationSchedulePolicy.suspend`Suspend indicates whether the migrations for the protection group are to be suspended.`boolean`

`spec.resourceConfiguration`ResourceConfiguration defines the resource configuration, including label rules, PVC inclusion and PVC label rules, and resource type filters.`object`

`spec.resourceConfiguration.customSelection`ResourceSelector controls which resources and volumes within the selected namespaces are protected.`object`

`spec.resourceConfiguration.customSelection.excludeLabelSelectors`ExcludeFilters is a set of label-based selectors used to filter the objects that should be excluded from the migration.`array`

`spec.resourceConfiguration.customSelection.excludeLabelSelectors.label`Key is the label key to match.`string`

`spec.resourceConfiguration.customSelection.excludeLabelSelectors.operator`Operator is the label operator to use.`string`

`spec.resourceConfiguration.customSelection.excludeLabelSelectors.value`Value is the label value to match.`string`

`spec.resourceConfiguration.customSelection.includeApplicationVolumes`IncludeApplicationVolumes specifies whether application volumes (PVCs) should
be included in the protection group.`boolean`

`spec.resourceConfiguration.customSelection.includeCIDRBasedNetworkPolicies`IncludeCIDRBasedNetworkPolicies specifies whether network policies with CIDR-based rules should be included in the migration.`boolean`

`spec.resourceConfiguration.customSelection.includeLabelSelectors`IncludeLabelSelectors is a set of label-based selectors used to filter the objects that should be included in the migration.`array`

`spec.resourceConfiguration.customSelection.includeLabelSelectors.label`Key is the label key to match.`string`

`spec.resourceConfiguration.customSelection.includeLabelSelectors.operator`Operator is the label operator to use.`string`

`spec.resourceConfiguration.customSelection.includeLabelSelectors.value`Value is the label value to match.`string`

`spec.resourceConfiguration.customSelection.resourceTypeSelector`ResourceTypeSelector controls which resource kinds are included or excluded from protection.`object`

`spec.resourceConfiguration.customSelection.resourceTypeSelector.exclude`Exclude is a list of resource types that should be excluded from the migration.`array`

`spec.resourceConfiguration.customSelection.resourceTypeSelector.include`Include is a list of optional Kubernetes resource types that should be included in the migration.`array`

`spec.resourceConfiguration.customSelection.startApplicationsAfterFailover`StartApplicationsAfterFailover determines whether migrated applications should be started after failover.`boolean`

`spec.resourceConfiguration.includeAllResources`IncludeAllResources specifies whether all resources in the selected namespaces should be included in the protection group.`boolean`

### status fields​

FieldDescriptionType

`status.activeSite`ActiveSite indicates which cluster site is currently active (Primary or Secondary).`string`

`status.applicationActivated`ApplicationActivated indicates whether the application is activated.`boolean`

`status.compliant`Compliant represents the compliance status of the protection group.`object`

`status.compliant.reason`Reason is short description of why the resource is in non compliant state.`string`

`status.compliant.status`Status: is true then resource is compliant and operational.`boolean`

`status.conditions`Conditions represent the latest available observations of the ProtectionGroup's state`array`

`status.conditions.lastTransitionTime`lastTransitionTime is the last time the condition transitioned from one status to another.
This should be when the underlying condition changed. If that is not known, then using the time when the API field changed is acceptable.`string`

`status.conditions.message`message is a human readable message indicating details about the transition.
This may be an empty string.`string`

`status.conditions.observedGeneration`observedGeneration represents the .metadata.generation that the condition was set based upon.
For instance, if .metadata.generation is currently 12, but the .status.conditions[x].observedGeneration is 9, the condition is out of date
with respect to the current state of the instance.`integer`

`status.conditions.reason`reason contains a programmatic identifier indicating the reason for the condition's last transition.
Producers of specific condition types may define expected values and meanings for this field,
and whether the values are considered a guaranteed API.
The value should be a CamelCase string.
This field may not be empty.`string`

`status.conditions.status`status of the condition, one of True, False, Unknown.`string`

`status.conditions.type`type of condition in CamelCase or in foo.example.com/CamelCase.`string`

`status.failbackNamespaces`FailbackNamespaces is the aggregated list of all namespaces that have been failed back.`array`

`status.failbackStatuses`FailbackStatuses contains status information for all failback operations.
Each entry is keyed by the DREvent UID that triggered the failback.`array`

`status.failbackStatuses.UID`UID is the unique identifier of the DR action that triggered this failback.`string`

`status.failbackStatuses.name`Name is the name of the DisasterRecoveryAction object created for this failback.`string`

`status.failbackStatuses.namespace`Namespace is the namespace of the DisasterRecoveryAction object created for this failback.`string`

`status.failbackStatuses.status`Status indicates the current status of the failback operation.`string`

`status.failoverNamespaces`FailoverNamespaces is the aggregated list of all namespaces that have been failed over.`array`

`status.failoverStatuses`FailoverStatuses contains status information for all failover operations.
Each entry is keyed by the DREvent UID that triggered the failover.`array`

`status.failoverStatuses.UID`UID is the unique identifier of the DR action that triggered this failover.`string`

`status.failoverStatuses.name`Name is the name of the DisasterRecoveryAction object created for this failover.`string`

`status.failoverStatuses.namespace`Namespace is the namespace of the DisasterRecoveryAction object created for this failover.`string`

`status.failoverStatuses.status`Status indicates the current status of the failover operation.`string`

`status.lastAgentUpdateTimestamp`LastAgentUpdateTimestamp is the time when the protection group status was last updated by the agent`string`

`status.migrationStatus`MigrationStatus groups recent migration runs by schedule policy type.`object`

`status.migrationStatus.creationTimestamp`CreationTimestamp is when the migration was created.`string`

`status.migrationStatus.finishTimestamp`FinishTimestamp is when the migration finished, if it has completed.`string`

`status.migrationStatus.name`Name is the name of the migration object created for this run.`string`

`status.migrationStatus.status`Status is the final (or current) status of the migration.`string`

`status.migrationStatus.summary`summary of the migration`object`

`status.migrationStatus.summary.elapsedTimeForResourceMigration`ElapsedTimeForResourceMigration provides the total time the
resource migration stage has been running or the total time
taken for the resource migration to complete if the volume migration has finished`string`

`status.migrationStatus.summary.elapsedTimeForVolumeMigration`ElapsedTimeForVolumeMigration provides the total time the
volume migration stage has been running or the total time
taken for the volume migration to complete if the volume migration has finished`string`

`status.migrationStatus.summary.migrationFailureReasons`MigrationFailureReasons provides the list of failure reasons for migration failures`array`

`status.migrationStatus.summary.numOfMigratedResources`NumberOfMigratedResources gives the total count of migrated k8s resources`integer`

`status.migrationStatus.summary.numOfMigratedVolumes`NumberOfMigratedVolumes gives the total count of successfully migrated volumes`integer`

`status.migrationStatus.summary.totalBytesMigrated`TotalBytesMigrated gives the total amount of bytes migrated across all the volumes`integer`

`status.migrationStatus.summary.totalNumberOfResources`TotalNumberOfResources gives the total count of resourcs`integer`

`status.migrationStatus.summary.totalNumberOfVolumes`TotalNumberOfVolumes gives the total count of volumes`integer`

`status.protectedNamespacesCount`ProtectedNamespacesCount is the count of namespaces currently protected by this protection group.`integer`

`status.protectionState`ProtectionState represents the overall state of the protection group.`string`

`status.reverseSpec`ReverseSpec defines the reverse direction configuration for this protection group.
This is used to track overridden spec attributes for the reverse DR direction (secondary to primary).
This is copied from the ReverseProtectionGroup CR created for the reverse direction.`object`

`status.reverseSpec.advanceConfiguration`AdvanceConfiguration provides fine-grained migration control options for reverse direction.
If not specified, the AdvanceConfiguration from the main ProtectionGroup is used.`object`

`status.reverseSpec.advanceConfiguration.applicationLifecycleHooks`ApplicationLifecycleHooks defines the hooks that should be executed before and after application migration.`object`

`status.reverseSpec.advanceConfiguration.applicationLifecycleHooks.postMigrationHook`PostMigrationHook is the list of hooks that should be executed after application migration completes.`object`

`status.reverseSpec.advanceConfiguration.applicationLifecycleHooks.preMigrationHook`PreMigrationHook is the list of hooks that should be executed before application migration starts.`object`

`status.reverseSpec.advanceConfiguration.ignoreDeletedNamespacesAtSource`SkipDeletedNamespaces determines whether namespaces that have been deleted should be skipped during migration.`boolean`

`status.reverseSpec.advanceConfiguration.ignoreOwnerReferencesValidation`IgnoreOwnerReferencesValidation specifies whether the migration should ignore checks related to owner references.`boolean`

`status.reverseSpec.advanceConfiguration.purgeDeletedResourcesAtSource`PurgeDeletedResources specifies whether deleted resources (that existed before but no longer exist) should be removed from destination cluster.`boolean`

`status.reverseSpec.advanceConfiguration.resourceTransformations`ResourceTransformations is a list of transformation specifications that should be applied to Kubernetes resources before they are migrated.`array`

`status.reverseSpec.advanceConfiguration.resourceTransformations`InlineResourceTransformation stores a full stork.libopenstorage.org/v1alpha1 ResourceTransformation object inline.`object`

`status.reverseSpec.advanceConfiguration.skipServiceUpdate`SkipServiceUpdate determines whether service updates should be skipped during migration.`boolean`

`status.reverseSpec.namespaceSelection`NamespaceSelection controls which namespaces are in the reverse protection group.
If not specified, the NamespaceSelection from the main ProtectionGroup is used.`object`

`status.reverseSpec.namespaceSelection.namespaceSelectors`NamespaceSelectors selects namespaces by label.`array`

`status.reverseSpec.namespaceSelection.namespaceSelectors.label`Key is the label key to match.`string`

`status.reverseSpec.namespaceSelection.namespaceSelectors.operator`Operator is the label operator to use.`string`

`status.reverseSpec.namespaceSelection.namespaceSelectors.value`Value is the label value to match.`string`

`status.reverseSpec.namespaceSelection.namespaces`Namespaces is the explicit list of namespaces that are part of this`array`

`status.reverseSpec.replicationSchedulePolicy`ReplicationSchedulePolicy defines the replication schedule for the reverse direction.
If not specified, the ReplicationSchedulePolicy from the main ProtectionGroup is used.`object`

`status.reverseSpec.replicationSchedulePolicy.interval`Interval policy that will be triggered at the specified interval`object`

`status.reverseSpec.replicationSchedulePolicy.interval.intervalMinutes`IntervalMinutes specifies the interval in minutes between triggers.`integer`

`status.reverseSpec.replicationSchedulePolicy.interval.retain`Retain specifies the number of backups to retain.`integer`

`status.reverseSpec.replicationSchedulePolicy.suspend`Suspend indicates whether the migrations for the protection group are to be suspended.`boolean`

`status.reverseSpec.resourceConfiguration`ResourceConfiguration for the reverse direction.
If not specified, the ResourceConfiguration from the main ProtectionGroup is used.`object`

`status.reverseSpec.resourceConfiguration.customSelection`ResourceSelector controls which resources and volumes within the selected namespaces are protected.`object`

`status.reverseSpec.resourceConfiguration.customSelection.excludeLabelSelectors`ExcludeFilters is a set of label-based selectors used to filter the objects that should be excluded from the migration.`array`

`status.reverseSpec.resourceConfiguration.customSelection.excludeLabelSelectors.label`Key is the label key to match.`string`

`status.reverseSpec.resourceConfiguration.customSelection.excludeLabelSelectors.operator`Operator is the label operator to use.`string`

`status.reverseSpec.resourceConfiguration.customSelection.excludeLabelSelectors.value`Value is the label value to match.`string`

`status.reverseSpec.resourceConfiguration.customSelection.includeApplicationVolumes`IncludeApplicationVolumes specifies whether application volumes (PVCs) should
be included in the protection group.`boolean`

`status.reverseSpec.resourceConfiguration.customSelection.includeCIDRBasedNetworkPolicies`IncludeCIDRBasedNetworkPolicies specifies whether network policies with CIDR-based rules should be included in the migration.`boolean`

`status.reverseSpec.resourceConfiguration.customSelection.includeLabelSelectors`IncludeLabelSelectors is a set of label-based selectors used to filter the objects that should be included in the migration.`array`

`status.reverseSpec.resourceConfiguration.customSelection.includeLabelSelectors.label`Key is the label key to match.`string`

`status.reverseSpec.resourceConfiguration.customSelection.includeLabelSelectors.operator`Operator is the label operator to use.`string`

`status.reverseSpec.resourceConfiguration.customSelection.includeLabelSelectors.value`Value is the label value to match.`string`

`status.reverseSpec.resourceConfiguration.customSelection.resourceTypeSelector`ResourceTypeSelector controls which resource kinds are included or excluded from protection.`object`

`status.reverseSpec.resourceConfiguration.customSelection.resourceTypeSelector.exclude`Exclude is a list of resource types that should be excluded from the migration.`array`

`status.reverseSpec.resourceConfiguration.customSelection.resourceTypeSelector.include`Include is a list of optional Kubernetes resource types that should be included in the migration.`array`

`status.reverseSpec.resourceConfiguration.customSelection.startApplicationsAfterFailover`StartApplicationsAfterFailover determines whether migrated applications should be started after failover.`boolean`

`status.reverseSpec.resourceConfiguration.includeAllResources`IncludeAllResources specifies whether all resources in the selected namespaces should be included in the protection group.`boolean`

`status.suspend`Suspend indicates whether the status of the migrations for the protection group is suspended.`boolean`

In this topic:
