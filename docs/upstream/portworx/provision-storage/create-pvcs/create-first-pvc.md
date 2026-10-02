# Create your first PVC

Source: https://docs.portworx.com/portworx-enterprise/provision-storage/create-pvcs/create-first-pvc (Portworx Enterprise latest)

Create your first PVC | Portworx Enterprise Documentation

This topic describes how to create a PVC after you install Portworx on a cluster.

For your apps to use persistent volumes powered by Portworx, you must use a StorageClass that references Portworx as the provisioner. Portworx includes a number of default StorageClasses, which you can reference with PersistentVolumeClaims (PVCs) you create. For a more general overview of how storage works within Kubernetes, see the Persistent Volumes section of the Kubernetes documentation.

Perform the following steps to create a PVC:

-
Create a PVC referencing the `px-csi-db` default StorageClass and save the file:

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

    name: px-check-pvc

spec:

    storageClassName: px-csi-db

    accessModes:

        - ReadWriteOnce

    resources:

        requests:

            storage: 2Gi

```

-
Run the command to create a PVC:

- Kubernetes

- OpenShift

```

kubectl apply -f <your-pvc-name>.yaml

```

```

persistentvolumeclaim/example-pvc created

```

```

oc apply -f <your-pvc-name>.yaml

```

```

persistentvolumeclaim/example-pvc created

```

## Verify your StorageClass and PVC​

-
Enter the following command:

- Kubernetes

- OpenShift

```

kubectl get storageclass

```

```

NAME                                 PROVISIONER                     RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE

px-csi-db                            pxd.portworx.com                Delete          Immediate           true                   43d

px-csi-db-cloud-snapshot             pxd.portworx.com                Delete          Immediate           true                   43d

px-csi-db-cloud-snapshot-encrypted   pxd.portworx.com                Delete          Immediate           true                   43d

px-csi-db-encrypted                  pxd.portworx.com                Delete          Immediate           true                   43d

px-csi-db-local-snapshot             pxd.portworx.com                Delete          Immediate           true                   43d

px-csi-db-local-snapshot-encrypted   pxd.portworx.com                Delete          Immediate           true                   43d

px-csi-replicated                    pxd.portworx.com                Delete          Immediate           true                   43d

px-csi-replicated-encrypted          pxd.portworx.com                Delete          Immediate           true                   43d

stork-snapshot-sc                    stork-snapshot                  Delete          Immediate           true                   43d

```

`kubectl` returns details about the StorageClasses available to you. Verify that `px-csi-db` appears in the list.

```

oc get storageclass

```

```

NAME                                 PROVISIONER                     RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE

px-csi-db                            pxd.portworx.com                Delete          Immediate           true                   43d

px-csi-db-cloud-snapshot             pxd.portworx.com                Delete          Immediate           true                   43d

px-csi-db-cloud-snapshot-encrypted   pxd.portworx.com                Delete          Immediate           true                   43d

px-csi-db-encrypted                  pxd.portworx.com                Delete          Immediate           true                   43d

px-csi-db-local-snapshot             pxd.portworx.com                Delete          Immediate           true                   43d

px-csi-db-local-snapshot-encrypted   pxd.portworx.com                Delete          Immediate           true                   43d

px-csi-replicated                    pxd.portworx.com                Delete          Immediate           true                   43d

px-csi-replicated-encrypted          pxd.portworx.com                Delete          Immediate           true                   43d

stork-snapshot-sc                    stork-snapshot                  Delete          Immediate           true                   43d

```

`oc` returns details about the StorageClasses available to you. Verify that `px-csi-db` appears in the list.

-
Enter the following command.
If this is the only StorageClass and PVC that you have created, the output displays only one entry.

- Kubernetes

- OpenShift

```

kubectl get pvc <your-pvc-name>

```

```

NAME          STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS           AGE

example-pvc   Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-2377767c8ce0   2Gi        RWO            example-storageclass   3m7s

```

`kubectl` returns details about your PVC if it was created correctly. Verify that the configuration details appear as you intended.

```

oc get pvc <your-pvc-name>

```

```

NAME          STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS           AGE

example-pvc   Bound    pvc-dce346e8-ff02-xxxx-xxxx-xxxxxxxxxxxx   2Gi        RWO            example-storageclass   3m7s

```

`oc` returns details about your PVC if it was created correctly. Verify that the configuration details appear as you intended.

In this topic:
