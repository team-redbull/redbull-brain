# Create PVCs using the ReadOnlyMany access mode

Source: https://docs.portworx.com/portworx-enterprise/provision-storage/create-pvcs/create-readonlymany-pvcs (Portworx Enterprise 3.6)

Create PVCs using the ReadOnlyMany access mode | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This guide provides steps for mounting a disk in the `ReadOnlyMany` (ROX) access mode. The in-tree Portworx driver for Kubernetes and OpenShift does not support creating PVCs with the `ReadOnlyMany` access mode. To achieve this functionality, follow the steps below:

-
Create a `sharedv4` volume. Note that you can access a `sharedv4` volume from multiple pods at the same time. For details about creating a `sharedv4` volume, refer to the Create sharedv4 PVCs page.

-
Add a `persistentVolumeClaim` subsection to the `volumes` section of your Pod, specifying the following fields and values:

-
readOnly: with the `true` value

-
claimName: with the name of the PVC you created in the step above

```

apiVersion: v1

kind: Pod

metadata:

  name: pvpod

spec:

  containers:

  - name: test-container

    image: gcr.io/google_containers/test-webserver

    volumeMounts:

    - name: test-vol

      mountPath: /test-portworx-volume

  volumes:

  - name: test-vol

    persistentVolumeClaim:

      claimName: pvcsc001

      readOnly: true

```
