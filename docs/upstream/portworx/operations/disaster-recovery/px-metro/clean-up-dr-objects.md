# Clean up disaster recovery objects

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/px-metro/clean-up-dr-objects (Portworx Enterprise latest)

Clean up disaster recovery objects | Portworx Enterprise Documentation

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

Once a `migrationschedule` object is deleted, also delete all associated migration objects that you retrieved in step 2 of the previous section.

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
Delete the cluster pair from the source cluster:

- Kubernetes

- OpenShift

```

kubectl delete clusterpair <migration-cluster-pair> -n <migrationnamespace>

```

```

oc delete clusterpair <migration-cluster-pair> -n <migrationnamespace>

```
