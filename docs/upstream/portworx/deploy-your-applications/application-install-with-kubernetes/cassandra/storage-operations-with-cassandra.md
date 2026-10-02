# Storage Operations with Cassandra

Source: https://docs.portworx.com/portworx-enterprise/deploy-your-applications/application-install-with-kubernetes/cassandra/storage-operations-with-cassandra (Portworx Enterprise 3.6)

Storage Operations with Cassandra | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## Scaling your Cassandra cluster​

When you add a new node or worker to your Kubernetes cluster, you do not need to manually install Portworx on it. Because Portworx is deployed and managed through the Portworx Operator, the Operator automatically detects and configures Portworx with the newly added nodes.

### Add a new node​

-
List your storage nodes on the cluster using the following command.

```

kubectl get storagenodes -n <px_namespace>

```

```

NAME                                   ID                                     STATUS   VERSION           AGE

ip-10-xx-xxx-161.pwx.purestorage.com   83ff9847-70d7-4237-xxxx-9f0ed0de6c92   Online   3.1.5.0-454b18c   24m

ip-10-xx-xxx-103.pwx.purestorage.com   d963e55c-96a5-4b9b-xxxx-1d7e6ce9f4de   Online   3.1.5.0-454b18c   24m

ip-10-xx-xxx-5.pwx.purestorage.com     221b7a93-76b4-4af9-xxxx-d1052a5e5c86   Online   3.1.5.0-454b18c   24m

```

-
Add a new node to your Kubernetes cluster and list your storage nodes on the cluster using the following command:

```

kubectl get storagenodes -n <px_namespace>

```

```

NAME                                   ID                                     STATUS         VERSION           AGE

ip-10-xx-xxx-161.pwx.purestorage.com   83ff9847-70d7-4237-xxxx-9f0ed0de6c92   Online         3.1.5.0-454b18c   26m

ip-10-xx-xxx-103.pwx.purestorage.com   d963e55c-96a5-4b9b-xxxx-1d7e6ce9f4de   Online         3.1.5.0-454b18c   26m

ip-10-xx-xxx-5.pwx.purestorage.com     221b7a93-76b4-4af9-xxxx-d1052a5e5c86   Online         3.1.5.0-454b18c   26m

ip-10-xx-xxx-7.pwx.purestorage.com                                            Initializing                     13s

```

New node is initializing on the cluster.

-
Use the `kubectl get pods` command to display your Pods:

```

kubectl get pods -n <px_namespace> -l "name=portworx"

```

```

NAME                                                    READY   STATUS    RESTARTS   AGE

px-cluster-78fcac4f-4e81-4e43-be80-aeed17cf96xx-xxxxc   1/1     Running   0          33m

px-cluster-78fcac4f-4e81-4e43-be80-aeed17cf96xx-xxxxz   1/1     Running   0          33m

px-cluster-78fcac4f-4e81-4e43-be80-aeed17cf96xx-xxxxp   1/1     Running   0          33m

px-cluster-78fcac4f-4e81-4e43-be80-aeed17cf96xx-xxxxv   1/1     Running   0          6m42s

```

-
Your Portworx cluster automatically scales as you scale your Kubernetes cluster. Portworx is installed on the newly added node. Display the status of your Portworx cluster, by entering the `pxctl status` command on one of the Portworx pods:

```

pxctl status

```

```

Status: PX is operational

Telemetry: Healthy

Metering: Disabled or Unhealthy

License: Trial (expires in 31 days)

Node ID: 27a55341-bf14-4363-xxxx-af176171e06b

 IP: 10.13.171.7

  Local Storage Pool: 2 pools

 POOL	IO_PRIORITY	RAID_LEVEL	USABLE	USED	STATUS	ZONE	REGION

 0	HIGH		raid0		64 GiB	4.0 GiB	Online	default	default

 1	HIGH		raid0		384 GiB	12 GiB	Online	default	default

 Local Storage Devices: 4 devices

 Device	Path		Media Type		Size		Last-Scan

 0:1	/dev/sdb	STORAGE_MEDIUM_SSD	64 GiB		23 Sep 24 13:29 UTC

 1:1	/dev/sdc	STORAGE_MEDIUM_SSD	128 GiB		23 Sep 24 13:29 UTC

 1:2	/dev/sdd	STORAGE_MEDIUM_SSD	128 GiB		23 Sep 24 13:29 UTC

 1:3	/dev/sde	STORAGE_MEDIUM_SSD	128 GiB		23 Sep 24 13:29 UTC

 total			-			448 GiB

 Cache Devices:

  * No cache devices

Cluster Summary

 Cluster ID: px-cluster-78fcac4f-4e81-4e43-xxxx-aeed17cf96a2

 Cluster UUID: e8cc86f5-d150-42a2-xxxx-d0241aff1fb9

 Scheduler: kubernetes

 Total Nodes: 4 node(s) with storage (4 online)

 IP		ID					SchedulerNodeName			Auth		StorageNode	Used	Capacity	Status	StorageStatus	Version		Kernel		OS

 10.xx.xxx.103	d963e55c-96a5-4bxx-xxxx-1d7e6ce9f4de	ip-10-xx-xxx-103.pwx.purestorage.com	Disabled	Yes		16 GiB	448 GiB		Online	Up		3.1.5.0-454b18c	6.5.0-27-generic	Ubuntu 22.04.3 LTS

 10.xx.xxx.161	83ff9847-70d7-42xx-xxxx-9f0ed0de6c92	ip-10-xx-xxx-161.pwx.purestorage.com	Disabled	Yes		16 GiB	448 GiB		Online	Up		3.1.5.0-454b18c	6.5.0-27-generic	Ubuntu 22.04.3 LTS

 10.xx.xxx.7	27a55341-bf14-43xx-xxxx-af176171e06b	ip-10-xx-xxx-7.pwx.purestorage.com	Disabled	Yes		16 GiB	448 GiB		Online	Up (This node)	3.1.5.0-454b18c	6.5.0-27-generic	Ubuntu 22.04.3 LTS

 10.xx.xxx.5	221b7a93-76b4-4axx-xxxx-d1052a5e5c86	ip-10-xx-xxx-5.pwx.purestorage.com	Disabled	Yes		16 GiB	448 GiB		Online	Up		3.1.5.0-454b18c	6.5.0-27-generic	Ubuntu 22.04.3 LTS

 Warnings:

   WARNING: Internal Kvdb is not using dedicated drive on nodes [10.xx.xxx.103 10.xx.xxx.5 10.xx.xxx.161]. This configuration is not recommended for production clusters.

Global Storage Pool

 Total Used    	:  64 GiB

 Total Capacity	:  1.8 TiB

```

### Scale up the Cassandra StatefulSet​

-
Display your stateful sets by entering the `kubectl get statefulsets` command:

```

kubectl get sts cassandra

```

```

NAME        READY   AGE

cassandra   3/3     35m

```

In the above example output, note that the number of replicas is three.

-
To scale up the `cassandra` stateful set, you must increase the number of replicas. Enter the `kubectl scale statefulsets` command, specifying the following:

- The name of your stateful set (this example uses `cassandra`)

- The desired number of replicas (this example creates four replicas)

```

kubectl scale statefulsets cassandra --replicas=4

```

```

statefulset "cassandra" scaled

```

-
To list your Pods, enter the `kubectl get pods` command:

```

kubectl get pods -l "app=cassandra"

```

```

NAME          READY   STATUS              RESTARTS   AGE

cassandra-0   1/1     Running             0          36m

cassandra-1   1/1     Running             0          35m

cassandra-2   1/1     Running             0          34m

cassandra-3   0/1     ContainerCreating   0          28s

```

In the above example output, a new pod is spinning up.

-
Display your stateful sets by entering the `kubectl get statefulsets` command:

```

kubectl get sts cassandra

```

```

NAME        READY   AGE

cassandra   4/4     45m

```

In the above example output, note that the number of replicas is now updated to four.

-
To open a shell session into one of your Pods, enter the following `kubectl exec` command, specifying your Pod name. This example opens the `cassandra-0` Pod:

```

kubectl exec -it cassandra-0 -- bash

```

-
Use the `nodetool status` command to retrieve information about your Cassandra cluster:

```

nodetool status

```

```

Datacenter: DC1-K8Demo

======================

Status=Up/Down

|/ State=Normal/Leaving/Joining/Moving

--  Address         Load       Tokens       Owns (effective)  Host ID                               Rack

UN  10.2xx.xxx.4    103.84 KiB  32           46.5%             xxxxxxxx-xxxx-xxxx-xxxx-2cc0159b9859  Rack1-K8Demo

UN  10.2xx.xx.199   83.12 KiB  32           57.7%             xxxxxxxx-xxxx-xxxx-xxxx-bfaf5a24b364  Rack1-K8Demo

UN  10.2xx.xx.135   83.16 KiB  32           48.0%             xxxxxxxx-xxxx-xxxx-xxxx-7d22d0cc1b0b  Rack1-K8Demo

UN  10.2xx.xxx.199  65.64 KiB  32           47.9%             xxxxxxxx-xxxx-xxxx-xxxx-b6b9e8b0a130  Rack1-K8Demo

```

-
Terminate the shell session:

```

exit

```

## Failover Cassandra with Portworx on Kubernetes​

### Pod failover​

Verify that your Cassandra cluster is formed of five nodes:

```

kubectl get pods -l "app=cassandra"

```

```

NAME          READY     STATUS    RESTARTS   AGE

cassandra-0   1/1       Running   0          1h

cassandra-1   1/1       Running   0          10m

cassandra-2   1/1       Running   0          18h

cassandra-3   1/1       Running   0          17h

cassandra-4   1/1       Running   0          13h

```

#### Add data to Cassandra​

-
Run the `bash` command on one of your Pods. The following example command runs the `bash` command on the `cassandra-2` Pod:

```

kubectl exec -it cassandra-2 -- bash

```

-
Start `cqlsh`, the command line shell for interacting with Cassandra:

```

cqlsh

```

```

Connected to TestCluster at 127.0.0.1:9042.

[cqlsh 5.0.1 | Cassandra 3.11.4 | CQL spec 3.4.4 | Native protocol v4]

Use HELP for help.

```

-
Enter the following example command to add data to a keyspace called `demodb`:

```

CREATE KEYSPACE demodb WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 2 };

use demodb;

CREATE TABLE emp(emp_id int PRIMARY KEY, emp_name text, emp_city text, emp_sal varint,emp_phone varint);

INSERT INTO emp (emp_id, emp_name, emp_city, emp_phone, emp_sal) VALUES(123423445,'Steve', 'Denver', 5910234452, 50000);

```

-
Run the `exit` command to terminate `cqlsh` and return to the shell session.

-
Display the list of nodes that host the data in your Cassandra ring based on its partition key:

```

nodetool getendpoints demodb emp 123423445

```

```

10.0.112.1

10.0.160.1

```

-
Terminate the shell session:

```

exit

```

-
Use the following command to list the nodes and the Pods they host:

```

kubectl get pods -l app=cassandra -o json | jq '.items[] | {"name": .metadata.name,"hostname": .spec.nodeName, "hostIP": .status.hostIP, "PodIP": .status.podIP}'

```

```

{

  "name": "cassandra-0",

  "hostname": "k8s-5",

  "hostIP": "10.140.0.8",

  "PodIP": "10.0.112.1"

}

{

  "name": "cassandra-1",

  "hostname": "k8s-0",

  "hostIP": "10.140.0.3",

  "PodIP": "10.0.160.1"

}

{

  "name": "cassandra-2",

  "hostname": "k8s-1",

  "hostIP": "10.140.0.5",

  "PodIP": "10.0.64.3"

}

{

  "name": "cassandra-3",

  "hostname": "k8s-3",

  "hostIP": "10.140.0.6",

  "PodIP": "10.0.240.1"

}

{

  "name": "cassandra-4",

  "hostname": "k8s-4",

  "hostIP": "10.140.0.7",

  "PodIP": "10.0.128.1"

}

```

Note that the `k8s-0` node hosts the `cassandra1` Pod.

#### Delete a Cassandra Pod​

-
Cordon a node where one of the replicas resides. The Kubernetes stateful set will schedule the Pod to another node. The following `kubectl cordon` command cordons the `k8s-0` node:

```

kubectl cordon k8s-0

```

```

node "k8s-0" cordoned

```

-
Use the `kubectl delete pods` command to delete the `cassandra-1` Pod:

```

kubectl delete pods cassandra-1

```

```

pod "cassandra-1" deleted

```

-
The Kubernetes stateful set schedules the `cassandra-1` Pod on a different host. You can use the `kubectl get pods -w` command to see where the Pod is in its lifecycle:

```

kubectl get pods -w

```

```

NAME          READY     STATUS              RESTARTS   AGE

cassandra-0   1/1       Running             0          1h

cassandra-1   0/1       ContainerCreating   0          1s

cassandra-2   1/1       Running             0          19h

cassandra-3   1/1       Running             0          17h

cassandra-4   1/1       Running             0          14h

cassandra-1   0/1       Running   0         4s

cassandra-1   1/1       Running   0         28s

```

-
To see the node on which the Kubernetes stateful set schedules the `cassandra-1` Pod, enter the following command:

```

kubectl get pods -l app=cassandra -o json | jq '.items[] | {"name": .metadata.name,"hostname": .spec.nodeName, "hostIP": .status.hostIP, "PodIP": status.podIP}'

```

```

{

  "name": "cassandra-0",

  "hostname": "k8s-5",

  "hostIP": "10.140.0.8",

  "PodIP": "10.0.112.1"

}

{

  "name": "cassandra-1",

  "hostname": "k8s-2",

  "hostIP": "10.140.0.4",

  "PodIP": "10.0.192.2"

}

{

  "name": "cassandra-2",

  "hostname": "k8s-1",

  "hostIP": "10.140.0.5",

  "PodIP": "10.0.64.3"

}

{

  "name": "cassandra-3",

  "hostname": "k8s-3",

  "hostIP": "10.140.0.6",

  "PodIP": "10.0.240.1"

}

{

  "name": "cassandra-4",

  "hostname": "k8s-4",

  "hostIP": "10.140.0.7",

  "PodIP": "10.0.128.1"

}

```

Note that the `cassandra-1` Pod is now scheduled on the `k8s-2` node.

-
Verify that there is no data loss by entering the following command:

```

kubectl exec cassandra-1 -- cqlsh -e 'select * from demodb.emp'

```

```

emp_id    | emp_city | emp_name | emp_phone  | emp_sal

-----------+----------+----------+------------+---------

123423445 |   Denver |    Steve | 5910234452 |   50000

(1 rows)

```

### Node failover​

-
List the Pods in your cluster by entering the following command:

```

kubectl get pods -l app=cassandra -o json | jq '.items[] | {"name": .metadata.name,"hostname": .spec.nodeName, "hostIP": .status.hostIP, "PodIP": status.podIP}'

```

```

{

  "name": "cassandra-0",

  "hostname": "k8s-5",

  "hostIP": "10.140.0.8",

  "PodIP": "10.0.112.1"

}

{

  "name": "cassandra-1",

  "hostname": "k8s-2",

  "hostIP": "10.140.0.4",

  "PodIP": "10.0.192.2"

}

{

  "name": "cassandra-2",

  "hostname": "k8s-1",

  "hostIP": "10.140.0.5",

  "PodIP": "10.0.64.3"

}

{

  "name": "cassandra-3",

  "hostname": "k8s-3",

  "hostIP": "10.140.0.6",

  "PodIP": "10.0.240.1"

}

{

  "name": "cassandra-4",

  "hostname": "k8s-4",

  "hostIP": "10.140.0.7",

  "PodIP": "10.0.128.1"

}

```

Note that Kubernetes scheduled the `cassandra-2` Pod on the `k8s-1` node.

-
Display the list of nodes and their labels:

```

kubectl get nodes --show-labels

```

```

NAME         STATUS        LABELS

k8s-0        Ready         cassandra-data-cassandra-1=true,cassandra-data-cassandra-3=true

k8s-1        Ready         cassandra-data-cassandra-1=true,cassandra-data-cassandra-4=true

k8s-2        Ready         cassandra-data-cassandra-0=true,cassandra-data-cassandra-2=true

k8s-3        Ready         cassandra-data-cassandra-3=true

k8s-4        Ready         cassandra-data-cassandra-4=true

k8s-5        Ready

k8s-master   Ready         cassandra-data-cassandra-0=true,cassandra-data-cassandra-2=true

```

note

This example output is truncated for brevity.

-
Decommission the `k8s-1` Portworx node by following the steps in the Decommission a Node section.

-
Decommission the `k8s-1` Kubernetes node by entering the `kubectl delete node` command with `k8s-1` as an argument:

```

kubectl delete node k8s-1

```

-
List the Pods in your cluster by entering the following command:

```

kubectl get pods -l app=cassandra -o json | jq '.items[] | {"name": .metadata.name,"hostname": .spec.nodeName, "hostIP": .status.hostIP, "PodIP": .status.podIP}'

```

```

{

  "name": "cassandra-0",

  "hostname": "k8s-5",

  "hostIP": "10.140.0.8",

  "PodIP": "10.0.112.1"

}

{

  "name": "cassandra-1",

  "hostname": "k8s-2",

  "hostIP": "10.140.0.4",

  "PodIP": "10.0.192.2"

}

{

  "name": "cassandra-2",

  "hostname": "k8s-0",

  "hostIP": "10.140.0.3",

  "PodIP": "10.0.160.2"

}

{

  "name": "cassandra-3",

  "hostname": "k8s-3",

  "hostIP": "10.140.0.6",

  "PodIP": "10.0.240.1"

}

{

  "name": "cassandra-4",

  "hostname": "k8s-4",

  "hostIP": "10.140.0.7",

  "PodIP": "10.0.128.1"

}

```

Note that the `cassandra-2` pod is scheduled on the `k8s-0` node.

-
Display the list of nodes and their labels:

```

kubectl get nodes --show-labels

```

```

NAME         STATUS        LABELS

k8s-0        Ready         cassandra-data-cassandra-1=true,cassandra-data-cassandra-3=true

k8s-2        Ready         cassandra-data-cassandra-0=true,cassandra-data-cassandra-2=true

k8s-3        Ready         cassandra-data-cassandra-3=true

k8s-4        Ready         cassandra-data-cassandra-4=true

k8s-5        Ready

k8s-master   Ready         cassandra-data-cassandra-0=true,cassandra-data-cassandra-2=true

```

## Application-level Replication with Portworx​

The data replication model for Cassandra provides application-level replication. Tangentially, Portworx allows you to configure a replication level (repl) for persistent volumes, providing storage-level replication. Replication at the storage layer allows for the quick recovery of individual Cassandra nodes in the event of a hardware failure without the need to rebuild nodes from other replicas.

The replication factor of Cassandra keyspaces and the number of Portworx volume replicas should be considered together to provide the appropriate level of redundancy depending on availability requirements.

As a baseline, a storage replication setting of 2 is recommended. The application-level replication provided by Cassandra makes the use of PX-Fast volumes (which require repl=1) suitable, assuming environment-specific prerequisites are met.

## Cassandra snapshots​

When you create a snapshot, Cassandra first flushes the application's memory. Then, it creates a hard-link to the `SSTable` files. This means that the snapshots are application-consistent, but the data stored on the underlying volume can be corrupted. Thus, if a failure occurs on the underlying volume, the data will be corrupted. A Portworx snapshot is a distinct volume from the one Cassandra is using, meaning that you can run a second instance of Cassandra in parallel using that volume. You can also use a Portworx snapshots to go back to a point in time where the issue is not present.

Portworx by Everpure recommends you use 3DSnaps for Cassandra as they are application-consistent.

In this topic:
