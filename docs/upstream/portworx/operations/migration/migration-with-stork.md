# Migration with Stork

Source: https://docs.portworx.com/portworx-enterprise/operations/migration/migration-with-stork (Portworx Enterprise 3.6)

Migration with Stork | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This guide shows you how to migrate your Portworx volumes one time between clusters using Stork. If you wish to set up disaster recovery, refer to the Disaster Recovery section.

## Prerequisites​

- Kubernetes

- OpenShift

- Secret Store: A secret store is configured on both clusters. This will store the credentials for the objectstore.

- Objectstore: An AWS S3 compatible, AWS S3, GCP Object Storage, or Azure Blob Storage.

- Network Connectivity:

- Kubernetes: All worker nodes are able to reach Kubernetes API endpoints on both Kubernetes clusters, for example, port 6443, 443 and so on.

- Portworx: Open port in the range of 9001-9020 for Portworx worker nodes to communicate with each other. To know more about the specific ports for your environment, see the Network table on the Prerequisites page.

- Default StorageClass: At most one StorageClass object is configured as the default. Having multiple default StorageClasses will cause PVC migrations to fail.

- Cloud Environment: Depending on your cloud provider (EKS, GKE, AAD enabled AKS, or OKE) ensure that you have successfully applied the instructions provided on the respective page for setting up your destination cluster.

- `storkctl` is installed on both clusters. Always use the latest `storkctl` binary tool by downloading it from the current running Stork container.

- Secret Store: A secret store is configured on both clusters. This will store the credentials for the objectstore.

- Objectstore: An AWS S3 compatible, AWS S3, GCP Object Storage, or Azure Blob Storage.

- Network Connectivity:

- OpenShift4+: All worker nodes are able to reach API endpoints on both clusters, for example, port 6443, 443 and so on.

- Portworx: You must open ports in the range of 17001-17020 to reach Portworx API endpoints. To know more about the specific ports for your environment, see the Network table on the Prerequisites page.

- Default StorageClass: At most one StorageClass object is configured as the default. Having multiple default StorageClasses will cause PVC migrations to fail.

- Cloud Environment: Depending on your cloud provider (EKS, GKE, AAD enabled AKS, or OKE) ensure that you have successfully applied the instructions provided on the respective page for setting up your destination cluster.

- Custom container images: If you use any custom container images, make sure the custom images are available from a registry that is accessible to both the source and destination clusters.

- `storkctl` is installed on both clusters. Always use the latest `storkctl` binary tool by downloading it from the current running Stork container.

note

- The default admin namespace is `kube-system`. In all examples, `<migrationnamespace>` is considered the admin namespace responsible for migrating all namespaces from your source cluster to the destination cluster. Alternatively, you can specify a non-admin namespace, in such a case, only that specific namespace will be migrated. To learn how to set up an admin namespace, refer to the Set up a Cluster Admin namespace for Migration page.

- Migration is not supported for FlashArray Direct Access and FlashBlade Direct Access volumes. Avoid configuring migration schedules for any namespaces containing these volumes.

## Create a ClusterPair object​

For migration with Stork, it is essential to pair two clusters to enable the migration of data and resources. To facilitate this process, you need to create a trust object, known as a ClusterPair object, on the source cluster. Portworx requires this object to establish a communication channel between the two clusters.

The ClusterPair object pairs the two clusters, allowing migration of resources and volumes.

### Pair your clusters​

Use the `storkctl create clusterpair` command to create your unidirectional ClusterPair using the command options specific to your environment, as explained in the following sections. The unidirectional ClusterPair will establish authentication from the source cluster to the destination cluster so resources and data can be migrated in one direction.

This command creates Clusterpair object on the source cluster using the source config file (`<source-kubeconfig-cluster>`) and the destination kubeconfig file (`<destination-kubeconfig-cluster>`) in the specified namespace (`<migrationnamespace>`). This object establishes and authenticates the connection between the two clusters for migrating resources and volumes within the specified namespace.

note

If you configured the `portworx-api` service to be accessible externally through ingresses or routes, specify the following two additional command options while creating the ClusterPair:

- `--dest-ep string`: Endpoint of the `portworx-api` service in the destination cluster.

- `--src-ep string`: Endpoint of the `portworx-api` service in the source cluster.

If the above endpoints are not specified, the storage status of the ClusterPair shows as `failed`.

#### Create a unidirectional ClusterPair​

Depending upon your ObjectStore, click the appropriate tab to run the command to create a unidirectional ClusterPair named `migration-cluster-pair` for cluster migration:

- Amazon S3 or S3 compatible

- Microsoft Azure

- GCP

- NFS

Run the following command to create a unidirectional ClusterPair named `migration-cluster-pair` for cluster migration:

```

storkctl create clusterpair migration-cluster-pair \

--namespace <migrationnamespace> \

--dest-kube-file <destination-kubeconfig-file> \

--src-kube-file <source-kubeconfig-file> \

--provider s3 \

--s3-endpoint s3.amazonaws.com \

--s3-access-key <s3-access-key> \

--s3-secret-key <s3-secret-key> \

--s3-region <s3-region> \

--mode migration \

--unidirectional

```

Portworx uses AWS S3 or S3 compatible blob storage for migrating volume data between the two clusters. The credentials specified in the above command authenticate you with your cloud platform. The S3 bucket information is provided with the specified access key, secret key, and region (`<s3-bucket-location>`) to facilitate the data transfer between the two clusters.

Run the following command to create a unidirectional ClusterPair named `migration-cluster-pair` for cluster migration:

```

storkctl create clusterpair migration-cluster-pair \

--namespace <migrationnamespace> \

--dest-kube-file <destination-kubeconfig-file> \

--src-kube-file <source-kubeconfig-file> \

--provider azure \

--azure-account-name <azure-account-name> \

--azure-account-key <azure-account-key> \

--mode migration \

--unidirectional

```

Portworx uses Azure blob storage for migrating volume data between the two clusters. The Azure credentials specified in the above command authenticate you with Azure.

Run the following command to create a unidirectional ClusterPair named `migration-cluster-pair` for cluster migration:

```

storkctl create clusterpair migration-cluster-pair \

--namespace <migrationnamespace> \

--dest-kube-file <destination-kubeconfig-file> \

--src-kube-file <source-kubeconfig-file> \

--provider google \

--google-project-id <gcp-project-ID> \

--google-json-key <gcp-json-auth-key> \

--mode migration \

--unidirectional

```

Portworx uses Google Cloud storage for migrating volume data between the two clusters. The Google Cloud credentials specified in the above command authenticate you with Google Cloud.

Prerequisites

- The minimum required version of Stork for NFS support is 24.4.0.

- The supported NFS version is limited to NFSv4.

Run the following command to create a unidirectional ClusterPair named `migration-cluster-pair` for cluster migration:

```

storkctl create clusterpair migration-cluster-pair \

  --src-kube-file </tmp/kubeconfig> \

  --dest-kube-file </tmp/kubeconfig2> \

  --provider nfs \

  --nfs-server <nfs-server-address> \

  --nfs-export-path <nfs-export-path> \

  --nfs-sub-path <nfs-sub-path> \

  --nfs-mount-opts <mount-options> \

  --nfs-timeout-seconds <timeout-seconds> \

  --unidirectional

```

Parameters:

- `--provider nfs`: Specifies the provider as NFS.

- `--nfs-server`: Specifies the address of the NFS server (hostname or IP address).

- `--nfs-export-path`: Specifies the exported path on the NFS server.

- `--nfs-sub-path`: Specifies the subpath within the export path to use. If you do not specify a subpath, Portworx creates one automatically.

- `--nfs-mount-opts`: (Optional) Specifies NFS mount options, for example, vers=4.0.

- `--nfs-timeout-seconds`: (Optional) Specifies the NFS IO timeout in seconds (default is 5, valid range is 1-30).

Portworx uses the specified NFS storage for migrating volume data between the two clusters.

#### Verify the status of your unidirectional ClusterPair​

The following command uses `storkctl` to retrieve information about the cluster pairs in the Kubernetes namespace `<migrationnamespace>`:

```

storkctl get clusterpair -n <migrationnamespace>

```

This command displays details such as the name and status of the existing cluster pairs within that specific namespace.

Source cluster details:

```

NAME                     STORAGE-STATUS  SCHEDULER-STATUS  CREATED

migration-cluster-pair   Ready           Ready             10 Mar 23 17:16 PST

```

On a successful pairing, you should see the `STORAGE-STATUS` and `SCHEDULER-STATUS` as `Ready`.
 Encountered an error?

If you see an error, you can get more information by running the following command:

`kubectl describe clusterpair <your-clusterpair-name> -n <migrationnamespace>`

### Use Rancher Projects with ClusterPair​

If you are using Rancher projects, follow the instructions on the Use Rancher Projects with ClusterPair page, otherwise skip to the next section.

## Start your migration​

Once the pairing is configured, applications can be migrated repeatedly to the destination cluster.

You can either use the `storkctl create migration` command or create a migration object and apply it manually to start the migration.

You can also use `pre-exec` and `post-exec` rules to run custom actions before or after each migration. For more information see Configure pre-exec and post-exec rules for Stork migrations

note

Starting from Stork 25.5.0, you can use the admin ClusterPair to create migration schedules in any namespace instead of creating a local ClusterPair and referencing it in the migration schedule. For more information, see Use the admin ClusterPair for migrations in any namespace.

- Using storkctl

- Using CRD

Use the `storkctl create migration` command with the required flags. For more information, refer to `storkctl create migration`.

note

If you have created an admin ClusterPair, you can use it instead of creating a local ClusterPair. Use the `--admin-cluster-pair` flag instead of `--clusterPair`.

Example:

```

storkctl create migration <your-migration-object-name> \

  --clusterPair migration-cluster-pair \

  --namespaces <app-namespace1>,<app-namespace2> \

  --includeResources=true \

  --startApplications=true \

  --namespace <migrationNamespace>

```

### Preview resources before starting migration​

To validate which resources will be included in a migration before creating it, use the `--preview` or `--previewFile` flags with the `storkctl create migration` command:

- Use `--preview` to display the resources that will be included in the migration without initiating it.

- Use `--previewFile <filename>` to save the preview output to a file.

This helps confirm which resources will be migrated before execution, including non-namespaced resources such as `ClusterRole` and `ClusterRoleBinding`.

Follow these steps to migrate your cluster resources and volumes.

### Define your migration object​

Paste the following spec into the `migration.yaml` file to define your migration object:

note

If you have created an admin ClusterPair, you can use it instead of creating a local ClusterPair. Use the `spec.adminClusterPair` field instead of `spec.clusterPair`.

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: Migration

metadata:

  name: <your-migration-object-name>

  namespace: <migrationnamespace>

spec:

  clusterPair: migration-cluster-pair

  includeResources: true

  startApplications: true

  namespaces:

  - <app-namespace1>

  - <app-namespace2>

  purgeDeletedResources: false

```

Where:

- apiVersion: is set as `stork.libopenstorage.org/v1alpha1`

- kind: is set as `Migration`

- metadata.name: is the name of the object that performs the migration

- metadata.namespace: is the name of the namespace in which you want to create the object

- spec.clusterPair: is the name of the `ClusterPair` object created in the Pair your clusters section

- spec.includeResources: is a boolean value specifying if the migration should include PVCs and other application specs. If you set this field to `false`, Portworx will only migrate your volumes.

- spec.startApplications: with a boolean value specifying if Portworx should automatically start applications on the destination cluster. If you set this field to `false`, then the `Deployment` and `StatefulSet` objects on the destination cluster will be set to zero. Note that, on the destination cluster, Portworx uses the `stork.openstorage.org/migrationReplicas` annotation to store the number of replicas from the source cluster.

- spec.namespaces: is the list of namespaces you want to migrate

- spec.purgeDeletedResources: with a boolean value specifying if Stork should automatically purge a resource from the destination cluster when you delete it from the source cluster. The default value is `false`.

### (Optional) Customize your migration​

You can define pre and post executable rules for your migration and specify them in your migration object spec to customize your migration. The pre-executable rule will run before the migration is triggered, and the post-executable rule will run after the migration has been triggered.

When you are using an admin namespace to migrate multiple namespaces and want to customize your migration using the pre or post executable rules, create these rules in the admin namespace.

The following example shows how you can specify the pre and post rules in your migration object:

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: Migration

metadata:

  name: <your-migration-object-name>

  namespace: <migrationnamespace>

spec:

  clusterPair: migration-cluster-pair

  includeResources: true

  startApplications: true

  preExecRule: <your-pre-rule>

  postExecRule: <your-post-rule>

  namespaces:

  - <app-namespace1>

  - <app-namespace2>

  purgeDeletedResources: false

```

If the rules do not exist, you will see an event and the migration will stop.

-
If the PreExec rule fails for any reason, it will log an event against the object and retry. The Migration will not be marked as failed.

-
If the PostExec rule fails for any reason, it will log an event and mark the Migration as failed. It will also try to cancel the migration that was started from the underlying storage driver.

### Apply the spec​

- Kubernetes

- OpenShift

Apply the spec to start the migration process:

```

kubectl apply -f migration.yaml

```

Apply the spec to start the migration process:

```

oc apply -f migration.yaml

```

## Monitoring a migration​

Once the migration has been started using the previous commands, you can check the status using `storkctl`:

```

storkctl get migration -n <migrationnamespace>

```

Here is an example output that you see initially when the migration is triggered:

```

NAME                                            CLUSTERPAIR              STAGE     STATUS       VOLUMES   RESOURCES   CREATED

<your-migration-object-name>-2022-12-12-200210  migration-cluster-pair   Volumes   InProgress   0/3       0/0         12 Dec 22 11:45 PST

```

If the migration is successful, the `STAGE` will change from `Volumes` to `Application` to `Final`.

Here is an example output of a successful migration:

```

NAME                                             CLUSTERPAIR            STAGE   STATUS       VOLUMES   RESOURCES   CREATED               ELAPSED

<your-migration-object-name>-2022-12-12-200210   migration-cluster-pair Final   Successful   3/3       10/10       12 Dec 22 12:02 PST   1m23s

```

 Need to see more details?

If you see an error, or you want to see more details of your migration, run the following command:

`kubectl describe clusterpair <your-clusterpair-name> -n <migrationnamespace>`

In this topic:
