# Clean up disaster recovery objects

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/async-dr/clean-up-dr-objects (Portworx Enterprise 3.6)

Clean up disaster recovery objects | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

If you no longer require a disaster recovery object, you can delete it.

Perform the following steps from a location where you have `kubectl` or `oc` access to the source cluster:

-
Delete the migration schedule:

- Kubernetes

- OpenShift

```

kubectl delete migrationschedules <migrationschedule-name> -n <migrationnamespace>

```

```

oc delete migrationschedules <migrationschedule-name> -n <migrationnamespace>

```

note

Once a `MigrationSchedule` object is deleted, also delete all associated migration objects that you retrieved in step 2 of the previous section.

-
Delete the associated schedule policy:

- Kubernetes

- OpenShift

```

kubectl delete schedulepolicy <your-schedule-policy>

```

```

oc delete schedulepolicy <your-schedule-policy>

```

-
Delete the cluster pair from the source cluster and reverse ClusterPair from the destination cluster, if applicable:

- Kubernetes

- OpenShift

```

kubectl delete clusterpair <migration-cluster-pair> -n <migrationnamespace>

```

```

oc delete clusterpair <migration-cluster-pair> -n <migrationnamespace>

```

-
Delete the ClusterPair resources on the destination cluster.

When you delete the unidirectional or bidirectional ClusterPair on the source cluster, it will not automatically delete the associated secret and backup location on the destination cluster.

You should manually delete the ClusterPair resources on the destination cluster using the following commands:

-
Delete the associated backup location that is created on the destination cluster. By default, it is created with the same name as your ClusterPair; otherwise, update it with your custom backup location name in the following command:

- Kubernetes

- OpenShift

```

kubectl delete backuplocation <migration-cluster-pair> -n <migrationnamespace>

```

```

oc delete backuplocation <migration-cluster-pair> -n <migrationnamespace>

```

-
Delete the secret object created on the destination cluster:

- Kubernetes

- OpenShift

```

kubectl delete secret <secret-name> -n <migrationnamespace>

```

```

oc delete secret <secret-name> -n <migrationnamespace>

```

note

- Portworx ensures that the associated backup location is not deleted when deleting a ClusterPair, if it is used by other ClusterPairs.

- If you change the backup location, you must delete all ClusterPairs associated with the backup location and recreate them.
