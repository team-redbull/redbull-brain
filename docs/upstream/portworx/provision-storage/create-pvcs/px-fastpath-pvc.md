# Create PX-Fast PVCs

Source: https://docs.portworx.com/portworx-enterprise/provision-storage/create-pvcs/px-fastpath-pvc (Portworx Enterprise latest)

Create PX-Fast PVCs | Portworx Enterprise Documentation

PX-Fast is a Portworx feature that enables an accelerated IO path for the volumes that meet certain prerequisites. It is optimized for workloads requiring consistent low latencies. PX-Fast is built on top of a Portworx PX-StoreV2 datastore.

note

- PX-Fast works only if Portworx is installed with PX-StoreV2 datastore.

- PX-Fast PVC is not supported in the following scenarios:

- When a PVC has more than one replica.

- On aggregated volumes

## Prerequisites​

You must have deployed Portworx with PX-StoreV2 datastore.

## Create PX-Fast PVCs​

Perform the following steps to create PX-Fast volumes.

### Create a StorageClass​

- Save the following as a YAML file:

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: px-fast

provisioner: pxd.portworx.com

parameters:

  repl: "1"

  fastpath: "true"

allowVolumeExpansion: true

```

Note that this StorageClass will have 1 replica, and the Portworx volumes referring to this StorageClass will also have 1 replica.

- Run the following command to create a StorageClass:

```

  kubectl apply -f <px-fast>.yaml

```

```

storageclass.storage.k8s.io/px-fast created

```

- Verify that the StorageClass is created:

```

kubectl describe storageclass px-fast

```

```

Provisioner:           pxd.portworx.com

Parameters:            fastpath=true,repl=1

AllowVolumeExpansion:  <unset>

MountOptions:          <none>

ReclaimPolicy:         Delete

VolumeBindingMode:     Immediate

Events:                <none>

```

### Create a PVC​

- Save the following as YAML file:

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: px-fast-pvc

spec:

  storageClassName: px-fast

  accessModes:

     - ReadWriteOnce

  resources:

     requests:

       storage: 1Gi

```

- Run the following command to create a PX-Fast PVC:

```

kubectl apply -f <px-pvc>.yaml

```

- Verify that a PVC is created:

```

kubectl get pvc

```

### Deploy an application using a PX-Fast PVC​

To utilize PX-Fast on the above PVCs, the application pods must run on the same node where the volume replica exists. The following sample deployment spec uses the `stork.libopenstorage.org/preferLocalNodeOnly: "true"` annotation, which enforces the pod to be scheduled on the node where the volume replica exists:

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

      annotations:

        stork.libopenstorage.org/preferLocalNodeOnly: "true"

      labels:

        app: mysql

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

          claimName: px-fast-pvc

```

The annotation `stork.libopenstorage.org/preferLocalNodeOnly: "true"` enforces the pod to be scheduled on the node where the volume replica exists. To avoid this enforced behavior, you can choose not to specify the `stork.libopenstorage.org/preferLocalNodeOnly: true` annotation. In such a case, Stork will do best-effort to place the application pod on the node where the replica exists, but if the application pod gets attached to a non-replica node, it cannot use PX-Fast.

## Reference​

PX-Fast volumes using pxctl

In this topic:
