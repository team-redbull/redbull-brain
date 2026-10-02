# NodeDrain CRD Reference

Source: https://docs.portworx.com/portworx-enterprise/reference/crd/nodedrain (Portworx Enterprise latest)

NodeDrain CRD Reference | Portworx Enterprise Documentation

NodeDrain (`storagenode.io/v1`, kind NodeDrain) is a namespaced custom resource that the Portworx Operator creates and reconciles to track the drain lifecycle of a single Kubernetes node during migration of its datastore from PX-StoreV1 to PX-StoreV2. The operator creates one NodeDrain custom resource per node (or per batch of storageless nodes) being drained and updates its `status` as the node progresses through cordoning, data evacuation, and node cleanup. For the full workflow, see Migrate Portworx Datastore from PX-StoreV1 to PX-StoreV2.

To inspect a NodeDrain custom resource:

```

kubectl get nodedrain -n <portworx>

kubectl describe nodedrain <node-drain-name> -n <portworx>

```

## NodeDrain​

FieldDescriptionType

`apiVersion`APIVersion defines the versioned schema of this representation of an object.
Servers should convert recognized schemas to the latest internal value and
may reject unrecognized values.
More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources`string`

`kind`Kind is a string value representing the REST resource that this object represents.
Servers may infer this value from the endpoint to which the client submits requests.
Cannot be updated.
In CamelCase.
More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds`string`

`spec`NodeDrainSpec defines the desired state of the drain operation.`object`

`status`Observed state of the drain operation.`object`

### `spec` fields​

FieldDescriptionType

`spec.type`Identifies the drain workflow this custom resource drives. For the PX-StoreV1-to-V2 migration workflow, this is always `PXStoreMigration`.`string`

`spec.sourceNodes`Portworx node IDs of the source nodes being drained.`array`

`spec.targetNodes`Portworx node IDs of the target nodes to which the pool drain should evacuate data. May be empty, in which case the pool drain selects target nodes itself.`array`

`spec.isStoragelessNode`Specifies whether the source node is a storageless node rather than a storage node.`boolean`

`spec.restart`Set by the StorageCluster controller (or an operator) to request that the NodeDrain controller replay unfinished steps from the first condition that hasn't succeeded. The controller acts only when `spec.restart.attempt` is greater than `status.lastRestart.attempt`.`object`

`spec.restart.attempt`A monotonically increasing counter that identifies this restart request.`integer`

`spec.restart.reason`Explanation of why the restart was requested.`string`

`spec.restart.timestamp`When the restart request was written.`string`

### `status` fields​

FieldDescriptionType

`status.phase`The current phase of the drain operation. See `status.phase` values.`string`

`status.jobID`The ID of the underlying Portworx job for the current phase, for example, the pool drain job. Empty when the current phase has no associated job.`string`

`status.nextState`The phase to which the controller plans to transition next. Empty for terminal phases (`Completed`, `Cancelled`, `Failed`).`string`

`status.repl3VolumeIds`IDs of volumes that were running with replication factor 3 and were temporarily reduced to replication factor 2 during the drain so that they can be restored to replication factor 3 afterward. Discovered once, early in the drain; volumes created after discovery aren't added to this list.`array`

`status.conditions`Tracks the observed state of each major workflow stage. Each entry corresponds to one stage, for example, `VolumeAttachmentsDrained` or `PoolDrainComplete`, and is updated as the controller progresses.`array`

`status.conditions.type`The workflow stage that this condition reports. See `status.conditions` types.`string`

`status.conditions.reason`Short CamelCase token for the condition's current status: `InProgress`, `Succeeded`, `Failed`, or `Paused`.`string`

`status.conditions.message`Details about the current state or failure.`string`

`status.conditions.lastTransitionTime`When this condition last changed status.`string`

`status.retries`Per-step retry counts, keyed by condition type and persisted so that retry counts survive operator restarts.`object`

`status.stepTimers`The time when each long-running step first started, keyed by condition type and persisted so that step timeouts survive operator restarts.`object`

`status.lastError`The most recent failure that moved the custom resource into the `Failed` phase. Cleared when a `spec.restart` request is accepted.`object`

`status.lastError.step`The condition type of the stage that failed.`string`

`status.lastError.reason`Short CamelCase token that describes why the step failed.`string`

`status.lastError.message`Complete error message.`string`

`status.lastError.retryable`Specifies whether the failure is transient and can be retried automatically or resolved with an operator restart.`boolean`

`status.lastError.retries`The retry count at the time of the final failure.`integer`

`status.lastError.lastObserved`When this error was last recorded.`string`

`status.lastPhaseChangeAt`When `status.phase` was last updated.`string`

`status.lastRestart`The most recently accepted `spec.restart` request.`object`

`status.lastRestart.attempt`Mirrors the accepted `spec.restart.attempt`.`integer`

`status.lastRestart.reason`Mirrors the accepted `spec.restart.reason`.`string`

`status.lastRestart.acceptedAt`When the controller recorded acceptance of the restart request.`string`

`status.preflight`Results of the per-node preflight checks that run before cordoning.`object`

`status.preflight.verdict`Overall preflight result: `Passed` or `Failed`.`string`

`status.preflight.checks`Individual check results.`array`

`status.preflight.checks.name`The check's identifier, for example, `KVDBQuorumHealthy` or `SufficientFreeSpaceForDrain`.`string`

`status.preflight.checks.passed`Specifies whether this check succeeded.`boolean`

`status.preflight.checks.message`Details returned by the check, especially on failure.`string`

`status.preflight.checks.lastRun`When this check last ran.`string`

`status.preflight.lastEvaluated`When preflight was last run.`string`

### `status.phase` values​

ValueDescription

`NotStarted`Initial state. Preflight checks run first; if they pass, the node is cordoned and volume attachments are evacuated. Advances to `ReducingVolumeReplicas` (three-storage-node clusters) or `Pending` once the pool drain job is submitted.

`ReducingVolumeReplicas`Three-storage-node clusters only. Replication-factor-3 volumes on the source node are being reduced to replication factor 2 before the pool drain.

`Pending`The pool drain job has been submitted and is queued.

`Running`The pool drain job is actively evacuating data.

`Paused`The underlying pool drain job is paused.

`Cancelled`The pool drain job was canceled. The migration is marked `Failed`; restarting resets this custom resource to `NotStarted`.

`Drained`The pool drain job finished; all data has been evacuated from the source node's pools.

`RestoringVolumeReplicas`Three-storage-node clusters only. Volumes temporarily reduced to replication factor 2 are being restored to replication factor 3.

`NodeWipeRunning`The node-wiper job is running on the source node.

`PxRestarting`Portworx is restarting on the source node with PX-StoreV2.

`DeletingOfflineNodes`The source node is being removed from Portworx cluster membership.

`Completed`The drain operation finished successfully.

`Failed`The drain operation failed. See `status.lastError` for details.

`Unknown`The phase couldn't be determined.

### `status.conditions` types​

TypeDescription

`PreflightPassed`Per-node preflight checks passed before the drain workflow begins.

`K8sNodeCordoned`The source Kubernetes node was marked unschedulable.

`VolumeAttachmentsDrained`All volume attachments were moved off the source node.

`VolumeRepl3Reduced`Three-storage-node clusters only. Replication-factor-3 volumes with a replica on the source node were temporarily reduced to replication factor 2.

`PoolDrainComplete`The pool drain job finished; all data was evacuated from the source node.

`PXStopped`Portworx was stopped on the source node.

`NodesRemovedFromCluster`The source node was removed from Portworx cluster membership.

`NodeWipeComplete`The storage wipe on the source node finished.

`CloudDriveConfigMapCleared`Cloud storage only. The source node's entry was removed from the Portworx cloud-drive ConfigMap.

`StorageProvisioned`New storage was provisioned on the source node after restart.

`PXRestarted`Portworx restarted and is healthy on the source node.

`KVDBHealthy`All KVDB members are healthy after the node rejoined the cluster.

`VolumeRepl3Restored`Three-storage-node clusters only. Replication factor 3 was restored on volumes after the drain phase completed.

`NodeUncordoned`The source node was made schedulable again after migration.

`DrainCompleted`The full drain and migration workflow completed successfully for this node.

The `reason` field for each condition has one of the following values: `InProgress`, `Succeeded`, `Failed`, or `Paused`.
