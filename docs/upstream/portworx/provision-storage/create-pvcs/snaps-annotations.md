# Create a PVC from a Snapshot

Source: https://docs.portworx.com/portworx-enterprise/provision-storage/create-pvcs/snaps-annotations (Portworx Enterprise latest)

Create a PVC from a Snapshot | Portworx Enterprise Documentation

This document will show you how to take a snapshot of a volume using Portworx and use that snapshot as the volume for a new pod.

note

Use Stork to manage snapshots on Kubernetes. For information on how to use Stork to manage snapshots, see Snapshots in Portworx.

## Managing snapshots through kubectl or oc​

### Taking periodic snapshots on a running POD​

When you create the Storage Class, you can specify a snapshot schedule on the volume as specified below:

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: portworx-io-priority-high

provisioner: pxd.portworx.com

parameters:

  repl: "1"

  snap_interval:   "24"

  io_priority:  "high"

```

### Creating a snapshot on demand​

You can trigger a new snapshot on a running POD by creating a PersistentVolumeClaim.

#### Using annotations​

Portworx uses a special annotation px/snapshot-source-pvc which can be used to identify the name of the source PVC whose snapshot needs to be taken.

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  namespace: prod

  name: ns.prod-name.px-snap-1

  annotations:

    volume.beta.kubernetes.io/storage-class: px-sc

    px/snapshot-source-pvc: px-vol-1

spec:

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 6Gi

```

Note the format of the name field - `ns.<namespace_of_source_pvc>-name.<name_of_the_snapshot>`. The above example takes a snapshot with the name px-snap-1 of the source PVC px-vol-1 in the prod namespace.

You can run the following command to edit your existing Portworx ClusterRole

- Kubernetes

- OpenShift

```

kubectl edit clusterrole node-get-put-list-role

```

```

oc edit clusterrole node-get-put-list-role

```

 Clone from a snapshot​
You can restore a clone from a snapshot using the following spec file. In 1.3 and higher releases, this is required to create a read-write clone as snapshots are read only.

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  namespace: prod

  name: ns.prod-name.px-snap-restore

  annotations:

    volume.beta.kubernetes.io/storage-class: px-sc

    px/snapshot-source-pvc: ns.prod-name.px-snap-1

spec:

   accessModes:

     - ReadWriteOnce

   resources:

     requests:

       storage: 2Gi

```

The above example restores a volume from the source snapshot PVC with name ns.prod-name.px-snap-1.

#### Using inline spec​

If you do not wish to use annotations you can take a snapshot by providing the source PVC name in the name field of the claim. However this method does not allow you to provide namespaces.

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: name.snap001-source.pvc001

  annotations:

    volume.beta.kubernetes.io/storage-class: px-sc

spec:

  accessModes:

     - ReadWriteOnce

  resources:

    requests:

      storage: 1Gi

```

Note the format of the “name” field. The format is `name.<new_snap_name>-source.<old_volume_name>`. Above example references the parent (source) persistent volume claim pvc001 and creates a snapshot by the name snap001.
 Clone from a snapshot​
You can restore a clone from a snapshot using the following spec file. In 1.3 and higher releases, this is required to create a read-write clone as snapshots are read only.

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: name.rollback001-source.snap001

  annotations:

    volume.beta.kubernetes.io/storage-class: px-sc

spec:

  accessModes:

     - ReadWriteOnce

  resources:

    requests:

      storage: 1Gi

```

Note we used the existing snapshot name in the source part of the inline spec.

### Using snapshots​

#### Listing snapshots​

To list your snapshots, use the `pxctl volume list --snapshot` command as follows:

```

pxctl volume list --snapshot

```

```

ID			NAME	SIZE	HA	SHARED	IO_PRIORITY	SCALE STATUS

1067822219288009613	snap001	1 GiB	2	no	LOW		1	up - detached

```

You can use the ID or NAME of the snapshots when using them to restore a volume.

#### Restoring a pod from a snapshot​

To restore a pod to use the created snapshot, use the pvc `name.snap001-source.pvc001` in the pod spec.

## Managing snapshots through pxctl​

To demonstrate the capabilities of the SAN like functionality offered by Portworx, try creating a snapshot of your mysql volume.

First create a database and a demo table in your mysql container.

```

mysql --user=root --password=password

```

```

create database pxdemo;

```

```

Query OK, 1 row affected (0.00 sec)

```

```

use pxdemo;

```

```

Database changed

```

```

create table grapevine (counter int unsigned);

```

```

Query OK, 0 rows affected (0.04 sec)

```

```

quit;

```

```

Bye

```

### Create a snapshot of this database using pxctl​

First use pxctl volume list to see what volume you want to snapshot

```

bin/pxctl volume list

```

```

ID					NAME										SIZE	HA	SHARED	ENCRYPTED	IO_PRIORITY	SCALE	STATUS

381983511213673988	pvc-xxxxxxxx-xxxx-xxxx-xxxx-7cd30ac1a138	20 GiB	2	no		no			LOW			0		up - attached on xx.xx.105.241

```

Then use pxctl to snapshot your volume

```

pxctl volume snapshot 381983511213673988 --name snap-01

```

```

Volume successfully snapped: 835956864616765999

```

You can use pxctl to see your snapshot

```

pxctl snap list

```

```

ID					NAME	SIZE	HA	SHARED	ENCRYPTED	IO_PRIORITY	SCALE	STATUS

835956864616765999	snap-01	20 GiB	2	no		no			LOW			0		up - detached

```

Now you can create a mysql Pod to mount the snapshot

- Kubernetes

- OpenShift

```

kubectl create -f portworx-mysql-snap-pod.yaml

```

```

oc create -f portworx-mysql-snap-pod.yaml

```

Download example

```

apiVersion: v1

kind: Pod

metadata:

  name: test-portworx-snapped-volume-pod

spec:

  containers:

  - image: mysql:5.6

    name: mysql-snap

    env:

      # Use secret in real usage

    - name: MYSQL_ROOT_PASSWORD

      value: password

    ports:

    - containerPort: 3306

      name: mysql

    volumeMounts:

    - name: snap-01

      mountPath: /var/lib/mysql

  volumes:

  - name: snap-01

    # This Portworx volume must already exist.

    portworxVolume:

      volumeID: "vol1"

```

Inspect that the database shows the cloned tables in the new mysql instance.

```

mysql --user=root --password=password

```

```

show databases;

```

```

+--------------------+

| Database           |

+--------------------+

| information_schema |

| mysql              |

| performance_schema |

| pxdemo             |

+--------------------+

4 rows in set (0.00 sec)

```

```

use pxdemo;

```

```

Reading table information for completion of table and column names

You can turn off this feature to get a quicker startup with -A

Database changed

```

```

show tables;

```

```

+------------------+

| Tables_in_pxdemo |

+------------------+

| grapevine        |

+------------------+

1 row in set (0.00 sec)

```

In this topic:
