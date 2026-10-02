# Asynchronous disaster recovery of the Portworx Backup server with workload identity

Source: https://docs.portworx.com/portworx-enterprise/how-to-guides/async-dr-px-backup-server-workload-identity (Portworx Enterprise latest)

Asynchronous disaster recovery of the Portworx Backup server with workload identity | Portworx Enterprise Documentation

This guide describes how to set up asynchronous disaster recovery (DR) for your Portworx Backup server, using cloud provider workload identity to authenticate with the backup location instead of static credentials. Workload identity removes the need to store and rotate long-lived cloud credentials for DR, which is required in environments that enforce federated identity for cloud access.

note

This guide covers disaster recovery for the Portworx Backup server's own control plane and datastores (the `px-backup` service, PX Central components, and their MongoDB and Keycloak datastores). It applies only when those components use Portworx to provision their PVCs, because the DR solution replicates the underlying Portworx volumes. It is unrelated to using Portworx Backup to back up your other Kubernetes applications and clusters.

## Prerequisites​

- A source cluster running Portworx Backup, and a destination cluster where Portworx Backup will run after failover. Both clusters must have Portworx Enterprise installed, meeting the System Requirements.

- Both clusters must meet the requirements described in Prerequisites for Asynchronous Disaster Recovery, including network access, a supported object store, and a single default StorageClass. If you run Gardener-provisioned clusters, review the cloud-specific Gardener requirements on that page as well; they cover sharing an Azure storage account between clusters, configuring a TCP proxy for cross-cluster connectivity on AWS, and keeping your Google Cloud Workload Identity Pool in sync.

- Workload identity must already be configured on the StorageCluster (STC) of both clusters, and Stork must be enabled to use it. Workload identity is configured through the Portworx Operator; it cannot be configured directly through `storkctl` or the `BackupLocation` custom resource.

- Portworx Backup must be installed on the source cluster. For more information, see Install Portworx Backup Using Portworx Central.

- An active Portworx Enterprise Disaster Recovery (DR) license.

- A user role with cluster-admin access on both clusters, since DR operations require access to multiple namespaces (including `kube-system`).

## Prepare your clusters​

-
Install `storkctl` and, if you're running in the cloud, configure an external load balancer for the `portworx-api` service on both clusters. For more information, see Prepare your Portworx cluster.

-
Update the suspend options on the `alertmanager` and `prometheus` ApplicationRegistration custom resources (CRs) on both clusters. Portworx Backup uses the Prometheus operator to manage these CRs, and DR needs to know how to scale them:

```

kubectl edit applicationregistration alertmanager

kubectl edit applicationregistration prometheus

```

Set the following field on each CR:

```

suspendOptions:

  path: spec.replicas

  type: int

  value: ""

```

## Pair your clusters with workload identity​

Pairing your clusters establishes the trust relationship needed to replicate your Portworx Backup server from the source to the destination cluster. Before you continue, review the configuration guidelines for cluster pairing.

Pair your clusters using the `--use-workload-identity` flag, along with the flags specific to your cloud provider. For the full flag reference, see storkctl create clusterpair.

- AWS (S3)

- Azure

- Google Cloud

```

storkctl create clusterpair eks-cp \

  --namespace kube-system \

  --src-kube-file <source-kubeconfig-file> \

  --dest-kube-file <destination-kubeconfig-file> \

  --provider s3 \

  --bucket <bucket-name> \

  --use-workload-identity

```

On Gardener clusters provisioned in AWS, use the proxy kubeconfig files and endpoints described in Prerequisites for Asynchronous Disaster Recovery instead:

```

storkctl create clusterpair eks-cp \

  --namespace kube-system \

  --src-kube-file <source-proxy-kubeconfig-file> \

  --dest-kube-file <destination-proxy-kubeconfig-file> \

  --provider s3 \

  --bucket <bucket-name> \

  --mode migration \

  --use-workload-identity \

  --s3-endpoint s3.amazonaws.com \

  --s3-region <s3-region> \

  --src-ep <source-cluster-proxy-endpoint>:9001 \

  --dest-ep <destination-cluster-proxy-endpoint>:9001

```

```

storkctl create clusterpair aks-cp \

  --namespace kube-system \

  --src-kube-file <source-kubeconfig-file> \

  --dest-kube-file <destination-kubeconfig-file> \

  --mode migration \

  --provider azure \

  --bucket <bucket-name> \

  --azure-account-name <azure-storage-account-name> \

  --use-workload-identity

```

```

storkctl create clusterpair gke-cp \

  --namespace kube-system \

  --src-kube-file <source-kubeconfig-file> \

  --dest-kube-file <destination-kubeconfig-file> \

  --provider google \

  --google-project-id <google-project-id> \

  --use-workload-identity

```

Once created, verify the cluster pairing status by following Verify the status of your bidirectional ClusterPair.

## Schedule ongoing replication​

Create a schedule policy on your source cluster if you don't already have one you want to reuse. For more information, see Create a schedule policy on your source cluster.

Create a schedule that keeps the `px-backup` namespace replicated to the destination cluster:

```

storkctl create migrationschedule -n kube-system --cluster-pair <clusterpair-name> --namespaces=px-backup <migration-schedule-name>

```

note

This assumes Portworx Backup is installed in the `px-backup` namespace. If you installed it in a different namespace, use that namespace instead.

Check the replication status:

```

storkctl get migrations -n kube-system

```

For more information, see Check your migration status on your source cluster.

## Fail-over your Portworx Backup server​

In the event of a disaster, fail-over your Portworx Backup server to the destination cluster.

-
Scale up the Prometheus operator on the destination cluster:

```

kubectl scale deployment.apps/prometheus-operator -n px-backup --replicas=1

```

-
Perform the failover, excluding the Prometheus operator from activation:

```

storkctl perform failover -m <migration-schedule-name> -n kube-system --exclude-selectors=k8s-app=prometheus-operator

```

note

The Prometheus operator is excluded here because it manages the `alertmanager` and `prometheus` CRs directly, and activating it as part of the failover can conflict with the scale-up step above.

For more failover options, including namespace and resource filtering, see Failover an application.

### Verify the failover​

Check that your Portworx Backup server's pods are running on the destination cluster:

```

kubectl get pods -n px-backup

```

```

NAME                                          READY   STATUS    RESTARTS      AGE

alertmanager-px-backup-alertmanager-0         2/2     Running   0             22h

alertmanager-px-backup-alertmanager-1         2/2     Running   0             22h

prometheus-operator-5fcfc6b6bf-tqlwl          1/1     Running   0             23h

prometheus-px-backup-dashboard-prometheus-0   2/2     Running   0             22h

prometheus-px-backup-dashboard-prometheus-1   2/2     Running   0             22h

px-backup-5648fcb687-qm76n                    1/1     Running   0             22h

pxc-backup-mongodb-0                          1/1     Running   0             22h

pxc-backup-mongodb-1                          1/1     Running   0             22h

pxc-backup-mongodb-2                          1/1     Running   0             22h

pxcentral-apiserver-5cb5b8cd9d-9sg99          1/1     Running   0             22h

pxcentral-backend-56c8c9bc8d-6q5rx            1/1     Running   4 (22h ago)   22h

pxcentral-frontend-8b7975bcd-scvct            1/1     Running   0             22h

pxcentral-keycloak-0                          1/1     Running   0             22h

pxcentral-keycloak-postgresql-0               1/1     Running   0             22h

pxcentral-lh-middleware-58d9b445c-xfzv8       1/1     Running   4 (22h ago)   22h

pxcentral-mysql-0                             1/1     Running   0             22h

```

## Fail-back your Portworx Backup server​

Once your original source cluster is restored and operational, you can fail-back your Portworx Backup server to it.

If your clusters were paired unidirectionally, create a reverse cluster pairing from the destination cluster back to the source cluster before failing back. For more information, see Create a reverse ClusterPair.

Perform the failback, again excluding the Prometheus operator:

```

storkctl perform failback -m <reverse-migration-schedule-name> -n kube-system --exclude-selectors=k8s-app=prometheus-operator

```

For more information, including how to reverse-sync your clusters before failback, see Failback an application.

## Clean up disaster recovery objects​

If you no longer need this DR setup, delete the migration schedule, schedule policy, and cluster pairing objects from both clusters. For more information, see Clean up disaster recovery objects.

In this topic:
