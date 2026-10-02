# Deploy MySQL with Portworx Enterprise

Source: https://docs.portworx.com/portworx-enterprise/deploy-your-applications/application-install-with-kubernetes/mysql (Portworx Enterprise 3.6)

Deploy MySQL with Portworx Enterprise | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

MySQL is an open-source RDBMS deployed on Kubernetes for scalable web applications. Integrating Portworx with MySQL provides dynamic storage provisioning, automated high-availability failover, and granular data security. This solution ensures reliable performance and robust disaster recovery for mission-critical data. Learn how to setup MySQL with Portworx on Kubernetes and test failover of your application.

To deploy MySQL with Portworx Enterprise, complete the following collection of tasks:

- Create a StorageClass for dynamic volume provisioning with Portworx

- Create a PVC to request a persistent storage

- Deploy MySQL using Stork as scheduler by Portworx

## Create a StorageClass​

-
Define a storageclass `px-mysql-sc` and save it in a file `px-mysql-sc.yaml`.

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

    name: px-mysql-sc

provisioner: pxd.portworx.com

parameters:

   repl: "2"

```

Note the following about this `StorageClass`:

- The `provisioner` parameter is set to `pxd.portworx.com`.

- Two replicas of each volume will be created.

-
Apply the spec by entering the following command:

```

kubectl apply -f px-mysql-sc.yaml

```

```

storageclass.storage.k8s.io/px-mysql-sc created

```

## Create a PVC​

-
Define a PVC and save it in a file `px-mysql-vol.yaml`.

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: mysql-data

spec:

  storageClassName: px-mysql-sc

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

```

This PVC references the `px-mysql-sc` storage class defined in the Create a StorageClass section. Kubernetes will automatically create a new PVC for each replica.

-
Apply the spec by entering the following command:

```

kubectl apply -f px-mysql-vol.yaml

```

```

persistentvolumeclaim/mysql-data created

```

## Deploy MySQL using Stork​

-
Define a deployment that uses Stork as a scheduler and save it in a file `px-mysql-app.yaml`.

```

apiVersion: apps/v1

kind: Deployment

metadata:

  name: mysql

spec:

  selector:

    matchLabels:

      app: mysql

  strategy:

    rollingUpdate:

      maxSurge: 1

      maxUnavailable: 1

    type: RollingUpdate

  replicas: 1

  template:

    metadata:

      labels:

        app: mysql

        version: "1"

    spec:

      schedulerName: stork

      containers:

      - image: mysql:5.6

        name: mysql

        env:

        - name: MYSQL_ROOT_PASSWORD

          value: password

        ports:

        - containerPort: 3306

        volumeMounts:

        - name: mysql-persistent-storage

          mountPath: /var/lib/mysql

      volumes:

      - name: mysql-persistent-storage

        persistentVolumeClaim:

          claimName: mysql-data

```

Note the following about the MySQL deployment:

-
MySQL is deployed as a single-replica Deployment using the `mysql:5.6` container image.

-
A PersistentVolumeClaim (`mysql-data`) is mounted at `/var/lib/mysql` to persist database data.

-
Portworx STORK scheduler is used to ensure storage-aware pod placement.

-
A rolling update strategy allows controlled updates with minimal disruption.

-
Apply the spec by entering the following command:

```

kubectl apply -f px-mysql-app.yaml

```

```

deployment.apps/mysql created

```

## Test Failover of a MySQL pod on Portworx​

Learn how to failover MySQL Pod to a different node on Portworx.

- Check the database exists on the Kubernetes cluster.

```

export MYSQLPOD=$(kubectl get pods -l app=mysql --no-headers | awk '{print $1}')

kubectl logs $MYSQLPOD

kubectl exec -ti $MYSQLPOD -- bash

mysql --user=root --password=password

```

- Create a database `TEST_1234`, verify that it is created and exit.

```

mysql> create database TEST_1234;

Query OK, 1 row affected (0.00 sec)

mysql> show databases;

+--------------------+

| Database           |

+--------------------+

| information_schema |

| TEST_1234          |

| mysql              |

| performance_schema |

+--------------------+

4 rows in set (0.00 sec)

mysql> exit

Bye

root@mysql-xxxx668f89-lqgg8:/# exit

exit

```

- View the node on which mysql pod is running.

```

kubectl get pods -o wide

NAME                     READY   STATUS    RESTARTS   AGE   IP            NODE                                  NOMINATED NODE   READINESS GATES

mysql-xxxx668f89-lqgg8   1/1     Running   0          46m   10.xxx.xx.7   ip-10-xx-xx-221.xxx.purestorage.com   <none>           <none>

```

- Mark the node on which mysql pod is running as unschedulable.

```

export MYSQL_NODE=$(kubectl describe pod -l app=mysql | grep Node: | awk -F'[ \t//]+' '{print $2}')

kubectl cordon $MYSQL_NODE

```

```

node/ip-10-xx-xx-221.pwx.purestorage.com cordoned

```

- Delete the mysql pod running on Kubernetes cluster.

```

kubectl delete pod -l app=mysql

```

```

pod "mysql-xxxx668f89-lqgg8" deleted

```

- Verify pod failover to a new node since old node is marked cordoned.

```

kubectl get pods -o wide

```

```

NAME                     READY   STATUS    RESTARTS   AGE    IP              NODE                                  NOMINATED NODE   READINESS GATES

mysql-xxxx668f89-nvw65   1/1     Running   0          101s   10.xxx.xx.135   ip-10-xx-xx-212.xxx.purestorage.com   <none>           <none>

```

Observe in the output that the node for the pod has changed.

- Verify the database `TEST_1234` exists on the cluster and is accessible.

```

export MYSQLPOD=$(kubectl get pods -l app=mysql --no-headers | awk '{print $1}')

kubectl exec -ti $MYSQLPOD -- bash

root@mysql-6b86668f89-nvw65:/# mysql --user=root --password=password

mysql> show databases;

+--------------------+

| Database           |

+--------------------+

| information_schema |

| TEST_1234          |

| mysql              |

| performance_schema |

+--------------------+

4 rows in set (0.01 sec)

```

The database still exists even when the pod went down with the persistent storage backend by Portworx.

- Exit the database and the mysql pod.

```

mysql> exit

Bye

root@mysql-6b86668f89-nvw65:/# exit

exit

```

## Clean up​

- Bring the cordoned node back online.

```

kubectl uncordon $MYSQL_NODE

```

- Delete the test database created.

```

mysql>drop database TEST_1234;

```

In this topic:
