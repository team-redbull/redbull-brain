# Create a ClusterPair

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/async-dr/generate-apply-clusterpair (Portworx Enterprise 3.6)

Create a ClusterPair | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

In an asynchronous DR setup, it is essential to pair two clusters to enable the migration of data and resources. To facilitate this process, you need to establish trust objects, known as ClusterPair objects, between the two clusters. Portworx requires these objects to establish a communication channel between the two clusters.

The ClusterPair objects pair the two Kubernetes clusters, allowing migration of resources and volumes.

Creation of the ClusterPair object does not initiate the actual migration of resources and volumes between the clusters. It establishes the foundation for a trust-based relationship between the clusters. Using this ClusterPair object, you can create a migration schedule that initiates the data migration between the two paired clusters.

Cluster pairings can be established in a unidirectional or bidirectional manner with Stork, allowing resources and data to migrate between two clusters in the specified direction. ​

- Unidirectional pairing: enables data and resource migrations in one direction between two clusters.

- Bidirectional pairing: enables data and resource migration in both directions between the two clusters. With bidirectional ClusterPair, you can configure clusters for seamless failover and failback from the beginning.

important

- Starting from Stork version 25.5.0, you can create an admin ClusterPair object that supports migration of both cluster-scoped and namespaced resources, including persistent volumes. This configuration allows you to create `Migration` and `MigrationSchedule` objects in any namespace and reference a centrally managed ClusterPair in the `admin` namespace. For more information, see Create admin ClusterPair.

- The default admin namespace is `kube-system`. In all examples, `<migrationnamespace>` is considered the admin namespace responsible for migrating all namespaces from your source cluster to the destination cluster. Alternatively, you can specify a non-admin namespace, but note that only that specific namespace will be migrated. To learn how to set up an admin namespace, refer to the Set up a Cluster Admin namespace for Migration page.

## Pair your clusters​

Use the `storkctl create clusterpair` command to create your unidirectional or bidirectional ClusterPair using the command options specific to your environment, as explained in the following sections. This command sets up a connection between a source cluster using the source config file (`<source-kubeconfig-cluster>`) and a destination cluster using the destination kubeconfig file (`<destination-kubeconfig-cluster>`). The pairing is created within the specified namespace (`<migrationnamespace>`). For the full list of available flags, see storkctl create clusterpair.

Starting with Stork version 25.5.0, you can create an admin ClusterPair and use it to migrate both cluster-scoped and namespaced resources, including volumes. Creating an admin ClusterPair is the same as creating a namespace-scoped ClusterPair, except that you must specify an admin namespace.

note

- If you're running Portworx Enterprise 3.4.0 or later and Stork 25.4.0, Stork validates the credentials before creating the cluster pair.

- Cluster pair creation fails if the validation fails.

- If you're running Portworx Enterprise 3.4.0 or later and Stork 25.4.1 or later, Stork validates the credentials before creating the cluster pair.

- When `--src-ep` or `--dest-ep` flags are provided, validation is skipped.

- You can also skip validation explicitly by using the `--skip-validation` flag.

### Configuration guidelines​

-
When creating multiple ClusterPairs, use only one external object store (`BackupLocation`).

-
If you configured the `portworx-api` service to be accessible externally through ingresses or routes or if you set the annotation `portworx.io/service-type: "portworx-api:NodePort"`, specify the following two additional command options while creating the ClusterPair:

- `--dest-ep <host.fqdn:port>`: Endpoint of the `portworx-api` service in the destination cluster.

- `--src-ep <host.fqdn:port>`: Endpoint of the `portworx-api` service in the source cluster.

If the above endpoints are not specified, the storage status of the ClusterPair will show as `failed`.

-
If you set up migrations and migration schedules using user accounts, you will encounter token expiration-related errors. To avoid these errors, Portworx Enterprise recommends setting up migrations and migration schedules using service accounts. For service accounts, you need to create a kubeconfig file by following the steps here and use the same file when creating a ClusterPair.

-
After creating the cluster pair, if you need to change the object store location, delete the existing cluster pair from both clusters and recreate it with the same name, using the new object store. This ensures that existing migration schedules remain unaffected.

-
If you use custom CA certificates with S3-compatible storage, secure them using the procedure described in Certificates as Kubernetes Secrets before creating clusterpair in your environment.

-
If you're pairing Gardener clusters provisioned in Amazon Web Services (AWS), Azure, or Google Cloud Platform (GCP), additional network or workload identity configuration is required before creating your ClusterPair. For more information, see Prerequisites for Asynchronous Disaster Recovery.

### Unidirectional ClusterPair​

​ A unidirectional ClusterPair establishes authentication from the source cluster to the destination cluster so resources and data can be migrated in one direction.

note

To create an admin ClusterPair, specify the admin namespace using the `--namespace` flag when creating the ClusterPair.

​

#### Create a unidirectional ClusterPair for Amazon S3 or S3 compatible​

​ Run the following command to create a unidirectional ClusterPair named `migration-cluster-pair` for cluster migration: ​

```

storkctl create clusterpair migration-cluster-pair \

  --namespace <migrationnamespace> \ # To create an admin ClusterPair, specify the admin namespace

  --dest-kube-file <destination-kubeconfig-file> \

  --src-kube-file <source-kubeconfig-file> \

  --provider s3 \

  --s3-endpoint s3.amazonaws.com \

  --s3-access-key <s3-access-key> \

  --s3-secret-key <s3-secret-key> \

  --s3-region <s3-region> \

  --unidirectional \

  # Use --dest-ep and --src-ep when configuring asynchronous disaster recovery in cloud platforms.

  # --dest-ep <host.fqdn:port> \

  # --src-ep <host.fqdn:port> \

  # Starting from Stork version 25.4.1, You can skip the credentials vadiation using the --skip-validation flag

  # --skip-validation

```

Portworx will use AWS S3 or S3 compatible blob storage for migrating volume data between the two clusters. The credentials specified in the above command are used for authenticating with your cloud platform. The S3 bucket information is provided with the specified access key, secret key, and region (`<s3-bucket-location>`) to facilitate the data transfer between the two clusters. For AWS S3 bucket permission, see the Create credentials on AWS using IAM section.

Automatic bucket creation:

In AWS, using the `--bucket` option in the `storkctl create clusterpair` command will automatically create two buckets named after the cluster UUIDs:

- First bucket: used to replicate resources from the source to the destination cluster.

- Second bucket: used for replication in the opposite direction.

Unidirectional clusterpair command for AWS S3 with bucket creation:

```

storkctl create clusterpair migration-cluster-pair \

  --namespace <migrationnamespace> \ # To create an admin ClusterPair, specify the admin namespace

  --src-kube-file <source-kubeconfig-file> \

  --dest-kube-file <destination-kubeconfig-file> \

  --provider s3 \

  --s3-endpoint s3.amazonaws.com \

  --s3-access-key <s3-access-key> \

  --s3-secret-key <s3-secret-key> \

  --s3-region <s3-region> \

  --unidirectional \

  # Use --dest-ep and --src-ep when configuring asynchronous disaster recovery in cloud platforms.

  # --dest-ep <host.fqdn:port> \

  # --src-ep <host.fqdn:port> \

  # Starting from Stork version 25.4.1, You can skip the credentials vadiation using the --skip-validation flag

  # --skip-validation

--bucket <source-cluster-bucket>

```

Using the `--use-existing-objectstorelocation` option:

The `--use-existing-objectstorelocation` option is used to specify that existing object store locations should be used instead of creating new ones. This is particularly useful when you already have object store locations configured and wish to reuse them.

Following is the unidirectional clusterpair command with existing object store location for AWS S3:

```

storkctl create clusterpair migration-cluster-pair \

  --namespace <migrationnamespace> \  # To create an admin ClusterPair, specify the admin namespace

  --src-kube-file <source-kubeconfig-file> \

  --dest-kube-file <destination-kubeconfig-file> \

  --provider s3 \

  --s3-endpoint s3.amazonaws.com \

  --s3-access-key <s3-access-key> \

  --s3-secret-key <s3-secret-key> \

  --s3-region <s3-region> \

  --unidirectional \

# Use --dest-ep and --src-ep when configuring asynchronous disaster recovery in cloud platforms.

# --dest-ep <host.fqdn:port> \

# --src-ep <host.fqdn:port> \

--use-existing-objectstorelocation

```

​

#### Create a unidirectional ClusterPair for Microsoft Azure​

​ Run the following command to create a unidirectional ClusterPair named `migration-cluster-pair` for cluster migration:

```

storkctl create clusterpair migration-cluster-pair \

  --namespace <migrationnamespace> \ # To create an admin ClusterPair, specify the admin namespace

  --dest-kube-file <destination-kubeconfig-file> \

  --src-kube-file <source-kubeconfig-file> \

  --provider azure \

  --azure-account-name <azure-account-name> \

  --azure-account-key <azure-account-key> \

  --unidirectional \

  # Use --dest-ep and --src-ep when configuring asynchronous disaster recovery in cloud platforms.

  # --dest-ep <host.fqdn:port> \

  # --src-ep <host.fqdn:port> \

  # Starting from Stork version 25.4.1, You can skip the credentials vadiation using the --skip-validation flag

  # --skip-validation

```

​ Portworx will use Azure blob storage for migrating volume data between the two clusters. The Azure credentials specified in the above command are used for authenticating with the Azure cloud platform. ​

#### Create a unidirectional ClusterPair for GCP​

​Run the following command to create a unidirectional ClusterPair named `migration-cluster-pair` for cluster migration:

```

storkctl create clusterpair migration-cluster-pair \

  --namespace <migrationnamespace> \ # To create an admin ClusterPair, specify the admin namespace

  --dest-kube-file <destination-kubeconfig-file> \

  --src-kube-file <source-kubeconfig-file> \

  --provider google \

  --google-project-id <gcp-project-ID> \

  --google-json-key <gcp-json-auth-key> \

  –-unidirectional \

  # Use --dest-ep and --src-ep when configuring asynchronous disaster recovery in cloud platforms.

  # --dest-ep <host.fqdn:port> \

  # --src-ep <host.fqdn:port> \

  # Starting from Stork version 25.4.1, You can skip the credentials vadiation using the --skip-validation flag

  # --skip-validation

```

​ Portworx will use Google Cloud storage for migrating volume data between the two clusters. The Google Cloud credentials specified in the above command are used for authenticating with the GCP.

note

Automatic bucket creation is not supported in Microsoft Azure. You need to manually create the buckets and provide the names using the `--bucket` option.

​

#### Create a unidirectional ClusterPair for NFS​

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

  # Use --dest-ep and --src-ep when configuring asynchronous disaster recovery in cloud platforms.

  # --dest-ep <host.fqdn:port> \

  # --src-ep <shost.fqdn:port> \

  # Starting from Stork version 25.4.1, You can skip the credentials vadiation using the --skip-validation flag

  # --skip-validation

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

​ The following command uses `storkctl` to retrieve information about the cluster pairs in the Kubernetes namespace `<migrationnamespace>`: ​

```

storkctl get clusterpair -n <migrationnamespace>

```

​ This command displays details such as the name and status of the existing cluster pairs within that specific namespace.

Source cluster details:

```

NAME                     STORAGE-STATUS  SCHEDULER-STATUS  CREATED

migration-cluster-pair   Ready           Ready             10 Mar 23 17:16 PST

```

​On a successful pairing, you should see the `STORAGE-STATUS` and `SCHEDULER-STATUS` as `Ready`.

### Bidirectional ClusterPair​

​ A bidirectional ClusterPair establishes authentication from the source cluster to the destination cluster, and vice versa, so resources and data can be migrated in both directions.

​With bidirectional ClusterPair the trust relationship between the two clusters is established in both directions. ​

note

To create an admin ClusterPair, specify the admin namespace using the `--namespace` flag when creating the ClusterPair.

#### Prerequisite​

​ Ensure the same Stork version 23.7.0 or newer is installed on both the source and destination clusters.

note

If you are using a Stork version prior to 23.7.0, then you can follow this procedure to generate an asynchronous DR ClusterPair.

​

#### Create a bidirectional ClusterPair for S3 or S3 compatible​

​ Run the following command to create a bidirectional cluster pairing named `migration-cluster-pair` for cluster migration: ​

```

storkctl create clusterpair migration-cluster-pair \

  --namespace <migrationnamespace> \

  --dest-kube-file <destination-kubeconfig-file> \

  --src-kube-file <source-kubeconfig-file> \

  --provider s3 \

  --s3-endpoint s3.amazonaws.com \

  --s3-access-key <s3-bucket-access-key> \

  --s3-secret-key <your-s3-bucket-access-key> \

  --s3-region <s3-bucket-location> \

  # Use --dest-ep and --src-ep when configuring asynchronous disaster recovery in cloud platforms.

  # --dest-ep <host.fqdn:port> \

  # --src-ep <host.fqdn:port>

```

​ Portworx will use AWS S3 or S3 compatible blob storage for migrating volume data between the two clusters. The credentials specified in the above command are used for authenticating with your cloud platform. The S3 bucket information is provided with the specified access key, secret key, and region (`<s3-bucket-location>`) to facilitate the data transfer between the two clusters.

Bidirectional clusterpair command for AWS S3 with bucket creation:

```

storkctl create clusterpair migration-cluster-pair \

  --namespace <migrationnamespace> \

  --src-kube-file <source-kubeconfig-file> \

  --dest-kube-file <destination-kubeconfig-file> \

  --mode async-dr \

  # Use --dest-ep and --src-ep when configuring asynchronous disaster recovery in cloud platforms.

  # --dest-ep <host.fqdn:port> \

  # --src-ep <host.fqdn:port> \

  # Starting from Stork version 25.4.1, You can skip the credentials vadiation using the --skip-validation flag

  # --skip-validation

--bucket source-cluster-bucket

```

​

#### Create a bidirectional ClusterPair for Microsoft Azure​

Run the following command to create a bidirectional cluster pairing named `migration-cluster-pair` for cluster migration: ​

```

storkctl create clusterpair migration-cluster-pair \

  --namespace <migrationnamespace> \

  --dest-kube-file <destination-kubeconfig-file> \

  --src-kube-file <source-kubeconfig-file> \

  --provider azure \

  --azure-account-name <azure-account-name> \

  --azure-account-key <azure-account-key> \

  # Use --dest-ep and --src-ep when configuring asynchronous disaster recovery in cloud platforms.

  # --dest-ep <host.fqdn:port> \

  # --src-ep <host.fqdn:port>

```

​ The data migration is carried out using the Azure cloud platform, and the Azure storage account information is provided with the specified account name and account key for authentication and data transfer between the two clusters. ​

#### Create a bidirectional ClusterPair for GCP​

Run the following command to create a bidirectional cluster pairing named `migration-cluster-pair` for cluster migration: ​

```

storkctl create clusterpair migration-cluster-pair \

  --namespace <migrationnamespace> \

  --dest-kube-file <destination-kubeconfig-file> \

  --src-kube-file <source-kubeconfig-file> \

  --namespace <migrationnamespace> \

  --provider google \

  --google-project-id <gcp-project-ID> \

  --google-json-key <gcp-json-auth-key> \

  # Use --dest-ep and --src-ep when configuring asynchronous disaster recovery in cloud platforms.

  # --dest-ep <host.fqdn:port> \

  # --src-ep <shost.fqdn:port>

```

​ The data migration is performed using the GCP, and the Google Cloud project is identified by the specified project ID (`<gcp-project-ID>`). Additionally, the JSON key (`<gcp-json-auth-key>`) is provided for authentication to access the required resources for the data transfer between the two clusters.

#### Create a bidirectional ClusterPair for NFS​

Prerequisites

- The minimum required version of Stork for NFS support is 24.4.0.

- The supported NFS version is limited to NFSv4. :::

Run the following command to create a bidirectional ClusterPair named `migration-cluster-pair` for cluster migration:

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

  # Use --dest-ep and --src-ep when configuring asynchronous disaster recovery in cloud platforms.

  # --dest-ep <host.fqdn:port> \

  # --src-ep <host.fqdn:port>

```

Parameters:

- `--provider nfs`: Specifies the provider as NFS.

- `--nfs-server`: Specifies the address of the NFS server (hostname or IP address).

- `--nfs-export-path`: Specifies the exported path on the NFS server.

- `--nfs-sub-path`: Specifies the subpath within the export path to use. If you do not specify a subpath, Portworx creates one automatically.

- `--nfs-mount-opts`: (Optional) Specifies NFS mount options, for example, vers=4.0.

- `--nfs-timeout-seconds`: (Optional) Specifies the NFS IO timeout in seconds (default is 5, valid range is 1-30).

Portworx uses the specified NFS storage for migrating volume data between the two clusters. ​

#### Verify the status of your bidirectional ClusterPair​

​ The following command uses `storkctl` to retrieve information about the cluster pairs in the Kubernetes namespace `<migrationnamespace>`: ​

```

storkctl get clusterpair -n <migrationnamespace>

```

​ This command displays details such as the name and status of the existing cluster pairs within that specific namespace.

Source cluster details:

```

NAME                    STORAGE-STATUS  SCHEDULER-STATUS  CREATED

migration-cluster-pair  Ready           Ready            10 Mar 23 17:16 PST

```

Destination cluster details:

```

NAME                    STORAGE-STATUS  SCHEDULER-STATUS  CREATED

migration-cluster-pair  Ready           Ready             10 Mar 23 17:16 PST

```

On a successful pairing, you should see the `STORAGE-STATUS` and `SCHEDULER-STATUS` as `Ready`.
 Encountered an error?

If you see an error, you can get more information by running the following command:

- Kubernetes

- OpenShift

`kubectl describe clusterpair <your-clusterpair-name> -n <migrationnamespace>`

`oc describe clusterpair <your-clusterpair-name> -n <migrationnamespace>`

In this topic:
