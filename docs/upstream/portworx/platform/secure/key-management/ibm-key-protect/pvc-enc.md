# Encrypt Kubernetes PVCs with IBM key management services

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/key-management/ibm-key-protect/pvc-enc (Portworx Enterprise 3.6)

Encrypt Kubernetes PVCs with IBM key management services | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## Portworx Encrypted Volumes​

Portworx has two different kinds of encrypted volumes:

-
Encrypted Volumes

Encrypted volumes are regular volumes which can be accessed from only one node.

-
Encrypted Sharedv4 Volumes

Encrypted sharedv4 volume allows access to the same encrypted volume from multiple nodes.

### Encryption using per volume secrets​

In this method each volume will use its own unique passphrase to encrypt the volume. Portworx uses IBM Key Protect APIs to generate a unique 256 bit passphrase. This passphrase will be used during encryption and decryption.

#### Step 1: Create a Storage Class​

Create a storage class with the `secure` parameter set to `true`.

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: px-secure-sc

provisioner: pxd.portworx.com

parameters:

  secure: "true"

  repl: "3"

```

To create a sharedv4 encrypted volume set the `sharedv4` parameter to `true` as well.

#### Step 2: Create a Persistent Volume Claim​

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: mysql-data

  annotations:

    volume.beta.kubernetes.io/storage-class: px-secure-sc

spec:

  storageClassName: px-mysql-sc

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

```

If you do not want to specify the `secure` flag in the storage class, but you want to encrypt the PVC using that Storage Class, then create the PVC as below

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: secure-pvc

  annotations:

    px/secure: "true"

spec:

  storageClassName: portworx-sc

  accessModes:

  - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

```

Note the `px/secure: "true"` annotation on the PVC object.

### Encryption using cluster wide secret​

In this method a default cluster wide secret will be set for the Portworx cluster. Such a secret will be referenced by the user and Portworx as default secret. Any PVC request referencing the secret name as `default` will use this cluster wide secret as a passphrase to encrypt the volume.

#### Step 1: Set the cluster wide secret key​

Use the following command to set the cluster wide secret key:

```

pxctl secrets set-cluster-key --secret <passphrase>

```

```

Successfully set cluster secret key!

```

The `<passphrase>` in the above command will be used for encrypting the volumes. The cluster wide secret key needs to be set only once.

note

DO NOT overwrite the cluster wide secret key, else any existing volumes using it will not be usable.

#### Step 2: Create a Storage Class​

Create a storage class with the `secure` parameter set to `true`.

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: px-secure-sc

provisioner: pxd.portworx.com

parameters:

  secure: "true"

  repl: "3"

```

To create a sharedv4 encrypted volume set the `sharedv4` parameter to `true` as well.

#### Step 3: Create a Persistent Volume Claim​

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: mysql-data

  annotations:

    px/secret-name: default

    volume.beta.kubernetes.io/storage-class: px-secure-sc

spec:

  storageClassName: px-mysql-sc

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

```

Take a note of the annotation `px/secret-name: default`. This specific annotation indicates Portworx to use the default secret to encrypt the volume. In this case it will NOT create a new passphrase for this volume and NOT use per volume encryption. If the annotation is not provided then Portworx will use the per volume encryption workflow as described in the previous section.

Again, if your Storage Class does not have the `secure` flag set, but you want to encrypt the PVC using the same Storage Class, then add the annotation `px/secure: "true"` to the above PVC.

note

If you want to migrate encrypted volumes created through this method between two different Portworx clusters:

- Create a secret with the same name (`--secret_id`) using Portworx CLI.

- Make sure you provide the same passphrase while generating the secret.

In this topic:
