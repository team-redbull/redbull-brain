# StorageCluster Admission Control

Source: https://docs.portworx.com/portworx-enterprise/concepts/storagecluster-admission-control (Portworx Enterprise 3.6)

StorageCluster Admission Control | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Starting with Portworx Operator 26.3.2, the operator enforces cluster-admin rights for all create, update, and delete operations on StorageCluster resources by using a Kubernetes `ValidatingAdmissionPolicy` (VAP). This policy prevents unauthorized users or service accounts from creating, modifying, or deleting the StorageCluster, which controls the entire Portworx storage cluster.

## Prerequisites​

- Portworx Operator 26.3.2 or later installed on your cluster.

- Kubernetes 1.30 or later to use StorageCluster admission control. On earlier Kubernetes versions, the operator skips VAP creation and logs a warning; all other functionality is unaffected.

## How StorageCluster admission control works​

When the operator starts, it creates or updates a `ValidatingAdmissionPolicy` and its binding on the cluster. The policy allows create, update, and delete operations on StorageCluster resources only for users or service accounts with cluster-admin-equivalent rights. The operator automatically exempts its own service account so that Portworx reconciliation operations aren't blocked. The operator immediately denies unauthorized requests and writes an audit log entry for each denial.

On Kubernetes versions earlier than 1.30, the `ValidatingAdmissionPolicy` API isn't available as a generally available (GA) feature. The operator detects this at startup, logs a warning, and skips policy reconciliation. StorageCluster admission control isn't enforced on these clusters.

For more information about Kubernetes `ValidatingAdmissionPolicy`, see the Kubernetes documentation.

## Impact on GitOps and Helm deployments​

StorageCluster resources managed by GitOps controllers such as Argo CD or Flux, or applied through Helm, are subject to this admission policy. The service account used by the GitOps controller or Helm operation must have `cluster-admin` or equivalent rights on the cluster. Operations from non-admin service accounts are denied on Kubernetes 1.30 or later with the following error:

```

user '<username>' does not have cluster-admin privileges required to manage StorageCluster resources

```

Verify that your GitOps controller's service account has a ClusterRoleBinding to the `cluster-admin` ClusterRole before upgrading to Operator 26.3.2 or later on clusters running Kubernetes 1.30 or later.

In this topic:
