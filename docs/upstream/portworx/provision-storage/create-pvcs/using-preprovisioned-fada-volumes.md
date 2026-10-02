# Using Pre-provisioned FlashArray Direct Access Volumes

Source: https://docs.portworx.com/portworx-enterprise/provision-storage/create-pvcs/using-preprovisioned-fada-volumes (Portworx Enterprise latest)

Using Pre-provisioned FlashArray Direct Access Volumes | Portworx Enterprise Documentation

This document describes how to import and use an existing FlashArray volume as a FlashArray Direct Access (FADA) PVC in your Kubernetes cluster. Unlike dynamic provisioning, where Portworx creates a new volume on the FlashArray, pre-provisioned FADA volumes let you consume volumes that already exist on the array.

## Prerequisites​

Before you begin, ensure the following:

- Portworx is installed and configured with your FlashArray backend. For more information, see Install Portworx with FlashArray.

- A FlashArray Direct Access StorageClass exists in your cluster. For more information, see Configure FlashArray as a Direct Access volume.

- The volume you want to import already exists on the FlashArray.

## Use a pre-provisioned FlashArray volume​

To use an existing FlashArray volume as a FADA PVC, create a PersistentVolumeClaim with the `pure_vol_name` annotation. This annotation tells Portworx to use the specified existing volume on the FlashArray instead of creating a new one.

### Create a PVC​

Create a PersistentVolumeClaim spec and add the `pure_vol_name` annotation in the `metadata.annotations` field. Set the value to the name of the existing volume on the FlashArray.

If the volume resides inside a FlashArray pod, use the format `<fa-pod-name>::<volume-name>`. If the volume is not in a pod, specify just the volume name.

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: preprovisioned-fa-pvc

  annotations:

    pure_vol_name: "<volume-name>"

spec:

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 20Gi

  storageClassName: sc-portworx-fa-direct-access

```

The following table describes the annotation used for pre-provisioned FADA volumes:

AnnotationDescriptionRequired

`pure_vol_name`The name of the existing volume on the FlashArray. Use the format `<fa-pod-name>::<volume-name>` if the volume is inside a FlashArray pod, or just `<volume-name>` if it is not.Yes

note

- The `storageClassName` must reference a FlashArray Direct Access StorageClass with `backend: "pure_block"`. For more information, see Create a StorageClass.

- The `storage` value in the PVC spec should be less than or equal to the size of the existing volume on the FlashArray.

- If the volume name specified in the annotation does not exist on the FlashArray, provisioning will fail with an error indicating the volume could not be looked up.

### Mount to a pod​

After you create the PVC, create a pod that references it. For example:

```

kind: Pod

apiVersion: v1

metadata:

  name: nginx-preprovisioned-fa

spec:

  volumes:

  - name: fa-vol

    persistentVolumeClaim:

      claimName: preprovisioned-fa-pvc

  containers:

  - name: nginx

    image: nginx

    volumeMounts:

    - name: fa-vol

      mountPath: /data

    ports:

    - containerPort: 80

```

Once you apply the pod spec, you can verify that the pod is running:

- Kubernetes

- Openshift

```

kubectl get pods

```

```

oc get pods

```

When the pod reaches a `Running` status, the pre-provisioned FlashArray volume is successfully mounted and available at the specified mount path.

## Related topics​

- Configure FlashArray as a Direct Access volume

- FlashArray Direct Access concepts

- Using pre-provisioned Portworx volumes

In this topic:
