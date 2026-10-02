# Failback an application

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/px-metro/failback-app (Portworx Enterprise latest)

Failback an application | Portworx Enterprise Documentation

Failback is the process of moving the application and its data back to the source cluster once the source cluster is restored and operational again.

Once your unhealthy Kubernetes cluster is back up and running, the Portworx nodes in that cluster will not immediately rejoin the cluster. They will stay in `Out of Quorum` state until you explicitly Activate this cluster domain.

After this domain is marked as Active you can failback the applications if you want.

important

Portworx supports failback operations at the namespace level. You can failback a set of VMs or applications using label-based or name-based selection within a namespace. Starting from Stork 26.4.0, you can also select or exclude specific resources by name. See:

- Perform failback for specific resources by name (Stork 26.4.0 and later)

The following considerations are used in the examples on this page. Update them to the appropriate values for your environment:

- Source Cluster is the Kubernetes cluster which is down and where your applications were originally running. The cluster domain for this source cluster is `us-east-1a`.

- Destination Cluster is the Kubernetes cluster where the applications will be failed over. The cluster domain for this destination cluster is `us-east-1b`.

- The Zookeeper application is being failed over to the destination cluster.

## Prerequisites​

-
You must ensure that Stork version 24.2.0 or newer is installed on both the source and destination clusters.

note

If you are using a Stork version prior to 24.2.0, then you can follow this procedure to perform a failback.

-
For operators deployed from the OpenShift OperatorHub, ensure that the operator and applications are in scaled down state on the destination cluster. Stork will leverage `spec.replicas` from most of the standard Kubernetes controllers such as Deployments, StatefulSets, and so on. However, for applications managed by an Operator, an `ApplicationRegistration` CR needs to be created which provides Stork with the necessary information required to perform a scale down of the application. For more information, see the Application Registration document.

## Create a reverse ClusterPair​

note

Skip this section if you have created a bidirectional ClusterPair, and move to the next section.

You need to create a reverse ClusterPair if you had initially paired your clusters in a unidirectional manner (from source to destination), and now you should establish a pairing from the destination cluster back to the source cluster. The reverse ClusterPair enables reverse communication between the clusters (from destination to source), allowing for failback.

Run the following command from your destination cluster to create a reverse ClusterPair:

```

storkctl create clusterpair reverse-migration-cluster-pair \

--namespace <migrationnamespace> \

--src-kube-file <destination-kubeconfig-file> \

--dest-kube-file <source-kubeconfig-file> \

--mode sync-dr \

--unidirectional

```

important

Ensure to provide the destination kubeconfig file with `src-kube-file` and the source kubeconfig file with `dest-kube-file` as mentioned in the above command.

## Reactivate your source cluster domain​

Once your source cluster is operational, perform the following steps from your destination cluster to activate your source cluster domain:

-
Run the following command to activate the source cluster domain:

```

storkctl activate clusterdomain us-east-1a

```

```

Cluster Domain activate operation started successfully for us-east-1a

```

-
Verify if the source cluster domain is activated:

```

storkctl get clusterdomainsstatus

```

```

NAME                            LOCAL-DOMAIN   ACTIVE                                     INACTIVE   CREATED

px-dr-cluster                   us-east-1a     us-east-1a (InSync), us-east-1b (InSync)              29 Nov 22 22:09 UTC

```

## Reverse sync your clusters​

If the destination cluster has been running applications for some time, it is possible that the state of your application on the destination cluster differs from your source cluster. This is due to the creation of new resources or changes in data within stateful applications on the destination cluster.

It is recommended to perform one migration from destination cluster to your source cluster before failing back your applications, so that you have the most up-to-date applications on your original source cluster.

As both of your clusters are accessible, follow the instructions to configure a reverse migration schedule:

-
Create a schedule policy on your destination cluster using the instructions in the Create a schedule policy section.

-
Create a migration schedule on your destination cluster using the `storkctl create migrationschedule` command. For more information on how to use the command, see Create MigrationSchedule with storkctl.

note

For operators deployed from the OpenShift OperatorHub, create a migration schedule with the `--exclude-resource-types` flag to exclude operator-related resources, as shown in the following example:

```

storkctl create migrationschedule -c cluster-pair -n zookeeper reverse-migration-schedule --exclude-resource-types ClusterServiceVersion,operatorconditions,OperatorGroup,InstallPlan,Subscription --exclude-selectors olm.managed=true

```

## Perform failback​

You can perform a failback using the `storkctl perform failback` command.

You can also use one of the following flags to include or exclude specific namespaces or resources during the failback operation. This allows you to have more control over which resources and namespaces are included in the failback operation.

-
Namespace filters

- `--include-namespaces` - Include only a specific subset of namespaces for the migration.

- `--exclude-namespaces` - Exclude specific namespaces from the migration.

-
Resource filters

- `--selectors` - Activate/deactivate only resources with the specified labels.

- `--exclude-selectors` - Exclude resources with the specified labels from activation/deactivation.

- `--resource-types` - Filter resources by type. Format: `KIND` or `GROUP/VERSION/KIND` (e.g., `apps/v1/Deployment`). Could be specified multiple times.

- `--include-objects` - Include specific objects by name. Format: `KIND/NAMESPACE/NAME` or `GROUP/VERSION/KIND/NAMESPACE/NAME`. Mutually exclusive with `--selectors`, `--exclude-selectors`, `--resource-types`, and `--exclude-objects`.

- `--exclude-objects` - Exclude specific objects by name. Format: `KIND/NAMESPACE/NAME` or `GROUP/VERSION/KIND/NAMESPACE/NAME`. Mutually exclusive with `--selectors`, `--exclude-selectors`, `--resource-types`, and `--include-objects`.

-
Operation flags

- `--skip-last-mile-migration` - Use this flag if you want to skip the last-mile migration before workloads are activated.

note

You cannot use `--include-namespaces` and `--exclude-namespaces` together, nor can you use `--selectors` and `--exclude-selectors` together, or you'll get an error.

```

storkctl perform failback --selectors=app=busybox --exclude-selectors=app=px-mongo-mongodb

```

```

error: can provide only one of --selectors or --exclude-selectors values at once

```

To start the failback operation, run the following command in the destination cluster:

```

storkctl perform failback -m <reverse-migration-schedule> -n <reverse-migration-schedule-namespace>

```

If the last migration status is in the `PartialSuccess` state, you'll be prompted to proceed with the failback operation. To bypass this prompt, use the `--force` flag.

Example:

```

storkctl perform failback -m reverse-migration-schedule -n zookeeper

```

```

Started failback for MigrationSchedule zookeeper/reverse-migration-schedule

To check failback status use the command : `storkctl get failback failback-reverse-migration-schedule-2024-05-21-115006 -n zookeeper`

```

Examples with filtering:

Namespace filtering:

```

# Perform failback for only specific namespaces

storkctl perform failback -m reverse-migration-schedule -n zookeeper --include-namespaces=app-ns1,app-ns2

```

```

# Perform failback for all namespaces except specific ones

storkctl perform failback -m reverse-migration-schedule -n zookeeper --exclude-namespaces=test-ns

```

Resource filtering:

```

# Perform failback for only the resources with the label app=busybox

storkctl perform failback -m reverse-migration-schedule -n zookeeper --selectors=app=busybox

```

```

# Perform failback for all resources except the ones with the label app=busybox

storkctl perform failback -m reverse-migration-schedule -n zookeeper --exclude-selectors=app=busybox

```

```

# Perform failback for only StatefulSet resources

storkctl perform failback -m reverse-migration-schedule -n zookeeper --resource-types=StatefulSet

```

```

# Perform failback for only Deployment and CronJob resources

storkctl perform failback -m reverse-migration-schedule -n zookeeper --resource-types Deployment --resource-types batch/v1/CronJob

```

### Perform failback for specific resources by name​

You can fail back or exclude specific Kubernetes resources by name using the `--include-objects` or `--exclude-objects` flags. These flags can be specified multiple times for multiple resources.

The format for `--include-objects` and `--exclude-objects` is one of:

- `KIND/NAMESPACE/NAME` (e.g., `VirtualMachine/app-ns/my-vm`)

- `GROUP/VERSION/KIND/NAMESPACE/NAME` (e.g., `apps/v1/Deployment/app-ns/payments-api`)

note

- The `NAMESPACE` in the object path is the namespace where the resource lives, which may differ from the MigrationSchedule namespace specified with `-n`.

- `--include-objects` and `--exclude-objects` are mutually exclusive with each other and with `--selectors`, `--exclude-selectors`, and `--resource-types`.

- Both flags can be combined with `--include-namespaces` and `--exclude-namespaces`.

Include specific resources:

```

# Fail back a specific KubeVirt VM by name

storkctl perform failback -m reverse-migration-schedule -n <namespace> \

  --include-objects VirtualMachine/app-ns/my-vm

```

```

# Fail back multiple resources by name

storkctl perform failback -m reverse-migration-schedule -n <namespace> \

  --include-objects VirtualMachine/app-ns/vm-payments \

  --include-objects VirtualMachine/app-ns/vm-billing

```

```

# Fail back a Deployment by name with full group/version syntax

storkctl perform failback -m reverse-migration-schedule -n <namespace> \

  --include-objects apps/v1/Deployment/app-ns/payments-api

```

Exclude specific resources:

```

# Fail back all resources except a specific VM

storkctl perform failback -m reverse-migration-schedule -n <namespace> \

  --exclude-objects VirtualMachine/app-ns/my-vm

```

## Check failback status​

Run the following command to check the status of the failback operation. You can get the `failback-action-name` from the output of the `storkctl perform failback` command.

```

storkctl get failback <failback-action-name> -n <reverse-migration-schedule-namespace>

```

Example:

```

storkctl get failback failback-reverse-migration-schedule-2024-05-21-115006 -n zookeeper

```

```

NAME                                 CREATED               STAGE       STATUS       MORE INFO

failback-reverse-migration-schedule-2024-05-21-115006   21 May 24 11:50 UTC   Completed   Successful   Scaled up Apps in : 1/1 namespaces

```

If the status is failed, you can use the following command to get more information about the failure:

- Kubernetes

- OpenShift

```

kubectl describe actions <failback-action-name> -n <reverse-migration-schedule-namespace>

```

```

oc describe actions <failback-action-name> -n <reverse-migration-schedule-namespace>

```

## Verify volumes and Kubernetes resources are migrated​

To verify the volumes and Kubernetes resources that are migrated to the source cluster, run the following command:

- Kubernetes

- OpenShift

```

kubectl get all -n <reverse-migration-schedule-namespace>

```

Example:

```

kubectl get all -n zookeeper

```

```

NAME                     READY   STATUS    RESTARTS   AGE

pod/zk-544ffcc474-6gx64   1/1     Running   0          18h

NAME                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE

service/zk-service   ClusterIP   10.233.22.60   <none>        3306/TCP   18h

NAME                 READY   UP-TO-DATE   AVAILABLE   AGE

deployment.apps/zk   1/1     1            1           18h

NAME                            DESIRED   CURRENT   READY   AGE

replicaset.apps/zk-544ffcc474   1         1         1       18h

```

```

oc get all -n <reverse-migration-schedule-namespace>

```

Example:

```

oc get all -n zookeeper

```

```

NAME                     READY   STATUS    RESTARTS   AGE

pod/zk-544ffcc474-6gx64   1/1     Running   0          18h

NAME                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE

service/zk-service   ClusterIP   10.233.22.60   <none>        3306/TCP   18h

NAME                 READY   UP-TO-DATE   AVAILABLE   AGE

deployment.apps/zk   1/1     1            1           18h

NAME                            DESIRED   CURRENT   READY   AGE

replicaset.apps/zk-544ffcc474   1         1         1       18h

```

In this topic:
