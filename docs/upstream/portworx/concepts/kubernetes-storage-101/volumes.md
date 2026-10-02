# Kubernetes Persistent volumes

Source: https://docs.portworx.com/portworx-enterprise/concepts/kubernetes-storage-101/volumes (Portworx Enterprise 3.6)

Kubernetes Persistent volumes | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

When dealing with persistent storage in Kubernetes, 3 key objects are important:

- StorageClass

- PersistentVolumeClaim

- PersistentVolume

## StorageClass​

A `StorageClass` provides a way for administrators to describe the “classes” of storage they offer. Different classes might map to quality-of-service levels, or to backup policies, or to arbitrary policies determined by the cluster administrators. This concept is sometimes called “profiles” in other storage systems.

A user would first create a bunch of StorageClass's in the cluster and then create volumes (PVCs) that reference the StorageClass.

Let's take an example.

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: portworx-sc-db

provisioner: pxd.portworx.com

parameters:

  repl: "3"

  io_profile: "db_remote"

  createoptions: -N 128000

```

In above StorageClass,

- provisioner: pxd.portworx.com indicates that volumes should be provisioned by the Portworx driver

- parameters provide driver specific parameters. The Kubernetes controller simply passes these parameters as-is to the underlying driver (Portworx in this example).

- repl: "3" indicates that the Portworx volume needs to have 3 replicas

- io_profile: "db_remote" indicates that the Portworx volume needs to have IO profile optimized for DB workloads.

- createoptions: indicates the filesystem formatting options for the specified filesystem (ext4 or xfs).

For information on supported StorageClass parameters, see Parameters Fields. See `man mkfs.ext4` to check all formatting options of ext4 and `man mkfs.xfs` to check all formatting options of xfs.

note

Some fields like `allowVolumeExpansion` cannot be added after the storage class has been created.

Let's take a look at an example.

To resize a Portworx PVC, you can simply edit the PVC spec and update the size. Let's take an example of resizing a MySQL PVC.

-
Download the MySQL StorageClass spec and apply it. Note that the StorageClass has `allowVolumeExpansion: true`.

-
Download the MySQL PVC spec and apply it. We will start with a 5GB volume.

-
Download the MySQL Deployment spec, specify your own values for the `ACCEPT_EULA` and `SA_PASSWORD`, and apply it. Wait till the pod becomes 1/1 and then proceed to next step.

-
Run `kubectl edit pvc mssql-data` and change the size in the "spec" to 10Gi.

After you save the spec, `kubectl describe pvc mssql-data` should have an entry like below that confirms the volume resize.

```

Normal  VolumeResizeSuccessful  5s    volume_expand                ExpandVolume succeeded for volume default/mssql-data

```

## PersistentVolumeClaim (PVC)​

A PersistentVolumeClaim (PVC) is a request for storage by a user. It is similar to a pod. Pods consume node resources and PVCs consume PV resources. Pods can request specific levels of resources (CPU and Memory). Claims can request specific size and access modes (e.g., can be mounted once read/write or many times read-only).

Let's take an example.

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: postgres-db

spec:

  storageClassName: portworx-sc-db

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 10Gi

```

In above PVC,

- name: postgres-db gives the name of the PVC.

- storageClassName: portworx-sc-db indicates that this PVC should be creating using the provisioner and parameters specified in the portworx-sc-db StorageClass.

- ReadWriteOnce indicates that only one pod is allowed to read and write to the volume.

- storage: 10Gi indicates this is a 10GiB PVC.

## PersistentVolume (PV)​

A PersistentVolume (PV) is a piece of storage in the cluster that has been provisioned by an administrator.

When you create a PVC, behind the scenes, either a new PV is created (dynamic provisioning) or an existing PV is bound to the PVC. In other words, there is a one-one mapping between a PVC and a PV.

To find the PV that is being used by a PVC, you can do

```

kubectl get pvc <pvc-name>

```

An end user needs to interact with a PV only when using pre-provisioned volumes. For dynamically provisioned volumes, end users only create PVCs and the backing storage provider creates the PV.

## ReadWriteMany and ReadWriteOnce​

A PVC can be

- ReadWriteMany: In the mode, multiple pods can mount and volume and access it at the same time.

- This should be used by applications like web servers (nginx, wordpress etc) that can handle multiple instances writing to the same volume. It is not recommended to use for databases.

- ReadWriteOnce: In the mode, only a single pod can access the volume at a given time

note

The StorageClass configuration for PVCs requiring `ReadWriteOnce` Portworx volumes is outlined below:

```

apiVersion: storage.k8s.io/v1

metadata:

  name: prometheus-sc

provisioner: pxd.portworx.com

parameters:

  repl: "2"

  priority_io: "high"

  nodiscard: "true"

allowVolumeExpansion: true

```

To back up Prometheus with Portworx PVC, use only non `sharedV4` volumes. For example:

```

monitoring:

      prometheus:

        enabled: true

        exportMetrics: true

        resources: {}

        storage:

          volumeClaimTemplate:

            metadata:

              name: prometheus-inline

            spec:

              accessModes:

              - ReadWriteOnce

              resources:

                requests:

                  storage: 100Gi

              storageClassName: prometheus-sc

            status: {}

      telemetry:

        enabled: true

```

## Useful References​

- Interactive tutorial - Resize Kubernetes volumes using kubectl

- Interactive tutorial - Persistent volumes on Kubernetes using Portworx

- Interactive tutorial - Using Portworx Shared Volumes

- Interactive tutorial - Encrypting volumes on Kubernetes

- Kubernetes Storage documentation

## Related videos​

### Backup and restore persistent volumes with Google Cloud Storage​

In this topic:
