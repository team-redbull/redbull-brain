# Deploy ScyllaDB with Portworx

Source: https://docs.portworx.com/portworx-enterprise/deploy-your-applications/application-install-with-kubernetes/scylladb (Portworx Enterprise 3.6)

Deploy ScyllaDB with Portworx | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

ScyllaDB is a NoSQL database that aims to provide low latency and high throughput. This article shows how you can create and run a ScyllaDB cluster on Kubernetes, which stores data on Portworx volumes.

To deploy ScyllaDB with Portworx Enterprise, complete the following collection of tasks:

- Create a StorageClass

- Deploy ScyllaDB

- Verify ScyllaDB Deployment

## Create a StorageClass​

-
Use the following command to list the nodes in your cluster:

```

kubectl get nodes -o wide

```

```

NAME                           STATUS   ROLES    AGE    VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE                KERNEL-VERSION              CONTAINER-RUNTIME

xxxx-blr-dev-dour-shoulder-0   Ready    master   103d   v1.14.1   X.X.X.119   <none>        CentOS Linux 7 (Core)   3.10.0-862.3.2.el7.x86_64   docker://18.9.6

xxxx-blr-dev-dour-shoulder-1   Ready    <none>   16d    v1.14.1   X.X.X.82    <none>        CentOS Linux 7 (Core)   3.10.0-862.3.2.el7.x86_64   docker://18.9.6

xxxx-blr-dev-dour-shoulder-2   Ready    <none>   103d   v1.14.1   X.X.X.118   <none>        CentOS Linux 7 (Core)   3.10.0-862.3.2.el7.x86_64   docker://18.9.6

xxxx-blr-dev-dour-shoulder-3   Ready    <none>   103d   v1.14.1   X.X.X.120   <none>        CentOS Linux 7 (Core)   3.10.0-862.3.2.el7.x86_64   docker://18.9.6

```

-
Define the following `portworx-sc.yaml` StorageClass:

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: scylla-ssd

provisioner: pxd.portworx.com

parameters:

  repl: "2"

reclaimPolicy: Delete

volumeBindingMode: Immediate

allowVolumeExpansion: true

```

-
Apply the StorageClass configuration:

```

kubectl apply -f portworx-sc.yml

```

## Deploy ScyllaDB​

-
Create a file called `scylla-configmap.yaml` with the following content:

```

apiVersion: v1

kind: ConfigMap

metadata:

  name: scylla

data:

  ready-probe.sh: |

    #!/bin/bash

    if [[ $(nodetool status | grep $POD_IP) == *"UN"* ]]; then

      if [[ $DEBUG ]]; then

        echo "UN";

      fi

      exit 0;

    else

      if [[ $DEBUG ]]; then

        echo "Not Up";

      fi

      exit 1;

    fi

```

-
Apply the ConfigMap:

```

kubectl apply -f scylla-configmap.yaml

```

-
Create a file called `scylla-service.yaml` with the following content:

```

apiVersion: v1

kind: Service

metadata:

  labels:

    app: scylla

  name: scylla

spec:

  clusterIP: None

  ports:

    - port: 9042

  selector:

    app: scylla

```

-
Apply the Service:

```

kubectl apply -f scylla-service.yaml

```

-
The spec below creates StatefulSet for ScyllaDB with 3 replicas and uses the Stork scheduler to place pods to closer to where their data is located. Create a file called `scylla-statefulset.yaml` with the following content:

```

apiVersion: apps/v1

kind: StatefulSet

metadata:

  name: scylla

  labels:

    app: scylla

spec:

  serviceName: scylla

  replicas: 3

  selector:

    matchLabels:

      app: scylla

  template:

    metadata:

      labels:

        app: scylla

    spec:

      schedulerName: stork

      containers:

        - name: scylla

          image: scylladb/scylla:2.0.0

          imagePullPolicy: IfNotPresent

          args: ["--seeds", "scylla-0.scylla.default.svc.cluster.local"]

          ports:

            - containerPort: 7000

              name: intra-node

            - containerPort: 7001

              name: tls-intra-node

            - containerPort: 7199

              name: jmx

            - containerPort: 9042

              name: cql

          resources:

            limits:

              cpu: 2

              memory: 4Gi

            requests:

              cpu: 2

              memory: 4Gi

          securityContext:

            capabilities:

              add:

                - IPC_LOCK

          lifecycle:

            preStop:

              exec:

                command: ["/bin/sh", "-c", "PID=$(pidof scylla) && kill $PID && while ps -p $PID > /dev/null; do sleep 1; done"]

          env:

            - name: POD_IP

              valueFrom:

                fieldRef:

                  fieldPath: status.podIP

          readinessProbe:

            exec:

              command:

                - /bin/bash

                - -c

                - exec

                - /opt/ready-probe.sh

            initialDelaySeconds: 15

            timeoutSeconds: 5

          volumeMounts:

            - name: scylla-data

              mountPath: /var/lib/scylla

            - name: scylla-ready-probe

              mountPath: /opt/ready-probe.sh

              subPath: ready-probe.sh

      volumes:

        - name: scylla-ready-probe

          configMap:

            name: scylla

  volumeClaimTemplates:

    - metadata:

        name: scylla-data

        annotations:

          volume.beta.kubernetes.io/storage-class: scylla-ssd

      spec:

        accessModes: ["ReadWriteOnce"]

        resources:

          requests:

            storage: 60Gi

```

-
Apply the `scylla-statefulset.yaml` StatefulSet:

```

kubectl apply -f scylla-statefulset.yaml

```

## Verify ScyllaDB Deployment​

-
Enter the `kubectl get pvc` command to verify that the PVCs are bound to a volume using the storage class. The PVC status shows as `Bound` if the operation succeeded:

```

kubectl get pvc

```

```

NAME                   STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE

scylla-data-scylla-0   Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-000c29886e3e   60Gi       RWO            scylla-ssd     3h

scylla-data-scylla-1   Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-000c29886e3e   60Gi       RWO            scylla-ssd     3h

scylla-data-scylla-2   Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-000c29886e3e   60Gi       RWO            scylla-ssd     3h

```

-
Enter the `kubectl get pods` command to verify that the ScyllaDB pods have deployed successfully. The pod status shows as `Running` if the operation succeeded:

```

kubectl get pods

```

```

NAME       READY   STATUS    RESTARTS   AGE

scylla-0   1/1     Running   0          3h

scylla-1   1/1     Running   0          3h

scylla-2   1/1     Running   0          3h

```

-
Run the `nodetool status` command in the `scylla-0` pod to verify that the ScyllaDB cluster was created:

```

kubectl exec scylla-0 -- nodetool status

```

```

Datacenter: datacenter1

=======================

Status=Up/Down

|/ State=Normal/Leaving/Joining/Moving

--  Address        Load       Tokens       Owns (effective)  Host ID                               Rack

UN  10.233.127.67  356.04 KB  256          61.5%             xxxxxxxx-xxxx-xxxx-xxxx-d9b928f1fc4a  rack1

UN  10.233.76.19   351.15 KB  256          70.5%             xxxxxxxx-xxxx-xxxx-xxxx-c897c7441895  rack1

UN  10.233.121.53  359.24 KB  256          68.0%             xxxxxxxx-xxxx-xxxx-xxxx-640ce9ec9f6e  rack1

```

Note the pods placement and the hosts on which they are scheduled

-
Enter the `kubectl get pods` command, filtering the output using the `jq` command to display the following:

-
Pod name

-
Hostname

-
Host IP

-
Pod IP

```

kubectl get pods -l app=scylla -o json | jq '.items[] | {"name": .metadata.name,"hostname": .spec.nodeName, "hostIP": .status.hostIP, "PodIP": .status.podIP}'

```

```

{

  "name": "scylla-0",

  "hostname": "xxxx-blr-dev-dour-shoulder-3",

  "hostIP": "X.X.X.120",

  "PodIP": "10.233.121.53"

}

{

  "name": "scylla-1",

  "hostname": "xxxx-blr-dev-dour-shoulder-1",

  "hostIP": "X.X.X.82",

  "PodIP": "10.233.76.19"

}

{

  "name": "scylla-2",

  "hostname": "xxxx-blr-dev-dour-shoulder-2",

  "hostIP": "X.X.X.118",

  "PodIP": "10.233.127.67"

}

```

-
Enter the `ssh` command to open a shell session into one of your nodes:

```

ssh X.X.X.120

```

-
Enter the `pxctl volume list` command to list your volume IDs. Save one of the node IDs for future reference:

```

pxctl volume list

```

```

ID			NAME						SIZE	HA	SHARED	ENCRYPTED	IO_PRIORITY	STATUS			SNAP-ENABLED

242236313329814877	pvc-xxxxxxxx-xxxx-xxxx-xxxx-000c29886e3e	60 GiB	2	no	no		LOW		up - attached on X.X.X.120	no

702215287887827398	pvc-xxxxxxxx-xxxx-xxxx-xxxx-000c29886e3e	60 GiB	2	no	no		LOW		up - attached on X.X.X.82	no

685261507172158119	pvc-xxxxxxxx-xxxx-xxxx-xxxx-000c29886e3e	60 GiB	2	no	no		LOW		up - attached on X.X.X.118	no

```

-
Enter the `pxctl volume inspect` command to examine your volume. In the example output below, the Portworx volume contains 2 replica sets and is attached to node 3:

```

pxctl volume inspect 242236313329814877

```

```

Volume	:  242236313329814877

  Name            	 :  pvc-xxxxxxxx-xxxx-xxxx-xxxx-000c29886e3e

  Size            	 :  60 GiB

  Format          	 :  ext4

  HA              	 :  2

  IO Priority     	 :  LOW

  Creation time   	 :  Oct 4 05:14:10 UTC 2019

  Shared          	 :  no

  Status          	 :  up

  State           	 :  Attached: xxxxxxxx-xxxx-xxxx-xxxx-fdb2c8379541 (X.X.X.120)

  Device Path     	 :  /dev/pxd/pxd242236313329814877

  Labels          	 :  pvc=scylla-data-scylla-0,repl=2,namespace=default

  Reads           	 :  887

  Reads MS        	 :  553

  Bytes Read      	 :  4526080

  Writes          	 :  4086

  Writes MS       	 :  27087

  Bytes Written   	 :  1032036352

  IOs in progress 	 :  0

  Bytes used      	 :  24 MiB

  Replica sets on nodes:

    Set 0

      Node 		 : X.X.X.120 (Pool 2)

      Node 		 : X.X.X.82 (Pool 2)

  Replication Status	 :  Up

  Volume consumers	 :

    - Name           : scylla-0 (xxxxxxxx-xxxx-xxxx-xxxx-000c29886e3e) (Pod)

      Namespace      : default

      Running on     : xxxx-blr-dev-dour-shoulder-3

      Controlled by  : scylla (StatefulSet)

```

## Verify Pod Failover works​

Once you've created a ScyllaDB cluster on Kubernetes and Portworx, you can test how the cluster reacts to a failure. The following steps simulate a pod failure and demonstrate Portworx and Kubernetes' ability to recover from that failure.

-
List the pods on which ScyllaDB is running:

```

kubectl get pods -l "app=scylla"

```

```

NAME       READY   STATUS    RESTARTS   AGE

scylla-0   1/1     Running   0          4h

scylla-1   1/1     Running   0          4h

scylla-2   1/1     Running   0          4h

```

-
Enter the following `kubectl exec` command to open a `bash` session with the worker node on which ScyllaDB is running:

```

kubectl exec -it scylla-0 -- bash

```

-
Enter the `cqlsh` command to open a Cassandra shell session:

```

cqlsh

```

```

Connected to Test Cluster at 10.233.121.53:9042.

[cqlsh 5.0.1 | Cassandra 3.0.8 | CQL spec 3.3.1 | Native protocol v4]

Use HELP for help.

cqlsh>

```

-
Enter the following `CREATE KEYSPACE` statement to create a keyspace named `demodb`:

```

CREATE KEYSPACE demodb WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 2 };

```

-
Enter the following commands to switch to the `demodb` keyspace and create a table called `emp` within it:

```

cqlsh> use demodb;

cqlsh:demodb> CREATE TABLE emp(emp_id int PRIMARY KEY, emp_name text, emp_city text, emp_sal varint,emp_phone varint);

```

-
Enter the following `INSERT INTO` statement to insert a record into the `emp` table:

```

cqlsh:demodb> INSERT INTO emp (emp_id, emp_name, emp_city, emp_phone, emp_sal) VALUES(123423445,'Steve', 'Denver', 5910234452, 50000);

```

-
Exit the Cassandra shell session:

```

cqlsh> exit

```

-
Enter the following `nodetool getendpoints` command to list the IP addresses of the nodes which are also hosting ScyllaDB information based on the partition key:

```

nodetool getendpoints demodb emp 123423445

```

```

10.233.76.19

10.233.127.67

```

-
Enter the following `kubectl get pods` command to crosscheck the pod IP addresses with the IP addresses you just listed:

```

kubectl get pods -l app=scylla -o json | jq '.items[] | {"name": .metadata.name,"hostname": .spec.nodeName, "hostIP": .status.hostIP, "PodIP": .status.podIP}'

```

```

{

  "name": "scylla-0",

  "hostname": "xxxx-blr-dev-dour-shoulder-3",

  "hostIP": "X.X.X.120",

  "PodIP": "10.233.121.53"

}

{

  "name": "scylla-1",

  "hostname": "xxxx-blr-dev-dour-shoulder-1",

  "hostIP": "X.X.X.82",

  "PodIP": "10.233.76.19"

}

{

  "name": "scylla-2",

  "hostname": "xxxx-blr-dev-dour-shoulder-2",

  "hostIP": "X.X.X.118",

  "PodIP": "10.233.127.67"

}

```

-
Enter the following `kubectl cordon` command to mark the `scylla-1` node as unschedulable:

```

kubectl cordon xxxx-blr-dev-dour-shoulder-1

```

-
Enter the following `kubectl delete` command to delete the `syclla-1` pod:

```

kubectl delete pods scylla-1

```

-
Enter the following `kubectl get pods` command to see if Kubernetes scheduled the `syclla-1` pod to a different node:

```

kubectl get pods -o wide

```

```

NAME       READY   STATUS    RESTARTS   AGE   IP              NODE                           NOMINATED NODE   READINESS GATES

scylla-0   1/1     Running   0          4h    10.233.121.53   xxxx-blr-dev-dour-shoulder-3   <none>           <none>

scylla-1   1/1     Running   0          25s   10.233.127.68   xxxx-blr-dev-dour-shoulder-2   <none>           <none>

scylla-2   1/1     Running   0          4h    10.233.127.67   xxxx-blr-dev-dour-shoulder-2   <none>           <none>

```

Note that the `scyla-1` pod is now scheduled to the `xxxx-blr-dev-dour-shoulder-2 ` node.

-
Enter the `kubectl get pods` command, filtering the output using the `jq` command to display the following:

- Pod name

- Host name

- Host IP

- Pod IP

```

kubectl get pods -l app=scylla -o json | jq '.items[] | {"name": .metadata.name,"hostname": .spec.nodeName, "hostIP": .status.hostIP, "PodIP": .status.podIP}'

```

```

{

  "name": "scylla-0",

  "hostname": "xxxx-blr-dev-dour-shoulder-3",

  "hostIP": "X.X.X.120",

  "PodIP": "10.233.121.53"

}

{

  "name": "scylla-1",

  "hostname": "xxxx-blr-dev-dour-shoulder-2",

  "hostIP": "X.X.X.118",

  "PodIP": "10.233.127.68"

}

{

  "name": "scylla-2",

  "hostname": "xxxx-blr-dev-dour-shoulder-2",

  "hostIP": "X.X.X.118",

  "PodIP": "10.233.127.67"

}

```

-
Enter the following `SELECT` statement to read the columns from the `demodb.emp` table:

```

kubectl exec scylla-1 -- cqlsh -e 'select * from demodb.emp'

```

```

 emp_id    | emp_city | emp_name | emp_phone  | emp_sal

-----------+----------+----------+------------+---------

 123423445 |   Denver |    Steve | 5910234452 |   50000

(1 rows)

```

In this topic:
