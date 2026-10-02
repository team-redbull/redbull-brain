# Deploy PostgreSQL with Portworx

Source: https://docs.portworx.com/portworx-enterprise/deploy-your-applications/application-install-with-kubernetes/postgresql (Portworx Enterprise latest)

Deploy PostgreSQL with Portworx | Portworx Enterprise Documentation

PostgreSQL is an open-source relational database management system known for its robustness, SQL compliance, and extensibility. Learn how to deploy and operate PostgreSQL with Portworx Enterprise on Kubernetes. Portworx provides a resilient, high-performance persistent storage layer that ensures data durability, fault tolerance, and seamless scaling for PostgreSQL database workloads.

Postgres serves as a core data store for many applications that require strong consistency, transactional integrity, and advanced querying capabilities. It can be configured to securely store and manage structured data for a wide range of workloads.

To deploy PostgreSQL with Portworx Enterprise, complete the following collection of tasks:

- Create a StorageClass for dynamic volume provisioning with Portworx Enterprise.

- Create a PVC to request a persistent storage.

- Deploy PostgreSQL using Stork.

## Create a StorageClass​

-
Define a storageclass `px-postgres-sc` and save it in a file `px-postgres-sc.yaml`.

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

    name: px-postgres-sc

provisioner: pxd.portworx.com

parameters:

  repl: "2"

allowVolumeExpansion: true

```

Note the following about this `StorageClass`:

- The `provisioner` parameter is set to `pxd.portworx.com`.

- Two replicas of each volume will be created

-
Apply the spec by entering the following command:

```

kubectl apply -f px-postgres-sc.yaml

```

```

storageclass.storage.k8s.io/px-postgres-sc created

```

## Create a PVC​

-
Define a PVC and save it in a file `px-postgres-vol.yaml`.

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: postgres-data

spec:

  storageClassName: px-postgres-sc

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 1Gi

```

This PVC references the `px-postgres-sc` storage class defined in the Create a StorageClass section. Kubernetes will automatically create a new PVC for each replica.

-
Apply the spec by entering the following command:

```

kubectl apply -f px-postgres-vol.yaml

```

```

persistentvolumeclaim/postgres-data created

```

## Deploy PostgreSQL using Stork​

-
Define a deployment that uses Stork as a scheduler and save it in a file `px-postgres-app.yaml`.

```

apiVersion: apps/v1

kind: Deployment

metadata:

  name: postgres

spec:

  selector:

    matchLabels:

      app: postgres

  strategy:

    rollingUpdate:

      maxSurge: 1

      maxUnavailable: 1

    type: RollingUpdate

  replicas: 1

  template:

    metadata:

      labels:

        app: postgres

    spec:

      schedulerName: stork

      affinity:

        nodeAffinity:

          requiredDuringSchedulingIgnoredDuringExecution:

            nodeSelectorTerms:

            - matchExpressions:

              - key: px/enabled

                operator: NotIn

                values:

                - "false"

      containers:

      - name: postgres

        image: postgres:18.1

        imagePullPolicy: "IfNotPresent"

        ports:

        - containerPort: 5432

        env:

        - name: POSTGRES_USER

          value: pgbench

        - name: POSTGRES_PASSWORD

          value: superpostgres

        - name: PGBENCH_PASSWORD

          value: superpostgres

        - name: PGDATA

          value: /var/lib/postgresql/data/pgdata

        volumeMounts:

        - mountPath: /var/lib/postgresql/data

          name: postgredb

      volumes:

      - name: postgredb

        persistentVolumeClaim:

          claimName: postgres-data

```

Note the following:

- Specifies Stork as scheduler (`schedulerName: stork`)

- Sets the following environment variables:

- POSTGRES_USER (defines the superuser)

- POSTGRES_PASSWORD (specifies the superuser password)

- PGDATA (configures the location for the database files)

- References the `postgres-data` PVC defined in the Create a PVC section.

-
Apply the spec by entering the following command:

```

kubectl apply -f px-postgres-app.yaml

```

```

deployment.apps/postgres created

```

## Verify your PostgreSQL installation​

-
Enter the following `kubectl get` command to list your storage classes:

```

kubectl get sc

```

```

NAME                                 PROVISIONER        RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE

px-postgres-sc                       pxd.portworx.com   Delete          Immediate           true                   4m41s

```

In the above example output, note that the provisioner is set to `pxd.portworx.com`

-
Enter the `kubectl get pvc` command to verify that the PVC is bound to a volume:

```

kubectl get pvc

```

```

NAME            STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS     VOLUMEATTRIBUTESCLASS   AGE

postgres-data   Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxb415   1Gi        RWO            px-postgres-sc   <unset>                 3m34s

```

-
Use the `kubectl get pods` command to verify the status of the PostgreSQL pod:

```

kubectl get pod

```

```

NAME                        READY   STATUS    RESTARTS   AGE

postgres-687bbdd6d9-zrdqz   1/1     Running   0          2m

```

Make a note of the name of the pod. You'll need it in the next step.

-
Enter the following `kubectl exec` command, specifying your own pod name, to open a shell session into your pod. This example opens the `postgres-86cb8587c4-l9r48` pod:

```

kubectl exec -it postgres-86cb8587c4-l9r48 -- bash

```

```

root@postgres-687bbdd6d9-zrdqz:/#

```

-
Start the PostgreSQL interactive shell. Use the`-U` flag to connect as the `pgbench` user:

```

root@postgres-86cb8587c4-l9r48:/# psql -U pgbench

```

```

psql (9.5.10)

Type "help" for help.

```

-
List your databases:

```

pgbench=# \l

```

```

   Name    |  Owner  | Encoding | Locale Provider |  Collate   |   Ctype    | Locale | ICU Rules |  Access privileges

-----------+---------+----------+-----------------+------------+------------+--------+-----------+---------------------

 pgbench   | pgbench | UTF8     | libc            | en_US.utf8 | en_US.utf8 |        |           |

 postgres  | pgbench | UTF8     | libc            | en_US.utf8 | en_US.utf8 |        |           |

 template0 | pgbench | UTF8     | libc            | en_US.utf8 | en_US.utf8 |        |           | =c/pgbench         +

           |         |          |                 |            |            |        |           | pgbench=CTc/pgbench

 template1 | pgbench | UTF8     | libc            | en_US.utf8 | en_US.utf8 |        |           | =c/pgbench         +

           |         |          |                 |            |            |        |           | pgbench=CTc/pgbench

(4 rows)

```

-
Exit the PostgreSQL interactive shell:

```

pgbench=# \q

root@postgres-687bbdd6d9-zrdqz:/# exit

exit

```

In this topic:
