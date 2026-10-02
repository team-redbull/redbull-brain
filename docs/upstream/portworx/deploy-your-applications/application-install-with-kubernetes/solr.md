# Deploy Solr with Portworx

Source: https://docs.portworx.com/portworx-enterprise/deploy-your-applications/application-install-with-kubernetes/solr (Portworx Enterprise latest)

Deploy Solr with Portworx | Portworx Enterprise Documentation

Solr is an open-source enterprise-search platform that can be deployed on Kubernetes cluster using Portworx volumes. Solr provides features like full-text search, hit highlighting, faceted search, real-time indexing and more. The document shows Solr deployment with Zookeeper ensemble that manages the Solr configuration and performs the leader election.

The following collection of tasks describe how to deploy Solr with Portworx:

- Create a StorageClass for dynamic provisioning of Portworx volumes

- Deploy ZooKeeper ensemble for Solr configuration management

- Verify ZooKeeper is running

- Deploy Solr for distributed search and indexing

- Verify Solr is running

Complete all the task to deploy Solr.

## Create a StorageClass​

- Check your cluster nodes to verify all nodes are up and running.

```

kubectl get nodes -o wide

```

```

NAME                                   STATUS   ROLES           AGE    VERSION   INTERNAL-IP     EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION     CONTAINER-RUNTIME

ip-xx-xx-xxx-111.xxx.purestorage.com   Ready    <none>          114m   v1.33.0   10.xx.xxx.111   <none>        Ubuntu 22.04.3 LTS   6.5.0-27-generic   docker://28.0.2

ip-xx-xx-xxx-120.xxx.purestorage.com   Ready    control-plane   115m   v1.33.0   10.xx.xxx.120   <none>        Ubuntu 22.04.3 LTS   6.5.0-27-generic   docker://28.0.2

ip-xx-xx-xxx-122.xxx.purestorage.com   Ready    <none>          114m   v1.33.0   10.xx.xxx.122   <none>        Ubuntu 22.04.3 LTS   6.5.0-27-generic   docker://28.0.2

ip-xx-xx-xxx-130.xxx.purestorage.com   Ready    <none>          114m   v1.33.0   10.xx.xxx.130   <none>        Ubuntu 22.04.3 LTS   6.5.0-27-generic   docker://28.0.2

ip-xx-xx-xxx-156.xxx.purestorage.com   Ready    <none>          114m   v1.33.0   10.xx.xxx.156   <none>        Ubuntu 22.04.3 LTS   6.5.0-27-generic   docker://28.0.2

```

- Define StorageClass that uses Portworx as provisioner. Save it in a file `portworx-sc.yml`.

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: portworx-sc

provisioner: pxd.portworx.com

parameters:

  repl: "2"

reclaimPolicy: Delete

allowVolumeExpansion: true

volumeBindingMode: Immediate

```

Note the following about this storageclass:

- The provisioner field is set to `pxd.portworx.com`

- The name of the StorageClass object is `portworx-sc`

- Portworx will create two replica of each volume

- Apply the StorageClass configuration

```

kubectl apply -f portworx-sc.yml

```

## Deploy ZooKeeper ensemble​

ZooKeeper ensemble is used for managing the configuration for Solr. It enables Solr by providing coordination, leader election, and centralized cluster state management.

- Define a headless service, PodDisruptionBudget and ZooKeeper statefulset. Save it in a file `zookeeper-ensemble.yml`.

```

apiVersion: v1

kind: Service

metadata:

  name: zk-hs

  labels:

    app: zk

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

kind: Service

metadata:

  name: zk-cs

  labels:

    app: zk

spec:

  ports:

  - port: 2181

    name: client

  selector:

    app: zk

---

apiVersion: policy/v1

kind: PodDisruptionBudget

metadata:

  name: zk-pdb

spec:

  selector:

    matchLabels:

      app: zk

  maxUnavailable: 1

---

apiVersion: apps/v1

kind: StatefulSet

metadata:

  name: zk

spec:

  selector:

    matchLabels:

      app: zk

  serviceName: zk-hs

  replicas: 3

  updateStrategy:

    type: RollingUpdate

  podManagementPolicy: OrderedReady

  template:

    metadata:

      labels:

        app: zk

    spec:

      affinity:

        podAntiAffinity:

          requiredDuringSchedulingIgnoredDuringExecution:

            - labelSelector:

                matchExpressions:

                  - key: "app"

                    operator: In

                    values:

                    - zk

              topologyKey: "kubernetes.io/hostname"

      containers:

      - name: kubernetes-zookeeper

        imagePullPolicy: Always

        image: "registry.k8s.io/kubernetes-zookeeper:1.0-3.4.10"

        resources:

          requests:

            memory: "1Gi"

            cpu: "0.5"

        ports:

        - containerPort: 2181

          name: client

        - containerPort: 2888

          name: server

        - containerPort: 3888

          name: leader-election

        command:

        - sh

        - -c

        - "start-zookeeper \

          --servers=3 \

          --data_dir=/var/lib/zookeeper/data \

          --data_log_dir=/var/lib/zookeeper/data/log \

          --conf_dir=/opt/zookeeper/conf \

          --client_port=2181 \

          --election_port=3888 \

          --server_port=2888 \

          --tick_time=2000 \

          --init_limit=10 \

          --sync_limit=5 \

          --heap=512M \

          --max_client_cnxns=60 \

          --snap_retain_count=3 \

          --purge_interval=12 \

          --max_session_timeout=40000 \

          --min_session_timeout=4000 \

          --log_level=INFO"

        readinessProbe:

          exec:

            command:

            - sh

            - -c

            - "zookeeper-ready 2181"

          initialDelaySeconds: 10

          timeoutSeconds: 5

        livenessProbe:

          exec:

            command:

            - sh

            - -c

            - "zookeeper-ready 2181"

          initialDelaySeconds: 10

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

          storage: 10Gi

```

Note the following about the ZooKeeper deployment:

-
ZooKeeper is deployed as a three-node ensemble using a StatefulSet.

-
A headless Service provides stable network identities required for quorum and leader election.

-
A PodDisruptionBudget ensures that at most one ZooKeeper pod is unavailable at any time.

-
Each ZooKeeper pod uses persistent storage dynamically provisioned using the `portworx-sc` StorageClass.

-
Pod anti-affinity spreads ZooKeeper pods across nodes to improve availability.

- Apply the above configuration.

```

kubectl create -f zookeeper-ensemble.yml

```

```

service/zk-hs created

service/zk-cs created

poddisruptionbudget.policy/zk-pdb created

statefulset.apps/zk created

```

### Verify Zookeeper is running​

- Verify the Zookeeper pods are up and running with Portworx volumes.

```

kubectl get pods

```

```

NAME   READY   STATUS    RESTARTS   AGE

zk-0   1/1     Running   0          17m

zk-1   1/1     Running   0          16m

zk-2   1/1     Running   0          16m

```

- Check the status of pvc created.

```

kubectl get pvc

```

```

NAME           STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE

datadir-zk-0   Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx61e0   10Gi       RWO            portworx-sc    <unset>                 17m

datadir-zk-1   Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx4212   10Gi       RWO            portworx-sc    <unset>                 17m

datadir-zk-2   Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx98df   10Gi       RWO            portworx-sc    <unset>                 16m

```

- Check the status of statefulset created.

```

kubectl get sts

```

```

NAME   READY   AGE

zk     3/3     24m

```

- Connect to one of the pods and check that the volumes are bound to Zookeeper pods using pxctl.

```

kubectl exec xxxxxxxxxxx-xx-2sjsx -n portworx -- /opt/pwx/bin/pxctl volume inspect pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx61e0

```

```

	Volume          	 :  xxxxxxxxxxxxxx8952

	Name            	 :  pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx61e0

	Size            	 :  10 GiB

	Format          	 :  ext4

	HA              	 :  2

	IO Priority     	 :  LOW

	Creation time   	 :  Jan 27 08:53:01 UTC 2026

	Shared          	 :  no

	Status          	 :  up

	State           	 :  Attached: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx6d80 (10.xx.xxx.xxx)

	Last Attached   	 :  Jan 27 08:53:02 UTC 2026

	Device Path     	 :  /dev/pxd/pxdxxxxxxxxxxxxxx8952

	Labels          	 :  app=zk,namespace=default,pvc=datadir-zk-0,repl=2

	Mount Options          	 :  discard

	Reads           	 :  59

	Reads MS        	 :  15

	Bytes Read      	 :  450560

	Writes          	 :  213

	Writes MS       	 :  856

	Bytes Written   	 :  168218624

	IOs in progress 	 :  0

	Bytes used      	 :  4.5 MiB

	Replica sets on nodes:

		Set 0

		  Node 		 : 10.xx.xxx.xx1

		   Pool UUID	 : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx0eb0

		  Node 		 : 10.xx.xxx.xx0

		   Pool UUID	 : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx2305

	Replication Status	 :  Up

	Volume consumers	 :

		- Name           : zk-0 (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxb86b) (Pod)

		  Namespace      : default

		  Running on     : ip-10-xx-xxx-xx1.xxx.purestorage.com

		  Controlled by  : zk (StatefulSet)

```

In the above output, the pvc is bound to `zk-0` Zookeeper pod.

- Verify that zookeeper ensemble is working by creating `/foo` on `zk-0`

```

kubectl exec -it zk-0 -- /opt/zookeeper/bin/zkCli.sh create /foo bar

```

```

Connecting to localhost:2181

2026-01-27 09:27:33,110 [myid:] - INFO  [main:Environment@100] - Client environment:host.name=zk-0.zk-hs.default.svc.cluster.local

...

2026-01-27 09:27:33,219 [myid:] - INFO  [main-SendThread(localhost:2181):ClientCnxn$SendThread@1299] - Session establishment complete on server localhost/127.0.0.1:2181, sessionid = 0x19bfea8f3390000, negotiated timeout = 30000

WATCHER::

WatchedEvent state:SyncConnected type:None path:null

Created /foo

```

- Access `/foo` from the `zk-2` Zookeeper pod.

```

kubectl exec -it zk-2 -- /opt/zookeeper/bin/zkCli.sh get /foo

```

```

WATCHER::

WatchedEvent state:SyncConnected type:None path:null

bar

cZxid = 0x100000002

ctime = Tue Jan 27 09:27:33 UTC 2026

mZxid = 0x100000002

mtime = Tue Jan 27 09:27:33 UTC 2026

pZxid = 0x100000002

cversion = 0

dataVersion = 0

aclVersion = 0

ephemeralOwner = 0x0

dataLength = 3

numChildren = 0

```

## Deploy Solr​

Solr provides a scalable, highly available search platform with centralized configuration, automatic failover, and persistent storage using Portworx. This will use the ZooKeeper ensemble for leader election that will be defined in the Solr configmap. Solr StatefulSet provides the compute and storage where indexes are actually hosted.

- Define config properties for solr configmap in a file `solr-config.properties`.

```

solrHome=/store/data

solrPort=8983

zkHost=zk-0.zkensemble:2181,zk-1.zkensemble:2181,zk-2.zkensemble:2181

solrLogsDir=/store/logs

solrHeap=1g

```

- Create configmap solr-cluster-config.

```

kubectl create configmap solr-cluster-config --from-env-file=solr-config.properties

```

```

configmap/solr-cluster-config created

```

- Define Solr service, PodDisruptionBudget and StatefulSet . Save it in a file `solr-cluster.yml`.

```

apiVersion: v1

kind: Service

metadata:

  name: solrcluster

  labels:

    app: solr-app

spec:

  clusterIP: None

  selector:

    app: solr-app

---

apiVersion: v1

kind: Service

metadata:

  name: solr-service

  labels:

    app: solr-app

spec:

  ports:

  - protocol: TCP

    port: 8983

    targetPort: 8983

  type: LoadBalancer

  selector:

    app: solr-app

---

apiVersion: apps/v1

kind: StatefulSet

metadata:

  name: solr

spec:

  selector:

    matchLabels:

      app: solr-app # has to match .spec.template.metadata.labels

  serviceName: "solrcluster"

  replicas: 2 # by default is 1

  template:

    metadata:

      labels:

        app: solr-app # has to match .spec.selector.matchLabels

    spec:

      terminationGracePeriodSeconds: 10

      restartPolicy: Always

      containers:

      - name: solr

        image: solr:9

        imagePullPolicy: IfNotPresent

        readinessProbe:

          tcpSocket:

            port: 8983

          initialDelaySeconds: 5

          periodSeconds: 10

        livenessProbe:

          tcpSocket:

            port: 8983

          initialDelaySeconds: 15

          periodSeconds: 20

        volumeMounts:

        - name: volsolr

          mountPath: /store

        ports:

        - name: solrport

          containerPort: 8983

        env:

          - name: MY_POD_NAME

            valueFrom:

              fieldRef:

                fieldPath: metadata.name

          - name: MY_POD_NAMESPACE

            valueFrom:

              fieldRef:

                fieldPath: metadata.namespace

          - name: MY_POD_IP

            valueFrom:

              fieldRef:

                fieldPath: status.podIP

          - name: SOLR_HOME

            valueFrom:

              configMapKeyRef:

                name: solr-cluster-config

                key: solrHome

          - name: ZK_HOST

            valueFrom:

              configMapKeyRef:

                name: solr-cluster-config

                key: zkHost

          - name: POD_HOST_NAME

            valueFrom:

              fieldRef:

                fieldPath: metadata.name

          - name: SOLR_HOST

            value: "$(POD_HOST_NAME).solrcluster"

          - name: SOLR_LOGS_DIR

            valueFrom:

              configMapKeyRef:

                name: solr-cluster-config

                key: solrLogsDir

          - name: SOLR_HEAP

            valueFrom:

              configMapKeyRef:

                name: solr-cluster-config

                key: solrHeap

      initContainers:

      - name: init-solr-data

        image: busybox

        command:

        - "/bin/sh"

        - "-c"

        - "if [ ! -d $SOLR_HOME/lib ] ; then mkdir -p $SOLR_HOME/lib && chown -R 8983:8983 $SOLR_HOME ; else true; fi"

        env:

          - name: SOLR_HOME

            valueFrom:

              configMapKeyRef:

                name: solr-cluster-config

                key: solrHome

        volumeMounts:

        - name: volsolr

          mountPath: /store

      - name: init-solr-logs

        image: busybox

        command:

        - "/bin/sh"

        - "-c"

        - "if [ ! -d $SOLR_LOGS_DIR ] ; then mkdir -p $SOLR_LOGS_DIR && chown 8983:8983 $SOLR_LOGS_DIR ; else true; fi"

        env:

          - name: SOLR_LOGS_DIR

            valueFrom:

              configMapKeyRef:

                name: solr-cluster-config

                key: solrLogsDir

        volumeMounts:

        - name: volsolr

          mountPath: /store

      - name: init-solr-xml

        image: solr:8.1.1

        command:

        - "/bin/sh"

        - "-c"

        - "if [ ! -f $SOLR_HOME/solr.xml ] ; then cp /opt/solr/server/solr/solr.xml $SOLR_HOME/solr.xml;\

               sed -i \"s/<solr>/<solr><str name='sharedLib'>\\/store\\/data\\/lib<\\/str>/g\" $SOLR_HOME/solr.xml ; else true; fi "

        env:

          - name: SOLR_HOME

            valueFrom:

              configMapKeyRef:

                name: solr-cluster-config

                key: solrHome

        volumeMounts:

        - name: volsolr

          mountPath: /store

  volumeClaimTemplates:

  - metadata:

      name: volsolr

    spec:

      storageClassName: portworx-sc

      accessModes: [ "ReadWriteOnce" ]

      resources:

        requests:

          storage: 32Gi

```

Note the following about the Solr deployment:

-
Solr is deployed as a StatefulSet with multiple replicas for distributed search and indexing.

-
A headless Service provides stable network identities for Solr pods, enabling intra-cluster communication.

-
A LoadBalancer Service exposes Solr externally on port 8983 for client access.

-
Each Solr pod uses persistent storage dynamically provisioned using the `portworx-sc` StorageClass to store indexes and data.

-
Solr pods connect to ZooKeeper for centralized configuration and cluster state management.

- Apply above configuration.

```

kubectl create -f solr-cluster.yml

```

### Verify Solr is running​

- Verify Solr resources created on the cluster.

```

kubectl get pods

```

```

NAME     READY   STATUS    RESTARTS   AGE

solr-0   1/1     Running   0          4m59s

solr-1   1/1     Running   0          3m53s

zk-0     1/1     Running   0          3h36m

zk-1     1/1     Running   0          3h35m

zk-2     1/1     Running   0          3h35m

```

- Check the status of pvc created on the cluster.

```

kubectl get pvc

```

```

NAME             STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE

datadir-zk-0     Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx61e0   10Gi       RWO            portworx-sc    <unset>                 3h36m

datadir-zk-1     Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx4212   10Gi       RWO            portworx-sc    <unset>                 3h36m

datadir-zk-2     Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx98df   10Gi       RWO            portworx-sc    <unset>                 3h35m

volsolr-solr-0   Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx91f9   32Gi       RWO            portworx-sc    <unset>                 5m19s

volsolr-solr-1   Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx14f8   32Gi       RWO            portworx-sc    <unset>                 4m13s

```

- Connect to one of the pods and check that the volumes using pxctl.

```

kubectl exec xxxxxxxxxxx-xx-2sjsx -n portworx -- /opt/pwx/bin/pxctl volume list

```

```

ID			NAME						SIZE	HA	SHARED	ENCRYPTED	PROXY-VOLUME	IO_PRIORITY	STATUS				SNAP-ENABLED

xxxxxxxxxxxxxx1100	pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx14f8	32 GiB	2	no	no		no		LOW	up - attached on 10.xx.xxx.xx6	no

xxxxxxxxxxxxxx0709	pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx4212	10 GiB	2	no	no		no		LOW	up - attached on 10.xx.xxx.xx2	no

xxxxxxxxxxxxxx0509	pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx98df	10 GiB	2	no	no		no		LOW	up - attached on 10.xx.xxx.xx6	no

xxxxxxxxxxxxxx8952	pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx61e0	10 GiB	2	no	no		no		LOW	up - attached on 10.xx.xxx.xx1	no

xxxxxxxxxxxxxx9096	pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx91f9	32 GiB	2	no	no		no		LOW	up - attached on 10.xx.xxx.xx0	no

```

- Verify volumes are bound to Solr pods.

```

kubectl exec sosrivastava-28-2sjsx -n portworx -- /opt/pwx/bin/pxctl volume inspect pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx14f8

```

```

	Volume          	 :  xxxxxxxxxxxxxx1100

	Name            	 :  pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx14f8

	Size            	 :  32 GiB

	Format          	 :  ext4

	HA              	 :  2

	IO Priority     	 :  LOW

	Creation time   	 :  Jan 27 12:25:11 UTC 2026

	Shared          	 :  no

	Status          	 :  up

	State           	 :  Attached: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx4f94 (10.xx.xxx.156)

	Last Attached   	 :  Jan 27 12:25:21 UTC 2026

	Device Path     	 :  /dev/pxd/pxdxxxxxxxxxxxxxx1100

	Labels          	 :  app=solr-app,namespace=default,pvc=volsolr-solr-1,repl=2

	Mount Options          	 :  discard

	Reads           	 :  70

	Reads MS        	 :  284

	Bytes Read      	 :  491520

	Writes          	 :  605

	Writes MS       	 :  2826

	Bytes Written   	 :  537567232

	IOs in progress 	 :  0

	Bytes used      	 :  4.8 MiB

	Replica sets on nodes:

		Set 0

		  Node 		 : 10.xx.xxx.111

		   Pool UUID	 : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx0eb0

		  Node 		 : 10.xx.xxx.156

		   Pool UUID	 : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxe38d

	Replication Status	 :  Up

	Volume consumers	 :

		- Name           : solr-1 (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx40d4) (Pod)

		  Namespace      : default

		  Running on     : ip-xx-xx-xxx-156.xxx.purestorage.com

		  Controlled by  : solr (StatefulSet)

```

## Verify Pod and Node Failover works​

### Node Failover​

- View the respective nodes on which solr pods are running and the Stateful Sets.

```

kubectl get pod -o=custom-columns=NODE:.spec.nodeName,NAME:.metadata.name

```

```

NODE                                   NAME

ip-xx-xx-xxx-130.xxx.purestorage.com   solr-0

ip-xx-xx-xxx-156.xxx.purestorage.com   solr-1

ip-xx-xx-xxx-111.xxx.purestorage.com   zk-0

ip-xx-xx-xxx-122.xxx.purestorage.com   zk-1

ip-xx-xx-xxx-156.xxx.purestorage.com   zk-2

```

- Check the stateful set status

```

kubectl get sts

```

```

NAME   READY   AGE

solr   2/2     12m

zk     3/3     3h44m

```

- Bring down the `ip-xx-xx-xxx-130.xxx.purestorage.com` node which is hosting solr-0.

```

kubectl drain ip-xx-xx-xxx-130.xxx.purestorage.com --ignore-daemonsets --delete-emptydir-data --force

```

```

node/ip-xx-xx-xxx-130.xxx.purestorage.com cordoned

pod/solr-0 evicted

node/ip-xx-xx-xxx-130.xxx.purestorage.com drained

```

- Inspect the Stateful Sets and the pods.

```

kubectl get sts

```

```

NAME   READY   AGE

solr   1/2     16m

zk     3/3     3h47m

```

Observe that Solr StatefulSet has only 1 replica in ready state.

- Check the placement of the `solr-0` Solr pod.

```

kubectl get pod -o=custom-columns=NODE:.spec.nodeName,NAME:.metadata.name

```

```

NODE                                   NAME

ip-xx-xx-xxx-122.xxx.purestorage.com   solr-0

ip-xx-xx-xxx-156.xxx.purestorage.com   solr-1

ip-xx-xx-xxx-111.xxx.purestorage.com   zk-0

ip-xx-xx-xxx-122.xxx.purestorage.com   zk-1

ip-xx-xx-xxx-156.xxx.purestorage.com   zk-2

```

Observe that `solr-0` pod is now on `ip-xx-xx-xxx-122.xxx.purestorage.com` node.

- Bring back the node and observe the pod placements.

```

kubectl uncordon ip-xx-xx-xxx-130.xxx.purestorage.com

```

```

node/ip-xx-xx-xxx-130.xxx.purestorage.com uncordoned

```

```

kubectl get pod -o=custom-columns=NODE:.spec.nodeName,NAME:.metadata.name

```

```

NODE                                   NAME

ip-xx-xx-xxx-122.xxx.purestorage.com   solr-0

ip-xx-xx-xxx-156.xxx.purestorage.com   solr-1

ip-xx-xx-xxx-111.xxx.purestorage.com   zk-0

ip-xx-xx-xxx-122.xxx.purestorage.com   zk-1

ip-xx-xx-xxx-156.xxx.purestorage.com   zk-2

```

### Pod Failover​

- Delete pod `solr-0`.

```

kubectl delete pod solr-0

```

```

pod "solr-0" deleted

```

- Check the status of pods to verify `solr-0` reinitializes.

```

kubectl get pods -o wide

```

```

NAME     READY   STATUS    RESTARTS   AGE     IP               NODE                                   NOMINATED NODE   READINESS GATES

solr-0   1/1     Running   0          2m34s   10.xx.xx.11    ip-xx-xx-xxx-122.xxx.purestorage.com   <none>           <none>

solr-1   1/1     Running   0          142m    10.xx.xx.13    ip-xx-xx-xxx-156.xxx.purestorage.com   <none>           <none>

zk-0     1/1     Running   0          5h54m   10.xx.xxx.18   ip-xx-xx-xxx-111.xxx.purestorage.com   <none>           <none>

zk-1     1/1     Running   0          5h53m   10.xx.xxx.6    ip-xx-xx-xxx-122.xxx.purestorage.com   <none>           <none>

zk-2     1/1     Running   0          5h53m   10.xx.xxx.15    ip-xx-xx-xxx-156.xxx.purestorage.com   <none>           <none>

```

In this topic:
