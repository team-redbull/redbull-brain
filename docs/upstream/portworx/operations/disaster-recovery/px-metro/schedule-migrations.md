# Schedule migrations

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/px-metro/schedule-migrations (Portworx Enterprise 3.6)

Schedule migrations | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Once your source and destination clusters are paired, you need to create a schedule to migrate one or more namespaces periodically. Because you have only one Portworx cluster stretched across your source and destination clusters, you will only migrate Kubernetes or OpenShift resources and not your volumes.

note

If you are using Stork version 24.2.0 or later, when you create a migration schedule in the source cluster, Stork automatically creates a corresponding migration schedule in the destination cluster. This migration schedule is used as a reference during the failover operation, and you must not manipulate this migration schedule on the destination cluster.

## Create a schedule policy on your source cluster​

You have two options for creating a schedule policy:

-
Use the `storkctl create schedulepolicy` command with the required flags. For more details and examples, refer to the Create schedule policy with storkctl section.

-
Alternatively, to schedule a migration, you must define a schedule policy. You can select from two types of policies:

- SchedulePolicy: A cluster-scoped policy that applies to the entire cluster.

- NamespacedSchedulePolicy: A namespace-scoped policy that applies only to the specified namespace in the policy spec.

Follow the steps below to create a schedule policy on your source cluster:

-
Create a spec file using one of the following methods.

-
For `SchedulePolicy`, create the following spec file:

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: SchedulePolicy

metadata:

  name: <your-schedule-policy>

policy:

  interval:

    intervalMinutes: 30

```

For a list of parameters that you can use to create a schedule policy, see the Schedule Policy page.

-
For `NamespacedSchedulePolicy`, create the following spec file:

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: NamespacedSchedulePolicy

metadata:

  name: <your-schedule-policy>

  namespace: <migrationnamespace>

policy:

  interval:

    intervalMinutes: 30

```

For a list of parameters that you can use to create a namespaced policy, you can use the fields described on the Schedule Policy page, replacing `SchedulePolicy` with `NamespacedSchedulePolicy`.

-
You can also use the schedule policies that are installed by default. Run the `storkctl get schedulepolicy` command to get the list of these policies, then specify a policy name in the next section for creating a migration schedule. You can skip the next step if you are using the default policies, as they are already applied to your cluster.

-
Apply your policy on the source cluster:

- Kubernetes

- OpenShift

```

kubectl apply -f <your-schedule-policy>.yaml

```

```

oc apply -f <your-schedule-policy>.yaml

```

-
Verify if the policy has been created:

```

storkctl get schedulepolicy <your-schedule-policy>

```

```

NAME                      INTERVAL-MINUTES    DAILY     WEEKLY             MONTHLY

<your-schedule-policy>          30             N/A       N/A                N/A

```

## Create a migration schedule on your source cluster​

Once a policy has been created, you can use it to schedule migrations.

note

For operators deployed from the OpenShift OperatorHub, create a migration schedule with the `--exclude-resource-types` flag to exclude operator-related resources, as shown in the following example:

```

storkctl create migrationschedule -c <cluster-pair> --namespaces <namespace> <migration-schedule> --exclude-resource-types ClusterServiceVersion,operatorconditions,OperatorGroup,InstallPlan,Subscription --exclude-selectors olm.managed=true

```

You have two options for creating a migration schedule:

-
Run the `storkctl create migrationschedule` command-line tool along with the required flags. See Create migration schedule with storkctl topic for more information about the commands with examples.

note

To validate which resources will be included in a MigrationSchedule before creating it, use the `--preview` or `--preview-file` flags with the `storkctl create migrationschedule` command. This helps ensure that all required resources—namespaced and non-namespaced—are identified in advance. For more information, see Preview resources before creating migration schedule.

or

-
Perform the following steps on your source cluster:

-
Copy and paste the following spec into a file called `migrationschedule.yaml`. Modify the following spec to use a different migration schedule name and/or namespace. Ensure that the `clusterPair` name is correct.

note

If you have created an admin ClusterPair, you can use it instead of creating a local ClusterPair. Use the `spec.template.spec.adminClusterPair` field instead of `spec.template.spec.clusterPair`.

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: MigrationSchedule

metadata:

  name: migrationschedule

  namespace: <migrationnamespace>

spec:

  template:

    spec:

      clusterPair: <your-clusterpair-name>

      includeResources: true

      startApplications: false

      includeVolumes: false

      namespaces:

      - <app-namespace1>

      - <app-namespace2>

  schedulePolicyName: <your-schedule-policy>

  suspend: false

  autoSuspend: true

```

note

- The option `startApplications` must be set to false in the spec to ensure that the application pods do not start on the remote cluster when the Kubernetes or OpenShift resources are being migrated.

- The option `includeVolumes` is set to false because the volumes are already present on the destination cluster as this is a single Portworx cluster.

- With Stork 23.2 or newer, you can set the `autoSuspend` flag to `true`, as shown in the above spec. In case of a disaster, this will suspend the DR migration schedules automatically on your source cluster, and you will be able to migrate your application to an active Kubernetes or OpenShift cluster. If you are using an older version of Stork, refer to the Failover an application page for achieving failover for your application.

- Apply your `migrationschedule.yaml` by entering the following command:

- Kubernetes

- OpenShift

```

kubectl apply -f migrationschedule.yaml

```

```

oc apply -f migrationschedule.yaml

```

If the policy name is missing or invalid there will be events logged against the schedule object. Success and failures of the migrations created by the schedule will also result in events being logged against the object. These events can be seen by running a `kubectl describe` or `oc describe` command on the object.

## Check your migration status​

-
Run the following command on your source cluster to check the status of your migration:

```

storkctl get migration -n <migrationnamespace>

```

```

NAMESPACE                      NAME                                                                CLUSTERPAIR                STAGE   STATUS       VOLUMES   RESOURCES   CREATED               ELAPSED                          TOTAL BYTES TRANSFERRED

bidirectional-clusterpair-ns   <your-app>-migration-schedule-interval-interval-2023-08-28-015917   birectional-cluster-pair   Final   Successful   1/1       4/4         27 Aug 23 19:59 MDT   Volumes (33s) Resources (1m2s)   4096

```

-
The output above indicates a successful migration in the `Status` column. It also provides a list of migration objects along with timestamps associated with your migration.

-
You can also run the following command to check details about specific migrations:

- Kubernetes

- OpenShift

```

kubectl describe migration -n <migrationnamespace>

```

```

oc describe migration -n <migrationnamespace>

```

-
Verify your application and associated resources have been migrated by running the following command on your destination cluster:

- Kubernetes

- OpenShift

```

kubectl get all -n zookeeper

```

```

oc get all -n zookeeper

```

```

  NAME                      TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE

  service/zk-service        ClusterIP   10.xxx.xx.68   <none>        xxxx/TCP   2m13s

  NAME                       READY   UP-TO-DATE   AVAILABLE   AGE

  deployment.apps/zk         0/0     0            0           2m13s

  NAME                               DESIRED   CURRENT   READY   AGE

  replicaset.apps/zk-59d878d987      0         0         0       2m13s

```

This confirms that the respective namespace has been created and the applications (for example, Zookeeper) are installed. However, the application pods will not be running because they are running on the source cluster.

note

As part of every Migration, Stork will also migrate the Kubernetes or OpenShift resources associated with your applications. For a successful migration, these applications need to be in a scaled down state on the destination side so that subsequent migrations from the same schedule can run to completion. To achieve this Stork will leverage `spec.replicas` from most of the standard controllers such as Kubernetes Deployments, StatefulSets, and so on. However, for applications managed by an Operator an `ApplicationRegistration` CR needs to be created which provides Stork with the necessary information required to perform a scale down of the application. Refer to the ApplicationRegistrations page for more details.

In this topic:
