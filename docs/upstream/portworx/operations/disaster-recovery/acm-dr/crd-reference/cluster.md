# Cluster CRD reference

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/acm-dr/crd-reference/cluster (Portworx Enterprise latest)

Cluster CRD reference | Portworx Enterprise Documentation

The `Cluster` CRD represents a workload cluster and exposes DR readiness, Portworx installation status, cluster health status, platform, and capacity information.

## Example​

```

apiVersion: multicluster.portworx.com/v1alpha1

kind: Cluster

metadata:

  name: <cluster-name>

  namespace: <namespace>

spec:

  # Name of the storage cluster as configured in the cluster environment

  clusterName: <storage-cluster-name>

  # Namespace of the storage cluster as configured in the cluster environment

  clusterNamespace: <storage-cluster-namespace>

```

## Cluster​

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

`spec`ClusterSpec defines the desired state and configuration of a cluster`object`

`status`ClusterStatus defines the observed state and runtime information of a cluster`object`

### spec fields​

FieldDescriptionType

`spec.clusterName`ClusterName represents the name of the storage cluster as configured in the cluster environment`string`

`spec.clusterNamespace`ClusterNamespace represents the namespace of the storage cluster as configured in the cluster environment`string`

### status fields​

FieldDescriptionType

`status.capacity`Storage capacity information including total and used capacity`object`

`status.capacity.total`Total storage capacity of the cluster in bytes`integer`

`status.capacity.used`Used storage capacity of the cluster in bytes`integer`

`status.drAdminNamespace`Admin namespace configured for the cluster for DR operations through Stork`string`

`status.drCapable`Indicates whether the cluster is capable of disaster recovery operations`boolean`

`status.drReadiness`Map of DR readiness checks with their detailed status and information
Key is the readiness check name defined in DrReadinessCheckKey and value is the readiness check details`object`

`status.drReadiness.info`Info provides additional details about the check result`string`

`status.drReadiness.status`Status of the readiness check (e.g., "passed", "failed", "warning")`string`

`status.health`Overall health status of the cluster (e.g., "healthy", "degraded", "offline")`string`

`status.lastStatusUpdateTimestamp`Timestamp of last update of the cluster status`string`

`status.license`License information including SKU and expiry details`object`

`status.license.expiry`Expiration date of the license in ISO 8601 format`string`

`status.license.sku`Stock Keeping Unit (SKU) identifier of the license`string`

`status.monitoringStatus`Status of monitoring services on the cluster`string`

`status.pxOperatorVersion`Version of Portworx Operator installed on the cluster`string`

`status.pxSecretsProviderType`Type of secrets provider used by the cluster (e.g., "vault", "k8s")`string`

`status.pxSecurityChecksum`Checksum of secret sync used in the PX security configuration`string`

`status.pxSecurityEnabled`Indicates whether PX security is enabled on the cluster`boolean`

`status.pxVersion`Version of Portworx software installed on the cluster`string`

`status.storageClusterUid`Unique identifier of the storage cluster`string`

`status.telemetryStatus`Status of telemetry collection on the cluster`string`

`status.topology`Topology information including regions, zones, and racks`object`

`status.topology.racks`List of racks where the cluster nodes are deployed`array`

`status.topology.regions`List of regions where the cluster nodes are deployed`array`

`status.topology.zones`List of availability zones where the cluster nodes are deployed`array`

In this topic:
