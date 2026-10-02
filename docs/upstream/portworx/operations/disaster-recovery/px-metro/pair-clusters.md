# Create a ClusterPair

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/px-metro/pair-clusters (Portworx Enterprise 3.6)

Create a ClusterPair | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

In a synchronous DR setup, it is essential to pair two clusters to enable the migration of resources. To facilitate this process, you need to establish trust objects, known as ClusterPair objects, between the two clusters. Portworx requires these objects to establish a communication channel between the two clusters.

The ClusterPair objects pair the two clusters, allowing migration of resources.

Creation of the ClusterPair object does not initiate the actual migration of resources between the clusters. It establishes the foundation for a trust-based relationship between the clusters. Using this ClusterPair object, you can create a migration schedule that initiate the data migration between the two paired clusters.

With Stork, you can establish bidirectional cluster pairing, which will enable resource migration in both directions across the two clusters. This also facilitates smooth application failover and failback processes.

important

- Starting from Stork version 25.5.0, you can create an admin ClusterPair object that supports migration of both cluster-scoped and namespaced resources, including persistent volumes. This configuration allows you to create `Migration` and `MigrationSchedule` objects in any namespace and reference a centrally managed ClusterPair in the `admin` namespace. For more information, see Create admin ClusterPair.

- The default admin namespace is `kube-system`. In all examples, `<migrationnamespace>` is considered the admin namespace responsible for migrating all namespaces from your source cluster to the destination cluster. Alternatively, you can specify a non-admin namespace, but note that only that specific namespace will be migrated. To learn how to set up an admin namespace, refer to the Set up a Cluster Admin namespace for Migration page.

## Pair your clusters​

​ You can create either unidirectional or bidirectional ClusterPairs. In Synchronous DR setup where there is a single stretched cluster, it is recommended to generate the bidirectional ClusterPair objects. The bidirectional ClusterPair establishes a trusted relationship between the two clusters in both directions, enabling seamless migration of resources and data in both directions.

Starting with Stork version 25.5.0, you can create an admin ClusterPair and use it to migrate both cluster-scoped and namespaced resources, including volumes. Creating an admin ClusterPair is the same as creating a namespace-scoped ClusterPair, except that you must specify an admin namespace.

note

If you set up migrations and migration schedules using user accounts, you will encounter token expiration-related errors. To avoid these errors, Portworx by Everpure. recommends setting up migrations and migration schedules using service accounts. For service accounts, you need to create a kubeconfig file by following the steps here and use the same file when creating a ClusterPair.

### Prerequisite​

​ The same Stork version 23.7.0 or newer is installed on both the source and destination clusters.

note

If you are using a Stork version prior to 23.7.0, then you can follow this procedure to generate a synchronous DR ClusterPair.

### Create a bidirectional ClusterPair​

​ Run the following command from the system where `storkctl` is installed. It creates a cluster pairing named `migration-cluster-pair` on both source and destination clusters: ​

```

storkctl create clusterpair migration-cluster-pair \

--namespace <migrationnamespace> \ # To create an admin ClusterPair, specify the admin namespace

--src-kube-file <source-kubeconfig-file> \

--dest-kube-file <destination-kubeconfig-file> \

--mode sync-dr

```

This command establishes authentication in both directions between each cluster. ​

### Verify the status of your bidirectional ClusterPair​

​ Run the following command to retrieve information about the cluster pairs in the cluster namespace `<migrationnamespace>`: ​

```

storkctl get clusterpair migration-cluster-pair -n <migrationnamespace>

```

​ Source cluster details:

```

NAME                     STORAGE-STATUS   SCHEDULER-STATUS   CREATED

migration-cluster-pair   NotProvided      Ready              14 Jun 23 18:24 UTC

```

Destination cluster details:

```

NAME                     STORAGE-STATUS   SCHEDULER-STATUS   CREATED

migration-cluster-pair   NotProvided      Ready              14 Jun 23 18:24 UTC

```

On a successful pairing you will see the scheduler status as `Ready`. Since there is only one Portworx cluster spanning both clusters, there is no need to pair Storage, thus the storage status will be `NotProvided`.
 Encountered an error?

If you see an error, you can get more information by running the following command:

- Kubernetes

- OpenShift

`kubectl describe clusterpair <your-clusterpair-name> -n <migrationnamespace>`

`oc describe clusterpair <your-clusterpair-name> -n <migrationnamespace>`

In this topic:
