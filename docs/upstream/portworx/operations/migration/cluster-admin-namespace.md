# Set up a Cluster Admin namespace for migration

Source: https://docs.portworx.com/portworx-enterprise/operations/migration/cluster-admin-namespace (Portworx Enterprise latest)

Set up a Cluster Admin namespace for migration | Portworx Enterprise Documentation

By default, you can only migrate namespaces in which the Migration object is created. This is to prevent any user from migrating namespaces for which they do not have access.
 By default, `kube-system` is the admin namespace, but you can also designate a different namespace as the admin namespace.
 This allows an admin who has access to that namespace to manage migrations for applications across the cluster.

## Configure the Cluster Admin namespace​

In the following example, we set up `portworx` as the admin namespace for migration by updating the Stork deployment.

For a Portworx Operator-based installation, follow these steps:

-
Run the following command to edit the Portworx cluster spec:

- Kubernetes

- OpenShift

```

kubectl edit storagecluster <clusterspecname> -n <px-namespace>

```

```

oc edit storagecluster <clusterspecname> -n <px-namespace>

```

-
In the editor, update the Stork arguments to specify the cluster admin namespace using the `admin-namespace` parameter:

```

stork:

  args:

    admin-namespace: portworx

    webhook-controller: "true"

```

-
Save the changes and wait for all Stork pods to restart and reach the `Running` state:

- Kubernetes

- OpenShift

```

kubectl get pods -l name=stork -n <px-namespace>

```

```

NAME                     READY   STATUS    RESTARTS   AGE

stork-6fdd7d567b-4w86q   1/1     Running   0          63s

stork-6fdd7d567b-lj47r   1/1     Running   0          60s

stork-6fdd7d567b-m6pk7   1/1     Running   0          59s

```

```

oc get pods -l name=stork -n <px-namespace>

```

```

NAME                     READY   STATUS    RESTARTS   AGE

stork-6fdd7d567b-4w86q   1/1     Running   0          63s

stork-6fdd7d567b-lj47r   1/1     Running   0          60s

stork-6fdd7d567b-m6pk7   1/1     Running   0          59s

```

## Create admin ClusterPair​

Creating an admin ClusterPair is the same as creating a regular ClusterPair, but you must specify the admin namespace.

The capabilities of the admin ClusterPair vary depending on the Stork version you use. Refer to the following sections for more information.

### Stork version 25.5.0 or later​

The admin ClusterPair supports migration of both cluster-scoped and namespaced resources, including volumes. This allows you to create Migration and MigrationSchedule objects in any namespace and reference a centrally managed ClusterPair that resides in the admin namespace.

Administrators can define a single ClusterPair with credentials in the admin namespace. Application owners in other namespaces can reference that ClusterPair using the `--admin-cluster-pair` flag.

### Stork version 25.4.1 or earlier​

-
The admin ClusterPair (a ClusterPair object created in the admin namespace) was used only for migrating cluster-scoped resources, such as:

- CustomResourceDefinition objects (CRDs)

- ClusterRole objects

- StorageClass objects

-
Namespaced resources, such as Deployment objects, PersistentVolumeClaim (PVC) objects, and Service objects, still required a ClusterPair to exist in the same namespace as the Migration or MigrationSchedule object.

## Use the admin ClusterPair for migrations in any namespace​

You can reference the ClusterPair in the admin namespace using the `--admin-cluster-pair` flag in your `Migration` or `MigrationSchedule` commands.

### Examples​

-
MigrationSchedule using admin ClusterPair

```

storkctl create migrationschedule mgs-admin \

  -n <migrationNamespace> \

  --namespaces <migration-namespaces> \

  --admin-cluster-pair=<admin-clusterpair-name> \

  --schedule-policy-name <migrationschedule-policy>

```

In this example:

- `<admin-clusterpair-name>` is the ClusterPair created in the admin namespace.

- The MigrationSchedule resides in the `<migrationNamespace>` namespace.

-
MigrationSchedule using both admin and local ClusterPairs

If both flags are provided, the admin ClusterPair takes precedence:

```

storkctl create migrationschedule mgs-mixed \

  -n <migrationNamespace> \

  --namespaces <migration-namespaces> \

  --cluster-pair=<local-clusterpair-name> \

  --admin-cluster-pair=<admin-clusterpair-name> \

  --schedule-policy-name <migrationschedule-policy>

```

-
Migration using admin ClusterPair

```

storkctl create migration <your-migration-object-name> \

  --admin-cluster-pair=<admin-clusterpair-name> \

  --namespaces <app-namespace1>,<app-namespace2> \

  --includeResources=true \

  --startApplications=true \

  --namespace <migrationNamespace>

```

In this example:

- `<admin-clusterpair-name>` is the ClusterPair created in the admin namespace.

- The Migration resides in the `<migrationNamespace>` namespace.

-
Migration using both admin and local ClusterPairs

If both flags are provided, the admin ClusterPair takes precedence:

```

storkctl create migration <your-migration-object-name> \

  --clusterPair <migration-cluster-pair> \

  --admin-cluster-pair=<admin-clusterpair-name> \

  --namespaces <app-namespace1>,<app-namespace2> \

  --includeResources=true \

  --startApplications=true \

  --namespace <migrationNamespace>

```

The Stork logs show which ClusterPair was used:

```

level=info msg="Using effective ClusterPair portworx/<admin-clusterpair-name> (adminClusterPair=\"<admin-clusterpair-name>\", clusterPair=\"<local-clusterpair-name>\")"

```

In this topic:
