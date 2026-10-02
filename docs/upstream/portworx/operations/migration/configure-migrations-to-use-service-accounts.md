# Configure migrations to use service accounts

Source: https://docs.portworx.com/portworx-enterprise/operations/migration/configure-migrations-to-use-service-accounts (Portworx Enterprise latest)

Configure migrations to use service accounts | Portworx Enterprise Documentation

If you set up migrations and migration schedules using user accounts, you will encounter token expiration-related errors. To avoid these errors, Portworx, Inc. recommends setting up migration and migration schedules using service accounts. ​ In contrast to user accounts, which expire after a specified interval of time has passed, service account tokens do not expire. Using service accounts ensures that you will not encounter token expiration-related errors. See the User accounts versus service accounts section of the Kubernetes documentation for more details about the differences between service accounts and user accounts. ​ Perform the following steps on the destination cluster to configure migrations to use service accounts. ​

## Create a service account and a cluster role binding​

Follow the instructions in the following sections to create a service account and cluster role binding.

### Create a service account​

-
Create a file called `service-account-migration.yaml` with the following content, specifying the `namespace:` to match one of the existing namespaces in your cluster. For this example we will use the `default` namespace:

```

 apiVersion: v1

 kind: ServiceAccount

 metadata:

   name: migration

   namespace: default

```

-
Apply the spec:

- Kubernetes

- OpenShift

```

kubectl apply -f service-account-migration.yaml

```

```

oc apply -f service-account-migration.yaml

```

### Create a cluster role binding​

- Create a file called `cluster-role-binding-migration.yaml` with the following content, specifying the `namespace:` field to match the namespace in the previous step:

```

apiVersion: rbac.authorization.k8s.io/v1

kind: ClusterRoleBinding

metadata:

  name: migration-clusterrolebinding

roleRef:

  apiGroup: rbac.authorization.k8s.io

  kind: ClusterRole

  name: cluster-admin

subjects:

- kind: ServiceAccount

  name: migration

  namespace: default

```

note

The `roleRef.name` field is set to `cluster-admin`. For details about super-user access, see the User-facing roles section of the Kubernetes documentation.

- Apply the spec:

- Kubernetes

- OpenShift

```

kubectl apply -f cluster-role-binding-migration.yaml

```

```

oc apply -f cluster-role-binding-migration.yaml

```

### Create a Secret​

- For Kubernetes version 1.24 or newer, you also need to create a secret. In the example below, the name in the annotation `kubernetes.io/service-account.name` must match the name of the service account that you created.

```

apiVersion: v1

kind: Secret

metadata:

  name: migration

  namespace: default

  annotations:

    kubernetes.io/service-account.name: migration

type: kubernetes.io/service-account-token

```

- Apply the secret:

- Kubernetes

- OpenShift

```

kubectl apply -f <migrationsecretname>.yaml

```

```

oc apply -f <migrationsecretname>.yaml

```

## Create a kubeconfig file​

- Download the create-migration-config.sh script file. Edit the file and change the values of the `SERVER` and `NAMESPACE` variables to match your environment.

- To create a kubeconfig file, enter the following commands:

```

chmod +x create-migration-config.sh && ./create-migration-config.sh > ~/.kube/migration-config.conf

```

- Set the value of the `KUBECONFIG` environment variable to point to the kubeconfig file that you created in the previous step:

```

export KUBECONFIG=~/.kube/migration-config.conf

```

## Create a ClusterPair​

- Generate `kubeconfig` files, using the Create a kubeconfig file procedure.

- Create an synchronous DR ClusterPair or Create an asynchronous DR ClusterPair depending upon your environment.

In this topic:
