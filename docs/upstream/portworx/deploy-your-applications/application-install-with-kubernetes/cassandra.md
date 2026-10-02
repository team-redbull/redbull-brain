# Deploy Cassandra with Portworx Enterprise

Source: https://docs.portworx.com/portworx-enterprise/deploy-your-applications/application-install-with-kubernetes/cassandra (Portworx Enterprise latest)

Deploy Cassandra with Portworx Enterprise | Portworx Enterprise Documentation

This document shows how you can deploy Cassandra, a distributed NoSQL database management system, with Portworx on Kubernetes. The following diagram shows the main components of a Cassandra with Portworx deployment running on top of Kubernetes:

To deploy Cassandra with Portworx Enterprise, complete the following collection of tasks:

- Create a headless service

- Create a storage class

- Create a stateful set

You will install Cassandra as a StatefulSet, which requires a headless service to provide network identity to the Pods it creates. Note that a headless service does not require load balancing and a single cluster IP address. For more details about headless services, see the Headless Services section of the Kubernetes documentation.

## Create a headless service​

Create a headless service for which:

- The `spec.clusterIP` field is set to `None`.

- The `spec.selector.app` field is set to `cassandra`.

The Kubernetes endpoints controller will configure the DNS to return addresses that point directly to your Cassandra Pods.

```

kubectl apply -f - <<EOF

apiVersion: v1

kind: Service

metadata:

  labels:

    app: cassandra

  name: cassandra

spec:

  clusterIP: None

  ports:

    - port: 9042

  selector:

    app: cassandra

EOF

```

```

service/cassandra created

```

## Create a storage class​

Use the following command to create a storage class:

```

kubectl apply -f - <<EOF

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: portworx-sc

provisioner: pxd.portworx.com

parameters:

  repl: "1"

  priority_io: "high"

  group: "cassandra_vg"

  fg: "true"

EOF

```

```

storageclass.storage.k8s.io/px-storageclass created

```

Note the following about this storage class:

- The provisioner field is set to `pxd.portworx.com`. For details about the Portworx-specific parameters, refer to the Portworx Volume section of the Kubernetes documentation

- The name of the `StorageClass` object is `portworx-sc`

- Portworx will create one replica of each volume

- Portworx will use a high priority storage pool

## Create a stateful set​

The following command creates a stateful set with three replicas and uses the STORK scheduler to place your Pods closer to where their data is located:

```

kubectl apply -f - <<EOF

apiVersion: "apps/v1"

kind: StatefulSet

metadata:

  name: cassandra

spec:

  selector:

    matchLabels:

      app: cassandra

  serviceName: cassandra

  replicas: 3

  template:

    metadata:

      labels:

        app: cassandra

    spec:

      schedulerName: stork

      securityContext:

        fsGroup: 999

        seccompProfile:

          type: RuntimeDefault

      containers:

      - name: cassandra

        image: cassandra:4.1

        #image: gcr.io/google-samples/cassandra:v12

        imagePullPolicy: Always

        command:

        - /bin/sh

        - -c

        args:

        - |

          exec /usr/local/bin/docker-entrypoint.sh cassandra -R -f

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

            cpu: "500m"

            memory: 1Gi

          requests:

            cpu: "500m"

            memory: 1Gi

        securityContext:

          allowPrivilegeEscalation: false

          runAsUser: 0

          capabilities:

            add:

            - SYS_CHROOT

            # IPC_LOCK removed for compliance

        lifecycle:

          preStop:

            exec:

              command: ["/bin/sh", "-c", "PID=$(pidof java) && kill $PID && while ps -p $PID > /dev/null; do sleep 1; done"]

        env:

          - name: MAX_HEAP_SIZE

            value: 512M

          - name: HEAP_NEWSIZE

            value: 100M

          - name: CASSANDRA_SEEDS

            value: "cassandra-0.cassandra.default.svc.cluster.local"

          - name: CASSANDRA_CLUSTER_NAME

            value: "K8Demo"

          - name: CASSANDRA_DC

            value: "DC1-K8Demo"

          - name: CASSANDRA_RACK

            value: "Rack1-K8Demo"

          - name: CASSANDRA_AUTO_BOOTSTRAP

            value: "false"

          - name: POD_IP

            valueFrom:

              fieldRef:

                fieldPath: status.podIP

          - name: POD_NAMESPACE

            valueFrom:

              fieldRef:

                fieldPath: metadata.namespace

        readinessProbe:

          exec:

            command:

            - /bin/sh

            - -c

            - "cqlsh 127.0.0.1 9042 -e 'DESCRIBE CLUSTER' >/dev/null 2>&1"

          initialDelaySeconds: 60

          periodSeconds: 10

          timeoutSeconds: 10

          failureThreshold: 6

        # These volume mounts are persistent. They are like inline claims,

        # but not exactly because the names need to match exactly one of

        # the stateful pod volumes.

        volumeMounts:

        - name: cassandra-data

          mountPath: /var/lib/cassandra

  # These are converted to volume claims by the controller

  # and mounted at the paths mentioned above.

  volumeClaimTemplates:

  - metadata:

      name: cassandra-data

      annotations:

        volume.beta.kubernetes.io/storage-class: portworx-sc

    spec:

      accessModes: [ "ReadWriteOnce" ]

      resources:

        requests:

          storage: 1Gi

EOF

```

```

statefulset.apps/cassandra configured

```

## Validate the cluster functionality​

-
Use the `kubectl get pvc` command to verify that the PVCs are bound to your persistent volumes:

```

kubectl get pvc

```

```

NAME                         STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE

cassandra-data-cassandra-0   Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx   1Gi        RWO            portworx-sc    <unset>                 4m41s

cassandra-data-cassandra-1   Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx   1Gi        RWO            portworx-sc    <unset>                 3m22s

cassandra-data-cassandra-2   Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx   1Gi        RWO            portworx-sc    <unset>                 2m21s

```

-
Verify that Kubernetes created the `portworx-sc` storage class:

```

kubectl get storageclass

```

```

NAME                                 PROVISIONER        RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE

portworx-sc                          pxd.portworx.com   Delete          Immediate           false                  2m1s

```

-
List your pod:

```

kubectl get pods

```

```

NAME          READY   STATUS    RESTARTS   AGE

cassandra-0   1/1     Running   0          8m47s

cassandra-1   1/1     Running   0          7m29s

cassandra-2   1/1     Running   0          6m28s

```

-
Use the `pxctl volume list` command to display the list of volumes in your cluster by running the following command on one of the pods that has Portworx installed:

```

kubectl exec <pxe_pod> -n portworx -- /opt/pwx/bin/pxctl volume list

```

```

ID			NAME						SIZE	HA	SHARED	ENCRYPTED	PROXY-VOLUME	IO_PRIORITY	STATUS				SNAP-ENABLED

1115044864166520043	pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx	1 GiB	1	no	no		no		HIGH	up - attached on 10.xx.xxx.xxx	no

98569876605418270	pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx	1 GiB	1	no	no		no		HIGH	up - attached on 10.xx.xxx.xxx	no

878365036667067046	pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx	1 GiB	1	no	no		no		HIGH	up - attached on 10.xx.xxx.xxx	no

```

Make a note of the ID of your volume. You'll need it in the next step.

-
To verify that your Portworx volumes has one replica, enter the `pxctl volume inspect` command, specifying the ID from the previous step. The following example command uses `1115044864166520043`:

```

kubectl exec <pxe_pod> -n portworx -- /opt/pwx/bin/pxctl volume inspect 1115044864166520043

```

```

Volume          	 :  1115044864166520043

Name            	 :  pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

Group            	 :  cassandra_vg

Size            	 :  1.0 GiB

Format          	 :  ext4

HA              	 :  1

IO Priority     	 :  HIGH

Creation time   	 :  Jan 12 08:03:40 UTC 2026

Shared          	 :  no

Status          	 :  up

State           	 :  Attached: 56344329-xxxx-xxxx-xxxx-xxxxxxxxxxxx (10.xx.xxx.xxx)

Last Attached   	 :  Jan 12 08:03:41 UTC 2026

Device Path     	 :  /dev/pxd/pxd1115044864xxxxxxxx

Labels          	 :  app=cassandra,fg=true,group=cassandra_vg,namespace=default,priority_io=high,pvc=cassandra-data-cassandra-1,repl=1

Mount Options          	 :  discard

Reads           	 :  51

Reads MS        	 :  4

Bytes Read      	 :  413696

Writes          	 :  881

Writes MS       	 :  3960

Bytes Written   	 :  27381760

IOs in progress 	 :  0

Bytes used      	 :  10.0 MiB

Replica sets on nodes:

 Set 0

   Node 		 : 10.xx.xxx.xxx

    Pool UUID	 : 38ee640a-xxxx-xxxx-xxxx-xxxxxxxxxxxx

Replication Status	 :  Up

Volume consumers	 :

 - Name           : cassandra-1 (22a0007d-xxxx-xxxx-xxxx-xxxxxxxxxxxx) (Pod)

   Namespace      : default

   Running on     : ip-10-xx-xxx-xxx.pwx.purestorage.com

   Controlled by  : cassandra (StatefulSet)

```

Note that this volume is up and the volume consumer is the `cassandra-1` pod. If you want to have more replicas of volume, increase the replica count while creating the StorageClass `portworx-sc`. Please ensure you accordingly increase the worker nodes also and Portworx is installed on all the node to avoid preemption issues.

-
Show the list of your Pods and the hosts on which Kubernetes scheduled them:

```

kubectl get pods -l app=cassandra -o json | jq '.items[] | {"name": .metadata.name,"hostname": .spec.nodeName, "hostIP": .status.hostIP, "PodIP": .status.podIP}'

```

```

{

  "name": "cassandra-0",

  "hostname": "ip-10-xx-xxx-xx8.xxx.purestorage.com",

  "hostIP": "10.xx.xxx.xx8",

  "PodIP": "10.xxx.xx.xx8"

}

{

  "name": "cassandra-1",

  "hostname": "ip-10-xx-xxx-xx0.xxx.purestorage.com",

  "hostIP": "10.xx.xxx.xx0",

  "PodIP": "10.xxx.xx.xx0"

}

{

  "name": "cassandra-2",

  "hostname": "ip-10-xx-xxx-xx6.xxx.purestorage.com",

  "hostIP": "10.xx.xxx.xx6",

  "PodIP": "10.xx.xxx.x"

}

```

-
To open a shell session into one of your Pods, enter the following `kubectl exec` command, specifying your Pod name. This example opens the `cassandra-0` Pod:

```

kubectl exec -it cassandra-0 -- bash

```

-
Use the `nodetool status` command to retrieve information about your Cassandra set up:

```

nodetool status

```

```

Datacenter: DC1-K8Demo

======================

Status=Up/Down

|/ State=Normal/Leaving/Joining/Moving

--  Address        Load       Tokens       Owns (effective)  Host ID                               Rack

UN  10.2xx.xx.xx0  65.66 KiB  32           64.7%             315bd721-xxxx-xxxx-xxxx-xxxxxxxxxxxx  Rack1-K8Demo

UN  10.2xx.xx.xx8  101.01 KiB  32           61.9%             2e686b0f-xxxx-xxxx-xxxx-xxxxxxxxxxxx  Rack1-K8Demo

UN  10.2xx.xx.x    65.66 KiB  32           73.4%             6eccbd09-xxxx-xxxx-xxxx-xxxxxxxxxxxx  Rack1-K8Demo

```

-
Terminate the shell session:

```

exit

```

## Related topics​

- Cassandra on Kubernetes: Step-by-step guide for the most popular Kubernetes platforms

- Run multiple Cassandra rings on the same hosts

In this topic:
