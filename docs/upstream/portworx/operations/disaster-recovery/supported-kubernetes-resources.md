# Supported Kubernetes Resources for DR

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/supported-kubernetes-resources (Portworx Enterprise latest)

Supported Kubernetes Resources for DR | Portworx Enterprise Documentation

Asynchronous DR and synchronous DR support the following Kubernetes resources:

- PersistentVolumeClaim (Portworx provisioned)

- PersistentVolume (Portworx provisioned)

- Deployment

- DeploymentConfig

- StatefulSet

- ConfigMap

- Service

- Secret

- DaemonSet

- ServiceAccount

- Role

- RoleBinding

- ClusterRole

- ClusterRoleBinding

- ImageStream

- Ingress

- Route

- Template

- CronJob

- ResourceQuota

- ReplicaSet

- LimitRange

- PodDisruptionBudget

- NetworkPolicy

note

- By default, Stork skips migrating NetworkPolicies that have `CIDR` set. To migrate NetworkPolicies with `CIDR` set, use the `skipNetworkPolicyCheck: true` flag in the migration object.

- Even if `startApplications` is set to `False`, DaemonSets migrated to the destination cluster will remain in a running state, similar to the source cluster, because Kubernetes does not allow scaling down DaemonSets. To prevent this behavior, you can add DaemonSets to `excludeResourceType`, ensuring they are not migrated to the destination cluster. Users must manually apply the DaemonSet specification after failover or failback to make the application operational.

Asynchronous DR and synchronous DR do not support migration of Kubernetes custom resources that belong to specific groups. These groups are specified by the group value in the Custom Resource Definition (CRD). Groups listed here are not supported for migration by asynchronous DR or synchronous DR:

- `autopilot.libopenstorage.org`

- `core.libopenstorage.org`

- `volumesnapshot.external-storage.k8s.io`

- `stork.libopenstorage.org`

- `kdmp.portworx.com`

If you have custom resources defined under any of these groups, asynchronous DR or synchronous DR will not be able to handle or move these resources during a disaster recovery operation.

note

Refer to the Application Registration document for information about supported custom resource definitions (CRDs) for asynchronous DR and synchronous DR. The document also provides steps for registering a new CRD if it is not already listed.
