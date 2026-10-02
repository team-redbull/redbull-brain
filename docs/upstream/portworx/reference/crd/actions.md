# Action CRD reference

Source: https://docs.portworx.com/portworx-enterprise/reference/crd/actions (Portworx Enterprise latest)

Action CRD reference | Portworx Enterprise Documentation

Action represents a task that will be performed once It is similar to a Kubernetes Job.

## Action​

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

`spec`ActionSpec specifies the type of Action`object`

`status`ActionStatus is the status of action operation`object`

### `spec` fields​

FieldDescriptionType

`spec.actionParameter`ActionParameter contains the parameters necessary for executing the specified action.`object`

`spec.actionParameter.failbackParameter`FailbackParameter contains configuration specific to failback actions.`object`

`spec.actionParameter.failbackParameter.excludeObjects`ExcludeObjects specifies specific objects to exclude from the DR operation.
Mutually exclusive with all other filtering flags (selectors, excludeSelectors, types, includeObjects).`array`

`spec.actionParameter.failbackParameter.excludeObjects.name`Name of the object`string`

`spec.actionParameter.failbackParameter.excludeObjects.namespace`Namespace of the object`string`

`spec.actionParameter.failbackParameter.excludeSelectors`ExcludeSelectors specifies label selectors that identify resources to be excluded from DR operations.`object`

`spec.actionParameter.failbackParameter.failbackNamespaces`FailbackNamespaces lists the namespaces that will be failed back to the original source cluster.`array`

`spec.actionParameter.failbackParameter.includeObjects`IncludeObjects specifies specific objects to include in the DR operation.
Mutually exclusive with all other filtering flags (selectors, excludeSelectors, types, excludeObjects).`array`

`spec.actionParameter.failbackParameter.includeObjects.name`Name of the object`string`

`spec.actionParameter.failbackParameter.includeObjects.namespace`Namespace of the object`string`

`spec.actionParameter.failbackParameter.migrationScheduleReference`MigrationScheduleReference is the name of the MigrationSchedule CR that this action references.`string`

`spec.actionParameter.failbackParameter.selectors`Selectors and ExcludeSelectors are mutually exclusive. Only one of these
may be set at a time to avoid ambiguous filtering of resources during DR
operations.`object`

`spec.actionParameter.failbackParameter.skipLastMileMigration`SkipLastMileMigration, when true, skips creating and waiting on the last-mile
Migration before activating workloads during failback.`boolean`

`spec.actionParameter.failbackParameter.types`Types restricts the DR operation to the specified Kubernetes resource kinds. If empty, all supported types are considered.`array`

`spec.actionParameter.failoverParameter`FailoverParameter contains configuration specific to failover actions.`object`

`spec.actionParameter.failoverParameter.excludeObjects`ExcludeObjects specifies specific objects to exclude from the DR operation.
Mutually exclusive with all other filtering flags (selectors, excludeSelectors, types, includeObjects).`array`

`spec.actionParameter.failoverParameter.excludeObjects.name`Name of the object`string`

`spec.actionParameter.failoverParameter.excludeObjects.namespace`Namespace of the object`string`

`spec.actionParameter.failoverParameter.excludeSelectors`ExcludeSelectors specifies label selectors that identify resources to be excluded from DR operations.`object`

`spec.actionParameter.failoverParameter.failoverNamespaces`FailoverNamespaces lists the namespaces that will be failed over to the destination cluster.`array`

`spec.actionParameter.failoverParameter.includeObjects`IncludeObjects specifies specific objects to include in the DR operation.
Mutually exclusive with all other filtering flags (selectors, excludeSelectors, types, excludeObjects).`array`

`spec.actionParameter.failoverParameter.includeObjects.name`Name of the object`string`

`spec.actionParameter.failoverParameter.includeObjects.namespace`Namespace of the object`string`

`spec.actionParameter.failoverParameter.migrationScheduleReference`MigrationScheduleReference is the name of the MigrationSchedule CR that this action references.`string`

`spec.actionParameter.failoverParameter.selectors`Selectors and ExcludeSelectors are mutually exclusive. Only one of these
may be set at a time to avoid ambiguous filtering of resources during DR
operations.`object`

`spec.actionParameter.failoverParameter.skipLastMileMigration`SkipLastMileMigration, when true, skips creating and waiting on the last-mile
Migration before activating workloads during failover.`boolean`

`spec.actionParameter.failoverParameter.skipSourceClusterDomainDeactivation`SkipSourceClusterDomainDeactivation, when true, skips deactivating the source cluster domain during failover.`boolean`

`spec.actionParameter.failoverParameter.skipSourceOperations`SkipSourceOperations, when true, skips performing operations on the source cluster as part of failover.`boolean`

`spec.actionParameter.failoverParameter.types`Types restricts the DR operation to the specified Kubernetes resource kinds. If empty, all supported types are considered.`array`

`spec.actionType`ActionType defines the type of action to be executed.
It can be one of the following:
 - failover
 - failback`string`

### `status` fields​

FieldDescriptionType

`status.finishTimestamp`FinishTimestamp records when the action reached a terminal state.`string`

`status.reason`Reason provides a human-readable explanation for the current status.`string`

`status.stage`ActionStageType is the stage of the action`string`

`status.status`ActionStatusType is the current status of the Action`string`

`status.summary`Summary contains a per-namespace breakdown of the action result.`object`

`status.summary.failbackSummary`FailbackSummaryItem contains per-namespace summaries for failback actions.`array`

`status.summary.failbackSummary.namespace`Namespace is the namespace on which the action was performed.`string`

`status.summary.failbackSummary.reason`Reason is a human-readable summary of the outcome for this namespace.`string`

`status.summary.failbackSummary.status`Status is the final status of the action for this namespace.`string`

`status.summary.failoverSummary`FailoverSummaryItem contains per-namespace summaries for failover actions.`array`

`status.summary.failoverSummary.namespace`Namespace is the namespace on which the action was performed.`string`

`status.summary.failoverSummary.reason`Reason is a human-readable summary of the outcome for this namespace.`string`

`status.summary.failoverSummary.status`Status is the final status of the action for this namespace.`string`

In this topic:
