# Encrypt Kubernetes PVCs with Google Cloud KMS

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/key-management/gcloud-kms/pvc-enc (Portworx Enterprise 3.6)

Encrypt Kubernetes PVCs with Google Cloud KMS | Portworx Enterprise Documentation

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

With this method, each volume uses a unique passphrase for encryption. Portworx automatically generates a 128-bit passphrase and uses it for both encryption and decryption. If you prefer to manage passphrases yourself, use named secrets as described here.

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

If you do not want to specify the `secure` flag in the storage class, but you want to encrypt the PVC using that Storage Class, then create the PVC as below:

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

Take a note of the annotation `px/secret-name: default`. This specific annotation indicates Portworx to use the default secret to encrypt the volume. In this case, it will NOT create a new passphrase for this volume and NOT use per volume encryption. If the annotation is not provided then Portworx will use the per volume encryption workflow as described in the previous section.

Again, if your Storage Class does not have the `secure` flag set, but you want to encrypt the PVC using the same Storage Class, then add the annotation `px/secure: "true"` to the above PVC.

note

If you want to migrate encrypted volumes created through this method between two different Portworx clusters:

- Create a secret with the same name (`--secret_id`) using Portworx CLI.

- Make sure you provide the same passphrase while generating the secret.

### Encryption using named secrets​

In this method Portworx will use the named secret created by you for encrypting and decrypting a volume.

#### Step 1: Create a Named Secret​

Use the following CLI command to create a new secret in Google Cloud KMS and provide it an identifier/name:

```

pxctl secrets gcloud create-secret --secret_id mysecret --passphrase mysecretpassphrase

```

The above command will create a new key-value pair `mysecret=mysecretpassphrase`. Portworx will use Google Cloud KMS to encrypt the passphrase `mysecretpassphrase` and store it in its internal metadata store. To use this passphrase for encrypting volumes provide only the secret ID `mysecret` to Portworx while creating/attaching the volume.

To list all the named secrets use the following command:

```

pxctl secrets gcloud list-secrets

```

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

    px/secret-name: mysecret

    volume.beta.kubernetes.io/storage-class: px-secure-sc

spec:

  storageClassName: px-mysql-sc

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

```

Take a note of the annotation `px/secret-name: mysecret`. This specific annotation indicates Portworx to use the secret called `mysecret` to encrypt the volume. In this case, it will NOT create a new passphrase for this volume and NOT use per volume encryption. If the annotation is not provided then Portworx will use the per volume encryption workflow as described in the previous section.

note

A single named secret can be used for encrypting multiple volumes.

Again, if your Storage Class does not have the `secure` flag set, but you want to encrypt the PVC using the same Storage Class, then add the annotation `px/secure: "true"` to the above PVC.

note

If you want to migrate encrypted volumes created through this method between two different Portworx clusters:

- Create a secret with the same name (`--secret_id`) using Portworx CLI.

- Make sure you provide the same passphrase while generating the secret.

In this topic:
