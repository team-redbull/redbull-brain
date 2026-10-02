# Deploy Kafka with ZooKeeper on Portworx

Source: https://docs.portworx.com/portworx-enterprise/deploy-your-applications/application-install-with-kubernetes/kafka-with-zookeeper (Portworx Enterprise 3.6)

Deploy Kafka with ZooKeeper on Portworx | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Apache Kafka is a distributed event streaming platform for real-time data, using ZooKeeper for broker coordination, metadata management, and cluster state consistency. This page provides instructions for deploying Apache Kafka and ZooKeeper with Portworx Enterprise on Kubernetes.

note

ZooKeeper's role has been replaced by KRaft (Kafka Raft), an internal consensus protocol that manages metadata directly within Kafka brokers. All new Kafka 4.0 clusters use KRaft mode by default. ZooKeeper-based clusters are now officially deprecated and unsupported. For existing ZooKeeper-based clusters, Kafka provides migration tools (introduced in version 3.5) to transition metadata to KRaft mode.

To deploy Kafka with ZooKeeper on Portworx, complete the following collection of tasks:

- Create a StorageClass for dynamic provisioning.

- Deploy ZooKeeper for cluster state consistency.

- Deploy Kafka for configuring event streaming platform

- Verify Setup by creating a topic and consuming message from it.

## Create a StorageClass​

Portworx provides volume(s) to ZooKeeper as well as Kafka.

- Create `portworx-sc.yaml` with Portworx as the provisioner.

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: portworx-sc

provisioner: pxd.portworx.com

parameters:

  repl: "1"

  priority_io: "high"

  group: "zk_vg"

  fg: "true"

---

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: portworx-sc-rep2

provisioner: pxd.portworx.com

parameters:

  repl: "2"

  priority_io: "high"

  group: "kafka_vg"

  fg: "true"

---

```

- Apply the configuration on your cluster.

```

kubectl apply -f portworx-sc.yaml

```

## Deploy ZooKeeper​

A StatefulSet in Kubernetes requires a headless service to provide network identity to the pods it creates. A headless service is also needed when Kafka is deployed. A headless service does not use a cluster IP. For information on headless services, read this article.

This is also important for the later stages of the deployment of Kafka, since, we would need to access ZooKeeper via the DNS records that are created by this headless service.

- Create a file called `zookeeper-all.yaml` with the following content:

```

apiVersion: v1

kind: Service

metadata:

  name: zk-headless

  labels:

    app: zk-headless

spec:

  ports:

  - port: 2888

    name: server

  - port: 3888

    name: leader-election

  clusterIP: None

  selector:

    app: zk

---

apiVersion: v1

kind: ConfigMap

metadata:

  name: zk-config

data:

  ensemble: "zk-0;zk-1;zk-2"

  jvm.heap: "2G"

  tick: "2000"

  init: "10"

  sync: "5"

  client.cnxns: "60"

  snap.retain: "3"

  purge.interval: "1"

---

apiVersion: policy/v1beta1

kind: PodDisruptionBudget

metadata:

  name: zk-budget

spec:

  selector:

    matchLabels:

      app: zk

  minAvailable: 2

---

apiVersion: apps/v1

kind: StatefulSet

metadata:

  name: zk

spec:

  selector:

    matchLabels:

      app: zk

  serviceName: zk-headless

  replicas: 3

  template:

    metadata:

      labels:

        app: zk

      annotations:

        pod.alpha.kubernetes.io/initialized: "true"

    spec:

      # Use the stork scheduler to enable more efficient placement of the pods

      schedulerName: stork

      affinity:

        nodeAffinity:

          requiredDuringSchedulingIgnoredDuringExecution:

            nodeSelectorTerms:

            - matchExpressions:

              - key: px/running

                operator: NotIn

                values:

                - "false"

              - key: px/enabled

                operator: NotIn

                values:

                - "false"

        podAntiAffinity:

          requiredDuringSchedulingIgnoredDuringExecution:

            - labelSelector:

                matchExpressions:

                  - key: "app"

                    operator: In

                    values:

                    - zk-headless

              topologyKey: "kubernetes.io/hostname"

      containers:

      - name: k8szk

        imagePullPolicy: Always

        image: gcr.io/google_samples/k8szk:v1

        ports:

        - containerPort: 2181

          name: client

        - containerPort: 2888

          name: server

        - containerPort: 3888

          name: leader-election

        env:

        - name : ZK_ENSEMBLE

          valueFrom:

            configMapKeyRef:

              name: zk-config

              key: ensemble

        - name : ZK_HEAP_SIZE

          valueFrom:

            configMapKeyRef:

                name: zk-config

                key: jvm.heap

        - name : ZK_TICK_TIME

          valueFrom:

            configMapKeyRef:

                name: zk-config

                key: tick

        - name : ZK_INIT_LIMIT

          valueFrom:

            configMapKeyRef:

                name: zk-config

                key: init

        - name : ZK_SYNC_LIMIT

          valueFrom:

            configMapKeyRef:

                name: zk-config

                key: tick

        - name : ZK_MAX_CLIENT_CNXNS

          valueFrom:

            configMapKeyRef:

                name: zk-config

                key: client.cnxns

        - name: ZK_SNAP_RETAIN_COUNT

          valueFrom:

            configMapKeyRef:

                name: zk-config

                key: snap.retain

        - name: ZK_PURGE_INTERVAL

          valueFrom:

            configMapKeyRef:

                name: zk-config

                key: purge.interval

        - name: ZK_CLIENT_PORT

          value: "2181"

        - name: ZK_SERVER_PORT

          value: "2888"

        - name: ZK_ELECTION_PORT

          value: "3888"

        command:

        - sh

        - -c

        - zkGenConfig.sh && zkServer.sh start-foreground

        readinessProbe:

          exec:

            command:

            - "zkOk.sh"

          initialDelaySeconds: 15

          timeoutSeconds: 5

        livenessProbe:

          exec:

            command:

            - "zkOk.sh"

          initialDelaySeconds: 15

          timeoutSeconds: 5

        volumeMounts:

        - name: datadir

          mountPath: /var/lib/zookeeper

      securityContext:

        runAsUser: 1000

        fsGroup: 1000

  volumeClaimTemplates:

  - metadata:

      name: datadir

    spec:

      storageClassName: portworx-sc

      accessModes: [ "ReadWriteOnce" ]

      resources:

        requests:

          storage: 2Gi

```

- Apply this configuration

```

kubectl apply -f zookeeper-all.yaml

```

- Verify that the ZooKeeper pods are running with provisioned Portworx volumes.

```

kubectl get pods

```

```

NAME      READY     STATUS    RESTARTS   AGE

zk-0      1/1       Running   0          23h

zk-1      1/1       Running   0          23h

zk-2      1/1       Running   0          23h

```

```

kubectl get pvc

```

```

NAME        STATUS    VOLUME                                     CAPACITY   ACCESSMODES   STORAGECLASS   AGE

data-zk-0   Bound     pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002   3Gi        RWO           portworx-sc    23h

data-zk-1   Bound     pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002   3Gi        RWO           portworx-sc    23h

data-zk-2   Bound     pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002   3Gi        RWO           portworx-sc    23h

```

```

kubectl get sts

```

```

NAME      DESIRED   CURRENT   AGE

zk        3         3         1d

```

```

pxctl volume inspect pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002

```

```

Volume  :  816480848884203913

        Name                     :  pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002

        Size                     :  3.0 GiB

        Format                   :  ext4

        HA                       :  1

        IO Priority              :  LOW

        Creation time            :  Aug 7 14:07:16 UTC 2017

        Shared                   :  no

        Status                   :  up

        State                    :  Attached: k8s-0

        Device Path              :  /dev/pxd/pxd816480848884203913

        Labels                   :  pvc=data-zk-0

        Reads                    :  59

        Reads MS                 :  252

        Bytes Read               :  466944

        Writes                   :  816

        Writes MS                :  3608

        Bytes Written            :  53018624

        IOs in progress          :  0

        Bytes used               :  65 MiB

        Replica sets on nodes:

                Set  0

                        Node     :  10.140.0.5

```

- Verify that the ZooKeeper ensemble is working.

```

kubectl exec zk-0 -- /opt/zookeeper/bin/zkCli.sh create /foo bar

```

```

WATCHER::

WatchedEvent state:SyncConnected type:None path:null

Created /foo

```

```

kubectl exec zk-2 -- /opt/zookeeper/bin/zkCli.sh get /foo

```

```

WATCHER::

WatchedEvent state:SyncConnected type:None path:null

cZxid = 0x10000004d

bar

ctime = Tue Aug 08 14:18:11 UTC 2017

mZxid = 0x10000004d

mtime = Tue Aug 08 14:18:11 UTC 2017

pZxid = 0x10000004d

cversion = 0

dataVersion = 0

aclVersion = 0

ephemeralOwner = 0x0

dataLength = 3

numChildren = 0

```

## Deploy Kafka​

-
Retrieve the FQDN of each ZooKeeper Pod by entering the following command:

```

for i in 0 1 2; do kubectl exec zk-$i -- hostname -f; done

```

```

zk-0.zk-headless.default.svc.cluster.local

zk-1.zk-headless.default.svc.cluster.local

zk-2.zk-headless.default.svc.cluster.local

```

-
Download the kafka-all.yaml file and use the `zookeeper.connect` property to specify your ZooKeeper hosts as a comma-separated list.

-
Apply the spec by entering the following command:

```

kubectl apply -f kafka-all.yaml

```

-
This step is optional. Run the following `kubectl apply` command if you are installing Kafka with ZooKeeper on AWS EKS:

```

kubectl apply -f https://raw.githubusercontent.com/Yolean/kubernetes-kafka/master/rbac-namespace-default/node-reader.yml

```

```

clusterrole.rbac.authorization.k8s.io/node-reader created

clusterrolebinding.rbac.authorization.k8s.io/kafka-node-reader created

```

-
Verify that Kafka resources are created on the cluster.

```

kubectl get pods -l "app=kafka" -n kafka -w

```

```

NAME      READY     STATUS     RESTARTS   AGE

kafka-0   1/1       Running    0          17s

kafka-1   0/1       Init:0/1   0          3s

kafka-1   0/1       Init:0/1   0         4s

kafka-1   0/1       PodInitializing   0         5s

kafka-1   0/1       Running   0         6s

kafka-1   1/1       Running   0         9s

kafka-2   0/1       Pending   0         0s

kafka-2   0/1       Pending   0         1s

kafka-2   0/1       Pending   0         3s

kafka-2   0/1       Init:0/1   0         4s

kafka-2   0/1       Init:0/1   0         6s

kafka-2   0/1       PodInitializing   0         8s

kafka-2   0/1       Running   0         9s

kafka-2   1/1       Running   0         15s

```

```

kubectl get pvc -n kafka

```

```

NAME           STATUS    VOLUME                                     CAPACITY   ACCESSMODES   STORAGECLASS       AGE

data-kafka-0   Bound     pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002   3Gi        RWO           portworx-sc-rep2   1m

data-kafka-1   Bound     pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002   3Gi        RWO           portworx-sc-rep2   57s

data-kafka-2   Bound     pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002   3Gi        RWO           portworx-sc-rep2   48s

```

```

pxctl volume list

```

```

ID                      NAME                                            SIZE    HA      SHARED  ENCRYPTED       IO_PRIORITY     SCALE   STATUS

523341158152507227      pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002        3 GiB   1       no      no              LOW             0       up - attached on 10.140.0.4

816480848884203913      pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002        3 GiB   1       no      no              LOW             0       up - attached on 10.140.0.5

262949240358217536      pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002        3 GiB   2       no      no              LOW             0       up - attached on 10.140.0.3

733731201475618092      pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002        3 GiB   2       no      no              LOW             0       up - attached on 10.140.0.5

360663112422496357      pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002        3 GiB   2       no      no              LOW             0       up - attached on 10.140.0.4

168733173797215691      pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002        3 GiB   1       no      no              LOW             0       up - attached on 10.140.0.3

```

```

pxctl volume inspect pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002

```

```

Volume  :  262949240358217536

        Name                     :  pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002

        Size                     :  3.0 GiB

        Format                   :  ext4

        HA                       :  2

        IO Priority              :  LOW

        Creation time            :  Aug 8 15:10:51 UTC 2017

        Shared                   :  no

        Status                   :  up

        State                    :  Attached: k8s-2

        Device Path              :  /dev/pxd/pxd262949240358217536

        Labels                   :  pvc=data-kafka-0

        Reads                    :  37

        Reads MS                 :  8

        Bytes Read               :  372736

        Writes                   :  354

        Writes MS                :  3096

        Bytes Written            :  53641216

        IOs in progress          :  0

        Bytes used               :  65 MiB

        Replica sets on nodes:

                Set  0

                        Node     :  10.140.0.5

                        Node     :  10.140.0.3

```

## Verify Setup​

- Find the Kafka brokers

```

for i in 0 1 2; do kubectl exec -n kafka kafka-$i -- hostname -f; done

```

```

kafka-0.broker.kafka.svc.cluster.local

kafka-1.broker.kafka.svc.cluster.local

kafka-2.broker.kafka.svc.cluster.local

```

- Create a topic with 3 partitions and which has a replication factor of 3

```

kubectl exec -n kafka -it kafka-0 -- bash

```

```

bin/kafka-topics.sh --zookeeper zk-headless.default.svc.cluster.local:2181 --create --if-not-exists --topic px-kafka-topic --partitions 3 --replication-factor 3

```

```

Created topic "px-kafka-topic".

```

```

bin/kafka-topics.sh --list --zookeeper zk-headless.default.svc.cluster.local:2181

```

```

px-kafka-topic

```

```

bin/kafka-topics.sh --describe --zookeeper zk-headless.default.svc.cluster.local:2181 --topic px-kafka-topic

```

```

Topic:px-kafka-topic    PartitionCount:3        ReplicationFactor:3     Configs:

Topic: px-kafka-topic   Partition: 0    Leader: 0       Replicas: 0,1,2 Isr: 0,1,2

Topic: px-kafka-topic   Partition: 1    Leader: 1       Replicas: 1,2,0 Isr: 1,2,0

Topic: px-kafka-topic   Partition: 2    Leader: 2       Replicas: 2,0,1 Isr: 2,0,1

```

- Publish messages on the topic

```

bin/kafka-console-producer.sh --broker-list kafka-0.broker.kafka.svc.cluster.local:9092,kafka-1.broker.kafka.svc.cluster.local:9092,kafka-2.broker.kafka.svc.cluster.local:9092 --topic px-kafka-topic

```

```

>Hello Kubernetes!

>This is Portworx saying hello

>Kafka says, I am just a messenger

```

- Consume messages from the topic

```

bin/kafka-console-consumer.sh --zookeeper zk-headless.default.svc.cluster.local:2181 —topic px-kafka-topic --from-beginning

```

```

This is Portworx saying hello

Hello Kubernetes!

Kafka says, I am just a messenger

```

## Verify Scaling​

Portworx Enterprise runs as a DaemonSet in Kubernetes. Hence when you add a new node to your kuberentes cluster you do not need to explicitly run Portworx on it.

The Portworx cluster before scaling the Kubernetes nodes.

```

pxctl cluster list

```

```

Cluster ID: px-kafka-cluster

Cluster UUID: xxxxxxxx-xxxx-xxxx-xxxx-52d914ff39d2

Status: OK

Nodes in the cluster:

ID      DATA IP         CPU             MEM TOTAL       MEM FREE        CONTAINERS      VERSION         STATUS

k8s-0   10.140.0.5      8.717949        3.9 GB          2.3 GB          N/A             1.2.9-17d16e4   Online

k8s-1   10.140.0.3      4.081633        3.9 GB          2.2 GB          N/A             1.2.9-17d16e4   Online

k8s-2   10.140.0.4      9.5             3.9 GB          2.2 GB          N/A             1.2.9-17d16e4   Online

```

```

kubectl get nodes -o wide

```

```

NAME         STATUS    AGE       VERSION   EXTERNAL-IP   OS-IMAGE       KERNEL-VERSION

k8s-0        Ready     2d        v1.7.0    <none>        Ubuntu 16.10   4.8.0-56-generic

k8s-1        Ready     2d        v1.7.0    <none>        Ubuntu 16.10   4.8.0-56-generic

k8s-2        Ready     2d        v1.7.0    <none>        Ubuntu 16.10   4.8.0-56-generic

k8s-3        Ready     19h       v1.7.0    <none>        Ubuntu 16.10   4.8.0-56-generic

k8s-master   Ready     2d        v1.7.0    <none>        Ubuntu 16.10   4.8.0-56-generic

```

Portworx scales along with your cluster.

```

pxctl status

```

```

Status: PX is operational

License: Trial (expires in 28 days)

Node ID: k8s-1

        IP: 10.140.0.4

        Local Storage Pool: 1 pool

        POOL    IO_PRIORITY     RAID_LEVEL      USABLE  USED    STATUS  ZONE    REGION

        0       MEDIUM          raid0           10 GiB  594 MiB Online  default default

        Local Storage Devices: 1 device

        Device  Path            Media Type              Size            Last-Scan

        0:1     /dev/sdb        STORAGE_MEDIUM_SSD      10 GiB          07 Aug 17 12:48 UTC

        total                   -                       10 GiB

Cluster Summary

        Cluster ID: px-kafka-cluster

        Cluster UUID: 8xxxxxxxx-xxxx-xxxx-xxxx-f99420435a90

        IP              ID      Used    Capacity        Status

        10.140.0.4      k8s-1   594 MiB 10 GiB          Online (This node)

        10.140.0.3      k8s-2   594 MiB 10 GiB          Online

        10.140.0.5      k8s-0   655 MiB 10 GiB          Online

        10.140.0.6      k8s-3   338 MiB 10 GiB          Online

Global Storage Pool

        Total Used      :  2.1 GiB

        Total Capacity  :  40 GiB

```

```

pxctl cluster list

```

```

Cluster ID: px-kafka-cluster

Cluster UUID: xxxxxxxx-xxxx-xxxx-xxxx-52d914ff39d2

Status: OK

Nodes in the cluster:

ID      DATA IP         CPU             MEM TOTAL       MEM FREE        CONTAINERS      VERSION         STATUS

k8s-1   10.140.0.4      8.163265        3.9 GB          2.2 GB          N/A             1.2.9-17d16e4   Online

k8s-2   10.140.0.3      6.565657        3.9 GB          2.2 GB          N/A             1.2.9-17d16e4   Online

k8s-0   10.140.0.5      4.102564        3.9 GB          2.3 GB          N/A             1.2.9-17d16e4   Online

k8s-3   10.140.0.6      4.040404        3.9 GB          3.4 GB          N/A             1.2.9-17d16e4   Online

```

Scale the Kafka cluster.

```

kubectl scale -n kafka sts kafka --replicas=4

```

```

statefulset "kafka" scaled

```

```

kubectl get pods -n kafka -l "app=kafka" -w

```

```

NAME      READY     STATUS            RESTARTS   AGE

kafka-0   1/1       Running           0          3h

kafka-1   1/1       Running           0          3h

kafka-2   1/1       Running           0          3h

kafka-3   0/1       PodInitializing   0          24s

kafka-3   0/1       Running           0          32s

kafka-3   1/1       Running           0          34s

```

```

kubectl get pvc -n kafka

```

```

NAME           STATUS    VOLUME                                     CAPACITY   ACCESSMODES   STORAGECLASS       AGE

data-kafka-0   Bound     pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002   3Gi        RWO           portworx-sc-rep2   3h

data-kafka-1   Bound     pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002   3Gi        RWO           portworx-sc-rep2   3h

data-kafka-2   Bound     pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002   3Gi        RWO           portworx-sc-rep2   3h

data-kafka-3   Bound     pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002   3Gi        RWO           portworx-sc-rep2   6m

```

Verify that the newly created kafka broker is part of the cluster.

```

kubectl exec -n kafka -it kafka-0 -- bash

```

```

zkCli.sh

```

You'll see a prompt similar to this:

```

[zk: localhost:2181(CONNECTED) 0]

```

Next, type:

```

ls /brokers/ids

```

```

[0, 1, 2, 3]

```

```

ls /brokers/topics

```

```

[px-kafka-topic]

```

```

get /brokers/ids/3

```

```

{"listener_security_protocol_map":{"PLAINTEXT":"PLAINTEXT"},"endpoints":["PLAINTEXT://kafka-3.broker.kafka.svc.cluster.local:9092"],"jmx_port":-1,"host":"kafka-3.broker.kafka.svc.cluster.local","timestamp":"1502217586002","port":9092,"version":4}

cZxid = 0x1000000e9

ctime = Tue Aug 08 18:39:46 UTC 2017

mZxid = 0x1000000e9

mtime = Tue Aug 08 18:39:46 UTC 2017

pZxid = 0x1000000e9

cversion = 0

dataVersion = 0

aclVersion = 0

ephemeralOwner = 0x25dbd0e499e000b

dataLength = 246

numChildren = 0

```

## Verify Pod and Node Failover​

### Pod Failover for ZooKeeper​

Killing the ZooKeeper Java process in the container terminates the pod. You could alternatively delete the pod as well. The Portworx volumes provide durable storage to the ZooKeeper pods which are run as a StatefulSet. Get the earlier inserted value from ZooKeeper to verify the same.

```

kubectl exec zk-0 -- pkill java

```

```

kubectl get pod -w -l "app=zk"

```

```

NAME      READY     STATUS    RESTARTS   AGE

zk-0      1/1       Running   0          1d

zk-1      1/1       Running   0          1d

zk-2      1/1       Running   0          1d

zk-0      0/1       Error     0          1d

zk-0      0/1       Running   1          1d

zk-0      1/1       Running   1          1d

```

```

kubectl exec zk-0 -- zkCli.sh get /foo

```

```

WATCHER::

WatchedEvent state:SyncConnected type:None path:null

bar

cZxid = 0x10000004d

ctime = Tue Aug 08 14:18:11 UTC 2017

mZxid = 0x10000004d

mtime = Tue Aug 08 14:18:11 UTC 2017

pZxid = 0x10000004d

cversion = 0

dataVersion = 0

aclVersion = 0

ephemeralOwner = 0x0

dataLength = 3

numChildren = 0

```

### Pod Failover for Kafka​

Find the hosts of the running kafka cluster, cordon a node so that pods are scheduled on it. Kill a kafka pod and notice that it is scheduled on a newer node, joining the cluster back again with durable storage which is backed by the Portworx volume.

```

kubectl get pods -n kafka -o wide

```

```

NAME      READY     STATUS    RESTARTS   AGE       IP           NODE

kafka-0   1/1       Running   0          21h       10.0.160.3   k8s-2

kafka-1   1/1       Running   0          21h       10.0.192.3   k8s-0

kafka-2   1/1       Running   0          21h       10.0.64.4    k8s-1

kafka-3   1/1       Running   0          18h       10.0.112.1   k8s-3

```

```

kubectl cordon k8s-0

```

```

node "k8s-0" cordoned

```

```

kubectl get nodes

```

```

NAME         STATUS                     AGE       VERSION

k8s-0        Ready,SchedulingDisabled   2d        v1.7.0

k8s-1        Ready                      2d        v1.7.0

k8s-2        Ready                      2d        v1.7.0

k8s-3        Ready                      19h       v1.7.0

k8s-master   Ready                      2d        v1.7.0

```

```

kubectl get pvc -n kafka | grep data-kafka-1

```

```

data-kafka-1   Bound     pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002   3Gi        RWO           portworx-sc-rep2   22h

```

```

/opt/pwx/bin/pxctl volume list | grep pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002

```

```

733731201475618092      pvc-xxxxxxxx-xxxx-xxxx-xxxx-42010a8c0002        3 GiB   2       no      no              LOW             0       up - attached on 10.140.0.5

```

```

kubectl exec -n kafka -it kafka-0 -- bash

```

```

bin/kafka-topics.sh --describe --zookeeper zk-headless.default.svc.cluster.local:2181 --topic px-kafka-topic

```

```

Topic:px-kafka-topic    PartitionCount:3        ReplicationFactor:3     Configs:

        Topic: px-kafka-topic   Partition: 0    Leader: 0       Replicas: 0,1,2 Isr: 0,1,2

        Topic: px-kafka-topic   Partition: 1    Leader: 1       Replicas: 1,2,0 Isr: 1,2,0

        Topic: px-kafka-topic   Partition: 2    Leader: 2       Replicas: 2,0,1 Isr: 2,0,1

```

```

kubectl delete po/kafka-1 -n kafka

```

```

pod "kafka-1" deleted

```

```

kubectl get pods -n kafka -w

```

```

NAME      READY     STATUS        RESTARTS   AGE

kafka-0   1/1       Running           0         22h

kafka-1   0/1       Terminating       0         22h

kafka-2   1/1       Running           0         22h

kafka-3   1/1       Running           0         18h

kafka-1   0/1       Terminating       0         22h

kafka-1   0/1       Terminating       0         22h

kafka-1   0/1       Pending           0         0s

kafka-1   0/1       Pending           0         0s

kafka-1   0/1       Init:0/1          0         0s

kafka-1   0/1       Init:0/1          0         2s

kafka-1   0/1       PodInitializing   0         3s

kafka-1   0/1       Running           0         5s

kafka-1   1/1       Running           0         11s

```

```

kubectl get pods -n kafka -o wide

```

```

NAME      READY     STATUS    RESTARTS   AGE       IP           NODE

kafka-0   1/1       Running   0          22h       10.0.160.3   k8s-2

kafka-1   1/1       Running   0          1m        10.0.112.2   k8s-3

kafka-2   1/1       Running   0          22h       10.0.64.4    k8s-1

kafka-3   1/1       Running   0          18h       10.0.112.1   k8s-3

```

```

bin/kafka-topics.sh --describe --zookeeper zk-headless.default.svc.cluster.local:2181 --topic px-kafka-topic

```

```

Topic:px-kafka-topic    PartitionCount:3        ReplicationFactor:3     Configs:

Topic: px-kafka-topic   Partition: 0    Leader: 0       Replicas: 0,1,2 Isr: 0,2,1

Topic: px-kafka-topic   Partition: 1    Leader: 1       Replicas: 1,2,0 Isr: 2,0,1

Topic: px-kafka-topic   Partition: 2    Leader: 2       Replicas: 2,0,1 Isr: 2,0,1

```

### Node Failover​

In the case of a StatefulSet, a node may become unreachable under one of the following conditions:

- The node is down for maintenance

- There has been a network partition.

There is no way for Kubernetes to know which of the case is it. Hence Kubernetes would not schedule the Statefulset and the pods running on those nodes would enter the ‘Terminating’ or ‘Unknown’ state after a timeout. If there was a network partition and when the partition heals, Kubernetes will complete the deletion of the Pod and remove it from the API server. It would subsequently schedule a new pod to honor the replication requirements mentioned in the Podspec.

For further information : Statefulset Pod Deletion

Decommissioning a Kubernetes node deletes the node object from the APIServer. Before that you would want to decommission your Portworx node from the cluster. Follow the steps mentioned in Decommission a Portworx node Once done, delete the Kubernetes node if it requires to be deleted permanently.

In this topic:
