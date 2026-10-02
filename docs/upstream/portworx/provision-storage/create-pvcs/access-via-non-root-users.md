# Access a PVC as Non-Root User

Source: https://docs.portworx.com/portworx-enterprise/provision-storage/create-pvcs/access-via-non-root-users (Portworx Enterprise latest)

Access a PVC as Non-Root User | Portworx Enterprise Documentation

This document describes how to access a Portworx Volume (PVC/PV) as a non-root user. By default, all the Persistent Volumes are accessible only by the root user. However, you can modify the application pod spec to allow a specific set of users to access the Persistent Volume as explained below.

#### Modify the application pod spec​

You can modify the PodSecurityContext section of a Pod to include an `fsGroup` field. Here is a snippet of a pod spec file:

```

spec:

  # Allow non-root user to access PersistentVolume

  securityContext:

    fsGroup: 1000

  containers:

```

The `fsGroup` field specifies that the given special supplemental group with ID 1000 is associated with all Containers in the Pod. When you specify a `fsGroup` the ownership of the volume is changed to be owned by the pod.

- The owning GID will be that of `fsGroup`.

- The `setgid` bit is set so that new files created in the volume are owned by the GID.

- The permission bits are OR’d with rw-rw—- For more information refer to the Kubernetes docs

In this topic:
