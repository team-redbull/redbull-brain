# Inspect Volumes

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/create-and-manage-volumes/inspect-volumes (Portworx Enterprise latest)

Inspect Volumes | Portworx Enterprise Documentation

This document explains how you can get detailed information about the settings and the usage of your Portworx volumes. This can be used to investigate various aspects related to your Portworx cluster such as identifying bottlenecks or improving the overall performance.

## Inspect a volume​

To inspect a volume, run the `pxctl volume inspect` command with the name of the volume as a parameter. The following example shows replication and aggregation, and the volumes are named accordingly. Note that these commands are run from the worker nodes. You can also execute these commands from a computer that has access to the Kubernetes cluster using `kubectl exec` commands.

```

pxctl volume create vol-rep1-size4gi-agg2  -r 1  -s 4 -a 2

```

```

Volume successfully created: 1006031320660300176

```

```

pxctl volume create vol-rep2-size4gi  -r 2  -s 4

```

```

Volume successfully created: 153462940070253844

```

This example volume uses an aggregation set and has no replication:

```

pxctl volume inspect 1006031320660300176

```

```

Volume          	    :  1006031320660300176

Name            	    :  vol-rep1-size4gi-agg2

Size            	    :  4.0 GiB

Format          	    :  ext4

HA              	    :  1

IO Priority     	    :  LOW

Creation time   	    :  Oct 28 17:17:43 UTC 2022

Shared          	    :  no

Status          	    :  up

State           	    :  detached

Mount Options           :  discard

Reads           	    :  0

Reads MS        	    :  0

Bytes Read      	    :  0

Writes          	    :  0

Writes MS       	    :  0

Bytes Written   	    :  0

Discards   	            :  0

Discards MS   	        :  0

Bytes Discarded         :  0

IOs in progress 	    :  0

Bytes used      	    :  2.1 MiB

Replica sets on nodes   :

  Set 0

    Node 		        : X.X.X.70

      Pool UUID         : <pool-UUID-1>

        FA-Name         : <FlashArray-name>

          Drive ID      : <drive-ID>

          Drive Path    : <drive-location>

  Set 1

    Node 		        : X.X.X.71

      Pool UUID         : <pool-UUID-2>

        FA-Name         : <FlashArray-name>

          Drive ID      : <drive-ID>

          Drive Path    : <drive-location>

Replication Status      :  Detached

```

This example volume uses a replication factor of 2 and no aggregation:

```

pxctl volume inspect 153462940070253844

```

```

Volume          	    :  153462940070253844

Name            	    :  vol-rep2-size4gi

Size            	    :  4.0 GiB

Format          	    :  ext4

HA              	    :  2

IO Priority     	    :  LOW

Creation time   	    :  Oct 28 17:18:02 UTC 2022

Shared          	    :  no

Status          	    :  up

State           	    :  detached

Mount Options           :  discard

Reads           	    :  0

Reads MS        	    :  0

Bytes Read      	    :  0

Writes          	    :  0

Writes MS       	    :  0

Bytes Written   	    :  0

Discards   	            :  0

Discards MS   	        :  0

Bytes Discarded         :  0

IOs in progress 	    :  0

Bytes used      	    :  2.1 MiB

Replica sets on nodes   :

  Set 0

    Node 		        : X.X.X.70

      Pool UUID         : <pool-UUID-1>

        Datastore       : <datastore-name>

          Drive ID      : <drive-ID>

          Drive Path    : <drive-path>

    Node 		        : X.X.X.71

      Pool UUID         : <pool-UUID-2>

        Datastore       : <datastore-name>

          Drive ID      : <drive-ID>

          Drive Path    : <drive-path>

Replication Status      :  Detached

```

By knowing what the fields mean, you can get a deeper insight into your volume's usage. For example:

- Volume: represents the ID of the volume. Every time a new volume gets created, Portworx generates a unique ID and assigns it to the newly created volume.

- Size: the size of the volume expressed in binary Gigabytes (GiB)

- Format: the file system used to store data. Currently, Portworx supports `xfs` and `ext4`.

- HA: represents the replication factor for the volume. As an example, if a volume has a replication factor of 3, it means the data is protected on 3 separate nodes.

You can set the replication factor while creating the volume by running the `pxctl volume create` command and passing it the `--repl` flag:

```

pxctl volume create testVol --repl=2

```

For applications that require node level availability and read parallelism across nodes, Portworx by Everpure recommends setting a replication factor of 2 or 3. Note that the maximum replication factor is 3.

You can also modify the replication factor of a volume by running the `pxctl volume ha-update` and passing it the following flags:

- `--repl` with the new replication factor

- `--node` with the ID(s) of the new node(s) to which the data will be replicated. Use a comma-separated list to specify more than one ID.

As an example, here's how you can update the replication factor of a volume called `testVol`:

```

pxctl volume ha-update --repl=3 --node xxxxxxxx-xxxx-xxxx-xxxx-0dc1c09781d8 testVol

```

See the updating volumes page for more details.

-
IO Priority: Portworx classifies disks into three different performance levels:

- High

- Medium,

- Low.

Then, it groups the volumes into separate pools. To run a low latency transactional workload like a database, create the volume with the `--io_priority` flag set to `high` as in the following example:

```

pxctl volume create --io_priority high volume-name

```

See the Storage pools page to get a better understanding of how performance levels work in Portworx. Additionally, note that Portworx provides an easy way to manage storage pools through the `pxctl service pool` command.

- Creation time: indicates the creation date and time of the volume.

- Shared: this field tells whether the volume is `sharedv4` or not. A sharedv4 volume is available to multiple containers running on different hosts at the same time. See the sharedv4 volumes page for more details

- Status: indicates the status of the volume. Possible values are `Up` and `Pending`. `Up` means that Portworx created the volume successfully. `Pending` means that Portworx currently creates the volume.

- State: shows whether the volume is `Attached` or `Detached`. `Attached` means that the volume is attached to a node and you can perform read and write operations on the volume. `Detached` means that the volume is not used and you can't perform read and write operation on the volume.

- Reads: the number of `read` operations served by the volume.

- Reads MS: the total amount of time spent doing reads, expressed in milliseconds.

- Bytes Read: measures the total number of bytes read from the volume.

- Writes: the number of `write` operations served by the volume.

- Writes MS: the total amount of time spent doing write operations, expressed in milliseconds.

- Bytes Written: represents the total amount of bytes written to the volume.

- Discards: indicates the total number of discard operations that have been issued to the volume. Discard operations are used to inform the underlying storage that specific blocks of data are no longer in use and can be erased, optimizing storage space and performance.

- Discards MS: shows the millisecond (ms) count of how long the discard operations took to complete. This metric is important for assessing the performance impact of the discard operations on the overall system.

- Bytes Discarded: represents the total amount of data in bytes that has been marked as no longer needed and discarded during the discard operations. It gives an idea of the volume of data that has been cleared from the storage, helping in storage management and optimization.

- IOs in progress: tells the number of IO operations currently in progress.

- Bytes used: indicates the amount of space used on the volume, expressed in KiB.

- Replication Status: tells whether the volume replication feature is disabled (`Detached`) or enabled (`Up`).

note

Starting from Portworx Enterprise version 3.1.1, for the vSphere and FlashArray provided drives, the following output fields appear under the `Replica sets on nodes` section:

- Datastore / FA-Name: Specifies the name of the datastore in a vSphere environment or the FlashArray in which the volume resides. It helps identify the storage system used for the volume, facilitating easier management and reference within these environments.

- Drive ID: Provides the unique identifier of the drive, which in the case of vSphere is the path to the VMDK file. It is crucial for identifying the specific virtual disk file associated with the volume on the datastore.

- Drive Path: Indicates the system path to the physical or logical drive where the volume data is actually stored. It offers a direct reference to locate the drive within the host system, aiding in tasks such as maintenance or troubleshooting.

## Inspect multiple volumes​

With `pxctl`, you can also inspect multiple volumes in one command as in the following example:

```

pxctl volume inspect testVol testVol2

```

```

Volume    :  188586323847560484

    Name                 :  testVol

    Size                 :  1.0 GiB

    Format               :  ext4

    HA                   :  1

    IO Priority          :  LOW

    Creation time        :  Jul 2 14:57:11 UTC 2019

    Shared               :  no

    Status               :  up

    State                :  detached

    Reads                :  0

    Reads MS             :  0

    Bytes Read           :  0

    Writes               :  0

    Writes MS            :  0

    Bytes Written        :  0

    IOs in progress      :  0

    Bytes used           :  340 KiB

    Replica sets on nodes:

        Set 0

          Node           : X.X.X.70 (Pool 0)

    Replication Status   :  Detached

Volume    :  1089720565647069203

    Name                 :  testVol2

    Size                 :  1.0 GiB

    Format               :  ext4

    HA                   :  1

    IO Priority          :  LOW

    Creation time        :  Jul 4 16:37:02 UTC 2019

    Shared               :  no

    Status               :  up

    State                :  detached

    Reads                :  0

    Reads MS             :  0

    Bytes Read           :  0

    Writes               :  0

    Writes MS            :  0

    Bytes Written        :  0

    IOs in progress      :  0

    Bytes used           :  340 KiB

    Replica sets on nodes:

        Set 0

          Node          : X.X.X.70 (Pool 0)

    Replication Status     :  Detached

```

## Example sequence​

Below is an example of PVC creation, followed by creation of a MYSQL service.

-
Create a PVC:

```

cat pvc.yaml

```

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: mysql-data

  annotations:

    volume.beta.kubernetes.io/storage-class: px-csi-db

spec:

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

```

-
Create a MYSQL application using the above PVC:

```

cat mysql.yaml

```

```

apiVersion: apps/v1

kind: Deployment

metadata:

  name: mysql

spec:

  strategy:

    rollingUpdate:

      maxSurge: 1

      maxUnavailable: 1

    type: RollingUpdate

  replicas: 1

  selector:

    matchLabels:

      app: mysql

  template:

    metadata:

      labels:

        app: mysql

        version: "1"

    spec:

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

-
List the deployment (App) and PVC:

```

kubectl get deployment

```

```

NAME    READY   UP-TO-DATE   AVAILABLE   AGE

mysql   1/1     1            1           67m

```

```

kubectl get pvc

```

```

NAME           STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE

mysql-data     Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-b36921371ce4   2Gi        RWO            px-csi-db      82m

```

-
Describe the PVC:

```

kubectl describe pvc mysql-data

```

```

Name:          mysql-data

Namespace:     default

StorageClass:  px-csi-db

Status:        Bound

Volume:        pvc-xxxxxxxx-xxxx-xxxx-xxxx-b36921371ce4

Labels:        <none>

Annotations:   pv.kubernetes.io/bind-completed: yes

              pv.kubernetes.io/bound-by-controller: yes

              volume.beta.kubernetes.io/storage-class: px-csi-db

              volume.beta.kubernetes.io/storage-provisioner: pxd.portworx.com

Finalizers:    [kubernetes.io/pvc-protection]

Capacity:      2Gi

Access Modes:  RWO

VolumeMode:    Filesystem

Used By:       mysql-6654679c44-qcpmv

Events:        <none>

```

The output shows that a CSI storage class is used and bound.

-
Inspect a volume:

```

pxctl volume inspect 949302306981516864

```

```

  Volume          	 :  949302306981516864

  Name            	 :  pvc-xxxxxxxx-xxxx-xxxx-xxxx-b36921371ce4

  Size            	 :  2.0 GiB

  Format          	 :  ext4

  HA              	 :  3

  IO Priority     	 :  LOW

  Creation time   	 :  Oct 28 16:28:10 UTC 2022

  Shared          	 :  no

  Status          	 :  up

  State           	 :  Attached: xxxxxxxx-xxxx-xxxx-xxxx-71365ac19514 (192.168.58.76)

  Last Attached   	 :  Oct 28 16:42:25 UTC 2022

  Device Path     	 :  /dev/pxd/pxd949302306981516864

  Labels          	 :  csi.storage.k8s.io/pv/name=pvc-xxxxxxxx-xxxx-xxxx-xxxx-b36921371ce4,csi.storage.k8s.io/pvc/name=mysql-data,csi.storage.k8s.io/pvc/namespace=default,io_profile=db_remote,namespace=default,pvc=mysql-data,repl=3

  Mount Options          	 :  discard

  Reads           	 :  51

  Reads MS        	 :  37

  Bytes Read      	 :  1105920

  Writes          	 :  636

  Writes MS       	 :  12752

  Bytes Written   	 :  169459712

  IOs in progress 	 :  0

  Bytes used      	 :  17 MiB

  Replica sets on nodes:

    Set 0

      Node 		 : 192.168.58.76 (Pool xxxxxxxx-xxxx-xxxx-xxxx-31df5f03ebcc )

      Node 		 : 192.168.74.160 (Pool xxxxxxxx-xxxx-xxxx-xxxx-246d810d4a07 )

      Node 		 : 192.168.25.112 (Pool xxxxxxxx-xxxx-xxxx-xxxx-46e648a2708a )

  Replication Status	 :  Up

  Volume consumers	 :

    - Name           : mysql-6654679c44-qcpmv (xxxxxxxx-xxxx-xxxx-xxxx-0e0a0130620b) (Pod)

      Namespace      : default

      Running on     : ip-192-168-58-76.us-east-2.compute.internal

      Controlled by  : mysql-6654679c44 (ReplicaSet)

```

In this topic:
