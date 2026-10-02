# Encrypt Kubernetes PVCs with AWS KMS

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/key-management/aws-kms/pvc-enc (Portworx Enterprise 3.6)

Encrypt Kubernetes PVCs with AWS KMS | Portworx Enterprise Documentation

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

In this method, each volume uses its own unique passphrase for encryption.

note

This is the recommended method for encrypting volumes when you want to take a cloud backup of an encrypted volume or migrate encrypted volumes between multiple clusters.

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

Create a new PVC as follows:

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

### Encryption using named secrets​

note

This method for encrypting volumes is not supported when you want to take a cloud backup of an encrypted volume or migrate encrypted volumes between two different Portworx clusters.

#### Step 1: Creating Named Secrets​

Use the following CLI command to generate AWS KMS Data keys. Portworx associates each KMS Data Key with a unique name provided through the `--secret_id` argument.

To generate a new KMS Data Key, run the following command:

```

pxctl secrets aws generate-kms-data-key --secret_id mysecret

```

The above command generates an AWS KMS Data Key and associates it with the name `mysecret`. To use this Data Key for encrypting volumes provide only the secret ID `mysecret` to Portworx while creating/attaching the volume.

important

You must not run the above command with the same `secret_id` if you have volumes using the `secret_id`.

To list all the named secrets, use the following command:

```

pxctl secrets aws list-secrets

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

Use the following to create a new PVC:

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

### Encryption using cluster wide secret​

From Portworx version 2.1 support for cluster-wide secrets has been deprecated. If you have volumes (using cluster-wide secret) that were created using older Portworx versions, those volumes will still seamlessly work with newer Portworx versions.

However, if you wish to use your previous cluster-wide secret, then you will need to pass its name as shown in the previous Named secrets section.

For example,

Lets say your generated KMS data key was called `portworx_secret` and you had set it as a your cluster-wide secret using the command `pxctl secrets set-cluster-key portworx_secret`.

To create new volumes using that same secret you will need to follow the previous Named secret section and provide the name `portworx_secret` as show above.

Again, existing volumes created with cluster wide, will still work without providing `portworx_secret`.

note

- For newer volumes if you do not provide any secret key, they will use per volume encryption and will NOT default to using cluster wide secret

- This method for encrypting volumes is not supported when you want to take a cloud backup of an encrypted volume or migrate encrypted volumes between two different Portworx clusters.

In this topic:
