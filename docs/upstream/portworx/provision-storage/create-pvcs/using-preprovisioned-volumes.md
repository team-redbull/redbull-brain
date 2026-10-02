# Using Pre-provisioned Volumes

Source: https://docs.portworx.com/portworx-enterprise/provision-storage/create-pvcs/using-preprovisioned-volumes (Portworx Enterprise 3.6)

Using Pre-provisioned Volumes | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This document describes how to use a pre-provisioned volume in your cluster.

## Create a Portworx volume using pxctl​

First create a volume using the Portworx CLI. On one of the nodes with Portworx installed, run the following command:

```

/opt/pwx/bin/pxctl volume create testvol --size 2

```

For more details on creating volumes using `pxctl`, see Concepts.

Alternatively, you can also use snapshots that you previously created.

## Use the Portworx volume​

Once you have a Portworx volume, you can use it in the following ways:

### 1. Using the Portworx volume directly in a pod​

You can create a pod that directly uses a Portworx volume as follows:

```

apiVersion: v1

kind: Pod

metadata:

   name: nginx-px

spec:

   containers:

   - image: nginx

     name: nginx-px

     volumeMounts:

     - mountPath: /test-portworx-volume

       name: testvol

   volumes:

   - name: testvol

     # This Portworx volume must already exist.

     portworxVolume:

       volumeID: testvol

```

note

The name and volumeID above must be the same and should be the name of the Portworx volume created using pxctl.

### 2. Using the Portworx volume by creating a PersistentVolume & PersistentVolumeClaim (in-tree)​

note

The following example uses the Portworx in-tree volume driver. If your PVCs were originally provisioned using CSI, see method 3 instead.

Creating PersistentVolume

First create a `PersistentVolume` that references the Portworx volume. Following is an example spec.

```

apiVersion: v1

kind: PersistentVolume

metadata:

  name: testvol

spec:

  capacity:

    storage: 2Gi

  claimRef:

    apiVersion: v1

    kind: PersistentVolumeClaim

    name: testvol-pvc

    namespace: default

  accessModes:

    - ReadWriteOnce

  persistentVolumeReclaimPolicy: Retain

  portworxVolume:

    volumeID: <px-volume-id>

```

note

The preceding `PersistentVolume` example references an existing Portworx volume called `testvol` that was created using `pxctl`.

#### Creating PersistentVolumeClaim​

Now create a `PersistentVolumeClaim` that will claim the previously created volume. Following is an example spec.

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: testvol-pvc

spec:

  selector:

    matchLabels:

      name: testvol

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

  volumeName: testvol

```

note

If you are planning to use the `PersistentVolumeClaim` in a pod in a non-default namespace, you must create the `PersistentVolumeClaim` in that namespace.

#### Creating a pod using the PersistentVolumeClaim​

Now you can create a pod that references the `PersistentVolumeClaim` that you created. Following is an example.

```

apiVersion: v1

kind: Pod

metadata:

   name: nginx-px

spec:

  containers:

  - image: nginx

    name: nginx-px

    volumeMounts:

    - mountPath: /test-portworx-volume

      name: testvol

  volumes:

  - name: testvol

    persistentVolumeClaim:

      claimName: testvol-pvc

```

note

To access PV/PVCs with a non-root user, refer to Access via Non-Root Users

### 3. Using the Portworx volume with the CSI driver​

If your volumes were originally provisioned using the CSI (Container Storage Interface) method, you must use CSI-based specs when creating PersistentVolumes and PersistentVolumeClaims. The in-tree driver specs shown in method 2 will not work for CSI-provisioned volumes.

Creating PersistentVolume

Create a `PersistentVolume` that references the Portworx volume using the CSI driver. Following is an example spec.

```

apiVersion: v1

kind: PersistentVolume

metadata:

  name: testvol

spec:

  capacity:

    storage: 2Gi

  claimRef:

    apiVersion: v1

    kind: PersistentVolumeClaim

    name: testvol-pvc

    namespace: default

  volumeMode: Filesystem

  accessModes:

    - ReadWriteOnce

  persistentVolumeReclaimPolicy: Retain

  storageClassName: <your-storage-class>

  csi:

    driver: pxd.portworx.com

    volumeHandle: "<px-volume-id>"

    fsType: ext4

```

note

- Replace `<px-volume-id>` with the ID of the Portworx volume you created using `pxctl`.

- Replace `<your-storage-class>` with the name of the StorageClass used to originally provision the volume.

- Adjust `fsType` if your volume uses a different filesystem (for example, `xfs`).

#### Creating PersistentVolumeClaim​

Now create a `PersistentVolumeClaim` that references the PersistentVolume. Following is an example spec.

```

apiVersion: v1

kind: PersistentVolumeClaim

metadata:

  name: testvol-pvc

  namespace: default

spec:

  storageClassName: <your-storage-class>

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

  volumeMode: Filesystem

  volumeName: testvol

```

note

- The `storageClassName` must match the StorageClass specified in the PersistentVolume.

- The `volumeName` must match the name of the PersistentVolume you created.

- If you are planning to use the `PersistentVolumeClaim` in a pod in a non-default namespace, you must create the `PersistentVolumeClaim` in that namespace and update the `claimRef` in the PersistentVolume accordingly.

#### Creating a pod using the PersistentVolumeClaim​

Now you can create a pod that references the `PersistentVolumeClaim` that you created. Following is an example.

```

apiVersion: v1

kind: Pod

metadata:

  name: nginx-px

  namespace: default

spec:

  containers:

  - name: nginx-px

    image: nginx

    volumeMounts:

    - mountPath: /test-portworx-volume

      name: testvol

  volumes:

  - name: testvol

    persistentVolumeClaim:

      claimName: testvol-pvc

```

note

To access PV/PVCs with a non-root user, refer to Access via Non-Root Users

In this topic:
