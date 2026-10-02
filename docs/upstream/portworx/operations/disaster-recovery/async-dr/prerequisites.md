# Prerequisites for Asynchronous Disaster Recovery

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/async-dr/prerequisites (Portworx Enterprise 3.6)

Prerequisites for Asynchronous Disaster Recovery | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

The prerequisites provided in this section ensure a stable foundation for data replication and failover when you enable asynchronous disaster recovery between the source and destination clusters. Review them carefully to prevent configuration issues during deployment.

Ensure that your cluster meets the following prerequisites in addition to the System Requirements:

-
An active Portworx Enterprise Disaster Recovery (DR) license.

-
You must have a user role with cluster-admin access to perform failover, failback, or other disaster recovery operations, as these operations require access to multiple namespaces (including `kube-system`) and full cluster-wide permissions.

-
Your environment must meet the following network requirements:

- All worker nodes in the source and destination clusters must be able to access the Kubernetes API endpoints (for example, ports 6443 and 443).

- For a Kubernetes-based distribution, the source cluster must be able to access port 9001 on the destination cluster to enable API calls and volume migration via the cluster-pair.
 For an OpenShift-based distribution, the source cluster must be able to access port 17001 on the destination cluster to enable API calls and volume migration via the cluster-pair.

For more information on the list of required ports for your environment, see Network Requirements.

-
Both the source and destination clusters are configured with the same CloudSnap object size.
 For information on how to configure the CloudSnap object size, see Increase the CloudSnap object size.

-
KubeVirt VMs with PX ReadWriteMany (RWX) block volumes must run OpenShift Virtualization 4.18.5 or later with OpenShift Container Platform 4.18.x to enable asynchronous disaster recovery. Running earlier OCP versions, such as 4.16.x, can cause I/O errors that may pause virtual machines.

-
NFS, AWS S3, Google Cloud Object Storage, Azure Blob Storage or any other S3-compatible Storage to be used as the Object Store.

-
A maximum of one StorageClass object is configured as the default. Having multiple default StorageClasses causes PVC migrations to fail.

-
Depending on your cloud provider (EKS, GKE, AAD enabled AKS, or OKE) ensure to enable secure, automated migration of applications and volumes between clusters using Stork.

-
A separate Portworx cluster with the same version is installed on both the source and destination clusters.

-
The latest version of `storkctl` is installed on the source and destination clusters. You can download the latest version from the currently running Stork container.
 For more information, see Prepare your Portworx Cluster.

-
For an OpenShift-based distribution, an ApplicationRegistration custom resource (CR) is created to enable successful migration of supported applications. For more information, see ApplicationRegistrations.
 Important: For certain Kubernetes applications, an ApplicationRegistration custom resource (CR) is created before initiating migration.

-
If you use any custom container images, make sure the custom images are available from a registry that is accessible to both the source and destination clusters.

-
GitOps tools such as ArgoCD, FluxCD, or Rancher Fleet do not overwrite the Kubernetes custom resources (CRs) migrated by Portworx disaster recovery (DR) `MigrationSchedules` on the destination cluster.

-
Gardener clusters provisioned in Azure: If you use Azure Blob Storage as your backup location, both the source and destination clusters must use the same Azure storage account. Grant the destination cluster's identity access to the source cluster's storage account:

```

az login

storageId=$(az storage account show -n <storage-account-name-of-source-cluster> -g <resource-group-of-source-cluster> --query id -o tsv)

az role assignment create \

    --assignee <azure-client-id-of-destination-cluster> \

    --role "Storage Blob Data Contributor" \

    --scope $storageId

az role assignment list \

    --assignee <azure-client-id-of-destination-cluster> \

    --scope $storageId \

    -o table

```

For more information, see the Azure storage account documentation.

-
Gardener clusters provisioned in AWS: When you pair two clusters for asynchronous DR, the Stork pods on each cluster connect to the Kubernetes API server of the other cluster, using the kubeconfig files you provide to `storkctl create clusterpair`. On Gardener clusters provisioned in AWS, this cross-cluster connection fails by default, because Gardener resolves the Kubernetes API server hostname to an internal seed IP that's reachable only through Gardener's VPN, not from the cluster's own pod network. To allow this connection, deploy a TCP proxy on each cluster and use kubeconfig files that point to the proxy instead of directly to the API server:

-
Deploy a `socat` proxy in the `portworx` namespace on each cluster. Don't deploy it in the `kube-system` namespace, since Gardener's deny-all NetworkPolicy blocks it there:

```

socat TCP-LISTEN:6443,fork,reuseaddr TCP:100.64.0.1:443

```

-
Expose the proxy using a `LoadBalancer` service. Your cloud provider provisions a load balancer per cluster.

-
Create modified kubeconfig files that point to the proxy load balancers, with `insecure-skip-tls-verify: true` set, since the proxy's certificate doesn't match the original API server hostname.

-
Use these modified kubeconfig files when creating your ClusterPair. For more information, see Create a ClusterPair.

-
Gardener clusters provisioned in Google Cloud Platform (GCP): Gardener assigns each Shoot cluster a new OIDC issuer URL, keyed to the Shoot's UUID, every time the Shoot is created or recreated. Your GCP Workload Identity Pool Provider must reference each cluster's current issuer URL; otherwise, GCP rejects the workload identity token exchange with an `invalid_grant` error when you create a ClusterPair. Whenever you create or recreate a Gardener cluster provisioned in GCP, update the Workload Identity Pool in your GCP project as follows:

-
Add an OIDC provider for the source cluster's Shoot issuer URL:

```

gcloud iam workload-identity-pools providers create-oidc <src-provider-id> \

    --location=global \

    --workload-identity-pool=<pool-id> \

    --issuer-uri="<src-cluster-shoot-issuer-url>" \

    --attribute-mapping="google.subject=assertion.sub"

```

-
Add an OIDC provider for the destination cluster's Shoot issuer URL:

```

gcloud iam workload-identity-pools providers create-oidc <dest-provider-id> \

    --location=global \

    --workload-identity-pool=<pool-id> \

    --issuer-uri="<dest-cluster-shoot-issuer-url>" \

    --attribute-mapping="google.subject=assertion.sub"

```

-
Grant `roles/iam.workloadIdentityUser` on the GCP service account for principals from both providers. Repeat this step for each cluster. To find the Portworx service account name, run `kubectl -n kube-system get sa`:

```

gcloud iam service-accounts add-iam-policy-binding \

    <gcp-service-account>@<project>.iam.gserviceaccount.com \

    --role=roles/iam.workloadIdentityUser \

    --member="principal://iam.googleapis.com/projects/<proj-num>/locations/global/workloadIdentityPools/<pool-id>/subject/system:serviceaccount:kube-system:<px-sa-name>"

```

-
Create your ClusterPair with workload identity. For more information, see Create a ClusterPair.
