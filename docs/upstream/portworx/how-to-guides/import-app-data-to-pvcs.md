# Import application data from non-Portworx PVC to Portworx PVCs

Source: https://docs.portworx.com/portworx-enterprise/how-to-guides/import-app-data-to-pvcs (Portworx Enterprise 3.6)

Import application data from non-Portworx PVC to Portworx PVCs | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

In modern Kubernetes-based infrastructure, data migration and application deployment are critical tasks. This document provides a step-by-step guide on how to import application data from a PVC backed by a non Portworx storage driver onto PVCs created by Portworx.

To import data into a Portworx PVC, Stork will use `rsync` to copy the data from an existing PVC into a PVC backed by Portworx. Stork will run a Kubernetes Job which runs the `rsync` command inside a container. This can be useful if you’re a new onboarding customer who was previously using a different storage provider, and who now needs to import data from non-Portworx PVCs into Portworx PVCs.

## Prerequisites​

- A Kubernetes or Openshift cluster set up

- Portworx deployed on this cluster with Stork version 23.8.0 or higher

## Import an application and its data onto PVCs​

- Kubernetes

- Openshift

-
Define a StorageClass and PVC to set up Portworx storage.

Create a Portworx PVC using the `px-csi-db` StorageClass. This StorageClass would be already created for you when you installed Portworx. This is the PVC into which you will be importing data into.

```

kubectl create -f destination-pvc.yaml

```

destination-pvc.yaml

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: postgres-data

  labels:

    app: postgres

spec:

  storageClassName: px-csi-db

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 5Gi

```

-
Scale down the application replicas to 0 to avoid data conflicts during migration.

Stork only supports offline data import. Scaling down the application using the non Portworx PVC ensures the data stays consistent as we import it into a Portworx PVC.

```

kubectl scale --replicas=0 <deployment>/<your-application-name>

```

Replace `<deployment>/<your-application-name>` in the above command with the appropriate resource.

-
Create a `DataExport` object specifying the source and destination of the data import.

The `DataExport` CR is the main driver for triggering the import between a non Portworx PVC (source) and the Portworx PVC (destination). Both these PVCs are provided in the `DataExport` CR specification.

```

kubectl create -f dataexport.yaml

```

dataexport.yaml

```

apiVersion: kdmp.portworx.com/v1alpha1

kind: DataExport

metadata:

  name: postgres-export

  namespace: default

spec:

  type: rsync

  source:

    apiVersion: v1

    kind: PersistentVolumeClaim

    name: pgbench-data

    namespace: default

  destination:

    apiVersion: v1

    kind: PersistentVolumeClaim

    name: postgres-data

    namespace: default

```

-
Monitor the progress of the data export using `kubectl describe`.

Following are the sample outputs for a data export process:

In progress

```

Spec:

  Destination:

    API Version:  v1

    Kind:         PersistentVolumeClaim

    Name:         postgres-data

    Namespace:    default

  Source:

    API Version:  v1

    Kind:         PersistentVolumeClaim

    Name:         pgbench-data

    Namespace:    default

  Type:           rsync

Status:

  Reason:

  Stage:        TransferInProgress

  Status:       InProgress

  Transfer ID:  default/import-rsync-pgbench-data

Events:         <none>

```

Completed

```

Spec:

Destination:

  API Version:  v1

  Kind:         PersistentVolumeClaim

  Name:         postgres-data

  Namespace:    default

Source:

  API Version:  v1

  Kind:         PersistentVolumeClaim

  Name:         pgbench-data

  Namespace:    default

Type:           rsync

Status:

  Progress Percentage:  100

  Stage:                Final

  Status:               Successful

  Transfer ID:          default/import-rsync-pgbench-data

Events:

```

-
Update the application's deployment configuration to use the Portworx PVC.

This section uses `kubectl edit` to modify your existing application to use the newly created Portworx PVC into which data has been imported. Based on your deployment model, you will need to change the application specifications to use the new Portworx PVC.

```

kubectl edit <deployment> <your-application-namespace>

```

-
Restore the application to its desired replica count:

```

kubectl scale --replicas=1 <deployment>/<your-application-name>

```

Replace `<deployment>/<your-application-name>` in steps 6 and 7 with the appropriate resource.

-
Define a StorageClass and PVC to set up Portworx storage.

Create a Portworx PVC using the `px-csi-db` StorageClass. This StorageClass would be already created for you when you installed Portworx. This is the PVC into which you will be importing data into.

```

oc create -f destination-pvc.yaml

```

destination-pvc.yaml

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: postgres-data

  labels:

    app: postgres

spec:

  storageClassName: px-csi-db

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 5Gi

```

-
Scale down the application replicas to 0 to avoid data conflicts during migration.

Stork only supports offline data import. Scaling down the application using the non Portworx PVC ensures the data stays consistent as we import it into a Portworx PVC.

```

oc scale --replicas=0 <deployment>/<your-application-name>

```

Replace `<deployment>/<your-application-name>` in the above command with the appropriate resource.

-
Create a `DataExport` object specifying the source and destination of the data import.

The `DataExport` CR is the main driver for triggering the import between a non Portworx PVC (source) and the Portworx PVC (destination). Both these PVCs are provided in the `DataExport` CR specification.

```

oc create -f dataexport.yaml

```

dataexport.yaml

```

apiVersion: kdmp.portworx.com/v1alpha1

kind: DataExport

metadata:

  name: postgres-export

  namespace: default

spec:

  type: rsync

  source:

    apiVersion: v1

    kind: PersistentVolumeClaim

    name: pgbench-data

    namespace: default

  destination:

    apiVersion: v1

    kind: PersistentVolumeClaim

    name: postgres-data

    namespace: default

```

-
Monitor the progress of the data export using `oc describe`.

Following are the sample outputs for a data export process:

In progress

```

Spec:

  Destination:

    API Version:  v1

    Kind:         PersistentVolumeClaim

    Name:         postgres-data

    Namespace:    default

  Source:

    API Version:  v1

    Kind:         PersistentVolumeClaim

    Name:         pgbench-data

    Namespace:    default

  Type:           rsync

Status:

  Reason:

  Stage:        TransferInProgress

  Status:       InProgress

  Transfer ID:  default/import-rsync-pgbench-data

Events:         <none>

```

Completed

```

Spec:

Destination:

  API Version:  v1

  Kind:         PersistentVolumeClaim

  Name:         postgres-data

  Namespace:    default

Source:

  API Version:  v1

  Kind:         PersistentVolumeClaim

  Name:         pgbench-data

  Namespace:    default

Type:           rsync

Status:

  Progress Percentage:  100

  Stage:                Final

  Status:               Successful

  Transfer ID:          default/import-rsync-pgbench-data

Events:

```

-
Update the application's deployment configuration to use the Portworx PVC.

This section uses `oc edit` to modify your existing application to use the newly created Portworx PVC into which data has been imported. Based on your deployment model, you will need to change the application specifications to use the new Portworx PVC.

```

oc edit <deployment> <your-application-namespace>

```

-
Restore the application to its desired replica count:

```

oc scale --replicas=1 <deployment>/<your-application-name>

```

Replace `<deployment>/<your-application-name>` in steps 6 and 7 with the appropriate resource.

## Additional options​

This section provides options for customization, such as specifying a custom Docker registry, using image pull secrets, running in OpenShift, and tweaking rsync flags. You should provide these options to Stork through environment variables, which you can configure in the StorageCluster specification.

### When using custom docker registry​

In cases where a custom Docker registry is employed, Stork needs to use such a registry while initiating the job which runs the `rsync` process. To customize the `rsync` image name, you can update the following environment variable in the StorageCluster specification:

```

stork:

  enabled: true

  env:

  - name: KDMP_RSYNC_IMAGE

    value: <custom-registry>/eeacms/rsync:<tag>

```

This allows you to specify a unique image location from your custom Docker registry.

### When using Image Pull Secrets​

The `rsync` operation runs inside the container `eeacms/rsync`. If you require the use of Image Pull Secrets to pull this image, you can provide the Kubernetes secret name as an environment variable. You should establish these image pull secrets within the same namespaces where Stork is deployed. You can manage this configuration as an environment variable in the StorageCluster specification, which you defined during Step 1 of the Import an application and its data onto PVCs section above.

```

stork:

  enabled: true

  env:

  - name: KDMP_RSYNC_IMAGE_SECRET

    value: <image-secret-name>

```

This allows for secure retrieval of the rsync image using the specified image pull secret.

### When running in OpenShift​

In an OpenShift environment, Stork requires the deployment of the `rsync` pod with an associated Security Context Constraints (SCC). You have the flexibility to specify a particular SCC for the deployment of this `rsync` pod. This configuration is achieved through an environment variable within the StorageCluster specification:

```

stork:

  enabled: true

  env:

  - name: KDMP_RSYNC_OPENSHIFT_SCC

    value: <openshift-scc>

```

By setting this variable, you ensure that the `rsync` pod operates under the defined SCC within the OpenShift environment, adhering to specific security and access policies as required.

### Customizing the rsync flags​

Customizing the `rsync` flags is possible, as the default configuration employs the following flags for the rsync command within the `rsync` job pod: `-avz`. To specify your own set of `rsync` flags, you can introduce an environment variable in the StorageCluster specification as follows:

```

stork:

  enabled: true

  env:

  - name: KDMP_RSYNC_FLAGS

    value: "-<custom-flags>"

```

Ensure to include a hyphen at the beginning of your custom flags within the specified value field. This enables you to fine-tune the `rsync` operation according to your specific requirements.

### Supported environment variables​

You should provide all the following environment variables within the `env` section for Stork in the StorageCluster specification:

Environment variableDescription

`KDMP_RSYNC_IMAGE`Custom image name for the rsync pod deployed by Stork’s KDMP controller

`KDMP_RSYNC_IMAGE_SECRET`Image pull secret for the rsync pod deployed by Stork’s KDMP controller

`KDMP_RSYNC_OPENSHIFT_SCC`Openshift SCC to be used with the rsync pod deployed by Stork’s KDMP controller

`KDMP_RSYNC_FLAGS`Custom rsync flags that will be used by the rsync command that runs inside the rsync pod deployed by Stork’s KDMP controller

`KDMP_RSYNC_REQUEST_CPU`Request CPU for the rsync pod deployed by Stork’s KDMP controller

`KDMP_RSYNC_REQUEST_MEMORY`Request Memory for the rsync pod deployed by Stork’s KDMP controller

`KDMP_RSYNC_LIMIT_CPU`CPU Limit for the rsync pod deployed by Stork’s KDMP controller

`KDMP_RSYNC_LIMIT_MEMORY`Memory Limit for the rsync pod deployed by Stork’s KDMP controller

In this topic:
